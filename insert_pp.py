import pandas as pd

# Carregar a planilha
file_path = "planilhas/Politicas Publicas.xlsx"
df = pd.read_excel(file_path)

# Mapas
map_tipo = {
    "Resolução": 1,
    "Decreto": 2,
    "Lei": 3,
    "Portaria": 4,
    "Programa": 5,
    "Relatório": 6,
    "Constituição": 7,
}

map_instituicao = {
    "Secretaria de Infraestrutura e Meio Ambiente": 1,
    "Secretaria do Meio Ambiente": 2,
    "Secretaria do Meio Ambiente, Infraestrutura e Logistica": 3,
    "Secretaria de Agricultura e Abastecimento": 4,
    "Governo do Estado de São Paulo": 5,
    "Assembleia legislativa do Estado de São Paulo": 6,
    "Ministério do Meio Ambiente": 7,
    "Ministério do Meio Ambiente e Mudança do Clima": 8,
    "Ministério da Agricultura": 9,
    "Ministério da Agricultura e Pecuária": 10,
    "Presidência da República - Subchefia para Assuntos Jurídicos": 11,
    "Presidência da República - Casa Civil": 12,
    "Presidência da República - Secretaria-Geral": 13,
    "Câmara dos deputados": 14,
    "Governo Federal do Brasil": 15,
    "Secretaria de estado do Meio Ambiente" : 16,
    "Os Secretários de Estado do Meio Ambiente, de Agricultura e Abastecimento e da Justiça e da Defesa da Cidadania": 17,
    "Agência ambiental do vale do paraiba" : 18,
    "Companhia Ambiental do Estado de São Paulo" : 19,
    "Instituto Chico Mendes de Conservação da Biodiversidade" : 20,
    "Prefeitura Municipal da Estância Balneária de Ubatuba" : 21,
    "Planalto" : 22,
}

# Listas para armazenar resultados
inserts = []
erros = []

for i, row in df.iterrows():
    title = str(row["TÍTULO"]).replace("'", "''") if pd.notna(row["TÍTULO"]) else None
    description = str(row["DESCRIÇÃO"]).replace("'", "''") if pd.notna(row["DESCRIÇÃO"]) else None
    fonte = str(row["FONTE"]).replace("'", "''") if pd.notna(row["FONTE"]) else None
    site = str(row["SITE"]).replace("'", "''") if pd.notna(row["SITE"]) else None
    
    tipo = map_tipo.get(str(row["TIPO/INFORMAÇÕES GERAIS"]).strip(), None)
    instituicao = map_instituicao.get(str(row["INSTITUIÇÃO"]).strip(), None)
    
    if tipo and instituicao:
        sql = f"""INSERT INTO public_policies 
        (title, description, bibliographicCitation, references_url, typeID, institutionID)
        VALUES ('{title}', '{description}', '{fonte}', '{site}', {tipo}, {instituicao});"""
        inserts.append(sql)
    else:
        erros.append({
            "linha": i+2,  # +2 porque Excel tem cabeçalho
            "tipo": row["TIPO/INFORMAÇÕES GERAIS"],
            "instituicao": row["INSTITUIÇÃO"]
        })

# Salvar em arquivo
with open("sql/inserts_public_policies.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(inserts))

if not erros:
    print("Tudo certo, patrão ✅🤠👍")
    print("Quantidade de Inserts gerados: ", len(inserts))
else:   
    erros_df = pd.DataFrame(erros)
    print("Algo deu errado, parceiro ❌🙅‍♂️")
    print("⚠️ Registros não convertidos: ")
    print(erros_df)
