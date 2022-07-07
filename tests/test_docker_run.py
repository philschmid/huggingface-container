import pytest
import docker


def test_docker_run(tag):
    client = docker.from_env()
    client.containers.run(tag)