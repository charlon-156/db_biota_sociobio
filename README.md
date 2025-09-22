
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
├── inserts/                # scripts SQL de inserção
│   ├── DDl_code.sql
│   ├── DML_code.sql
│   ├── SELECT_code.sql
│   └── ...
│
├── docs/                   # documentação e diagramas
│   └── modelo\_banco.png
│
└── planilhas/                 # arquivos de dados brutos (local, não versionado)
    ├── municipios.xlsx
    ├── politicas.xlsx
    └── ...

````

⚠️ A pasta `data/` contém arquivos **Excel/CSV** utilizados para alimentar os scripts de inserção, mas **não é versionada** por conter dados brutos.

---

## 🚀 Como usar

### 1. Clonar o repositório
```bash
git clone https://github.com/charlon-156/db_biota_sociobio.git
cd db_biota_sociobio
````


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


