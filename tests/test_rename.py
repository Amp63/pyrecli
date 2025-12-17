from unittest.mock import patch
from pyrecli.pyrecli import main
from contextlib import redirect_stdout
import io
from pyrecli.util import parse_templates_from_string


def test_file(tmp_path, rename_input_file):
    output_file = tmp_path / 'renamed.dfts'
    with patch('sys.argv', ['pyrecli', 'rename', str(rename_input_file), str(output_file), 'MY_CONSTANT', 'RENAMED_CONSTANT']):
        result = main()
        assert result == 0
        assert output_file.exists()


def test_stdout(rename_input_file):
    with patch('sys.argv', ['pyrecli', 'rename', str(rename_input_file), '-', 'MY_CONSTANT', 'RENAMED_CONSTANT']):
        result = main()
        assert result == 0


def test_local(rename_input_file):
    with patch('sys.argv', ['pyrecli', 'rename', str(rename_input_file), '-', 'i', 'j', '-s', 'line']):
        renamed_templates = io.StringIO()
        with redirect_stdout(renamed_templates):
            result = main()
            assert result == 0
        
        parse_templates_from_string(renamed_templates.getvalue())  # Make sure output templates can be parsed
