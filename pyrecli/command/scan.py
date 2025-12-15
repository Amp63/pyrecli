from pyrecli.util import write_output_file, connect_to_codeclient, print_status


def scan_command(output_path: str, token: str|None=None):
    ws = connect_to_codeclient('read_plot', token)

    print_status('Scanning plot...')
    ws.send('scan')

    scan_results = ws.recv()
    print_status('Done.')
    ws.close()

    write_output_file(output_path, scan_results)
