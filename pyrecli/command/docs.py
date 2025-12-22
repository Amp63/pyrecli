from typing import Literal, TypedDict
from dfpyre import DFTemplate, Item, Parameter
from pyrecli.util import read_input_file, write_output_file, parse_templates_from_string


STARTER_BLOCK_LOOKUP = {
    'func': 'Function',
    'process': 'Process'
}


def escape_md(s: str) -> str:
    MD_CHARS = r'*`$#!&^~'
    for char in MD_CHARS:
        s = s.replace(char, rf'\{char}')
    return s


class TemplateDocData(TypedDict):
    template_type: Literal['Function', 'Process']
    function_name: str
    doc_lines: list[str]


def docs_command(input_path: str, output_path: str, title: str, include_hidden: bool, omit_toc: bool):
    templates_string = read_input_file(input_path)
    templates = parse_templates_from_string(templates_string)

    def get_function_name(template: DFTemplate) -> str:
        first_block = template.codeblocks[0]
        function_name = first_block.data.get('data')
        return escape_md(function_name)

    block_type_order = list(STARTER_BLOCK_LOOKUP.keys())
    templates = [t for t in templates if t.codeblocks[0].action_name == 'dynamic']
    templates.sort(key=get_function_name)
    templates.sort(key=lambda t: block_type_order.index(t.codeblocks[0].type))

    output_lines: list[str] = [
        f'# {title}',
        ''
    ]

    template_docs: list[TemplateDocData] = []
    for template in templates:
        first_block = template.codeblocks[0]

        # Skip if hidden
        if first_block.tags.get('Is Hidden') == 'True' and not include_hidden:
            continue

        # Add function / process name
        template_type = STARTER_BLOCK_LOOKUP[first_block.type]
        template_name = get_function_name(template)
        template_doc_lines: list[str] = []      

        template_doc_lines.append(f'## {template_type}: {template_name}')

        # Parse description
        if first_block.args:
            first_arg = first_block.args[0]
            if isinstance(first_arg, Item):
                try:
                    lore_text = [escape_md(l.to_string()) for l in first_arg.get_lore()]
                    if lore_text:
                        template_doc_lines.extend(lore_text)
                except:
                    # There are so many things that can go wrong here due to various legacy
                    # item formats and weird MC string edge cases, so we can just skip
                    # if there's a problem.
                    pass
            
        # Parse parameters
        parameter_lines: list[str] = []
        for arg in first_block.args:
            if isinstance(arg, Parameter):
                optional_text = "*" if arg.optional else ""
                default_value_text = f'= `{escape_md(arg.default_value.__repr__())}`' if arg.default_value else ''
                parameter_lines.append(f'- *`{escape_md(arg.name)}{optional_text}`*: `{arg.param_type.get_string_value()}` {default_value_text}')
                if arg.description:
                    parameter_lines.append(f'  - {escape_md(arg.description)}')
                if arg.note:
                    parameter_lines.append(f'  - {escape_md(arg.note)}')
        if parameter_lines:
            template_doc_lines.append('')
            template_doc_lines.append('### Parameters:')
            template_doc_lines.extend(parameter_lines)
        
        doc_data = TemplateDocData(template_type=template_type, function_name=template_name, doc_lines=template_doc_lines)
        template_docs.append(doc_data)
    

    # Add table of contents
    def add_toc_group(doc_data_list: list[TemplateDocData], group_title: str):
        if doc_data_list:
            output_lines.append(f'### {group_title}')
            for doc_data in doc_data_list:
                link = f'#{doc_data["template_type"]}-{doc_data["function_name"]}'.lower().replace(' ', '-')
                output_lines.append(f'- [{doc_data["function_name"]}]({link})')
    
    if not omit_toc:
        output_lines.append('## Contents')
        function_templates = [d for d in template_docs if d['template_type'] == 'Function']
        add_toc_group(function_templates, 'Functions')
        output_lines.append('')
        process_templates = [d for d in template_docs if d['template_type'] == 'Process']
        add_toc_group(process_templates, 'Processes')
        output_lines.append('\n')

    # Add template docs to output lines
    for doc_data in template_docs:
        output_lines.extend(doc_data['doc_lines'])
        output_lines.append('')
    
    write_output_file(output_path, '\n'.join(output_lines))
