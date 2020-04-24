import pathlib

import os_scrapy_cookiecutter


def test_version():
    version_file = (
        pathlib.Path(__file__)
        .parents[1]
        .joinpath("src/os_scrapy_cookiecutter/VERSION")
        .absolute()
    )
    assert os_scrapy_cookiecutter.__version__ == open(version_file).read().strip()


if __name__ == "__main__":
    test_version()
