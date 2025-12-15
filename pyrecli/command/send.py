from pyrecli.util import connect_to_codeclient, read_input_file, parse_templates_from_string, print_status


def send_command(input_path: str):
    templates_string = read_input_file(input_path)
    templates = parse_templates_from_string(templates_string)

    ws = connect_to_codeclient()

    for template in templates:
        item = template.generate_template_item()
        ws.send(f'give {item.get_snbt()}')
    
    ws.close()
    
    print_status(f'Sent {len(templates)} template{"s" if len(templates) != 1 else ''} successfully.')
