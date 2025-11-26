import pandas as pd
import numpy as np

# Carregar as abas relevantes
policies_df = pd.read_excel('dados_biologicos.xlsx', sheet_name='Conexão com Políticas Públicas')
species_df = pd.read_excel('dados_biologicos.xlsx', sheet_name='Informações sobre as espécies')

# Criar dicionário de mapeamento de políticas para características biológicas
policy_mapping = {}
for _, policy in policies_df.iterrows():
    if pd.notna(policy['biologicalLink']) and pd.notna(policy['speciesInformationColumn']):
        policy_key = f"{policy['type']} - {policy['title']}"
        if policy_key not in policy_mapping:
            policy_mapping[policy_key] = {
                'biologicalCompetence': policy['biologicalCompetence'],
                'mappings': []
            }
        policy_mapping[policy_key]['mappings'].append({
            'biologicalLink': policy['biologicalLink'],
            'speciesColumn': policy['speciesInformationColumn']
        })

# Função para verificar correspondência
def check_match(species_value, policy_value):
    if pd.isna(species_value):
        return False
    species_values = str(species_value).split('//')
    return any(policy_value.strip() in val.strip() for val in species_values)

# Criar matriz de correlação
results = []

for policy_key, policy_data in policy_mapping.items():
    for mapping in policy_data['mappings']:
        biological_link = mapping['biologicalLink']
        species_column = mapping['speciesColumn']
        
        if species_column not in species_df.columns:
            continue
            
        for _, species in species_df.iterrows():
            species_name = species['scientificName']
            species_value = species[species_column]
            
            if check_match(species_value, biological_link):
                results.append({
                    'Política': policy_key,
                    'Competência Biológica': policy_data['biologicalCompetence'],
                    'Link Biológico': biological_link,
                    'Coluna Espécie': species_column,
                    'Espécie': species_name,
                    'Nome Popular': species['vernacularName'],
                    'Valor na Espécie': species_value
                })

# Criar DataFrame com resultados
correlation_df = pd.DataFrame(results)

# Salvar resultados
correlation_df.to_excel('correlacao_politicas_especies.xlsx', index=False)
print("Correlação concluída! Arquivo 'correlacao_politicas_especies.xlsx' gerado.")

# Gerar também uma visualização resumida
summary = correlation_df.groupby(['Política', 'Espécie']).size().reset_index(name='Correspondências')
summary.to_excel('resumo_correlacao.xlsx', index=False)
print("Resumo da correlação salvo em 'resumo_correlacao.xlsx'")

# Mostrar estatísticas
print(f"\nEstatísticas da Correlação:")
print(f"Total de políticas analisadas: {len(policy_mapping)}")
print(f"Total de correspondências encontradas: {len(correlation_df)}")
print(f"Espécies com correspondências: {correlation_df['Espécie'].nunique()}")