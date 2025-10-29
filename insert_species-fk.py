import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_lifeForm, map_substrate

# === Função para leitura robusta (ignora linhas em branco antes do cabeçalho) ===
def read_clean_excel(path, sheet):
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    header_row = raw.first_valid_index()
    df = pd.read_excel(path, sheet_name=sheet, skiprows=header_row)
    return df

# === Carregar planilha e aba ===
file_path = "docs/dados_biologicos.xlsx"
df = read_clean_excel(file_path, "espécies")

# === Instanciar controladores SQL separados ===
db_life = SQLGenerator(df)
db_sub = SQLGenerator(df)

# === Loop principal ===
for i, row in df.iterrows():

    species_id = int(row["speciesID"]) 

    lifeforms = str(row["lifeForm"]).split("//") if pd.notna(row["lifeForm"]) else []
    for lf in lifeforms:
        lf = lf.strip()
        lf_id = map_lifeForm.get(lf, None)

        if lf_id:
            sql_lf = f"INSERT INTO species_lifeForms (speciesID, lifeFormID) VALUES ({species_id}, {lf_id});"
            db_life.inserts.append(sql_lf)
        else:
            db_life.erros.append({
                "linha": i+2,
                "speciesID": species_id,
                "lifeForm": lf
            })


    substrates = str(row["substrate"]).split("//") if pd.notna(row["substrate"]) else []
    for s in substrates:
        s = s.strip()
        s_id = map_substrate.get(s, None)

        if s_id:
            sql_sub = f"INSERT INTO species_substrates (speciesID, substrateID) VALUES ({species_id}, {s_id});"
            db_sub.inserts.append(sql_sub)
        else:
            db_sub.erros.append({
                "linha": i+2,
                "speciesID": species_id,
                "substrate": s
            })


db_life.save_sql("inserts_species_lifeForms.sql")
db_sub.save_sql("inserts_species_substrates.sql")

# === Relatar resultados ===
print("\n===== LIFE FORMS =====")
db_life.report()

print("\n===== SUBSTRATES =====")
db_sub.report()
