from pyrecli.util import connect_to_codeclient, write_output_file


def cctoken_command(output_path: str, scopes: str):
    ws = connect_to_codeclient(scopes)

    ws.send('token')
    token = ws.recv().replace('token ', '')

    write_output_file(output_path, token)
