def package_get_version():
    with open("version.txt", "r") as f:
        return f.read().strip()


def package_minimal_setup():
    from setuptools import setup

    return setup(
        version=package_get_version()
    )
