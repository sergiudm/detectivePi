import socket


def do_client(gesture, server_ips, server_port):  # gesture is int, server_ips is a list
    """
    Establishes connections with a list of servers and sends a gesture.

    Args:
        gesture: The gesture to send (should be a string, not an int, to be encoded).
        server_ips: A list of server IP addresses.
        server_port: The port to connect to on each server.
    """
    sockets = []
    for server_ip in server_ips:
        try:
            # Create a socket object
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the server
            client_socket.connect((server_ip, server_port))
            print(f"Connected to {server_ip}:{server_port}")

            sockets.append(client_socket)

        except ConnectionRefusedError:
            print(f"Connection refused for {server_ip}:{server_port}")
        except Exception as e:
            print(f"Error connecting to {server_ip}:{server_port}: {e}")

    try:
        for client_socket in sockets:
            # Send the gesture to each connected server
            client_socket.sendall(
                str(gesture).encode("utf-8")
            )  # Convert gesture to string
            print(f"Sent gesture '{gesture}' to {client_socket.getpeername()}")

    except KeyboardInterrupt:
        print("Interrupted by user. Closing connections...")
    except Exception as e:
        print(f"Error sending data: {e}")
    finally:
        # Close all connections
        for client_socket in sockets:
            try:
                client_socket.shutdown(socket.SHUT_RDWR)
            except Exception as e:
                print(f"Error during shutdown: {e}")
            finally:
                client_socket.close()
        print("Connections closed.")
