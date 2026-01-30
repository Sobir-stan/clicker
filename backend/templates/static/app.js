document.addEventListener("DOMContentLoaded", async () => {
    const path = window.location.pathname;
    const token = localStorage.getItem("token");

    /* =======================
       LOGIN PAGE LOGIC
       ======================= */
    if (path === "/login") {
        const form = document.getElementById("login-form");
        if (!form) return;

        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const error = document.getElementById("error");

            error.textContent = "";

            try {
                const response = await fetch("/auth/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ username, password }),
                });

                if (!response.ok) {
                    throw new Error("Invalid username or password");
                }

                const data = await response.json();
                localStorage.setItem("token", data.access_token);

                // Redirect to clicker
                window.location.href = "/clicker";
            } catch (err) {
                error.textContent = err.message;
            }
        });

        return;
    }

    /* =======================
       CLICKER PAGE LOGIC
       ======================= */
    if (path === "/clicker") {
        if (!token) {
            window.location.href = "/login";
            return;
        }

        const clickBtn = document.getElementById("click-btn");
        const countEl = document.getElementById("count");
        const errorEl = document.getElementById("error");

        // Fetch current score
        try {
            const res = await fetch("/ranking/me", {
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            });

            if (!res.ok) throw new Error("Failed to fetch click count");

            const data = await res.json();
            countEl.textContent = data.click_count;
        } catch (err) {
            errorEl.textContent = err.message;
        }

        // Click handler
        clickBtn.addEventListener("click", async () => {
            try {
                const res = await fetch("/click", {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                    },
                });

                if (!res.ok) throw new Error("Click failed");

                const data = await res.json();
                countEl.textContent = data.click_count;
            } catch (err) {
                errorEl.textContent = err.message;
            }
        });
    }

        /* =======================
       LEADERBOARD PAGE LOGIC
       ======================= */
    if (path === "/ranking") {
        const tbody = document.getElementById("leaderboard-body");
        const errorEl = document.getElementById("error");

        try {
            const res = await fetch("/ranking/top?limit=10");
            if (!res.ok) throw new Error("Failed to load leaderboard");

            const data = await res.json();

            tbody.innerHTML = "";

            data.forEach((row, index) => {
                const tr = document.createElement("tr");

                tr.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${row.username}</td>
                    <td>${row.click_count}</td>
                `;

                tbody.appendChild(tr);
            });
        } catch (err) {
            errorEl.textContent = err.message;
        }
    }

});
