import tkinter as tk

root = tk.Tk()
root.geometry("400x300")

# Tạo Frame cho thanh tiện ích ở dưới cùng
bottom_bar = tk.Frame(root, bg="gray", height=40)
bottom_bar.pack(side="bottom", fill="x")

# Tạo Frame cho navbar
navbar = tk.Frame(root, bg="blue", height=40)
navbar.pack(side="top", fill="x")

# Thêm các nút vào navbar
home_button = tk.Button(navbar, text="Home", bg="lightblue")
about_button = tk.Button(navbar, text="About", bg="lightblue")
contact_button = tk.Button(navbar, text="Contact", bg="lightblue")

home_button.pack(side="left", padx=10, pady=5)
about_button.pack(side="left", padx=10, pady=5)
contact_button.pack(side="left", padx=10, pady=5)

# Tạo canvas cho nội dung cuộn
content_canvas = tk.Canvas(root, bg="green")
content_canvas.pack(side="left", fill="both", expand=True)

# Thêm thanh cuộn dọc
scrollbar = tk.Scrollbar(root, orient="vertical", command=content_canvas.yview)
scrollbar.pack(side="right", fill="y")
content_canvas.configure(yscrollcommand=scrollbar.set)

# Frame cho nội dung bên trong canvas
content_frame = tk.Frame(content_canvas, bg="pink")
frame_id = content_canvas.create_window((0, 0), window=content_frame, anchor="nw")


def on_canvas_configure(event):
    content_canvas.itemconfig(frame_id, width=event.width)


content_canvas.bind("<Configure>", on_canvas_configure)


# Hàm cập nhật vùng cuộn của canvas
def update_scroll_region(event):
    content_canvas.configure(scrollregion=content_canvas.bbox("all"))


content_frame.bind("<Configure>", update_scroll_region)

content_canvas.bind_all(
    "<MouseWheel>",
    lambda e: content_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
)

# Thêm nội dung vào content_frame
for i in range(20):
    box = tk.Frame(content_frame, bg="brown")
    box.pack(fill="x", pady=10, padx=10, expand=True)
    label = tk.Label(box, text=f"Content Item {i+1}", bg="white")
    label.pack(side="left" if i % 2 == 0 else "right")

root.mainloop()
