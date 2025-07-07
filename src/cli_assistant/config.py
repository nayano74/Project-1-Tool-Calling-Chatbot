from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

@dataclass
class Config:
    openai_api_key: str
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.7
    
    @classmethod
    def from_env(cls) -> 'Config':
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        return cls(
            openai_api_key=api_key,
            model_name=os.getenv('MODEL_NAME', 'gpt-4o-mini'),
            temperature=float(os.getenv('TEMPERATURE', '0.7'))
        )