from importlib.metadata import version, PackageNotFoundError

def get_version():
    try:
        return version("mysql-text-search")
    except PackageNotFoundError:
        return "0.0.0-dev"