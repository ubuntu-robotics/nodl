from ament_flake8.main import main

import pytest


@pytest.mark.flake8
@pytest.mark.linter
def test_flake8():
    rc = main(argv=['--linelength', '100'])
    assert rc == 0, 'Found errors'
