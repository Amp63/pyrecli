import json
from rapidnbt import nbtio, CompoundTagVariant
from pyrecli.util import write_output_file, connect_to_codeclient, print_status


def grabinv_command(output_path: str, token: str|None=None):
    ws = connect_to_codeclient('inventory', token)

    ws.send('inv')
    inventory = ws.recv()
    ws.close()

    inventory = f'{{inventory:{inventory}}}'
    inventory_nbt = nbtio.loads_snbt(inventory)

    template_codes: list[str] = []
    for tag in inventory_nbt['inventory']:
        tag: CompoundTagVariant
        components = tag['components']
        if components.is_null():
            continue

        custom_data = components['minecraft:custom_data']
        if custom_data.is_null():
            continue
            
        pbv_tag = custom_data['PublicBukkitValues']
        if pbv_tag.is_null():
            continue
        
        code_template_data = pbv_tag['hypercube:codetemplatedata']
        if code_template_data.is_null():
            continue
        
        code_template_json = json.loads(code_template_data.get_string())
        
        template_code = code_template_json.get('code')
        if template_code:
            template_codes.append(template_code)

    if not template_codes:
        print_status('Could not find any templates in the inventory.')

    write_output_file(output_path, '\n'.join(template_codes))
