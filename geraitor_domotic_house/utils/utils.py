from pathlib import Path

def get_root_path():
    """
    This method returns the root path of the project.

    Returns:
        The root path of the project.

    """
    return Path(__file__).parent.parent


def get_config_path():
    """
    This method returns the path where the configuration files should be.

    Returns:
        The path of the configuration folder. By default /config.

    """
    return get_root_path() / 'config'


def get_project_root():
    """
    This method returns the root folder of the project.

    Returns:
        The path of the root folder of the project.

    """
    return get_root_path().parent


def get_output_path():
    """
    This method returns the folder where the output files will be stored.

    Returns:
        The path of the output folder.

    """
    if not os.path.exists(Path.cwd() / 'output'):
        os.mkdir(Path.cwd() / "output")
    return Path.cwd() / 'output'
