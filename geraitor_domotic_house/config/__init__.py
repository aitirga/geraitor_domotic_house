"""
This configuration module initializes the logging and local/global configuration variables
"""
import logging.config
import os
from pathlib import Path
import pandas as pd

import yaml
from box import Box

from geraitor_domotic_house.utils import get_config_path
import logging

logger = logging.getLogger(__name__)
# First read the local configuration file

try:
    _config_file = list(
        Path(os.getcwd()).glob("**/*config*.yaml") and Path(os.getcwd()).glob("**/*config*.yaml") and Path().cwd().glob(
            "*config*.yml") and Path().cwd().glob(
            "*config*.yaml"))
    _config_file = _config_file if _config_file else list(Path(__file__).parent.glob("config.yml"))
    assert len(_config_file) == 1, "Please provide a configuration file that has a '*config.yaml' name structure"
    local_configuration_file = _config_file[0]
except IndexError:
    local_configuration_file = get_config_path() / "local_config.yml"
    logging.warning(
        f"Local configuration file was not provided, using default local_config.yml instead (located at {get_config_path() / 'local_config.yml'}")
with open(local_configuration_file.absolute(), "r") as yml_file:
    local_yaml_file = yaml.safe_load(yml_file)
    try:
        config = Box(local_yaml_file, default_box=True)
    except:
        config =Box({}, default_box=True)

# Add global configuration
if not config.globals.is_globals_loaded:
    try:
        with open(get_config_path() / "global_config.yml", "r") as yml_file:
            local_yaml_file = yaml.safe_load(yml_file)
            config.globals = local_yaml_file
            config.globals.is_globals_loaded = True
    except:
        config.globals = {}
        config.globals.is_globals_loaded = True

# Initialize logging
if not config.globals.is_logging_loaded or config.general.unittest:
    os.makedirs(Path.cwd() / "logs", exist_ok=True)
    with open(get_config_path() / "logger_config.yml", "r") as yml_file:
        log_config = yaml.safe_load(yml_file)
        logging.config.dictConfig(log_config)
        config.globals.is_logging_loaded = True
if not config.general.use_pandas_chained_warning:
    pd.options.mode.chained_assignment = None  # default='warn'