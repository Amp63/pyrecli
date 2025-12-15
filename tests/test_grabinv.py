import pytest
from unittest.mock import patch
import time
from pyrecli.pyrecli import main


@pytest.mark.codeclient_api
@pytest.mark.cc_grabinv
def test_file(tmp_path, codeclient_auth_token):
    output_file = tmp_path / 'templates.dfts'
    with patch('sys.argv', ['pyrecli', 'grabinv', str(output_file), '--token', codeclient_auth_token]):
        result = main()
        time.sleep(0.1)  # Wait for the socket to finish closing
        assert result == 0
        assert output_file.exists()


@pytest.mark.codeclient_api
@pytest.mark.cc_grabinv
def test_stdout(codeclient_auth_token):
    with patch('sys.argv', ['pyrecli', 'grabinv', '-', '--token', codeclient_auth_token]):
        result = main()
        time.sleep(0.1)
        assert result == 0
