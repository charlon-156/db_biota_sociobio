import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_tipo, map_instituicao

# Carregar a planilha
file_path = "docs/public_policies.xlsx"
df = pd.read_excel(file_path)

db = SQLGenerator(df)

for i, row in df.iterrows():
    title = str(row["title"]).replace("'", "''") if pd.notna(row["title"]) else None
    description = str(row["description"]).replace("'", "''") if pd.notna(row["description"]) else None
    fonte = str(row[" bibliographicCitation"]).replace("'", "''") if pd.notna(row[" bibliographicCitation"]) else None
    site = str(row["referencesURL"]).replace("'", "''") if pd.notna(row["referencesURL"]) else None
    
    tipo = map_tipo.get(str(row["type"]).strip(), None)
    instituicao = map_instituicao.get(str(row["institution"]).strip(), None)
    
    if tipo and instituicao:
        sql = f"""INSERT INTO public_policies 
        (title, description, bibliographicCitation, references_url, typeID, institutionID)
        VALUES ('{title}', '{description}', '{fonte}', '{site}', {tipo}, {instituicao});"""
        db.inserts.append(sql)
    else:
        db.erros.append({
            "linha": i+2,  # +2 porque Excel tem cabeçalho
            "tipo": row["type"],
            "instituicao": row["institution"]
        })

# Salvar e relatar o arquivo SQL
db.save_sql("inserts_public_policies.sql")
db.report()