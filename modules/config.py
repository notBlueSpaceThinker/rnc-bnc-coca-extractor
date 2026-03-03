from environs import Env
from dataclasses import dataclass

env = Env()
env.read_env()

def load_RNC_token() -> str:
    return env.str("RNC_TOKEN")

@dataclass
class CorpusSettings:
    RNC_SUBCORPUS: str
    DATE_START: int
    DATE_END: int

def load_corpus_settings() -> CorpusSettings:
    return CorpusSettings(
        RNC_SUBCORPUS=env.str("RNC_SUBCORPUS", default="MAIN"),
        DATE_START=env.int("DATE_START", default=2000),
        DATE_END=env.int("DATE_END", default=2026)
    )
    
