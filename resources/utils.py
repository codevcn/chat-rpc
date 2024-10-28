from PIL import Image, ImageTk
import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, height, width=0, bg="white"):
        super().__init__(parent, height=height, bg=bg)

        # Tạo canvas và scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.main_frame = tk.Frame(self.canvas)

        # Thiết lập canvas
        self.main_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        # Kết nối scrollbar với canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Đặt layout
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

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
