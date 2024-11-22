import socket
import struct
import threading

# 设置服务器的IP地址和端口号
server_ip = "10.12.107.213"  # "10.13.220.234"
server_port = 12345

# 创建一个socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定IP地址和端口号
server_socket.bind((server_ip, server_port))

# 使socket开始监听传入连接
server_socket.listen(5)

print(f"Server listening on {server_ip}:{server_port}")


def handle_client(client_socket, addr):
    print(f"Connected by {addr}")
    try:
        # 接收一个字节的数据
        data = client_socket.recv(1)
        if not data:
            return

        # 解包数据
        bool_array = struct.unpack("B", data)[0]
        print(f"Received boolean array as integer: {bool_array}")
        print(f"Received boolean array as binary: {bin(bool_array)[2:].zfill(8)}")

        # 接收图片数据长度
        image_length_data = client_socket.recv(4)
        image_length = int.from_bytes(image_length_data, byteorder="big")
        print(f"Image length: {image_length}")

        # 接收图片数据
        image_data = b""
        while len(image_data) < image_length:
            packet = client_socket.recv(image_length - len(image_data))
            if not packet:
                break
            image_data += packet

        # 保存图片
        with open("received_image.png", "wb") as image_file:
            image_file.write(image_data)
        print("Image received and saved as received_image.png")

    finally:
        client_socket.close()


if __name__ == "__main__":
    while True:
        # 等待客户端连接
        client_socket, addr = server_socket.accept()
        # 为每个客户端连接创建一个新线程
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, addr)
        )
        client_thread.start()
