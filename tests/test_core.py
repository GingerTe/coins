# coding: utf-8


def test_testing_config(app):
    assert app.config['TESTING']
