"""
Gerenciamento de persistência de dados.
"""
import json
import os
from constants import DATA_FILE


def load_data():
    """Carrega os dados do arquivo JSON, com backward compatibility."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Backward compatibility
            if "total_drops" not in data:
                data["total_drops"] = sum(len(k["drops"]) for k in data.get("kills", []))
            if "unique_items" not in data:
                data["unique_items"] = sorted({d for k in data.get("kills", []) for d in k.get("drops", [])})
            return data
    return {"kills": [], "total_kills": 0, "total_drops": 0, "unique_items": []}


def save_data(data):
    """Salva os dados no arquivo JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
