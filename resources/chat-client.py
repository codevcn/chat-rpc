# tkinter_client.py
import tkinter as tk
import asyncio
import websockets
import threading
from tkinter import messagebox
from utils import create_label_image, ScrollableFrame
import json

# styling
regular_font_xsm_bold = ("Arial", 10, "bold")
regular_font_sm = ("Arial", 12)
regular_font_sm_bold = ("Arial", 12, "bold")
regular_font_empty = ("Arial", 15, "bold")
default_user_avt_path = "./resources/imgs/user-avt.png"
default_guest_avt_path = "./resources/imgs/guest-avt.png"


class ChatRoomScreen:
    msg_user_avts_sharing: list = []
    empty_msg_flag: bool = True

    def __init__(self, root: tk.Tk, username: str) -> None:
        self.root = root
        self.username = username

        # Tạo frame
        self.root_frame = tk.Frame(self.root)
        self.root_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Regular var
        reg_color = "white"

        # Tạo avatar
        self.avt_frame = tk.Frame(self.root_frame)
        self.avt_frame.pack(pady=(0, 10), fill="x")
        self.user_photo = create_label_image(default_user_avt_path, height=50, width=50)
        self.user_avt = tk.Label(self.avt_frame, image=self.user_photo)
        self.user_avt.pack(side="left")
        self.user_info = tk.Label(
            self.avt_frame, text=f"username: {username}", font=regular_font_sm_bold
        )
        self.user_info.pack(side="left", padx=(10, 0))

        # Tạo messages list
        self.msg_list = ScrollableFrame(self.root_frame, pady=5, padx=5)
        self.msg_list.pack(fill="both", expand=True)

        # Empty messages
        self.empty_msg = tk.Label(
            self.msg_list.main_frame,
            bg=reg_color,
            text="Empty...",
            font=regular_font_empty,
            fg="gray",
        )
        self.empty_msg.pack(expand=True, anchor="center")

        # Tạo frame nhập tin nhắn
        self.msg_entry_frame = tk.Frame(self.root_frame)
        self.msg_entry_frame.pack(pady=(10, 10), fill="x", side="bottom")
        # Tạo thanh input
        self.msg_entry = tk.Entry(
            self.msg_entry_frame, borderwidth=0.5, relief="solid", font=regular_font_sm
        )
        self.msg_entry.pack(fill="both", side="left", expand=True)
        self.msg_entry.bind("<Return>", lambda e: self.send_message())
        self.msg_entry.focus()
        # Tạo nút gửi tin nhắn
        self.send_button = tk.Button(
            self.msg_entry_frame,
            text="Gửi Tin Nhắn",
            command=lambda: self.send_message(),
            borderwidth=0.5,
            relief="solid",
            font=regular_font_sm_bold,
            bg="#000",
            fg="#fff",
        )
        self.send_button.bind(
            "<Enter>", lambda e: self.send_button.config(cursor="hand2")
        )
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(cursor=""))
        self.send_button.pack(side="right")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Tạo sự kiện để đóng kết nối
        self.stop_event = asyncio.Event()

        # Khởi chạy vòng lặp asyncio trong luồng mới
        threading.Thread(target=self.run_async_loop, daemon=True).start()

    async def connect_ws_server(self):
        host_address: str = "192.168.1.10"
        socket_server_port: int = 8000
        chatting_ns: str = "chatting"
        uri = f"ws://{host_address}:{socket_server_port}/{chatting_ns}?username={self.username}"
        self.websocket = await websockets.connect(uri)
        print(">>> connected to ws server")
        await self.receive_messages()

    async def receive_messages(self):
        while not self.stop_event.is_set():
            try:
                data = await self.websocket.recv()
                res_data = json.loads(data)
                self.show_message(
                    res_data["message"],
                    res_data["username"],
                )
            except websockets.ConnectionClosed:
                break

    def show_message(self, message: str, username: str):
        # Hiển thị tin nhắn trên giao diện Tkinter
        myself = username == self.username

        if self.empty_msg_flag:
            self.empty_msg.destroy()
            self.empty_msg_flag = False

        msg_frame = tk.Frame(self.msg_list.main_frame, bg="white")
        msg_frame.pack(fill="x", pady=(0, 10))
        self.msg_user_avts_sharing.append(
            create_label_image(
                default_user_avt_path if myself else default_guest_avt_path,
                height=25,
                width=25,
            )
        )
        msg_user_avt = tk.Label(
            msg_frame,
            image=self.msg_user_avts_sharing[len(self.msg_user_avts_sharing) - 1],
            bg="white",
        )
        reg_color = "#b5faff"
        wrapper = tk.Frame(msg_frame, bg=reg_color)
        msg_text_frame = tk.Frame(wrapper, bg=reg_color)
        msg_text_frame.pack(padx=5, pady=(0, 5), fill="x")
        msg_username = tk.Label(
            msg_text_frame,
            text=username,
            borderwidth=0,
            font=regular_font_xsm_bold,
            bg=reg_color,
            fg="brown",
        )
        msg_username.pack(pady=(0, 5))
        msg_text = tk.Label(
            msg_text_frame,
            text=message,
            borderwidth=0,
            font=regular_font_sm,
            bg=reg_color,
        )
        msg_text.pack()
        if myself:
            msg_user_avt.pack(side="right", anchor="n")
            wrapper.pack(side="right", padx=(0, 5))
            msg_username.pack(pady=(0, 5), anchor="e")
        else:
            reg_color = "#b5ffde"
            msg_user_avt.pack(side="left", anchor="n")
            wrapper.pack(side="left", padx=(5, 0))
            wrapper.config(bg=reg_color)
            msg_text_frame.config(bg=reg_color)
            msg_username.pack(anchor="w")
            msg_username.config(bg=reg_color)
            msg_text.config(bg=reg_color)

    def validate_message_before_send(self, message: str):
        if len(message) == 0:
            messagebox.showerror("Message is empty", "Please enter your message!")
            return False
        return True

    def send_message(self):
        data = {"message": self.msg_entry.get(), "username": self.username}
        if self.validate_message_before_send(data["message"]):
            asyncio.run_coroutine_threadsafe(
                self.websocket.send(json.dumps(data)), self.loop
            )
            self.show_message(data["message"], data["username"])
            self.msg_entry.delete(0, tk.END)

    async def close_connection(self):
        self.stop_event.set()
        await self.websocket.close()  # Đóng kết nối một cách chuẩn xác

    def run_async_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect_ws_server())

    def on_closing(self):
        # Đảm bảo kết nối đóng đúng cách trước khi thoát
        asyncio.run_coroutine_threadsafe(self.close_connection(), self.loop).result()
        self.loop.stop()
        self.root.destroy()


class AuthScreen:
    min_len_username: int = 2
    max_len_username: int = 20

    def __init__(self, root: tk.Tk, show_chat_room_window):
        self.root = root
        self.show_chat_room_window = show_chat_room_window

        # Tạo frame
        self.root_frame = tk.Frame(self.root)
        self.root_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame nhập username
        self.username_frame = tk.Frame(self.root_frame)
        self.username_frame.pack(expand=True)
        # Label hướng dẫn
        self.label = tk.Label(self.username_frame, text="Enter your username:")
        self.label.pack(pady=10)

        # Entry để nhập username
        self.username_entry = tk.Entry(
            self.username_frame,
            width=30,
            borderwidth=0.5,
            font=regular_font_sm,
            relief="solid",
        )
        self.username_entry.pack(pady=5, fill="x")
        self.username_entry.bind("<Return>", lambda e: self.confirm_username())
        self.username_entry.focus()

        # Button xác nhận username
        self.confirm_button = tk.Button(
            self.username_frame,
            text="Confirm",
            command=self.confirm_username,
            relief="solid",
            font=regular_font_sm_bold,
            bg="#000",
            fg="#fff",
        )
        self.confirm_button.bind(
            "<Enter>", lambda e: self.confirm_button.config(cursor="hand2")
        )
        self.confirm_button.bind(
            "<Leave>", lambda e: self.confirm_button.config(cursor="")
        )
        self.confirm_button.pack(pady=10)

    def confirm_username(self):
        username = self.username_entry.get().strip()
        if self.min_len_username <= len(username) <= self.max_len_username:
            # Gọi callback để chuyển sang giao diện chat nếu username hợp lệ
            self.show_chat_room_window(username)
        else:
            messagebox.showerror(
                "Invalid Username", "Username must be between 1 and 20 characters."
            )

    def destroy(self):
        # Xóa các widget của cửa sổ nhập username
        self.label.destroy()
        self.root_frame.destroy()
        self.username_entry.destroy()
        self.confirm_button.destroy()


class RootLayout:
    def __init__(self) -> None:
        # Tạo root
        self.root = tk.Tk()
        self.root.title("Giao diện Nhắn tin")
        self.root.geometry("600x300")
        self.root.state("zoomed")

        self.show_username_window()

        # Khởi tạo giao diện Tkinter
        self.root.mainloop()

    def show_username_window(self):
        self.auth_window = AuthScreen(self.root, self.show_chat_room_window)

    def show_chat_room_window(self, username):
        # Xóa cửa sổ nhập username
        self.auth_window.destroy()

        # Tạo cửa sổ phòng chat khi username hợp lệ
        self.chat_room_window = ChatRoomScreen(self.root, username)


# Khởi tạo giao diện Tkinter và chạy client
RootLayout()
