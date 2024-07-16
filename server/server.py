import socket
import threading
import logging
from handler import conn_handler

def start_server():
    logging.info("Starting server...")
    with socket.create_server(("localhost", 4221), reuse_port=True) as server:
        logging.info("Server started, waiting for connections...")
        while True:
            conn, addr = server.accept()
            logging.info(f"Connection accepted from {addr}")
            threading.Thread(target=conn_handler, args=[conn]).start()
