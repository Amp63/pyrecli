from typing import Literal
import re
from dfpyre import Variable, Number, String, Text, Parameter
from pyrecli.util import read_input_file, write_output_file, parse_templates_from_string


TEXT_CODE_PATTERNS = [
    re.compile(r"%var\(([a-zA-Z0-9!@#$%^&*~`\-_=+\\|;':\",.\/<>? ]+)\)"),
    re.compile(r"%index\(([a-zA-Z0-9!@#$%^&*~`\-_=+\\|;':\",.\/<>? ]+),\d+\)"),
    re.compile(r"%entry\(([a-zA-Z0-9!@#$%^&*~`\-_=+\\|;':\",.\/<>? ]+),[a-zA-Z0-9!@#$%^&*~`\-_=+\\|;':\",.\/<>? ]+\)")
]


def rename_var_in_text_code(s: str, var_to_rename: str, new_var_name: str):
    for pattern in TEXT_CODE_PATTERNS:
        match = pattern.search(s)
        if match and match.group(1) == var_to_rename:
            s = s.replace(match.group(1), new_var_name)
    return s


def rename_command(input_path: str, output_path: str,
                   var_to_rename: str, new_var_name: str,
                   var_to_rename_scope: Literal['game', 'saved', 'local', 'line']|None):
    
    templates_string = read_input_file(input_path)
    templates = parse_templates_from_string(templates_string)

    for template in templates:
        for codeblock in template.codeblocks:
            for argument in codeblock.args:
                # Try to rename variable
                if isinstance(argument, Variable):
                    if argument.name == var_to_rename and (var_to_rename_scope is None or argument.scope == var_to_rename_scope):
                        argument.name = new_var_name
                    argument.name = rename_var_in_text_code(argument.name, var_to_rename, new_var_name)
                
                # Try to rename parameter
                elif isinstance(argument, Parameter) and var_to_rename_scope == 'line':
                    if argument.name == var_to_rename:
                        argument.name = new_var_name
                
                # Check for occurrences of the variable in text codes
                elif isinstance(argument, (Number, String, Text)) and isinstance(argument.value, str):
                    argument.value = rename_var_in_text_code(argument.value, var_to_rename, new_var_name)
            
            # Check for text codes in function calls
            if codeblock.type in {'call_func', 'start_process'}:
                new_data = rename_var_in_text_code(codeblock.data.get('data'), var_to_rename, new_var_name)
                codeblock.data['data'] = new_data
    
    new_file_content = '\n'.join(t.build() for t in templates)
    write_output_file(output_path, new_file_content)
