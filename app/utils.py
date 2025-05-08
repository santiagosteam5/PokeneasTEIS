import socket

def get_docker_id():
    return socket.gethostname()