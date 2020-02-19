#!/usr/bin/env python3

import yaml
import argparse

parser = argparse.ArgumentParser(description='Script for generating ssh config file from hosts map yaml file.')

parser.add_argument("-i", "--input", help="Output file name.", required=True)
parser.add_argument("-o", "--output", help="Input file name.", required=True)
parser.add_argument("-k", "--key", help="Identity file (default: ~/.ssh/id_ed25519)", default="~/.ssh/id_ed25519")

args = parser.parse_args()

with open(args.input, 'r') as r, open(args.output, 'w+') as w:
    data = yaml.safe_load(r)
    for host, v in data.items():
      w.write(
"""Host {}
  HostName {}
  IdentityFile {}
  User ubuntu
  ProxyJump {}

""".format(host, v['ip'], args.key, v['bastion']))
