#!/usr/bin/python3
"""A fabric script"""
from os import path
from datetime import datetime
from fabric.api import local


def do_pack():
    """A function that generates an archive"""
    now = datetime.now()
    archive = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day,
        now.hour, now.minute, now.second
    )
    # check if archive is created
    if not path.isdir("versions"):
        if local("mkdir versions").failed:
            return None
    cmd = "cd web_static && tar -cvzf ../{} . && cd -".format(archive)
    
    if local(cmd).succeeded:
        return archive
    
    return None
