# websocket_server.py
import asyncio
import websockets
from websockets import WebSocketServerProtocol, Data
from urllib.parse import urlparse, parse_qs


class ConnectedClient:
    def __init__(self, client_socket: WebSocketServerProtocol, username: str):
        self.client_socket = client_socket
        self.username = username


connected_clients = set[ConnectedClient]()


def check_username(username: str):
    for client in connected_clients:
        if client.username == username:
            return False
    return True


def extract_username_in_path(path: str):
    username = parse_qs(urlparse(path).query)["username"]
    return username[0] if username else None


async def broadcast_all(msg: Data):
    """truyền đến tất cả mọi người"""
    for client in connected_clients:
        await client.client_socket.send(msg)


async def broadcast(websocket: WebSocketServerProtocol, data: Data):
    """truyền đến tất cả mọi người trừ người gửi"""
    for client in connected_clients:
        if client != websocket:
            await client.client_socket.send(data)


async def emit_back(websocket: WebSocketServerProtocol, data: Data):
    """truyền ngược lại người gửi"""
    await websocket.send(data)


async def chatting_ns_handler(websocket: WebSocketServerProtocol):
    try:
        async for data in websocket:
            # Phát tin nhắn tới tất cả client đã kết nối
            await broadcast(websocket, data=data)
    finally:
        # Xóa client khi ngắt kết nối
        connected_clients.remove(websocket)


async def handle_client(websocket: WebSocketServerProtocol, path: str):
    print(">>> connected client:", websocket.id, "-", path)

    # Thêm client vào danh sách các client đã kết nối
    username = extract_username_in_path(path)
    connected_clients.add(ConnectedClient(websocket, username))

    # Xử lý các namespace
    match path:
        case "/chatting":
            await chatting_ns_handler(websocket)


async def main():
    # Khởi tạo server WebSocket
    socket_server_port: int = 8000
    host_address: str = "192.168.1.10"
    async with websockets.serve(handle_client, host_address, socket_server_port):
        print(f">>> Server listening on ws://localhost:{socket_server_port}")
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
