from unittest.mock import patch
from pyrecli.pyrecli import main
from contextlib import redirect_stdout
import io


def test_directory(tmp_path, primes_input_file):
    output_dir = tmp_path / 'scripts'
    with patch('sys.argv', ['pyrecli', 'script', str(primes_input_file), str(output_dir)]):
        result = main()
        assert result == 0
        assert output_dir.exists()


def test_file(tmp_path, primes_input_file):
    output_path = tmp_path / 'primes.py'
    with patch('sys.argv', ['pyrecli', 'script', str(primes_input_file), str(output_path), '--onefile']):
        result = main()
        assert result == 0
        assert output_path.exists()


def test_stdout(primes_input_file):
    with patch('sys.argv', ['pyrecli', 'script', str(primes_input_file), '-']):
        primes_script = io.StringIO()
        with redirect_stdout(primes_script):
            result = main()
            assert result == 0
        assert primes_script
