import os
from dfpyre import DFTemplate
from pyrecli.util import read_input_file, write_output_file, parse_templates_from_string


def write_to_directory(dir_name: str, templates: list[DFTemplate], flags: dict[str, int|bool]):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    
    for template in templates:
        script_path = f'{dir_name}/{template.get_template_name()}.py'
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
    
    write_output_file(file_path, '\n\n'.join(file_content))


def script_command(input_path: str, output_path: str, one_file: bool, flags: dict[str, int|bool]):
    templates_string = read_input_file(input_path)
    templates = parse_templates_from_string(templates_string)
    
    if one_file or output_path == '-':
        return write_to_single_file(output_path, templates, flags)
    
    return write_to_directory(output_path, templates, flags)
