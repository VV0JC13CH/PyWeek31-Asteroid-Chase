"""
data.py

Parser for getting data from ini files
"""
import configparser
from pathlib import Path


def parse_path(directory, file):
    return str(Path.cwd().joinpath(directory, file).resolve())


def load_settings():
    # Let's load some data
    _settings = configparser.ConfigParser()
    _settings.read(parse_path('data', 'settings.ini'))
    return _settings


def load_parameters():
    # Let's load some data
    _parameters = configparser.ConfigParser()
    _parameters.read(parse_path('data', 'parameters.ini'))
    return _parameters

