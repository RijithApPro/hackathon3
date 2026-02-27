"""Tests for Challenge 1: Hello World."""
from hello_world import greet, main
import io
import sys


def test_greet_default():
    assert greet() == "Hello, World!"


def test_greet_custom_name():
    assert greet("Automotive Developer") == "Hello, Automotive Developer!"


def test_main_output(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out
    assert "Hello, Automotive Developer!" in captured.out
    assert "Environment setup complete" in captured.out
