from importlib.resources import files

from wgfinder import __version__


def test_version():
    assert __version__ == "0.3"


def test_package_resources_are_available():
    assert files("wgfinder").joinpath("templates", "message.txt").is_file()
    assert files("wgfinder").joinpath("config", "logging.ini").is_file()
