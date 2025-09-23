from dataclasses import dataclass
from dotenv import load_dotenv
import os
import sys

load_dotenv()

def _get_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError:
        return default

@dataclass(frozen=True)
class Settings:
    chunk_size: int = _get_int("CHUNK_SIZE", 800)
    chunk_overlap: int = _get_int("CHUNK_OVERLAP", 120)
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    embed_model: str = os.getenv("EMBED_MODEL","text-embedding-3-small")
    chat_model: str = os.getenv("CHAT_MODEL","gpt-4o-mini")

    def validate(self, require_api:bool = False)->None:
        errors =[]
        if (self.chunk_size <=0):
            errors.append("CHUNK_SIZE MUST BE > 0")
        if (self.chunk_overlap<0):
            errors.append("CHUNK_OVERLAP MUST >=0")
        if (require_api and not self.openai_api_key):
            errors.append("OPENAI_API_KEY is required but not set")
        if errors:
            print("Configuration error(s):",*errors,sep="\n- ")
            sys.exit(1)

settings = Settings()