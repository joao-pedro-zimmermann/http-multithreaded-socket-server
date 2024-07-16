# HTTP Multithreaded Socket Server

## Overview

This HTTP Socket server is a simple application designed to study concepts of the HTTP protocol and the use of the `socket` library. It is multithreaded and can handle multiple simultaneous connections. The server accepts a few example endpoints, each performing a specific function.

## Accepted Endpoints

1. **Root (`/`)**
    - **Supported Method**: `GET`
    - **Description**: Returns a basic response indicating that the server is running.
    - **Response**:
      ```
      HTTP/1.1 200 OK
      ```

2. **User-Agent (`/user-agent`)**
    - **Supported Method**: `GET`
    - **Description**: Returns the value of the `User-Agent` header sent by the client.
    - **Response**:
      ```
      HTTP/1.1 200 OK
      Content-Type: text/plain
      Content-Length: <value length>
      
      <User-Agent value>
      ```

3. **Echo (`/echo/<message>`)**
    - **Supported Method**: `GET`
    - **Description**: Returns the message provided in the path. If the `Accept-Encoding` header includes `gzip`, the response will be compressed.
    - **Response** (without gzip):
      ```
      HTTP/1.1 200 OK
      Content-Type: text/plain
      Content-Length: <message length>
      
      <message>
      ```
    - **Response** (with gzip):
      ```
      HTTP/1.1 200 OK
      Content-Type: text/plain
      Content-Encoding: gzip
      Content-Length: <compressed message length>
      
      <compressed message>
      ```

4. **Files (`/files/<filename>`)**
    - **Supported Methods**: `GET`, `POST`
    - **Description**: 
        - **GET**: Returns the contents of the specified file. If the file does not exist, it returns a 404 error.
        - **POST**: Creates or replaces the specified file with the request body.
    - **GET Response (file found)**:
      ```
      HTTP/1.1 200 OK
      Content-Type: application/octet-stream
      Content-Length: <file length>
      
      <file content>
      ```
    - **GET Response (file not found)**:
      ```
      HTTP/1.1 404 Not Found
      ```
    - **POST Response**:
      ```
      HTTP/1.1 201 Created
      ```

## Limitations

- **Request Size**: The server reads up to 4096 bytes of the request body. Larger requests may not be processed correctly.
- **Threads**: Each accepted connection is handled in a new thread. In high-load environments, this can lead to resource exhaustion.
- **File Directory**: The server must be started with a specified directory for file operations (`/files`). If not specified, file operations may fail.
- **Gzip**: Gzip compression is only supported on the `/echo` endpoint.

## Startup Example

To start the server, use the following command:
```bash
python3 server/main.py --directory <file directory>
