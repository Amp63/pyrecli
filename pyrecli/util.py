import os
import re
from result import Result, Ok, Err
import websocket
from dfpyre import DFTemplate


CODECLIENT_URL = 'ws://localhost:31375'

BASE64_REGEX = re.compile(r'^[A-Za-z0-9+/]+={0,2}$')


def connect_to_codeclient(scopes: str|None=None) -> Result[websocket.WebSocket, str]:
    ws = websocket.WebSocket()
    try:
        ws.connect(CODECLIENT_URL)
    except ConnectionRefusedError:
        return Err('Failed to connect to CodeClient.')
    
    print('Connected to CodeClient.')

    if scopes:
        print('Please run /auth in game.')
        ws.send(f'scopes {scopes}')
        auth_message = ws.recv()

        if auth_message != 'auth':
            return Err('Failed to authenticate.')
        print('Authentication received.')
    
    return Ok(ws)


def parse_templates_from_string(templates: str) -> Result[list[DFTemplate], str]:
    template_codes = templates.split('\n')
    
    for i, template_code in enumerate(template_codes):
        if not BASE64_REGEX.match(template_code):
            return Err(f'Template code at line {i+1} is not a base64 string.')
    
    try:
        return Ok([DFTemplate.from_code(c) for c in template_codes])
    except Exception as e:
        return Err(str(e))


def read_input_file(path: str) -> Result[str, str]:
    if path == '-':
        try:
            input_string = input()
        except EOFError:
            return Ok(input_string)
    
    if not os.path.isfile(path):
        return Err(f'"{path}" is not a file.')
    
    try:
        with open(path, 'r') as f:
            return Ok(f.read())
    except OSError as e:
        return Err(str(e))


def write_output_file(path: str, content: str) -> Result[None, str]:
    if path == '-':
        print(content, end='')
    else:
        try:
            with open(path, 'w') as f:
                f.write(content)
        except OSError as e:
            return Err(str(e))

    return Ok(None)
