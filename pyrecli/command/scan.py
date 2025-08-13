from result import Result, Ok, Err
from pyrecli.util import connect_to_codeclient


def scan_command(output_path: str) -> Result[None, str]:
    ws_result = connect_to_codeclient('read_plot')
    if ws_result.is_err():
        return Err(ws_result.err_value)
    ws = ws_result.ok_value

    print('Scanning plot...')
    ws.send('scan')

    scan_results = ws.recv()
    print('Done.')
    ws.close()

    with open(output_path, 'w') as f:
        f.write(scan_results)

    amount_templates = scan_results.count('\n')
    print(f'Scanned {amount_templates} template{"s" if amount_templates != 1 else ''} successfully.')
    
    return Ok(None)
