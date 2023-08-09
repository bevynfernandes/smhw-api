import pytest

import smhw_api as api

__author__ = "EpicGamerCodes"
__copyright__ = "EpicGamerCodes"
__license__ = "GPL-3.0-or-later"


def test_server():
    """API Tests"""
    with pytest.raises(api.exceptions.InvalidAuth):
        api.Server("Should fail - Test Auth", 0, 0)
