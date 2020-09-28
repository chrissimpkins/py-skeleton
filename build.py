#!/usr/bin/env python3

import glob
import os
import shutil
import sys

import toml

TEMPLATE_DIRS = os.path.join("lib", "PROJECT")

TEMPLATE_FILES = (
    "setup.py",
    "Makefile",
    ".travis.yml",
    os.path.join("lib", "PROJECT", "__main__.py"),
    os.path.join("github-IN", "py-coverage.yml"),
    os.path.join("github-IN", "py-lint.yml"),
    os.path.join("github-IN", "py-typecheck.yml"),
)

README_FILE = "README.md"

PROJECT = "{{ PROJECT }}"
DESCRIPTION = "{{ DESCRIPTION }}"
AUTHOR = "{{ AUTHOR }}"
EMAIL = "{{ EMAIL }}"
URL = "{{ URL }}"
MIN_PY = "{{ PYTHON }}"
LICENSE = "{{ LICENSE }}"

try:
    with open("project.toml") as f:
        settings = toml.load(f)
except Exception as e:
    sys.stderr.write(
        f"[ERROR] Failed to read the project.toml settings file with "
        f"error: {str(e)}{os.linesep}"
    )
    sys.exit(1)

assert "project" in settings and settings["project"] != ""
assert "description" in settings and settings["description"] != ""
assert "author" in settings and settings["author"] != ""
assert "email" in settings and settings["email"] != ""
assert "url" in settings and settings["url"] != ""
assert "min_python" in settings and settings["min_python"] != ""
assert "license" in settings and settings["license"] != ""

# Introduction
project_name = settings["project"]
print(f"Starting '{project_name}' build...")
# replace template strings in files with user settings
for filepath in TEMPLATE_FILES:
    with open(filepath, "r") as fr:
        file_text = fr.read()

    file_text = file_text.replace(PROJECT, settings["project"])
    file_text = file_text.replace(DESCRIPTION, settings["description"])
    file_text = file_text.replace(AUTHOR, settings["author"])
    file_text = file_text.replace(EMAIL, settings["email"])
    file_text = file_text.replace(URL, settings["url"])
    file_text = file_text.replace(MIN_PY, settings["min_python"])
    file_text = file_text.replace(LICENSE, settings["license"])

    with open(filepath, "w") as fw:
        fw.write(file_text)
    print(f"[*] Built template: {filepath}...")

# update library path name
os.rename(TEMPLATE_DIRS, os.path.join("lib", settings["project"]))
print(f"[*] Changed library directory name to: '{project_name}'...")

# update README.md text
with open(README_FILE, "w") as fw:
    fw.write(f"## {project_name}{os.linesep}")
    print(f"[*] Updated README.md file with '{project_name}' project name...")

# move GH Action configuration files to
# appropriate dir path for execution on CI
try:
    for filepath in glob.glob("github-IN/*.yml"):
        filename = os.path.basename(filepath)
        newpath = os.path.join(".github", "workflows", filename)
        shutil.move(filepath, newpath)
        print(f"[*] moved {filename} GitHub Action configuration to production dir")
except Exception as e:
    sys.stderr.write(f"File move error. {e}{os.linesep}")
    sys.exit(1)

# clean up GH Action template in directory
shutil.rmtree("github-IN")
print("[*] Cleaned up temp in paths...")

print("[*] Build complete!")
print("OK to remove the build.py and project.toml files")
