import pytest
from pathlib import Path
import io
from contextlib import redirect_stdout
from pyrecli.command.cctoken import cctoken_command


@pytest.fixture
def fixtures_dir():
    return Path(__file__).parent / 'fixtures'


@pytest.fixture
def sample_input_file(fixtures_dir):
    return fixtures_dir / 'sample.dfts'


@pytest.fixture
def rename_input_file(fixtures_dir):
    return fixtures_dir / 'rename_sample.dfts'


@pytest.fixture
def primes_input_file(fixtures_dir):
    return fixtures_dir / 'primes_sample.dfts'


@pytest.fixture
def slice_input_file(fixtures_dir):
    return fixtures_dir / 'slice_sample.dfts'


@pytest.fixture(scope='session')
def codeclient_auth_token():
    SCOPES = 'read_plot inventory'

    f = io.StringIO()
    with redirect_stdout(f):
        cctoken_command('-', SCOPES)
    
    return f.getvalue()
