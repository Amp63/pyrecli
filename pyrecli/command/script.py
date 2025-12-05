import os
from result import Result, Ok, Err
from dfpyre import DFTemplate
from pyrecli.util import read_input_file, write_output_file, parse_templates_from_string


def write_to_directory(dir_name: str, templates: list[DFTemplate], flags: dict[str, int|bool]) -> Result[None, str]:
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    
    for template in templates:
        script_path = f'{dir_name}/{template._get_template_name()}.py'
        script_string = template.generate_script(**flags)
        try:
            with open(script_path, 'w') as f:
                f.write(script_string)
        except OSError as e:
            return Err(str(e))
    
    return Ok(None)


def write_to_single_file(file_path: str, templates: list[DFTemplate], flags: dict[str, int|bool]) -> Result[None, str]:
    file_content = []
    for i, template in enumerate(templates):
        if i == 0:
            template_script = template.generate_script(include_import=True, assign_variable=True, **flags)
        else:
            template_script = template.generate_script(include_import=False, assign_variable=True, **flags)
        file_content.append(template_script)
    
    return write_output_file(file_path, '\n\n'.join(file_content))


def script_command(input_path: str, output_path: str, one_file: bool, flags: dict[str, int|bool]) -> Result[None, str]:
    input_result = read_input_file(input_path)
    if input_result.is_err():
        return Err(input_result.err_value)

    templates_result = parse_templates_from_string(input_result.ok_value)
    if templates_result.is_err():
        return Err(templates_result.err_value)
    templates = templates_result.ok_value
    
    if one_file or output_path == '-':
        return write_to_single_file(output_path, templates, flags)
    
    return write_to_directory(output_path, templates, flags)
