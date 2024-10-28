# Hệ thống chat (trao đổi văn bản) trong mạng nội bộ theo nhóm với gRCP

## Cách setup và chạy server:

1. Clone repo xuống local
2. Điều hướng đến thư mục root
3. Chạy `./ins` (terminal) hoặc `ins.cmd` (cmd) để cài các thư viện cần thiết
4. Sau khi cài xong, vào file dev.cmd để thay đổi rootfolder thành thư mục root vừa clone vào và chạy file dev.cmd như bước 3 để chạy server, lúc này 1 tab shell mới được mở ra
5. Sau khi chạy server xong, tại tab mới vừa được mở, chạy file ui.cmd để mở giao diện Tkinter

## Về `git commit`:

- Ta sử dụng thư viện pre-commit để format code trước khi đẩy code lên github nên quá trình commit sẽ mất thêm thời gian để format (sẽ mất nhiều thời gian hơn cho lần format đầu tiên, có thể tới vài phút, vì tụi thư viện thực hiện setup môi trường cho các lần format sau đó)
- Khi thực hiện `git commit` ta sẽ thực hiện 2 lần (hoặc 1 lần nếu ko có lỗi format), lần đầu để format, lần 2 để thực sự commit
- Còn ae nào ko thích format thì thêm cờ `--no-verify` (`git commit --no-verify`) để bỏ qua tụi pre-commit. Nhưng mà đã làm cái format thì vui lòng tuân theo, thằng nào mà bỏ qua pre-commit thì coi chừng tao...
