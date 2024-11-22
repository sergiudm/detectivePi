import socket
import struct

# 设置服务器的IP地址和端口号
server_ip = "10.13.220.234"  # 替换X为服务器的实际IP地址
server_port = 12345

# 创建一个socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务器
client_socket.connect((server_ip, server_port))

try:
    # 创建一个8位的布尔数组
    bool_array = [1, 0, 0, 1, 0, 0, 1, 0]  # 示例数组

    # 将布尔数组打包成一个字节
    packed_data = struct.pack("B", int("".join(map(str, bool_array)), 2))
    # 发送数据到服务器
    client_socket.sendall(packed_data)

    with open("resources/test.png", "rb") as image_file:
        image_data = image_file.read()

    # 发送图片数据长度
    client_socket.sendall(len(image_data).to_bytes(4, byteorder="big"))

    # 发送图片数据
    client_socket.sendall(image_data)

    ###

    # 接收服务器的响应
    #response = client_socket.recv(1024)
    #print(f"Received from server: {response.decode('utf-8')}")
except KeyboardInterrupt:
    # shutdown the connection
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
    print("Exit")
finally:
    # 关闭连接
    client_socket.close()
