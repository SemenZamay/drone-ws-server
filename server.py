from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()
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
    uvicorn.run(app, host="0.0.0.0", port=10000)
