#!/usr/bin/env python

"""Tests for `super_json_normalize` package."""

import pytest


from super_json_normalize import super_json_normalize


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    pass

def test_path():
    """
    ensure that a variety of paths will return as expected
    """

    assert super_json_normalize.clean_path("./") == "./"
    assert super_json_normalize.clean_path(".") == "./"
    assert super_json_normalize.clean_path("/mypath/") == "/mypath/"
    assert super_json_normalize.clean_path("/mypath") == "/mypath/"