import tkinter as tk

root = tk.Tk()
root.geometry("400x300")

# Tạo Frame cho thanh tiện ích ở dưới cùng
bottom_bar = tk.Frame(root, bg="gray", height=40)
bottom_bar.pack(side="bottom", fill="x")

# Thêm các nút vào thanh tiện ích
save_button = tk.Button(bottom_bar, text="Save", bg="lightgray")
cancel_button = tk.Button(bottom_bar, text="Cancel", bg="lightgray")

save_button.pack(side="left", padx=10, pady=5)
cancel_button.pack(side="right", padx=10, pady=5)

# Tạo Canvas để chứa nội dung cuộn
content_canvas = tk.Canvas(root)
content_canvas.pack(side="left", fill="both", expand=True)

# Thêm thanh cuộn dọc cho Canvas
scrollbar = tk.Scrollbar(root, orient="vertical", command=content_canvas.yview)
scrollbar.pack(side="right", fill="y")
content_canvas.configure(yscrollcommand=scrollbar.set)

# Frame chứa nội dung bên trong Canvas
content_frame = tk.Frame(content_canvas)
content_canvas.create_window((0, 0), window=content_frame, anchor="nw")


# Cập nhật vùng cuộn của Canvas
def update_scroll_region(event):
    content_canvas.configure(scrollregion=content_canvas.bbox("all"))


content_frame.bind("<Configure>", update_scroll_region)

# Thêm nội dung vào content_frame
for i in range(30):
    label = tk.Label(content_frame, text=f"Content Item {i+1}", bg="white")
    label.pack(pady=5, padx=10)

root.mainloop()
