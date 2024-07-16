import re

def headers_list_to_dict(headers: list) -> dict:
    dict = {}
    for header in headers:
        header_name = re.search(r"(.*):", header).group(1)
        header_value = re.search(r": (.*)", header).group(1)
        dict[header_name] = header_value
    return dict


def print_startup_message():
    print(r"""
 _      ____  ______   ____ 
| |    / __ \|  __  \ / __ \
| |   | |  | | |__)  | |  | |  
| |   | |  | |  __  /| |  | |  
| |___| |__| | |  \ \| |__| |
|______\____/|_|   \_\\____/
          
A simple http server implementing just 
standard python libraries :)
____________________________________          
""")