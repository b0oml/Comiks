import os
import shutil
import toml

HOME = os.path.expanduser('~')
HOME_CONFIG_DIR = os.path.join(HOME, '.config/comiks')
HOME_CONFIG_FILE = os.path.join(HOME_CONFIG_DIR, 'config.toml')

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(CURRENT_PATH, 'config.toml')


def init_config_file():
    if not os.path.isfile(HOME_CONFIG_FILE):
        os.makedirs(HOME_CONFIG_DIR, exist_ok=True)
        shutil.copyfile(DEFAULT_CONFIG_FILE, HOME_CONFIG_FILE)


def load_config(config_path=None):
    if config_path is None:
        init_config_file()
        config_path = HOME_CONFIG_FILE

    with open(config_path) as f:
        return toml.loads(open(config_path).read())
