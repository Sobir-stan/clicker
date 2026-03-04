let ws;
const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const wsUrl = `${wsProtocol}//${window.location.host}/ws/${window.username}`;

function connectWebSocket() {
    ws = new WebSocket(wsUrl);

    ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if (data.type === 'state_update') {
            updateUI(data.state);
        }
    };

    ws.onclose = function () {
        setTimeout(connectWebSocket, 1000);
    };
}

function sendAction(action, payload = {}) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action, ...payload }));
    }
}

connectWebSocket();
