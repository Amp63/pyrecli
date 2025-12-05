from result import Result, Err
from pyrecli.util import read_input_file, write_output_file, parse_templates_from_string

def slice_command(input_path: str, output_path: str, target_length: int) -> Result[None, str]:
    input_result = read_input_file(input_path)
    if input_result.is_err():
        return Err(input_result.err_value)

    templates_result = parse_templates_from_string(input_result.ok_value)
    if templates_result.is_err():
        return Err(templates_result.err_value)
    templates = templates_result.ok_value

    if not templates:
        return Err(f'Could not find any templates in {input_path}')
    
    first_template = templates[0]
    sliced_templates = first_template.slice(target_length)
    built_templates = [t.build() for t in sliced_templates]

    return write_output_file(output_path, '\n'.join(built_templates))
