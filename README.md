
# Scripts de Inserção - Banco de Dados Sociobiodiversidade

Este repositório organiza e centraliza os **scripts SQL de inserção de dados** no banco de dados **biota_sociobiodiversidade**.  
O objetivo é manter códigos Python de geração de comandos `INSERT INTO` versionados de forma clara, reprodutível e acessível.


## 📂 Estrutura do Repositório

```

sociobiodiversidade-inserts/
│
├── README.md               # documentação principal
├── .gitignore              # arquivos ignorados pelo git
│
├── sql/                    # scripts SQL de inserção
│   ├── error/
│   │    ├── errors-inserts_... 
│   │    └── [...]
│   ├── DDl_code.sql
│   ├── DML_code.sql
│   ├── SELECT_code.sql
│   └── ...
│
├── utils/                   # documentação e diagramas
│   ├── base.py
│   └── maps.py
│
└── doc/                 # arquivos de dados brutos (local, não versionado)
    ├── municipios.xlsx
    ├── politicas.xlsx
    └── [...]

````

⚠️ A pasta `data/` contém arquivos **Excel/CSV** utilizados para alimentar os scripts de inserção, mas **não é versionada** por conter dados brutos.

---

## 🚀 Como usar

### 1. Clonar o repositório
```bash
git clone https://github.com/charlon-156/db_biota_sociobio.git
cd db_biota_sociobio
````
## 🐍 Scripts Python

Além dos arquivos SQL, o repositório contém scripts em Python que automatizam
a geração dos `INSERT INTO` a partir de planilhas Excel localizadas em `docs/`.

### Estrutura de `utils/`

- **base.py** → Classe `SQLGenerator` para auxiliar na criação de comandos SQL,
  garantindo consistência de valores nulos, textos e números.
- **maps.py** → Dicionários de mapeamento para conversão de nomes em códigos (ex.: municípios, tipos de políticas, classificações climáticas).
- **helpers.py** → 

Esses módulos são usados pelos scripts de geração (ex.: `insert_municipality.py`).

### Exemplo de uso

```bash
python insert_municipality.py
```

---

## 📖 Requisitos

* **Banco de dados**: MySQL ou MariaDB (adaptável para PostgreSQL, se necessário).
* **Ferramentas**: cliente `mysql` ou equivalente.

---

## 🤝 Contribuição

* Mantenha os scripts organizados dentro da pasta `sql/`.
* Use nomes de arquivos que correspondam às tabelas (`inserts_[nomeDaTabela].sql`).
* Documente no início de cada arquivo `.sql` o que ele insere.

Pull requests e melhorias são bem-vindos!

---

## 📜 Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.


