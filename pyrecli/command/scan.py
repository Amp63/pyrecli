from result import Result, Err
from pyrecli.util import write_output_file, connect_to_codeclient


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

    write_result = write_output_file(output_path, scan_results)
    return write_result
