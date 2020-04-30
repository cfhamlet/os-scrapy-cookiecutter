#!/usr/bin/env python

import errno
import os
import re
import subprocess
import sys
from importlib import import_module

from cookiecutter.exceptions import FailedHookException
from cookiecutter.hooks import EXIT_SUCCESS


def log(level, *msg):
    print(f"{level}:", *msg, file=sys.stderr)


def LogError(*msg):
    log("ERROR", *msg)


def LogInfo(*msg):
    log("INFO", *msg)


def valid_project_name(project_name):
    def _module_exists(module_name):
        try:
            import_module(module_name)
            return True
        except ImportError:
            return False

    if not re.search(r"^[_a-zA-Z]\w*$", project_name):
        LogError(
            "Project names must begin with a letter and contain"
            " only\nletters, numbers and underscores"
        )
    elif _module_exists(project_name):
        LogError("Module %r already exists" % project_name)
    else:
        return True
    return False


def startproject(project_name, project_dir, cwd="."):
    run_thru_shell = sys.platform.startswith("win")
    try:
        proc = subprocess.Popen(
            ["scrapy", "startproject", project_name, project_dir],
            shell=run_thru_shell,
            cwd=cwd,
        )
        exit_status = proc.wait()
        if exit_status != EXIT_SUCCESS:
            raise FailedHookException(
                "Hook script failed (exit status: {})".format(exit_status)
            )
    except OSError as os_error:
        if os_error.errno == errno.ENOEXEC:
            raise FailedHookException(
                "Hook script failed, might be an " "empty file or missing a shebang"
            )
        raise FailedHookException("Hook script failed (error: {})".format(os_error))


try:
    pass
except Exception:
    LogError("can not import scrapy")
    sys.exit(1)

project_name = "{{cookiecutter.project_name}}"
if not valid_project_name(project_name):
    LogError(f"invalid project name: {project_name}")
    sys.exit(1)

project_dir = os.getcwd()
if not project_dir:
    LogError("do not know project dir")
    sys.exit(1)

try:
    startproject(project_name, project_dir, project_dir)
except Exception as e:
    LogError(f"scrapy startproject {e}")
    sys.exit(1)


demo_item = """

class DemoItem(scrapy.Item):
    # auto generated by os-scrapy-cookiecutter
    url = scrapy.Field()
    status = scrapy.Field()
    headers = scrapy.Field()
    meta = scrapy.Field()
    body = scrapy.Field()
"""

demo_item_file = os.path.join(project_dir, "{{cookiecutter.project_name}}", "items.py")

with open(demo_item_file, "a+") as f:
    f.write(demo_item)


demo_spider = """
import scrapy

from {{cookiecutter.project_name}}.items import DemoItem


class DemoSpider(scrapy.Spider):
    \"\"\" DemoSpider
    Auto generated by os-scrapy-cookiecuter

    Run:
        scrapy crawl demo
    \"\"\"

    name = "demo"

    start_urls = ["http://example.com/"]

    def parse(self, response):
        yield DemoItem(
            url=response.url,
            status=response.status,
            headers=response.headers,
            meta=response.meta,
            body=response.body,
        )
"""

demo_spider_file = os.path.join(
    project_dir, "{{cookiecutter.project_name}}", "spiders", "__init__.py"
)

with open(demo_spider_file, "a+") as f:
    f.write(demo_spider)
