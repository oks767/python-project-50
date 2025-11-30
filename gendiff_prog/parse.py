import yaml
import json
from typing import Dict, Any

def parse_files(file_path: str) -> Dict[str, Any]:
    with open (file_path, 'r', encoding='utf-8') as file:
        if file_path.endswith('.json'):
            return json.load(file)
        elif file_path.endswith(('.yml', '.yaml')):
            return yaml.safe_load(file)
        else:
            raise ValueError(f"Неверный формат: {file_path}")