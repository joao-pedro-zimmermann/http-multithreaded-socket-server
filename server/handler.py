import re
import zlib
import logging
import config
from utils import headers_list_to_dict

def conn_handler(cli_socket):
    try:
        request_data = cli_socket.recv(4096)
        request_data_str = request_data.decode('utf-8')

        split_request = request_data_str.split('\r\n')
        request_line = split_request[0]
        headers = split_request[1:-2]
        body = split_request[-1]

        headers_dict = headers_list_to_dict(headers)
        method = request_line.split(' ')[0]
        path = request_line.split(' ')[1].split('/')
        
        logging.info(f"Path called: {'/'.join(path)}")
        
        response = generate_response(method, path, headers_dict, body)
        
        total_sent = 0
        while total_sent < len(response):
            sent = cli_socket.send(response[total_sent:])
            if sent == 0:
                raise RuntimeError('Socket connection broke')
            total_sent += sent
    except Exception as e:
        logging.error(f"Error handling request: {e}")
    finally:
        cli_socket.close()
        logging.info('Connection closed')

def generate_response(method, path, headers_dict, body):
    try:
        match path[1]:
            case '':
                return b'HTTP/1.1 200 OK\r\n\r\n'
            case 'user-agent':
                return handle_user_agent(headers_dict)
            case 'echo':
                return handle_echo(path, headers_dict)
            case 'files':
                return handle_files(method, path, body)
            case _:
                return b'HTTP/1.1 404 Not Found\r\n\r\n'
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return b'HTTP/1.1 500 Internal Server Error\r\n\r\n'

def handle_user_agent(headers_dict):
    user_agent = headers_dict.get('User-Agent', 'Unknown')
    header_value_bytes_len = len(user_agent.encode())
    response_string = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {header_value_bytes_len}\r\n\r\n{user_agent}'
    return response_string.encode()

def handle_echo(path, headers_dict):
    response_string = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n'
    string_bytes = path[2].encode()
    if 'Accept-Encoding' in headers_dict:
        accept_encoding = headers_dict['Accept-Encoding'].split(', ')
        if 'gzip' in accept_encoding:
            response_string += 'Content-Encoding: gzip\r\n'
            compressed_data = zlib.compress(string_bytes, wbits=31)
            data_len = len(compressed_data)
            response_string += f'Content-Length: {data_len}\r\n\r\n'
            return response_string.encode() + compressed_data
    str_bytes_len = len(string_bytes)
    response_string += f'Content-Length: {str_bytes_len}\r\n\r\n{path[2]}'
    return response_string.encode()

def handle_files(method, path, body):
    filename = path[2]
    if method == 'GET':
        return handle_file_get(filename)
    if method == 'POST':
        return handle_file_post(filename, body)
    return b'HTTP/1.1 405 Method Not Allowed\r\n\r\n'

def handle_file_get(filename):
    try:
        with open(f'{config.DIRECTORY}/{filename}', 'rb') as f:
            file = f.read()
        file_length = len(file)
        response_string = f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {file_length}\r\n\r\n'
        return response_string.encode() + file
    except FileNotFoundError:
        return b'HTTP/1.1 404 Not Found\r\n\r\n'

def handle_file_post(filename, body):
    with open(f'{config.DIRECTORY}/{filename}', 'w') as f:
        f.write(body)
    return b'HTTP/1.1 201 Created\r\n\r\n'
