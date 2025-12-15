from pyrecli.util import read_input_file, write_output_file, parse_templates_from_string, NoTemplatesError


def slice_command(input_path: str, output_path: str, target_length: int):
    templates_string = read_input_file(input_path)
    templates = parse_templates_from_string(templates_string)

    if not templates:
        raise NoTemplatesError(f'Could not find any templates in {input_path}')
    
    first_template = templates[0]
    sliced_templates = first_template.slice(target_length)
    built_templates = [t.build() for t in sliced_templates]

    write_output_file(output_path, '\n'.join(built_templates))
