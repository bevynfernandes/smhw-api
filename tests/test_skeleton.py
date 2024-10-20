import pytest

import smhw_api as api

__author__ = "bevynfernandes"
__copyright__ = "bevynfernandes"
__license__ = "GPL-3.0-or-later"


def test_server():
    """API Tests"""
    with pytest.raises(api.exceptions.InvalidAuth):
        api.Client("Should fail - Test Auth", 0, 0)
