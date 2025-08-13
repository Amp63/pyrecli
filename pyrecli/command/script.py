import os
from result import Result, Ok, Err
from dfpyre import DFTemplate
from pyrecli.util import parse_templates_from_file


def write_to_directory(dir_name: str, templates: list[DFTemplate], flags: dict[str, int|bool]):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    
    for template in templates:
        script_path = f'{dir_name}/{template._get_template_name()}.py'
        script_string = template.generate_script(**flags)
        with open(script_path, 'w') as f:
            f.write(script_string)


def write_to_single_file(file_path: str, templates: list[DFTemplate], flags: dict[str, int|bool]):
    file_content = []
    for i, template in enumerate(templates):
        if i == 0:
            template_script = template.generate_script(include_import=True, assign_variable=True, **flags)
        else:
            template_script = template.generate_script(include_import=False, assign_variable=True, **flags)
        file_content.append(template_script)

    with open(file_path, 'w') as f:
        f.write('\n\n'.join(file_content))


def script_command(input_path: str, output_path: str, one_file: bool, flags: dict[str, int|bool]) -> Result[None, str]:
    templates_result = parse_templates_from_file(input_path)
    if templates_result.is_err():
        return Err(templates_result.err_value)
    templates = templates_result.ok_value
    
    if one_file:
        write_to_single_file(output_path, templates, flags)
    else:
        write_to_directory(output_path, templates, flags)

    return Ok(None)
