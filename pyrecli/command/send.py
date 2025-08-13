from result import Result, Ok, Err
from pyrecli.util import connect_to_codeclient, parse_templates_from_file


def send_command(input_path: str) -> Result[None, str]:
    templates_result = parse_templates_from_file(input_path)
    if templates_result.is_err():
        return Err(templates_result.err_value)
    templates = templates_result.ok_value

    ws_result = connect_to_codeclient()
    if ws_result.is_err():
        return Err(ws_result.err_value)
    ws = ws_result.ok_value

    for template in templates:
        item = template.generate_template_item()
        ws.send(f'give {item.get_snbt()}')
    
    ws.close()
    print(f'Sent {len(templates)} template{"s" if len(templates) != 1 else ''} successfully.')
    return Ok(None)