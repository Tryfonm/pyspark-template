import pytest


@pytest.mark.xfail
def test_divide_by_zero():
    assert 1 / 0 == 1


def test_one_equals_one():
    assert 1 == 1
