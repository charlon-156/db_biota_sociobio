import pandas as pd
from utils.base import SQLGenerator
from utils.helpers import normalize_key
from utils.maps import map_vale_ribeira, map_vale_paraiba, map_litoral_norte

file_pp = "docs/public_policies.xlsx"
file_municipalities = "docs/municipality.xlsx"

output_sql = "inserts_public_policies_municipalities.sql"

# LOAD DATA

df_pp = pd.read_excel(file_pp)
df_mun = pd.read_excel(file_municipalities)

db = SQLGenerator(df_pp)

map_municipalities = {
    normalize_key(r["municipality"]): int(r["municipalityID"])
    for _, r in df_mun.iterrows()
    if pd.notna(r["municipality"])
    and pd.notna(r["municipalityID"])
}

all_municipalities = list(map_municipalities.values())

vale_ribeira = map_vale_ribeira
vale_paraiba = map_vale_paraiba
litoral_norte = map_litoral_norte

seen = set()

for i, row in df_pp.iterrows():

    try:
        resource_id = int(row["resourceID"])
    except Exception:
        db.add_error({
            "linha_excel": i + 2,
            "erro": "resourceID inválido",
            "value": row.get("resourceID")
        })
        continue

    dominio = row.get("DOMÍNIO")

    if pd.isna(dominio):
        db.add_error({
            "linha_excel": i + 2,
            "erro": "DOMÍNIO vazio"
        })
        continue

    dominio_norm = normalize_key(dominio)

    # CASO SP / BRASIL
    # aplica para TODOS municípios

    if dominio_norm in ["sao paulo", "sp", "brasil"]:

        for municipality_id in all_municipalities:

            key = (resource_id, municipality_id)

            if key not in seen:
                db.add_insert(
                    f"""
                    INSERT INTO public_policies_municipalities (resourceID, municipalityID) VALUES ({resource_id}, {municipality_id});
                    """.strip()
                )

                seen.add(key)

        continue
    
    # CASO REGIÃO LITORAL NORTE
    # aplica em todos os mun. da sub-região
    
    if dominio_norm in ["litoral norte"]:
        
        for municipality_id in litoral_norte:
            
            key = (resource_id, municipality_id)
            
            if key not in seen:
                
                db.add_insert(
                    f"""
                    INSERT INTO public_policies_municipalities (resourceID, municipalityID) VALUES ({resource_id}, {municipality_id});
                    """.strip()
                )
                
                seen.add(key)
                
        continue
    
    if dominio_norm in ["vale do ribeira"]:
        
        for municipality_id in vale_ribeira:
            
            key = (resource_id, municipality_id)
            
            if key not in seen:
                
                db.add_insert(
                    f"""
                    INSERT INTO public_policies_municipalities (resourceID, municipalityID) VALUES ({resource_id}, {municipality_id});
                    """.strip()
                )
                
                seen.add(key)
                
        continue
    
    if dominio_norm in ["vale do paraiba"]:
        
        for municipality_id in vale_paraiba:
            
            key = (resource_id, municipality_id)
            
            if key not in seen:
                
                db.add_insert(
                    f"""
                    INSERT INTO public_policies_municipalities (resourceID, municipalityID) VALUES ({resource_id}, {municipality_id});
                    """.strip()
                )
                
                seen.add(key)
                
        continue
    
    # CASO LISTA DE MUNICÍPIOS
    # separados por //

    municipalities = [
        normalize_key(v)
        for v in str(dominio).split("//")
        if normalize_key(v)
    ]

    matches = []

    for municipality in municipalities:

        if municipality in map_municipalities:
            matches.append(map_municipalities[municipality])

        else:
            db.add_error({
                "linha_excel": i + 2,
                "erro": "Município não encontrado",
                "municipio": municipality,
                "resourceID": resource_id
            })

    if not matches:
        db.add_error({
            "linha_excel": i + 2,
            "erro": "Nenhum município correspondeu",
            "DOMÍNIO": dominio
        })

        continue

    for municipality_id in matches:

        key = (resource_id, municipality_id)

        if key not in seen:
            db.add_insert(
                f"""
                INSERT INTO public_policies_municipalities (resourceID, municipalityID) VALUES ({resource_id}, {municipality_id});
                """.strip()
            )

            seen.add(key)

# OUTPUT
db.save_sql(output_sql)
db.report()