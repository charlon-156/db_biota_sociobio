import pandas as pd
import unicodedata
from utils.base import SQLGenerator
from utils.maps import map_lifeForm, map_substrate, map_biomes, map_states, map_typesOfUses, map_vegetation, map_luminosity

def normalize_key(s):
    if s is None:
        return None
    s = str(s).strip()
    if s == "":
        return None
    # remover acentos
    s = unicodedata.normalize("NFKD", s)
    s = "".join([c for c in s if not unicodedata.combining(c)])
    # normalizar espaços múltiplos e minuscula
    s = " ".join(s.split()).lower()
    return s

# === util: cria mapa normalizado a partir do map original ===
def normalize_map(map_orig):
    new = {}
    for k, v in map_orig.items():
        nk = normalize_key(k)
        if nk:
            new[nk] = v
    return new

# normaliza todos os maps usados
n_map_life = normalize_map(map_lifeForm)
n_map_sub = normalize_map(map_substrate)
n_map_biomes = normalize_map(map_biomes)
n_map_states = normalize_map(map_states)
n_map_types = normalize_map(map_typesOfUses)
n_map_veg = normalize_map(map_vegetation)
n_map_lum = normalize_map(map_luminosity)

# leitura robusta (se o cabeçalho tem linhas em branco)
def read_clean_excel(path, sheet):
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    header_row = raw.first_valid_index()
    df = pd.read_excel(path, sheet_name=sheet, skiprows=header_row)
    return df

file_path = "docs/dados_biologicos.xlsx"
df = read_clean_excel(file_path, "Informações sobre as espécies ")

db = SQLGenerator(df)

# para evitar inserts duplicados (opcional)
seen_inserts = set()

# função auxiliar para processar uma célula com valores separados por '//'
def process_multi(value):
    if pd.isna(value):
        return []
    # split por //, também tolera barra simples se houver
    parts = [p.strip() for p in str(value).split("//") if p.strip() != ""]
    return parts

for i, row in df.iterrows():
    # tenta obter speciesID; se não existir pula a linha
    try:
        species_id = int(row["speciesID"])
    except Exception:
        # marca erro caso queira revisar linhas sem speciesID
        db.erros.append({"linha Excel": i+2, "field": "speciesID", "value": row.get("speciesID")})
        continue

    # lista de (col_name, parts, normalized_map, target_table, target_colname)
    tasks = [
        ("lifeForm", process_multi(row.get("lifeForm")), n_map_life, "species_lifeForms", "lifeFormID"),
        ("substrate", process_multi(row.get("substrate")), n_map_sub, "species_substrates", "substrateID"),
        ("biome", process_multi(row.get("biome")), n_map_biomes, "species_biomes", "biomeID"),
        ("vegetationType", process_multi(row.get("vegetationType")), n_map_veg, "species_vegetation", "vegetationTypeID"),
        ("locality", process_multi(row.get("locality")), n_map_states, "species_localityStates", "localityStatesID"),
        ("typesOfUses", process_multi(row.get("typesOfUses")), n_map_types, "species_typesOfUses", "typeOfUseID"),
        ("luminosity", process_multi(row.get("luminosity")), n_map_lum, "species_luminosity", "luminosityID"),
    ]

    for col_name, parts, nmap, table, target_col in tasks:
        for part in parts:
            raw_value = part
            key = normalize_key(part)
            if key and key in nmap:
                target_id = nmap[key]
                sql = f"INSERT INTO {table} (speciesID, {target_col}) VALUES ({species_id}, {target_id});"

                if sql not in seen_inserts:
                    db.inserts.append(sql)
                    seen_inserts.add(sql)
            else:

                db.erros.append({
                    "linha Excel": i+2,
                    "speciesID": species_id,
                    "field": col_name,
                    "value": raw_value
                })


db.save_sql("inserts_species_fk.sql")

# salvar erros detalhados em CSV para análise
if db.erros:
    pd.DataFrame(db.erros).to_csv("sql/erros_species_fk.csv", index=False, encoding="utf-8")

# relatório
print("\n===== RELATÓRIO FINAL =====")
db.report()
if db.erros:
    print("Arquivo de erros salvo em: sql/erros_species_fk.csv")
