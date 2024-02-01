#!/usr/bin/python3
"""Fabric script"""
from os import path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ["52.86.41.7", "18.207.2.253"]


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


def do_deploy(archive_path):
    """Distributes archives to web servers"""
    if not path.exists(archive_path):
        return False

    compressed_file = archive_path.split("/")[-1]
    file_name = compressed_file.split(".")[0]
    upload_path = "/tmp/{}".format(compressed_file)

    if put(archive_path, upload_path).failed:
        return False

    current_release = '/data/web_static/releases/{}'.format(file_name)
    if run("rm -rf {}".format(current_release)).failed:
        return False

    if run("mkdir -p {}".format(current_release)).failed:
        return False

    uncompress = "tar -xzf /tmp/{} -C {}".format(
        compressed_file, current_release
    )
    if run(uncompress).failed:
        return False

    delete_archive = "rm -f /tmp/{}".format(compressed_file)
    if run(delete_archive).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False

    relink = "ln -s {} /data/web_static/current".format(current_release)
    if run(relink).failed:
        return False

    return True


def deploy():
    """Creates and distributes an archive to your web servers"""
    archive_path = do_pack()

    if archive_path is None:
        return False

    return do_deploy(archive_path)
