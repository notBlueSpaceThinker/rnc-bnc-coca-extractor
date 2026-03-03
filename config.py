from environs import Env

env = Env()
env.read_env()

def load_RNC_token() -> str:
    return env.str("RNC_TOKEN")

def load_BNC_token() -> str:
    return env.str("BNC_TOKEN")

def load_COCA_token() -> str:
    return env.str("COCA_TOKEN")