from unittest.mock import patch
from pyrecli.pyrecli import main
from contextlib import redirect_stdout
import io
from pyrecli.util import parse_templates_from_string
from dfpyre.tool.slice import get_template_length


def test_file(tmp_path, slice_input_file):
    TARGET_LENGTH = 30
    output_path = tmp_path / 'sliced.dfts'
    with patch('sys.argv', ['pyrecli', 'slice', str(slice_input_file), str(output_path), str(TARGET_LENGTH)]):
        result = main()
        assert result == 0
        assert output_path.exists()


def test_stdout(slice_input_file):
    TARGET_LENGTH = 30
    with patch('sys.argv', ['pyrecli', 'slice', str(slice_input_file), '-', str(TARGET_LENGTH)]):
        template_strings = io.StringIO()
        with redirect_stdout(template_strings):
            result = main()
            assert result == 0
        
        sliced_templates = parse_templates_from_string(template_strings.getvalue())
        for template in sliced_templates:
            assert get_template_length(template.codeblocks) <= TARGET_LENGTH


def test_small_target(slice_input_file):
    TARGET_LENGTH = 15
    with patch('sys.argv', ['pyrecli', 'slice', str(slice_input_file), '-', str(TARGET_LENGTH)]):
        template_strings = io.StringIO()
        with redirect_stdout(template_strings):
            result = main()
            assert result == 0
        
        sliced_templates = parse_templates_from_string(template_strings.getvalue())
        for template in sliced_templates:
            assert get_template_length(template.codeblocks) <= TARGET_LENGTH


def test_large_target(slice_input_file):
    TARGET_LENGTH = 300
    with patch('sys.argv', ['pyrecli', 'slice', str(slice_input_file), '-', str(TARGET_LENGTH)]):
        template_strings = io.StringIO()
        with redirect_stdout(template_strings):
            result = main()
            assert result == 0
        
        sliced_templates = parse_templates_from_string(template_strings.getvalue())
        assert len(sliced_templates) == 1
