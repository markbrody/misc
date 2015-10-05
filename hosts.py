#!/usr/bin/env python

import os
import re

dir = os.path.expanduser('~/etc/apache2/')
confs_file = os.path.expanduser('~/etc/hosts.local')
hosts_file = '/etc/hosts'


def write_to_file(filename, data):
    file = open(filename, 'w')
    file.write(data)
    file.close()


def parse_confs():
    config = ''
    hosts = []
    excludes = ['localhost', '127.0.0.1']

    for file in os.listdir(dir):
        if re.search(r'^[^\.][\w\.]+\.conf$', file):
            config += open(dir + file).read(os.path.getsize(dir + file))
    match = re.findall(r'Server(Name|Alias)\s+([\w\t\. ]+)', config)
    for definition, name in match:
        names = re.sub(r'\s+', ' ', name).split(' ')
        for host in names:
            if host not in excludes:
                hosts.append(host)
    output = '\n'.join(str(i) for i in hosts)
    return output
    

def parse_hosts():
    hosts = re.sub(r'\s+', r'\t', open(confs_file).read(os.path.getsize(confs_file)))
    output = re.sub(r'(127\.0\.0\.1\s+localhost).*\b', r'\1\t' + hosts,
                    open(hosts_file).read(os.path.getsize(hosts_file)))
    return output


if __name__ == "__main__":
    write_to_file(confs_file, parse_confs())
    write_to_file(hosts_file, parse_hosts())

