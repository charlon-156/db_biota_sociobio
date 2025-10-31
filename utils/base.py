###############################################################
# Dev.: Charlon F. Monteiro
# project: Banco de Dados Sociobiodiversidade
# file: base.py
# description: Important module responsible for centralizing 
#              functions to support the generation of SQL 
#              commands for insertion from Excel spreadsheets
# Last update: 2025-09-31
###############################################################

'''
Módulo utilitário responsável por centralizar funções de suporte à geração
de comandos SQL de inserção a partir de planilhas Excel.

Principais componentes:
- Classe SQLGenerator: abstrai a lógica de conversão de valores do pandas 
  para SQL, acumula os inserts gerados e registra erros.
- Funções auxiliares (ex.: num): garantem que valores nulos, floats e strings
  sejam corretamente adaptados para SQL.
'''


import pandas as pd
import os

class SQLGenerator:
    def __init__(self, df, output_dir="sql"):
        self.df = df
        self.inserts = []
        self.erros = []
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)



    @staticmethod
    def num(val):
        if pd.isna(val):
            return "NULL"
        if isinstance(val, (int, float)):
            return str(int(val)) if float(val).is_integer() else str(val)
        return str(val).replace("'", "''")
    


    def save_sql(self, filename):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.inserts))

    

    def report(self):
        if self.erros:
            erros_df = pd.DataFrame(self.erros)
            print("\nAlgo deu errado, parceiro ❌🙅‍♂️")
            print("⚠️  Registros não convertidos:", len(self.erros))
            print(erros_df)

        else:
            print("\nTudo certo, patrão ✅🤠👍")
            print("Quantidade de Inserts gerados:", len(self.inserts))