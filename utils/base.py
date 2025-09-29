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
            print("⚠️ Registros não convertidos:", len(self.erros))
            print(erros_df)

        else:
            print("\nTudo certo, patrão ✅🤠👍")
            print("Quantidade de Inserts gerados:", len(self.inserts))