import socket
import struct

# 设置服务器的IP地址和端口号
server_ip = "10.13.220.234"
server_port = 12345

# 创建一个socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定IP地址和端口号
server_socket.bind((server_ip, server_port))

# 使socket开始监听传入连接
server_socket.listen(5)

print(f"Server listening on {server_ip}:{server_port}")

while True:
    # 等待客户端连接
    client_socket, addr = server_socket.accept()
    print(f"Connected by {addr}")

    try:
        # # 接收一个字节的数据
        # data = client_socket.recv(1)
        # if not data:
        #     break

        # # 解包数据
        # bool_array = struct.unpack('B', data)[0]
        # print(f"Received boolean array as integer: {bool_array}")
        # print(f"Received boolean array as binary: {bin(bool_array)[2:].zfill(8)}")

        # # 回传确认信息
        # client_socket.sendall(b"Received")

        ###

        # 接收图片数据长度
        data_length = int.from_bytes(client_socket.recv(4), byteorder="big")

        # 接收图片数据
        image_data = b""
        while len(image_data) < data_length:
            packet = client_socket.recv(4096)  # 每次接收4096字节
            if not packet:
                break
            image_data += packet

        # 将接收到的图片数据写入文件
        with open("store/received_image.jpg", "wb") as image_file:
            image_file.write(image_data)

        ###

    except KeyboardInterrupt:
        client_socket.close()
    finally:
        # 关闭连接
        client_socket.close()

# 关闭服务器socket（实际上不会执行到这里，因为服务器会一直运行）
server_socket.close()
