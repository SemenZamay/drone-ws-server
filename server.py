# server.py
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
clients = set()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    print(f"[+] Client connected: {ws.client}")
    try:
        while True:
            data = await ws.receive_text()
            for client in clients:
                if client != ws:
                    await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(ws)
        print(f"[-] Client disconnected: {ws.client}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # 👈 Render задає PORT автоматично
    uvicorn.run(app, host="0.0.0.0", port=port)
