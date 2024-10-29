from PIL import Image, ImageTk
import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, height=0, width=0, bg="white", pady=0, padx=0):
        super().__init__(parent, height=height, width=width)

        # Tạo canvas và scrollbar
        self.canvas = tk.Canvas(self, bg=bg)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        # Frame cho content bên trong canvas
        self.main_frame = tk.Frame(self.canvas, bg=bg, pady=pady, padx=padx)

        # Thiết lập canvas
        self.main_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.main_frame_id = self.canvas.create_window(
            (0, 0), window=self.main_frame, anchor="nw"
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.main_frame_id, width=e.width),
        )

        # Kết nối scrollbar với canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )


def create_label_image(img_path: str, height: int, width: int):
    """
    tạo ảnh với thư viện PIL

    Các tham số:
        img_path (str): đường dẫn tới ảnh.
        height (int): chiều cao của ảnh (pixels).
        width (int): chiều rộng của ảnh (pixels).
    """
    return ImageTk.PhotoImage(Image.open(img_path).resize((width, height)))
