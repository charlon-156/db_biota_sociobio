import pandas as pd
import unicodedata


# =========================
# NORMALIZAÇÃO DE TEXTO
# =========================

def normalize_key(value):
    """
    Normaliza string para comparação:
    - remove acentos
    - remove espaços extras
    - lowercase
    """
    if value is None or pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))

    return " ".join(value.split()).lower()


# =========================
# NORMALIZA MAPAS
# =========================

def normalize_map(map_dict):
    """
    Normaliza chaves de um dicionário para permitir matching robusto
    """
    normalized = {}

    for k, v in map_dict.items():
        nk = normalize_key(k)

        if nk:
            normalized[nk] = v

    return normalized


# =========================
# MULTI VALORES (//)
# =========================

def process_multi(value, sep="//"):
    """
    Divide campos com múltiplos valores
    """
    if pd.isna(value):
        return []

    return [v.strip() for v in str(value).split(sep) if v.strip()]


# =========================
# MATCH COM MAP (SEGURANÇA)
# =========================

def safe_map(value, map_dict):
    """
    Faz lookup com normalização
    """
    key = normalize_key(value)

    if key and key in map_dict:
        return map_dict[key]

    return None