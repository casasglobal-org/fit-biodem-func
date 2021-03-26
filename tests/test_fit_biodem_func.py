import pytest

from fit_biodem_func.bdm_lib import development_rate


@pytest.mark.parametrize("temperature, expected", [
    (38, 0),
    (33, 0.05637022735784853),
    (1, 0),
    (10, 0.0050399999999999915),
    (20, 0.02903999996501595),
])
def test_development_rate(temperature, expected):
    actual = development_rate(temperature, 0.0024, 3.95, 7.9, 34.95)
    assert actual == expected
