import socket


def do_client(gesture, server_ip, server_port):  # gesture is int
    # 创建一个socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接到服务器
    client_socket.connect((server_ip, server_port))

    try:
        client_socket.sendall(gesture.encode("utf-8"))

    except KeyboardInterrupt:
        # shutdown the connection
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
        print("Exit")
    finally:
        # 关闭连接
        client_socket.close()
