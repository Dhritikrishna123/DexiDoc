import os
import tomli
from typing import Any, Dict
from pathlib import Path

CONFIG_DIR = Path.home() / "dexidoc"
CONFIG_FILE = CONFIG_DIR / "config.toml"

def load_config() -> Dict[str, Any]:
    """
    Load configuration from ~/.dexidoc/config.toml
    """
    if not CONFIG_FILE.exists():
        # return default config if file doesn't exist
        return {
            "config_path" : str(CONFIG_FILE),
            "logging" : {
                "level" : "INFO",
                "file" : str(CONFIG_DIR/ "dexidoc.log")
            },
            "excludes": ['.*', '__pycache__', 'node_modules', '.git', '.venv'],
            "extensions": ['.pdf', '.txt', '.docx']
        }
    
    try:
        with open(CONFIG_FILE, "rb") as f:
            config = tomli.load(f)
            config["config_path"] = str(CONFIG_FILE) # Inject path for reference
            
            # Set defaults for missing keys
            config.setdefault("excludes", ['.*', '__pycache__', 'node_modules', '.git', '.venv'])
            config.setdefault("extensions", ['.pdf', '.txt', '.docx'])
            
            return config
        
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}
    
def ensure_config_dir():
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)