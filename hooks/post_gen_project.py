#!/usr/bin/env python
import os
import sys


def log(level, *msg):
    print(f"{level}:", *msg, file=sys.stderr)


def LogError(*msg):
    log("ERROR", *msg)


def write_scrapy_requirement(project_dir):
    requirements_file = os.path.join(project_dir, "requirements", "requirements.txt")
    with open(requirements_file, "a+") as f:
        import scrapy

        requirement = "Scrapy>=" + scrapy.__version__
        f.write(requirement)


project_dir = os.getcwd()
if not project_dir:
    LogError("do not know project dir")
    sys.exit(1)

try:
    write_scrapy_requirement(project_dir)
except Exception as e:
    LogError(f"write scrapy version to requirements file {e}")
    sys.exit(1)
