import socket
import time


def is_connected():
    try:
        # connect to the host -- tells us if the host is actually reachable
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        pass
    return False


def main():
    while True:
        if is_connected():
            print("Connected")
        else:
            print("Not connected")
        time.sleep(1)


if __name__ == "__main__":
    main()
