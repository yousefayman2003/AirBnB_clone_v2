#!/usr/bin/python3
"""A Fabric script"""
import os
from fabric.api import cd, env, local, run

env.hosts = ["52.86.41.7", "18.207.2.253"]

def do_clean(number=0):
    """
        Deletes out-of-date archives
        Args:
            number (int): number of the archives
    """
    n = 1 if int(number) == 0 else int(number)
    
    files = [f for f in os.listdir('./versions')]
    files.sort(reverse=True)
    
    for file_ in files[n:]:
        local("rm -f versions/{}".format(file_))
    
    remote = "/data/web_static/releases/"
    with cd(remote):
        tgz = run(
            "ls -tr | grep -E '^web_static_([0-9]{6,}){1}$'"
        ).split()
        tgz.sort(reverse=True)
        for arc in tgz[n:]:
            run("rm -rf {}{}".format(remote, arc))
