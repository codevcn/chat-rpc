from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    print(">>> Hello, World! 1")  # In ra màn hình console
    return ">>> Hello, World! 2"  # Trả về chuỗi "Hello, World!" khi truy cập trang web


if __name__ == "__main__":
    app.run(debug=True, port=5555)
