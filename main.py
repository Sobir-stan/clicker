# Auction Game API
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form, HTTPException, status, Response, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
from typing import Dict, Optional

app = FastAPI()

os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, ws: WebSocket, username: str):
        await ws.accept()
        self.active_connections[username] = ws

    def disconnect(self, username: str):
        if username in self.active_connections:
            del self.active_connections[username]

    async def send_personal_message(self, message: dict, username: str):
        if username in self.active_connections:
            await self.active_connections[username].send_text(json.dumps(message))

manager = ConnectionManager()

class GameState:
    def __init__(self):
        self.admin_username = "admin"
        self.admin_password = "password"
        self.starting_money = 0.0
        self.game_started = False
        self.game_ended = False
        self.users = {}
        self.current_lot = None

    def reset(self):
        self.starting_money = 0.0
        self.game_started = False
        self.game_ended = False
        self.users = {}
        self.current_lot = None

state = GameState()

def get_admin_state():
    return {
        "game_started": state.game_started,
        "game_ended": state.game_ended,
        "users": state.users,
        "current_lot": state.current_lot,
        "starting_money": state.starting_money
    }

def get_user_state(username: str):
    user_lot = None
    if state.current_lot:
        user_lot = {
            "name": state.current_lot["name"],
            "price": state.current_lot["price"],
            "icon": state.current_lot["icon"],
            "highest_bid": state.current_lot["highest_bid"],
            "highest_bidder": state.current_lot["highest_bidder"],
            "closed": state.current_lot["closed"]
        }
    
    return {
        "game_started": state.game_started,
        "game_ended": state.game_ended,
        "money": state.users.get(username, {}).get("money", 0),
        "points": state.users.get(username, {}).get("points", 0),
        "current_lot": user_lot,
        "users": state.users if state.game_ended else None
    }

async def broadcast_state():
    await manager.send_personal_message({"type": "state_update", "state": get_admin_state()}, state.admin_username)
    for u in state.users:
        await manager.send_personal_message({"type": "state_update", "state": get_user_state(u)}, u)

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(username: str = Form(...), password: Optional[str] = Form(None)):
    if username == state.admin_username:
        if password == state.admin_password:
            response = RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
            response.set_cookie(key="user", value=username)
            return response
        else:
            raise HTTPException(status_code=400, detail="Noto'g'ri admin ma'lumotlari")
            
    if state.game_ended:
        raise HTTPException(status_code=400, detail="O'yin allaqachon tugagan")
        
    if username not in state.users:
        state.users[username] = {"money": state.starting_money if state.game_started else 0.0, "points": 0.0}
            
    response = RedirectResponse(url="/user", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user", value=username)
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="user")
    return response

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    username = request.cookies.get("user")
    if username != state.admin_username:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("admin.html", {"request": request, "username": username})

@app.get("/user", response_class=HTMLResponse)
async def user_page(request: Request):
    username = request.cookies.get("user")
    if not username or username == state.admin_username:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("user.html", {"request": request, "username": username})

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        if username == state.admin_username:
            await manager.send_personal_message({"type": "state_update", "state": get_admin_state()}, username)
        else:
            if username not in state.users:
                state.users[username] = {"money": state.starting_money if state.game_started else 0.0, "points": 0.0}
            await broadcast_state() # Tell admin screen about new user connection
            
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            action = payload.get("action")
            
            if username == state.admin_username:
                if action == "start_game":
                    state.starting_money = float(payload.get("money", 0))
                    state.game_started = True
                    for u in state.users:
                        state.users[u]["money"] = state.starting_money
                    await broadcast_state()
                    
                elif action == "create_lot":
                    state.current_lot = {
                        "name": payload.get("name"),
                        "price": float(payload.get("price")),
                        "points": float(payload.get("points")),
                        "icon": payload.get("icon"),
                        "highest_bid": float(payload.get("price")),
                        "highest_bidder": None,
                        "closed": False
                    }
                    await broadcast_state()
                    
                elif action == "close_lot":
                    if state.current_lot and not state.current_lot["closed"]:
                        state.current_lot["closed"] = True
                        winner = state.current_lot["highest_bidder"]
                        if winner:
                            state.users[winner]["points"] += state.current_lot["points"]
                        await broadcast_state()
                        
                elif action == "end_game":
                    if not state.game_ended:
                        exchange_rate = float(payload.get("exchange_rate", 0.1))
                        state.game_ended = True
                        for u, data_val in state.users.items():
                            extra_points = data_val["money"] * exchange_rate
                            data_val["points"] += extra_points
                            data_val["money"] = 0
                        await broadcast_state()

                elif action == "reset_game":
                    state.reset()
                    await broadcast_state()
                    
            else: # Regular user
                if action == "bid" and state.current_lot and not state.current_lot["closed"]:
                    bid_amount = float(payload.get("amount", 0))
                    user_money = state.users[username]["money"]
                    current_highest = state.current_lot["highest_bid"]
                    
                    if bid_amount > current_highest and bid_amount <= user_money:
                        prev_winner = state.current_lot["highest_bidder"]
                        if prev_winner:
                            state.users[prev_winner]["money"] += current_highest
                            
                        state.users[username]["money"] -= bid_amount
                        state.current_lot["highest_bid"] = bid_amount
                        state.current_lot["highest_bidder"] = username
                        
                        await broadcast_state()
                        
    except WebSocketDisconnect:
        manager.disconnect(username)
