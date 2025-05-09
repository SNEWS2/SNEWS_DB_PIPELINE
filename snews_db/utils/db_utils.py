from dotenv import load_dotenv
import os


def set_env(env_path=None):
    """Set environment parameters

    Parameters
    ----------
    env_path : `str`, (optional)
        path for the environment file.
        Use default settings if not given

    """
    default_env_path = os.path.dirname(__file__) + "/../tests/etc/test-config.env"
    env = env_path or default_env_path
    load_dotenv(env)
