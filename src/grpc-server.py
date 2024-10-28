import grpc
from concurrent import futures
import chat_pb2
import chat_pb2_grpc


class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def GetOnlineUsers(self, request, context):
        # Trả về danh sách người dùng online (dùng với Tkinter)
        pass

    def SendMessage(self, request, context):
        # Xử lý gửi tin nhắn
        pass


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
server.add_insecure_port("[::]:50051")
server.start()
print(">>> grpc server is working")
server.wait_for_termination()
