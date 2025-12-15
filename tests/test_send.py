import pytest
from unittest.mock import patch
import io
import sys
import time
from pyrecli.pyrecli import main


@pytest.mark.codeclient_api
@pytest.mark.cc_send
def test_file(sample_input_file):
    with patch('sys.argv', ['pyrecli', 'send', str(sample_input_file)]):
        result = main()
        time.sleep(0.1)
        assert result == 0


@pytest.mark.codeclient_api
@pytest.mark.cc_send
def test_stdin(sample_input_file, monkeypatch):
    templates = sample_input_file.read_text()
    redirected_stdin = io.StringIO(templates)
    monkeypatch.setattr(sys, 'stdin', redirected_stdin)
    
    with patch('sys.argv', ['pyrecli', 'send', '-']):
        result = main()
        time.sleep(0.1)
        assert result == 0
