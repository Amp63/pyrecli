import sys
import argparse
import importlib.metadata

from pyrecli.command.scan import scan_command
from pyrecli.command.send import send_command
from pyrecli.command.script import script_command
from pyrecli.command.rename import rename_command
from pyrecli.command.grabinv import grabinv_command
from pyrecli.command.docs import docs_command
from pyrecli.command.slice import slice_command
from pyrecli.command.cctoken import cctoken_command
from pyrecli.util import print_status


def rename_target_scope(value):
    SCOPES = {'game', 'saved', 'local', 'line'}
    if value not in SCOPES:
        raise argparse.ArgumentTypeError(f'Expected one of {SCOPES} for rename target scope')
    return value


def slice_target_length(value):
    MINIMUM_LENGTH = 5
    ivalue = int(value)
    if ivalue < MINIMUM_LENGTH:
        raise argparse.ArgumentTypeError(f'Target length must be at least {MINIMUM_LENGTH} codeblocks')
    return ivalue


def main() -> int:
    parser = argparse.ArgumentParser(prog='pyrecli', description='Command line utilities for DiamondFire templates')
    parser.add_argument('--version', '-v', action='version', version=f'pyrecli {importlib.metadata.version('pyrecli')}')
    subparsers = parser.add_subparsers(dest='command', help='Available commands:', required=True, metavar='<command>')

    parser_scan = subparsers.add_parser('scan', help='Scan the current plot templates with CodeClient')
    parser_scan.add_argument('output_path', help='The file to output template data to', type=str)
    parser_scan.add_argument('--token', '-t', help='The CodeClient authentication token to use', type=str, default=None)

    parser_send = subparsers.add_parser('send', help='Send templates to DiamondFire with CodeClient')
    parser_send.add_argument('input_path', help='The file containing template data', type=str)

    parser_script = subparsers.add_parser('script', help='Create python scripts from template data')
    parser_script.add_argument('input_path', help='The file containing template data', type=str)
    parser_script.add_argument('output_path', help='The file or directory to output to', type=str)
    parser_script.add_argument('--onefile', help='Output template data as a single script', action='store_true')
    parser_script.add_argument('--indent_size', '-i', help='The multiple of spaces to add when indenting lines', type=int, default=4)
    parser_script.add_argument('--literal_shorthand', '-ls', help='Output Text and Number items as strings and ints respectively', action='store_false')
    parser_script.add_argument('--var_shorthand', '-vs', help='Write all variables using variable shorthand', action='store_true')
    parser_script.add_argument('--preserve_slots', '-s', help='Save the positions of items within chests', action='store_true')
    parser_script.add_argument('--build_and_send', '-b', help='Add `.build_and_send()` to the end of the generated template(s)', action='store_true')

    parser_rename = subparsers.add_parser('rename', help='Rename all occurrences of a variable')
    parser_rename.add_argument('input_path', help='The file containing template data', type=str)
    parser_rename.add_argument('output_path', help='The file to output to', type=str)
    parser_rename.add_argument('var_to_rename', help='The variable to rename', type=str)
    parser_rename.add_argument('new_var_name', help='The new name for the variable', type=str)
    parser_rename.add_argument('--var_scope', '-s', help='The scope to match', type=rename_target_scope, default=None)

    parser_grabinv = subparsers.add_parser('grabinv', help='Save all templates in the inventory to a file with CodeClient')
    parser_grabinv.add_argument('output_path', help='The file to output template data to', type=str)
    parser_grabinv.add_argument('--token', '-t', help='The CodeClient authentication token to use', type=str, default=None)

    parser_docs = subparsers.add_parser('docs', help='Generate markdown documentation from template data')
    parser_docs.add_argument('input_path', help='The file containing template data', type=str)
    parser_docs.add_argument('output_path', help='The file to output to', type=str)
    parser_docs.add_argument('--title', '-t', help='The title for the docs', type=str, default='Template Docs')
    parser_docs.add_argument('--include_hidden', '-ih', help='Include hidden functions and processes', action='store_true')
    parser_docs.add_argument('--notoc', help='Omit the table of contents', action='store_true')

    parser_slice = subparsers.add_parser('slice', help='Slice a template into multiple smaller templates')
    parser_slice.add_argument('input_path', help='The file containing template data', type=str)
    parser_slice.add_argument('output_path', help='The file to output template data to', type=str)
    parser_slice.add_argument('target_length', help='The maximum length of each sliced template', type=slice_target_length)

    parser_cctoken = subparsers.add_parser('cctoken', help='Request a CodeClient token with the specified scopes')
    parser_cctoken.add_argument('output_path', help='The file to output the token to', type=str)
    parser_cctoken.add_argument('scopes', help='The scopes to request', type=str)


    parsed_args = parser.parse_args()

    try:
        match parsed_args.command:
            case 'scan':
                scan_command(parsed_args.output_path, parsed_args.token)
            
            case 'send':
                send_command(parsed_args.input_path)
            
            case 'script':
                scriptgen_flags = {
                    'indent_size': parsed_args.indent_size, 
                    'literal_shorthand': parsed_args.literal_shorthand,
                    'var_shorthand': parsed_args.var_shorthand,
                    'preserve_slots': parsed_args.preserve_slots,
                    'build_and_send': parsed_args.build_and_send
                }
                script_command(parsed_args.input_path, parsed_args.output_path, parsed_args.onefile, scriptgen_flags)
            
            case 'rename':
                rename_command(
                    parsed_args.input_path, parsed_args.output_path,
                    parsed_args.var_to_rename, parsed_args.new_var_name, parsed_args.var_scope
                )
            
            case 'grabinv':
                grabinv_command(parsed_args.output_path, parsed_args.token)
            
            case 'docs':
                docs_command(
                    parsed_args.input_path, parsed_args.output_path,
                    parsed_args.title, parsed_args.include_hidden, parsed_args.notoc
                )
            
            case 'slice':
                slice_command(
                    parsed_args.input_path, parsed_args.output_path,
                    parsed_args.target_length
                )
            
            case 'cctoken':
                cctoken_command(parsed_args.output_path, parsed_args.scopes)
    
    except Exception as e:
        print_status(e)
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
