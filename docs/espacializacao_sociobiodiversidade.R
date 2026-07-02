# =============================================================================
# REDE DE SOCIOBIODIVERSIDADE DO ESTADO DE SÃO PAULO
# Script de espacialização e correlação de dados
# -----------------------------------------------------------------------------
# Autor(es): Charlon Fernandes Monteiro / Rede de Bioeconomia da
#            Sociobiodiversidade do Estado de São Paulo (USP)
# Objetivo : Ler as tabelas Excel/CSV do projeto, gerar mapas coropléticos,
#            gráficos de distribuição, visualizações climáticas/abióticas e
#            a correlação entre POLÍTICAS PÚBLICAS e ESPÉCIES de interesse.
#
# Como usar :
#   1. Ajuste o caminho em `dir_dados` (pasta com os 5 arquivos enviados).
#   2. Rode o script inteiro (source) ou bloco a bloco.
#   3. Todos os gráficos são salvos em `dir_saida` (subpasta "figuras").
#
# Observação importante sobre GEOMETRIAS:
#   As geometrias embutidas nas planilhas (coluna `geometry`, no formato
#   texto R "list(list(c(...)))") estão TRUNCADAS pelo limite de células do
#   Excel (32.767 caracteres). Cerca de 2/3 dos polígonos municipais terminam
#   no meio de uma coordenada e NÃO podem ser fechados de forma confiável.
#   Por isso, a rota PRINCIPAL de mapas usa os limites oficiais do IBGE via
#   pacote `geobr`, unidos aos seus dados pela chave `municipalityID`.
#   A função `parse_geometria_excel()` (Bloco 6B) fica disponível como rota
#   ALTERNATIVA, para o caso de vocês corrigirem a origem das geometrias.
# =============================================================================


# =============================================================================
# BLOCO 0 — PACOTES
# -----------------------------------------------------------------------------
# Instala (se necessário) e carrega os pacotes usados no script.
# =============================================================================

# --- Ajustes de DOWNLOAD (resolvem 'Timeout of 60 seconds was reached') ------
options(timeout = max(600, getOption("timeout")))
options(repos = c(CRAN = "https://cloud.r-project.org"))

# No Windows, baixar pacotes BINÁRIOS (.zip já compilados) evita ter de compilar
# do código-fonte (que exigiria Rtools + GDAL/GEOS). Em Linux/Mac é ignorado.
.tipo_pkg <- if (.Platform$OS.type == "windows") "binary" else getOption("pkgType")

# Pacotes ESSENCIAIS: sem eles o script não roda (incluem o pipe %>% do dplyr).
pacotes_essenciais <- c(
  "readxl",      # ler arquivos .xlsx
  "readr",       # ler .csv
  "dplyr",       # manipulação de dados (fornece o operador %>%)
  "tidyr",       # pivotagem (wide/long)
  "stringr",     # limpeza de texto
  "ggplot2",     # gráficos
  "scales",      # formatação de eixos
  "forcats"      # reordenar fatores
)

# Pacotes de REDE: necessários para o grafo de correlação (Bloco 5C).
pacotes_rede <- c(
  "igraph",      # redes (grafos)
  "ggraph",      # visualização de redes com ggplot2
  "tidygraph"    # manipulação de grafos no estilo tidyverse
)

# Pacotes ESPACIAIS: necessários para os MAPAS (Bloco 6). Exigem bibliotecas
# de sistema (GDAL/GEOS/PROJ). Se a instalação falhar, o resto do script
# continua funcionando — apenas os mapas serão pulados.
pacotes_espaciais <- c(
  "sf",          # dados espaciais (vetoriais)
  "geobr"        # malhas oficiais do IBGE (municípios, UFs, etc.)
)

# Instala apenas o que estiver faltando -------------------------------------
instalar_se_preciso <- function(pkgs) {
  faltando <- pkgs[!pkgs %in% rownames(installed.packages())]
  if (length(faltando) > 0) {
    message("Instalando pacotes: ", paste(faltando, collapse = ", "))
    # type = .tipo_pkg => no Windows usa binários (.zip) e dispensa compilação
    install.packages(faltando, dependencies = TRUE, type = .tipo_pkg)
  }
}

# Carrega um conjunto de pacotes e RETORNA TRUE só se todos carregarem.
# Diferente de lapply(library), aqui os erros NÃO são silenciados.
carregar_pacotes <- function(pkgs, obrigatorio = FALSE) {
  instalar_se_preciso(pkgs)
  ok <- vapply(pkgs, function(p) {
    suppressWarnings(suppressPackageStartupMessages(
      requireNamespace(p, quietly = TRUE) && library(p, character.only = TRUE, logical.return = TRUE)
    ))
  }, logical(1))
  if (!all(ok)) {
    falhos <- pkgs[!ok]
    msg <- paste0("Não foi possível carregar: ", paste(falhos, collapse = ", "))
    if (obrigatorio) {
      stop(msg, "\n>>> Instale manualmente com: install.packages(c(",
           paste(sprintf('\"%s\"', falhos), collapse = ", "), "))", call. = FALSE)
    } else {
      warning(msg, " — funcionalidades dependentes serão puladas.", call. = FALSE)
    }
  }
  all(ok)
}

# 1) Essenciais — se algum falhar, o script PARA aqui com mensagem clara
#    (é isso que resolve o erro 'não foi possível encontrar a função "%>%"').
carregar_pacotes(pacotes_essenciais, obrigatorio = TRUE)

# 2) Rede e espaciais — opcionais: registram se estão disponíveis ou não
TEM_REDE      <- carregar_pacotes(pacotes_rede,      obrigatorio = FALSE)
TEM_ESPACIAIS <- carregar_pacotes(pacotes_espaciais, obrigatorio = FALSE)

message("Pacotes essenciais: OK | rede: ", TEM_REDE, " | espaciais: ", TEM_ESPACIAIS)

# Tema visual padrão para todos os gráficos -----------------------------------
tema_projeto <- theme_minimal(base_size = 12) +
  theme(
    plot.title    = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(color = "grey30"),
    plot.caption  = element_text(color = "grey45", size = 8),
    legend.position = "right",
    panel.grid.minor = element_blank()
  )
theme_set(tema_projeto)

# Paleta de cores do projeto (harmônica, segura para daltonismo) ---------------
cor_primaria   <- "#20808D"  # teal
cor_secundaria <- "#A84B2F"  # terra/rust
paleta_cat <- c("#20808D", "#A84B2F", "#1B474D", "#FFC553",
                "#944454", "#848456", "#6E522B", "#BCE2E7")


# =============================================================================
# BLOCO 1 — CAMINHOS E SAÍDA
# -----------------------------------------------------------------------------
# AJUSTE AQUI o caminho da pasta onde estão os 5 arquivos.
# =============================================================================

dir_dados <- "C:/Users/charl/programs/db_biota_sociobio/docs"                       # <- pasta com os arquivos de entrada # nolint
dir_saida <- file.path(dir_dados, "repo")
dir.create(dir_saida, recursive = TRUE, showWarnings = FALSE)

arq_abioticos <- file.path(dir_dados, "Dados abióticos.xlsx")
arq_biologico <- file.path(dir_dados, "dados_biologicos.xlsx")
arq_municipio <- file.path(dir_dados, "municipality.xlsx")
arq_politicas <- file.path(dir_dados, "public_policies.xlsx")
arq_ligacao   <- file.path(dir_dados, "public_policies_species.csv")

# Função utilitária para salvar gráficos de forma padronizada -----------------
salvar_fig <- function(plot, nome, larg = 10, alt = 7, dpi = 200) {
  caminho <- file.path(dir_saida, paste0(nome, ".png"))
  ggsave(caminho, plot = plot, width = larg, height = alt, dpi = dpi, bg = "white")
  message("Figura salva: ", caminho)
  invisible(caminho)
}

# Converte "null"/"-----------"/"" em NA (padrões frequentes nas planilhas) ----
para_na <- function(x) {
  x <- as.character(x)
  x <- str_trim(x)
  x[x %in% c("null", "NULL", "NA", "", "-", "-----------")] <- NA
  x
}


# =============================================================================
# BLOCO 2 — LEITURA E LIMPEZA DOS DADOS
# =============================================================================

# 2.1 Municípios (atributos socioeconômicos) ----------------------------------
municipios <- read_excel(arq_municipio, sheet = "municipality") %>%
  mutate(
    municipalityID = as.character(suppressWarnings(as.integer(round(as.numeric(municipalityID))))),
    municipality   = str_trim(municipality),
    population        = as.numeric(population),
    areaKM2           = as.numeric(areaKM2),
    populationDensity = as.numeric(populationDensity)
  ) %>%
  filter(!is.na(municipalityID))

# 2.2 Clima de Köppen + temperatura/precipitação mensais ----------------------
koppen <- read_excel(arq_abioticos, sheet = "Koppen") %>%
  mutate(
    municipalityID    = as.character(suppressWarnings(as.integer(round(as.numeric(municipalityID))))),
    municipality      = str_trim(municipality),
    koppen            = str_trim(dynamicProperties),  # classe climática (ex.: Cfa, Cwa)
    elevation         = as.numeric(elevation)
  ) %>%
  filter(!is.na(municipalityID))

# 2.3 Espécies de interesse ---------------------------------------------------
# Selecionamos apenas as colunas úteis para gráficos/correlação e as limpamos.
especies <- read_excel(arq_biologico, sheet = "Informações sobre as espécies ") %>%
  rename_with(str_trim) %>%
  mutate(
    speciesID            = suppressWarnings(as.integer(round(as.numeric(`speciesID`)))),
    vernacularName       = para_na(vernacularName),
    scientificName       = para_na(scientificName),
    family               = para_na(family),
    threatenedStatusIUCN = para_na(threatenedStatusIUCN),
    lifeForm             = para_na(lifeForm),
    origin               = para_na(origin),
    endemism             = para_na(endemism),
    typesOfUses          = para_na(typesOfUses)
  ) %>%
  filter(!is.na(speciesID))

# 2.4 Políticas públicas (aba biológica) --------------------------------------
politicas <- read_excel(arq_politicas, sheet = "POLITICAS PUBLICAS (BIOLOGICAS ") %>%
  rename_with(str_trim) %>%
  mutate(
    resourceID        = suppressWarnings(as.integer(round(as.numeric(resourceID)))),
    type              = str_squish(str_to_title(para_na(type))),         # "Decreto ", "Decreto\n" -> "Decreto"
    title             = str_squish(para_na(title)),
    LegislativeStatus = str_squish(para_na(LegislativeStatus)),
    Typology          = str_squish(para_na(Typology))
  ) %>%
  filter(!is.na(resourceID))

# 2.5 Ligação políticas <-> espécies (lista de arestas) -----------------------
ligacao <- read_csv(arq_ligacao, show_col_types = FALSE) %>%
  mutate(
    resourceID = as.integer(resourceID),
    speciesID  = as.integer(speciesID)
  ) %>%
  distinct()

message("Resumo da leitura:")
message("  municípios: ", nrow(municipios))
message("  Köppen    : ", nrow(koppen))
message("  espécies  : ", nrow(especies))
message("  políticas : ", nrow(politicas))
message("  ligações  : ", nrow(ligacao),
        " (", n_distinct(ligacao$resourceID), " políticas x ",
        n_distinct(ligacao$speciesID), " espécies)")


# =============================================================================
# BLOCO 3 — GRÁFICOS DE DISTRIBUIÇÃO (ESPÉCIES E POLÍTICAS)
# =============================================================================

# 3.1 Espécies por família ----------------------------------------------------
g_familia <- especies %>%
  filter(!is.na(family)) %>%
  count(family, sort = TRUE) %>%
  slice_head(n = 15) %>%
  ggplot(aes(x = n, y = fct_reorder(family, n))) +
  geom_col(fill = cor_primaria) +
  geom_text(aes(label = n), hjust = -0.2, size = 3) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.1))) +
  labs(
    title = "Espécies de interesse por família botânica",
    subtitle = "15 famílias mais frequentes",
    x = "Nº de espécies", y = NULL,
    caption = "Fonte: Rede de Bioeconomia da Sociobiodiversidade do Estado de São Paulo"
  )
salvar_fig(g_familia, "01_especies_por_familia")

# 3.2 Espécies por status de ameaça (IUCN) ------------------------------------
g_iucn <- especies %>%
  mutate(IUCN = ifelse(is.na(threatenedStatusIUCN), "Sem avaliação", threatenedStatusIUCN)) %>%
  count(IUCN, sort = TRUE) %>%
  ggplot(aes(x = fct_reorder(IUCN, n), y = n)) +
  geom_col(fill = cor_secundaria) +
  geom_text(aes(label = n), vjust = -0.4, size = 3) +
  labs(
    title = "Status de ameaça das espécies (IUCN)",
    subtitle = "LC = pouco preocupante; VU = vulnerável; EN = em perigo; DD = dados insuficientes",
    x = "Categoria IUCN", y = "Nº de espécies",
    caption = "Fonte: IUCN / dados do projeto"
  )
salvar_fig(g_iucn, "02_especies_por_status_iucn")

# 3.3 Espécies por forma de vida ----------------------------------------------
# A coluna lifeForm pode trazer múltiplos valores separados por "//".
g_forma <- especies %>%
  filter(!is.na(lifeForm)) %>%
  separate_rows(lifeForm, sep = "//") %>%
  mutate(lifeForm = str_squish(lifeForm)) %>%
  count(lifeForm, sort = TRUE) %>%
  slice_head(n = 12) %>%
  ggplot(aes(x = n, y = fct_reorder(lifeForm, n))) +
  geom_col(fill = cor_primaria) +
  geom_text(aes(label = n), hjust = -0.2, size = 3) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.1))) +
  labs(title = "Espécies por forma de vida", x = "Nº de registros", y = NULL,
       caption = "Fonte: dados do projeto")
salvar_fig(g_forma, "03_especies_por_forma_de_vida")

# 3.4 Políticas por tipo ------------------------------------------------------
g_pol_tipo <- politicas %>%
  filter(!is.na(type)) %>%
  count(type, sort = TRUE) %>%
  ggplot(aes(x = n, y = fct_reorder(type, n))) +
  geom_col(fill = cor_secundaria) +
  geom_text(aes(label = n), hjust = -0.2, size = 3) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.1))) +
  labs(title = "Políticas públicas por tipo de instrumento",
       x = "Nº de políticas", y = NULL,
       caption = "Fonte: dados do projeto")
salvar_fig(g_pol_tipo, "04_politicas_por_tipo")

# 3.5 Políticas por situação legislativa --------------------------------------
g_pol_status <- politicas %>%
  filter(!is.na(LegislativeStatus)) %>%
  count(LegislativeStatus, sort = TRUE) %>%
  ggplot(aes(x = n, y = fct_reorder(LegislativeStatus, n))) +
  geom_col(fill = cor_primaria) +
  geom_text(aes(label = n), hjust = -0.2, size = 3) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.1))) +
  labs(title = "Situação legislativa das políticas públicas",
       x = "Nº de políticas", y = NULL,
       caption = "Fonte: dados do projeto")
salvar_fig(g_pol_status, "05_politicas_por_situacao")


# =============================================================================
# BLOCO 4 — DADOS CLIMÁTICOS / ABIÓTICOS
# =============================================================================

# 4.1 Distribuição das classes de Köppen --------------------------------------
g_koppen_barras <- koppen %>%
  filter(!is.na(koppen)) %>%
  count(koppen, sort = TRUE) %>%
  ggplot(aes(x = fct_reorder(koppen, n), y = n)) +
  geom_col(fill = cor_primaria) +
  geom_text(aes(label = n), vjust = -0.4, size = 3) +
  labs(title = "Municípios por classe climática de Köppen",
       x = "Classe de Köppen", y = "Nº de municípios",
       caption = "Fonte: classificação de Köppen / dados do projeto")
salvar_fig(g_koppen_barras, "06_koppen_distribuicao")

# 4.2 Climograma médio (temperatura x precipitação) ---------------------------
# Reorganiza as colunas mensais T_jan..T_dec e R_jan..R_dec para formato longo.
meses <- c("jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec")
meses_pt <- c("Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez")

temp_long <- koppen %>%
  select(municipalityID, starts_with("measurementOrFact_T_")) %>%
  pivot_longer(-municipalityID, names_to = "mes", values_to = "temp") %>%
  mutate(mes = str_remove(mes, "measurementOrFact_T_"), temp = as.numeric(temp))

prec_long <- koppen %>%
  select(municipalityID, starts_with("measurementOrFact_R_")) %>%
  pivot_longer(-municipalityID, names_to = "mes", values_to = "prec") %>%
  mutate(mes = str_remove(mes, "measurementOrFact_R_"), prec = as.numeric(prec))

clima_mes <- temp_long %>%
  left_join(prec_long, by = c("municipalityID", "mes")) %>%
  group_by(mes) %>%
  summarise(temp = mean(temp, na.rm = TRUE),
            prec = mean(prec, na.rm = TRUE), .groups = "drop") %>%
  mutate(mes = factor(mes, levels = meses, labels = meses_pt))

# Climograma: barras = precipitação; linha = temperatura (eixo secundário)
fator <- max(clima_mes$prec, na.rm = TRUE) / max(clima_mes$temp, na.rm = TRUE)
g_climograma <- ggplot(clima_mes, aes(x = mes)) +
  geom_col(aes(y = prec), fill = "#BCE2E7") +
  geom_line(aes(y = temp * fator, group = 1), color = cor_secundaria, linewidth = 1.1) +
  geom_point(aes(y = temp * fator), color = cor_secundaria, size = 2) +
  scale_y_continuous(
    name = "Precipitação média (mm)",
    sec.axis = sec_axis(~ . / fator, name = "Temperatura média (°C)")
  ) +
  labs(title = "Climograma médio dos municípios da rede",
       subtitle = "Média entre os 71 municípios",
       x = NULL,
       caption = "Fonte: dados climáticos do projeto") +
  theme(axis.title.y.right = element_text(color = cor_secundaria))
salvar_fig(g_climograma, "07_climograma_medio")


# =============================================================================
# BLOCO 5 — CORRELAÇÃO POLÍTICAS PÚBLICAS x ESPÉCIES
# -----------------------------------------------------------------------------
# Usa a lista de arestas (ligacao) para construir:
#   (A) uma matriz/heatmap políticas x espécies
#   (B) uma rede (grafo bipartido) políticas <-> espécies
# =============================================================================

# Rótulos legíveis para políticas e espécies ----------------------------------
rot_politicas <- politicas %>%
  transmute(resourceID,
            rotulo_pol = str_squish(paste0(coalesce(type, "Política"), " ",
                                           str_trunc(coalesce(title, ""), 30))))
rot_especies <- especies %>%
  transmute(speciesID,
            rotulo_sp = coalesce(scientificName, vernacularName,
                                 paste0("sp_", speciesID)))

ligacao_rot <- ligacao %>%
  left_join(rot_politicas, by = "resourceID") %>%
  left_join(rot_especies,  by = "speciesID") %>%
  mutate(
    rotulo_pol = coalesce(rotulo_pol, paste0("Política ", resourceID)),
    rotulo_sp  = coalesce(rotulo_sp,  paste0("Espécie ", speciesID))
  )

# 5.A HEATMAP (matriz de incidência) ------------------------------------------
g_heatmap <- ligacao_rot %>%
  count(rotulo_pol, rotulo_sp) %>%
  ggplot(aes(x = rotulo_sp, y = rotulo_pol, fill = n)) +
  geom_tile(color = "white", linewidth = 0.3) +
  scale_fill_gradient(low = "#BCE2E7", high = cor_primaria, name = "Vínculo") +
  labs(title = "Matriz de correlação: políticas públicas x espécies",
       subtitle = "Cada célula indica um vínculo entre uma política e uma espécie",
       x = "Espécie", y = "Política pública",
       caption = "Fonte: tabela de ligação do projeto") +
  theme(axis.text.x = element_text(angle = 60, hjust = 1, size = 7),
        axis.text.y = element_text(size = 7))
salvar_fig(g_heatmap, "08_heatmap_politicas_especies", larg = 14, alt = 11)

# 5.B Espécies mais "cobertas" por políticas e vice-versa ---------------------
g_sp_top <- ligacao_rot %>%
  count(rotulo_sp, sort = TRUE) %>%
  slice_head(n = 20) %>%
  ggplot(aes(x = n, y = fct_reorder(rotulo_sp, n))) +
  geom_col(fill = cor_primaria) +
  geom_text(aes(label = n), hjust = -0.2, size = 3) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.1))) +
  labs(title = "Espécies com mais vínculos a políticas públicas",
       x = "Nº de políticas vinculadas", y = NULL,
       caption = "Fonte: tabela de ligação do projeto")
salvar_fig(g_sp_top, "09_especies_mais_vinculadas")

g_pol_top <- ligacao_rot %>%
  count(rotulo_pol, sort = TRUE) %>%
  slice_head(n = 20) %>%
  ggplot(aes(x = n, y = fct_reorder(rotulo_pol, n))) +
  geom_col(fill = cor_secundaria) +
  geom_text(aes(label = n), hjust = -0.2, size = 3) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.1))) +
  labs(title = "Políticas que abrangem mais espécies",
       x = "Nº de espécies abrangidas", y = NULL,
       caption = "Fonte: tabela de ligação do projeto")
salvar_fig(g_pol_top, "10_politicas_mais_abrangentes")

# 5.C REDE (grafo bipartido) políticas <-> espécies ---------------------------
# Só roda se os pacotes de rede (igraph/ggraph/tidygraph) carregaram.
if (isTRUE(TEM_REDE)) {
  nos_pol <- ligacao_rot %>% distinct(name = rotulo_pol) %>% mutate(tipo = "Política")
  nos_sp  <- ligacao_rot %>% distinct(name = rotulo_sp)  %>% mutate(tipo = "Espécie")
  nos <- bind_rows(nos_pol, nos_sp)

  arestas <- ligacao_rot %>% transmute(from = rotulo_pol, to = rotulo_sp)

  grafo <- tbl_graph(nodes = nos, edges = arestas, directed = FALSE) %>%
    mutate(grau = centrality_degree())

  set.seed(42)  # layout reprodutível
  g_rede <- ggraph(grafo, layout = "fr") +
    geom_edge_link(alpha = 0.25, color = "grey60") +
    geom_node_point(aes(color = tipo, size = grau)) +
    geom_node_text(aes(label = ifelse(grau >= quantile(grau, 0.85), name, "")),
                   repel = TRUE, size = 2.5, max.overlaps = 20) +
    scale_color_manual(values = c("Política" = cor_secundaria, "Espécie" = cor_primaria),
                       name = NULL) +
    scale_size_continuous(range = c(1.5, 8), name = "Grau (conexões)") +
    labs(title = "Rede de correlação: políticas públicas e espécies",
         subtitle = "Nós maiores = mais conexões; rótulos apenas para os mais conectados",
         caption = "Fonte: tabela de ligação do projeto") +
    theme_void(base_size = 12) +
    theme(plot.title = element_text(face = "bold", size = 14),
          plot.subtitle = element_text(color = "grey30"),
          legend.position = "right")
  salvar_fig(g_rede, "11_rede_politicas_especies", larg = 12, alt = 10)
} else {
  message("Bloco 5C (rede) pulado: pacotes igraph/ggraph/tidygraph não disponíveis.")
}


# =============================================================================
# BLOCO 6 — MAPAS COROPLÉTICOS
# =============================================================================

# -----------------------------------------------------------------------------
# 6A — ROTA PRINCIPAL: limites oficiais do IBGE (geobr)
# -----------------------------------------------------------------------------
# Baixa a malha de municípios de SP e une aos dados pela chave municipalityID.
# Requer conexão com a internet na primeira execução (geobr faz cache local).

mapas_geobr <- if (!isTRUE(TEM_ESPACIAIS)) {
  message("Bloco 6 (mapas) pulado: pacotes sf/geobr não disponíveis.")
  FALSE
} else tryCatch({
  sp_mun <- read_municipality(code_muni = "SP", year = 2022, showProgress = FALSE) %>%
    mutate(municipalityID = as.character(code_muni))
  TRUE
}, error = function(e) {
  message("AVISO: não foi possível baixar a malha via geobr (", conditionMessage(e), ").")
  message("       Os mapas do Bloco 6A serão pulados. Verifique a conexão com a internet.")
  FALSE
})

if (isTRUE(mapas_geobr)) {

  # Mantém só os municípios da rede (ou mostra todos com NA fora da rede) ------
  base_mapa <- sp_mun %>%
    left_join(koppen %>% select(municipalityID, koppen, elevation), by = "municipalityID") %>%
    left_join(municipios %>% select(municipalityID, population, populationDensity),
              by = "municipalityID")

  # 6A.1 Mapa: classe climática de Köppen -------------------------------------
  m_koppen <- ggplot(base_mapa) +
    geom_sf(aes(fill = koppen), color = "white", linewidth = 0.1) +
    scale_fill_manual(values = paleta_cat, na.value = "grey90", name = "Köppen") +
    labs(title = "Classificação climática de Köppen — municípios da rede (SP)",
         caption = "Limites: IBGE/geobr 2022 | Clima: dados do projeto") +
    theme_void() + theme(plot.title = element_text(face = "bold"))
  salvar_fig(m_koppen, "12_mapa_koppen")

  # 6A.2 Mapa: elevação -------------------------------------------------------
  m_elev <- ggplot(base_mapa) +
    geom_sf(aes(fill = elevation), color = "white", linewidth = 0.1) +
    scale_fill_gradient(low = "#BCE2E7", high = "#1B474D", na.value = "grey90",
                        name = "Elevação (m)") +
    labs(title = "Elevação média por município (rede SP)",
         caption = "Limites: IBGE/geobr 2022 | Elevação: dados do projeto") +
    theme_void() + theme(plot.title = element_text(face = "bold"))
  salvar_fig(m_elev, "13_mapa_elevacao")

  # 6A.3 Mapa: população -------------------------------------------------------
  m_pop <- ggplot(base_mapa) +
    geom_sf(aes(fill = population), color = "white", linewidth = 0.1) +
    scale_fill_viridis_c(option = "mako", trans = "log10", na.value = "grey90",
                         labels = label_number(big.mark = "."), name = "População") +
    labs(title = "População por município (rede SP)",
         subtitle = "Escala logarítmica",
         caption = "Limites: IBGE/geobr 2022 | População: IBGE/dados do projeto") +
    theme_void() + theme(plot.title = element_text(face = "bold"))
  salvar_fig(m_pop, "14_mapa_populacao")

  # 6A.4 Mapa: nº de espécies de interesse por município -----------------------
  # OBS.: a coluna `locality` das espécies traz UFs (ocorrência confirmada),
  # não municípios de SP. Portanto NÃO há, nos dados atuais, uma ligação direta
  # espécie -> município de SP. Este mapa fica como ESQUELETO: assim que houver
  # uma tabela espécie x municipalityID, basta preencher `especies_por_municipio`.
  #
  # especies_por_municipio <- <sua tabela com colunas municipalityID e n_especies>
  # m_sp <- ggplot(sp_mun %>% left_join(especies_por_municipio, by="municipalityID")) +
  #   geom_sf(aes(fill = n_especies), color="white", linewidth=0.1) +
  #   scale_fill_gradient(low="#BCE2E7", high=cor_primaria, na.value="grey90") + ...
  message("NOTA: mapa de espécies por município requer tabela espécie x municipalityID ",
          "(ver comentário no Bloco 6A.4).")
}

# -----------------------------------------------------------------------------
# 6B — ROTA ALTERNATIVA: reconstruir polígonos a partir do texto R do Excel
# -----------------------------------------------------------------------------
# Esta função interpreta a string "list(list(c(lon...), c(lat...)))" da coluna
# `geometry`. ATENÇÃO: muitas células estão TRUNCADAS no limite do Excel, então
# a função tenta fechar o anel e EMITE UM AVISO para os polígonos suspeitos.
# Use apenas se/quando a origem das geometrias for corrigida.

parse_geometria_excel <- function(txt) {
  if (is.na(txt) || !nzchar(txt)) return(NULL)
  # Extrai todos os blocos "c(...)" (1º = longitudes, 2º = latitudes)
  blocos <- str_match_all(txt, "c\\(([^)]*)\\)")[[1]][, 2]
  if (length(blocos) < 2) return(NULL)

  num <- function(s) as.numeric(str_split(s, ",")[[1]] %>% str_trim())
  lon <- num(blocos[1]); lat <- num(blocos[2])

  # Se truncado, as últimas coordenadas podem estar incompletas/NA: limpamos.
  ok  <- !is.na(lon) & !is.na(lat)
  lon <- lon[ok]; lat <- lat[ok]
  n   <- min(length(lon), length(lat))
  if (n < 4) return(NULL)
  lon <- lon[1:n]; lat <- lat[1:n]

  truncado <- str_length(txt) >= 32760  # heurística do limite do Excel
  if (truncado) warning("Geometria possivelmente TRUNCADA (", str_length(txt),
                        " caracteres). Polígono pode estar incorreto.")

  # Fecha o anel (1º ponto == último ponto), exigência do formato POLYGON
  if (lon[1] != lon[n] || lat[1] != lat[n]) {
    lon <- c(lon, lon[1]); lat <- c(lat, lat[1])
  }
  st_polygon(list(cbind(lon, lat)))
}

# Exemplo de uso (descomente para experimentar com a aba Köppen) --------------
# kop_raw <- read_excel(arq_abioticos, sheet = "Koppen")
# geoms <- lapply(kop_raw$geometry, parse_geometria_excel)
# validos <- !vapply(geoms, is.null, logical(1))
# sf_excel <- st_sf(
#   municipalityID = as.character(as.integer(kop_raw$municipalityID[validos])),
#   koppen         = str_trim(kop_raw$dynamicProperties[validos]),
#   geometry       = st_sfc(geoms[validos], crs = 4674)  # SIRGAS 2000 = EPSG:4674
# )
# ggplot(sf_excel) + geom_sf(aes(fill = koppen)) + theme_void()


# =============================================================================
# BLOCO 7 — FIM
# =============================================================================
message("\nConcluído. Todas as figuras foram salvas em: ", normalizePath(dir_saida))
message("Mapas (Bloco 6A) dependem do pacote geobr e de internet na 1ª execução.")
