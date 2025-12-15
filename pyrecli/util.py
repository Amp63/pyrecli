import os
import re
import sys
import websocket
from dfpyre import DFTemplate


CODECLIENT_URL = 'ws://localhost:31375'

BASE64_REGEX = re.compile(r'^[A-Za-z0-9+/]+={0,2}$')

class TemplateParsingError(Exception):
    """Exception class for DFTemplate parsing errors"""

class NoTemplatesError(Exception):
    """Exception class for empty template list"""


def print_status(*args, **kwargs):
    """Prints a message to stderr"""
    print(*args, **kwargs, file=sys.stderr)


def connect_to_codeclient(scopes: str|None=None, token: str|None=None) -> websocket.WebSocket:
    """
    Tries to connect to the CodeClient websocket server with the specified scopes.

    Args:
        scopes: The scopes to request
        token: The CodeClient authentication token to use

    Returns:
        The connected websocket

    Raises:
        ConnectionRefusedError: If connection to the server could not be established
        PermissionError: If scope authentication fails
    """
    ws = websocket.WebSocket()
    ws.connect(CODECLIENT_URL)
    
    print_status('Connected to CodeClient.')

    if token:
        ws.send(f'token {token}')
        auth_message = ws.recv()
    elif scopes:
        print_status('Please run /auth in game.')
        ws.send(f'scopes {scopes}')
        auth_message = ws.recv()
    
    if (token or scopes):
        if auth_message != 'auth':
            raise PermissionError('Failed to authenticate.')
        else:
            print_status('Authentication successful.')
    
    return ws


def parse_templates_from_string(templates: str) -> list[DFTemplate]:
    """
    Parses a newline-delimited string of template codes into a list of templates.
    
    Args:
        templates: The string of templates to parse
    
    Returns:
        The list of parsed templates
    
    Raises:
        ValueError: If a template code is not a valid base64 string
        TemplateParsingError: If a template failed to parse
    """
    template_codes = templates.split('\n')
    
    for i, template_code in enumerate(template_codes):
        if not BASE64_REGEX.match(template_code):
            raise ValueError(f'Template code at line {i+1} is not a base64 string.')
    
    try:
        return [DFTemplate.from_code(c) for c in template_codes]
    except Exception as e:
        raise TemplateParsingError(f'Error while parsing template: {e}') from None


def read_input_file(path: str) -> str:
    """
    Returns the string content of the file at a specified path.
    If the path is a hyphen ('-'), then input will be read from stdin.

    Args:
        path: The file path to read
    
    Returns:
        The file content or input from stdin
    
    Raises:
        FileNotFoundError: If the path is not a file or the file doesn't exist
        OSError: If the file was unable to be opened or read
    """
    if path == '-':
        try:
            input_string = sys.stdin.read()
        except EOFError:
            pass
        return input_string.strip()
    
    if not os.path.isfile(path):
        raise FileNotFoundError(f'"{path}" is not a file.')
    
    with open(path, 'r') as f:
        return f.read()


def write_output_file(path: str, content: str):
    """
    Writes string content to a specified file.
    If the file path is a hyphen ('-') then the content will be printed to stdout.

    Args:
        path: The file path to write to
        content: The string content to write
    
    Raises:
        OSError: If the file was unable to be accessed
    """
    if path == '-':
        print(content, end='')
    else:
        with open(path, 'w') as f:
            f.write(content)
