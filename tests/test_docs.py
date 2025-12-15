from unittest.mock import patch
from pyrecli.pyrecli import main


def test_file(tmp_path, sample_input_file):
    output_file = tmp_path / 'output.md'
    with patch('sys.argv', ['pyrecli', 'docs', str(sample_input_file), str(output_file), '--title', 'Sample Docs']):
        result = main()
        assert result == 0
        assert output_file.exists()


def test_stdout(sample_input_file):
    with patch('sys.argv', ['pyrecli', 'docs', str(sample_input_file), '-', '--title', 'Sample Docs']):
        result = main()
        assert result == 0


def test_hidden(tmp_path, sample_input_file):
    output_file = tmp_path / 'output.md'
    with patch('sys.argv', ['pyrecli', 'docs', str(sample_input_file), str(output_file), '--title', 'Sample Docs', '--include_hidden']):
        result = main()
        assert result == 0
        assert output_file.exists()


def test_default_title(tmp_path, sample_input_file):
    output_file = tmp_path / 'output.md'
    with patch('sys.argv', ['pyrecli', 'docs', str(sample_input_file), str(output_file)]):
        result = main()
        assert result == 0
        assert output_file.exists()
