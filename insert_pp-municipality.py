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

vale_ribeira = [
    3502705, 3505351, 3505401, 3509254, 3514809, 3517604, 3521200, 3522158, 3522653, 
    3523305, 3524600, 3526100, 3526209, 3529906, 3536208, 3537206, 3542602, 3542800, 
    3543006, 3543253, 3549953, 3551801, 3553500
    ]

vale_paraiba = [
    3502507, 3503158, 3503505, 3504909, 3508504, 3508603, 3509700, 3509957, 3513405,
    3513603, 3518305, 3518404, 3520202, 3524402, 3524907, 3525508, 3526308, 3526605, 
    3527207, 3531704, 3532306, 3532405, 3535606, 3538006, 3538501, 3538600, 3540754, 
    3541901, 3542305, 3544301, 3545001, 3546009, 3546801, 3548203, 3548609, 3549607, 
    3549904, 3550001,3552007, 3554102, 3554805
    ]

litoral_norte = [3510500, 3520400, 3550704, 3555406]

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