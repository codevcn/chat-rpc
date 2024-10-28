import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="brown")

        # Tạo canvas và scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas)

        # Thiết lập canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Kết nối scrollbar với canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Đặt layout
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Scrollable Window")
        self.root.state("zoomed")

        # Tạo một ScrollableFrame
        self.scrollable_frame = ScrollableFrame(root)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.box = tk.Frame(self.scrollable_frame.scrollable_frame, bg="yellow")
        # self.box.pack(fill="both", expand=True)
        self.box.place(
            height=20, width=20, x=0, y=0, anchor="center", relwidth=1, relheight=1
        )

        # Thêm một số widget vào scrollable_frame
        for i in range(50):
            frame = tk.Frame(self.box, bg="red")
            frame.pack(padx=0, pady=10, fill="x")
            label = tk.Label(frame, text=f"Label {i+1}", bg="orange")
            label.pack(
                side="left" if i % 2 == 0 else "right",
            )  # side="left" if i % 2 == 0 else "right"


# Khởi tạo cửa sổ Tkinter
root = tk.Tk()
app = App(root)
root.mainloop()
