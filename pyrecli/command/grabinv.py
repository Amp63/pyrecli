import json
from result import Result, Ok, Err
import amulet_nbt
from amulet_nbt import CompoundTag, StringTag
from pyrecli.util import write_output_file, connect_to_codeclient


def grabinv_command(output_path: str) -> Result[None, str]:
    ws_result = connect_to_codeclient('inventory')
    if ws_result.is_err():
        return Err(ws_result.err_value)
    ws = ws_result.ok_value

    ws.send('inv')
    inventory = ws.recv()
    inventory_nbt = amulet_nbt.from_snbt(inventory)

    template_codes: list[str] = []
    for tag in inventory_nbt:
        components: CompoundTag = tag.get('components')
        if components is None:
            continue

        custom_data: CompoundTag = components.get('minecraft:custom_data')
        if custom_data is None:
            continue
            
        pbv_tag: CompoundTag = custom_data.get('PublicBukkitValues')
        if pbv_tag is None:
            continue
        
        code_template_data: StringTag = pbv_tag.get('hypercube:codetemplatedata')
        if code_template_data is None:
            continue
        
        code_template_json = json.loads(str(code_template_data))
        
        template_code = code_template_json.get('code')
        if template_code:
            template_codes.append(template_code)

    if not template_codes:
        return Err('Could not find any templates in the inventory.')

    output_result = write_output_file(output_path, '\n'.join(template_codes))
    if output_result.is_err():
        return output_result
    
    return Ok(None)
