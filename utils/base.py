###############################################################
# Dev.: Charlon F. Monteiro
# project: Banco de Dados Sociobiodiversidade
# file: base.py
# description: Important module responsible for centralizing 
#              functions to support the generation of SQL 
#              commands for insertion from Excel spreadsheets
# Last update: 2026-04-02
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
        self.error_dir = os.path.join(output_dir, "error")

        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.error_dir, exist_ok=True)

        self.sql_path = None
        self.error_path = None

    @staticmethod
    def num(val):
        if pd.isna(val):
            return "NULL"
        if isinstance(val, (int, float)):
            return str(int(val)) if float(val).is_integer() else str(val)
        return str(val).replace("'", "''")

    @staticmethod
    def text(val):
        if pd.isna(val):
            return "NULL"
        cleaned = str(val).replace("'", "''")
        return f"'{cleaned}'"
                                        
    # =========================
    # Registro
    # =========================

    def add_insert(self, sql):
        self.inserts.append(sql)

    def add_error(self, error_dict):
        self.erros.append(error_dict)

    # =========================
    # Persistência
    # =========================
    
    def save_sql(self, filename):
        self.sql_path = os.path.join(self.output_dir, filename)
        self.sql_filename = filename  # <- guarda nome base

        with open(self.sql_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.inserts))

    def save_errors(self, filename=None):
        if not self.erros:
            return None

        if filename is None:
            base_name = os.path.splitext(self.sql_filename)[0]
            filename = f"errors-{base_name}.csv"

        self.error_path = os.path.join(self.error_dir, filename)

        pd.DataFrame(self.erros).to_csv(
            self.error_path,
            index=False,
            encoding="utf-8"
        )

        return self.error_path

    # =========================
    # Relatório
    # =========================

    def report(self):
        total_inserts = len(self.inserts)
        total_errors = len(self.erros)

        print("\n===== RELATÓRIO FINAL =====")

        if self.sql_path:
            print(f"💾 SQL gerado em: {self.sql_path}")

        print(f"📌 Inserts: {total_inserts}")

        if total_errors > 0:
            error_file = self.save_errors()

            print(f"⚠️  Erros: {total_errors}")

            if error_file:
                print(f"📄 Arquivo de erros: {error_file}")

        else:
            print("✅ Nenhum erro encontrado")

        # retorno estruturado (útil pra automação/testes)
        return {
            "sql_path": self.sql_path,
            "total_inserts": total_inserts,
            "total_errors": total_errors,
            "error_path": self.error_path
        }