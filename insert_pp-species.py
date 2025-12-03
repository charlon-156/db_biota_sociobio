import pandas as pd
import unicodedata
import os

# CONFIG
file_bio = "docs/dados_biologicos.xlsx"
file_pp = "docs/public_policies.xlsx"
sheet_conn = "Conexão com Políticas Públicas"
sheet_species = "Informações sobre as espécies "
out_file = "sql/inserts_public_policies_species.sql"
os.makedirs("sql", exist_ok=True)

def normalize(s):
    if pd.isna(s) or s is None:
        return None
    s = str(s).strip()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s.lower()

print("🔄 Carregando planilhas...")
df_conn = pd.read_excel(file_bio, sheet_name=sheet_conn)
df_pp = pd.read_excel(file_pp)
df_sp = pd.read_excel(file_bio, sheet_name=sheet_species)

# Mapa de políticas públicas: title → resourceID
map_pp = {
    normalize(r["title"]): int(r["resourceID"])
    for _, r in df_pp.iterrows()
    if pd.notna(r["title"]) and pd.notna(r["resourceID"])
}

# Prepara saída
inserts = []
erros = []

print("🚀 Iniciando processamento...")

for i, row in df_conn.iterrows():

    title = normalize(row["title"])
    species_col = row["speciesInformationColumn"]
    link_value = row["biologicalLink"]

    if title not in map_pp:
        erros.append({"linha Excel": i+2, "erro": "Título não encontrado", "title": row["title"]})
        continue

    resourceID = map_pp[title]

    if species_col not in df_sp.columns:
        erros.append({"linha Excel": i+2, "erro": "Coluna inexistente", "column": species_col})
        continue

    target_norm = normalize(link_value)

    # Filtra todas as espécies que atendem a condição
    matches = []
    for _, sp_row in df_sp.iterrows():
        cell = sp_row[species_col]
        if pd.isna(cell):
            continue

        options = [normalize(x) for x in str(cell).split("//")]

        if target_norm in options:
            matches.append(int(sp_row["speciesID"]))

    # Se nada deu match → reporta erro
    if not matches:
        erros.append({
            "linha Excel": i+2,
            "erro": "Nenhuma espécie correspondeu ao valor",
            "column": species_col,
            "value": link_value
        })
        continue

    # Gerar inserts
    for sid in matches:
        inserts.append(
            f"INSERT INTO public_policies_species (resourceID, speciesID) VALUES ({resourceID}, {sid});"
        )

# Salvar resultados
with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(inserts))

pd.DataFrame(erros).to_csv("sql/erros_pp_species.csv", index=False, encoding="utf-8")

print("\n===== FINALIZADO =====")
print("💾 SQL gerado em:", out_file)
print("📌 Inserts:", len(inserts))
print("⚠️ Erros:", len(erros))
print("Arquivo de erros: sql/erros_pp_species.csv")
