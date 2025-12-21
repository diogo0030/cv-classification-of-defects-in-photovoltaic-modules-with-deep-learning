#!/usr/bin/env python3
# fix_remove_widgets.py
# Remove qualquer chave "widgets" em todo o JSON do notebook (top-level, células, outputs, etc).
# NÃO reexecuta células — apenas edita o ficheiro JSON.

import json
from pathlib import Path
import shutil
import sys

NB_FILENAME = "classification_of_defects_in_photovoltaic_modules.ipynb"
NB_PATH = Path(NB_FILENAME)

if not NB_PATH.exists():
    print(f"Ficheiro não encontrado: {NB_PATH}")
    sys.exit(1)

BACKUP = NB_PATH.with_suffix(".ipynb.bak")
if not BACKUP.exists():
    shutil.copy2(NB_PATH, BACKUP)
    print(f"Backup criado: {BACKUP}")

with NB_PATH.open("r", encoding="utf-8") as f:
    try:
        nb = json.load(f)
    except json.JSONDecodeError as e:
        print("Erro ao ler o JSON do notebook:", e)
        sys.exit(1)

def remove_widgets(obj):
    changed = False
    if isinstance(obj, dict):
        if "widgets" in obj:
            # remove a chave "widgets"
            del obj["widgets"]
            changed = True
        # percorre outras chaves
        for k, v in list(obj.items()):
            if remove_widgets(v):
                changed = True
    elif isinstance(obj, list):
        for item in obj:
            if remove_widgets(item):
                changed = True
    return changed

changed = remove_widgets(nb)

if changed:
    with NB_PATH.open("w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"Alterações aplicadas. {NB_PATH} atualizado. Backup em {BACKUP}")
else:
    print("Nenhuma chave 'widgets' encontrada — nada alterado.")