#!/usr/bin/env python3

import subprocess
import json
from pprint import pprint


def get_root(package):
    result = subprocess.run(['brew', '--cellar', package], capture_output=True)
    return result.stdout.decode('utf-8').strip()


def get_info(package):
    result = subprocess.run(['brew', 'info', '--json=v1', package], capture_output=True)
    return json.loads(result.stdout)


def build_tree(package, visited):
    if package in visited:
        return

    info = get_info(package)[0]
    dependencies = list(dep['full_name'] for dep in info['installed'][0]['runtime_dependencies'])
    root = get_root(package)

    visited[package] = {
        'package': package,
        'root': root,
        'info': info,
        'dependencies': dependencies,
    }

    for d in dependencies:
        build_tree(d, visited)

print("Hello from GRAB.py")

packages = {'python@3.9': {}}
build_tree('gtk+3', packages)
del packages['python@3.9']

# pprint(packages)

with open('./packages.json', 'w') as f:
    f.write(json.dumps(packages, indent=2))

dirs = list(p['root'] for p in packages.values())

subprocess.run(['tar', '-cf' './gtk.tar', './packages.json'] + dirs)
