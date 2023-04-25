from pathlib import Path

from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

environ_env = Env()
environ_env.read_env()
