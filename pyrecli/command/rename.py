from typing import Literal
import re
from result import Result, Ok, Err
from dfpyre import Variable, Number, String, Text
from pyrecli.util import parse_templates_from_file


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


def rename_command(input_path: str, output_path: str|None,
                   var_to_rename: str, new_var_name: str,
                   renamed_var_scope: Literal['game', 'saved', 'local', 'line']|None) -> Result[None, str]:
    templates_result = parse_templates_from_file(input_path)
    if templates_result.is_err():
        return Err(templates_result.err_value)
    templates = templates_result.ok_value

    for template in templates:
        for codeblock in template.codeblocks:
            for argument in codeblock.args:
                if isinstance(argument, Variable):
                    if argument.name == var_to_rename:
                        if renamed_var_scope is None:
                            argument.name = new_var_name
                        elif argument.scope != renamed_var_scope:
                            argument.name = new_var_name
                    argument.name = rename_var_in_text_code(argument.name, var_to_rename, new_var_name)
                
                elif isinstance(argument, (Number, String, Text)) and isinstance(argument.value, str):
                    argument.value = rename_var_in_text_code(argument.value, var_to_rename, new_var_name)
            
            if codeblock.type in {'call_func', 'start_process'}:
                new_data = rename_var_in_text_code(codeblock.data.get('data'), var_to_rename, new_var_name)
                codeblock.data['data'] = new_data
    
    new_file_content = '\n'.join(t.build() for t in templates)
    write_path = output_path if output_path else input_path
    with open(write_path, 'w') as f:
        f.write(new_file_content)
    
    return Ok(None)
