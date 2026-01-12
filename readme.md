# 🔊 Streamlit Residual Stress Analyzer

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit Version](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 📝 Índice

1.  [Descrição Geral](#1-descrição-geral)
2.  [Características Principais](#2-características-principais)
3.  [Conceitos Científicos](#3-conceitos-científicos)
    *   [Efeito Acustoelástico](#efeito-acustoelástico)
    *   [Fórmulas Matemáticas](#fórmulas-matemáticas)
    *   [Limitações e Considerações](#limitações-e-considerações)
4.  [Requisitos Técnicos](#4-requisitos-técnicos)
5.  [Instalação](#5-instalação)
    *   [Pré-requisitos](#pré-requisitos)
    *   [Criação de Ambiente Virtual](#criação-de-ambiente-virtual)
    *   [Instalação das Dependências](#instalação-das-dependências)
6.  [Estrutura do Projeto](#6-estrutura-do-projeto)
7.  [Guia de Uso](#7-guia-de-uso)
    *   [Como Executar o Aplicativo](#como-executar-o-aplicativo)
    *   [Visão Geral da Interface](#visão-geral-da-interface)
    *   [Guia Passo a Passo](#guia-passo-a-passo)
8.  [Formatos de Entrada](#8-formatos-de-entrada)
    *   [CSV/Excel](#csvexcel)
    *   [NPY/NPZ (A-scan)](#npynpz-a-scan)
    *   [Exemplos de Dados](#exemplos-de-dados)
9.  [Modos de Operação](#9-modos-de-operação)
    *   [Modo Longitudinal (TOF)](#modo-longitudinal-tof)
    *   [Modo Cisalhante (Birefringência)](#modo-cisalhante-birefringência)
    *   [Dados Sintéticos de Teste](#dados-sintéticos-de-teste)
10. [Parâmetros de Configuração](#10-parâmetros-de-configuração)
    *   [Modo de Medição](#modo-de-medição)
    *   [Espessura do Componente](#espessura-do-componente)
    *   [Velocidade de Referência (v_ref)](#velocidade-de-referência-v_ref)
    *   [Constante Acustoelástica K](#constante-acustoelástica-k)
    *   [Correção Térmica](#correção-térmica)
    *   [Gate(s) de Tempo (para A-scan)](#gates-de-tempo-para-a-scan)
    *   [Passo da Malha](#passo-da-malha)
    *   [Colormap e Normalização](#colormap-e-normalização)
11. [Processamento de Dados](#11-processamento-de-dados)
    *   [Fluxo de Processamento](#fluxo-de-processamento)
    *   [Cálculos Realizados](#cálculos-realizados)
    *   [Interpolação e Grade](#interpolação-e-grade)
12. [Visualizações](#12-visualizações)
    *   [Heatmap do Índice de Tensão](#heatmap-do-índice-de-tensão)
    *   [Histogramas e Estatísticas](#histogramas-e-estatísticas)
13. [Exportações](#13-exportações)
    *   [Heatmap (PNG)](#heatmap-png)
    *   [Dados Processados (CSV)](#dados-processados-csv)
    *   [Relatório Sumarizado (TXT/Markdown)](#relatório-sumarizado-txtmarkdown)
14. [Exemplos Práticos](#14-exemplos-práticos)
    *   [Exemplo com Dados Sintéticos](#exemplo-com-dados-sintéticos)
    *   [Exemplo com Dados Reais](#exemplo-com-dados-reais)
    *   [Interpretação de Resultados](#interpretação-de-resultados)
15. [Validação e Calibração](#15-validação-e-calibração)
    *   [Validação de Resultados](#validação-de-resultados)
    *   [Calibração da Constante K](#calibração-da-constante-k)
    *   [Boas Práticas](#boas-práticas)
16. [Troubleshooting](#16-troubleshooting)
    *   [Problemas Comuns](#problemas-comuns)
    *   [FAQ](#faq)
17. [Limitações](#17-limitações)
    *   [Limitações do Método Acustoelástico](#limitações-do-método-acustoelástico)
    *   [Limitações do Software](#limitações-do-software)
18. [Contribuindo](#18-contribuindo)
19. [Licença](#19-licença)
20. [Referências](#20-referências)
21. [Contato e Suporte](#21-contato-e-suporte)
22. [Changelog](#22-changelog)

---

## 1. Descrição Geral

O **Streamlit Residual Stress Analyzer** é um aplicativo web interativo desenvolvido em Python usando o framework Streamlit. Ele permite a visualização e análise de tensões residuais relativas em materiais metálicos, utilizando dados de ultrassom (mapas C-scan ou matrizes de A-scan) e o princípio do **efeito acustoelástico**.

O objetivo principal é transformar leituras de tempo de voo (TOF) ou velocidades de ondas cisalhantes em mapas de calor de "índice de tensão residual" (Δv/v ou birefringência), oferecendo ferramentas para calibração, correção térmica e exportação de resultados e relatórios.

⚠️ **Aviso Importante:** Os resultados gerados por este aplicativo são **RELATIVOS**. A obtenção de valores absolutos de tensão residual requer calibração externa e validação com técnicas complementares (como difração de raios-X ou furo incremental).

---

## 2. Características Principais

✨ **Funcionalidades Essenciais:**

*   **Upload Flexível de Dados:** Suporte a arquivos CSV/Excel para dados de C-scan (TOF, v1, v2).
*   **Modos de Análise:**
    *   **Longitudinal (TOF):** Calcula Δv/v a partir do tempo de voo.
    *   **Cisalhante (Birefringência):** Calcula birefringência a partir de velocidades de polarizações ortogonais (v1, v2).
*   **Correções Avançadas:**
    *   **Correção Térmica:** Ajusta a velocidade ultrassônica com base na temperatura.
    *   **Velocidade de Referência (v_ref):** Definição manual ou por seleção de Região de Interesse (ROI) nos dados.
*   **Visualização Intuitiva:**
    *   **Heatmaps:** Mapas de calor do índice de tensão residual com colormaps configuráveis.
    *   **Histogramas:** Distribuição estatística do índice de tensão.
    *   **Estatísticas:** Média, desvio padrão, mínimo, máximo do índice.
*   **Estimativa Quantitativa (Opcional):** Conversão do índice Δv/v para tensão (MPa) usando uma constante acustoelástica (K) fornecida pelo usuário, com os devidos avisos de limitação.
*   **Exportação de Resultados:**
    *   **PNG:** Imagem do heatmap.
    *   **CSV:** Dados processados e interpolados.
    *   **Relatório:** Sumário detalhado em formato TXT/Markdown com parâmetros e estatísticas.
*   **Dados Sintéticos:** Geração de um dataset sintético para testes rápidos da interface e funcionalidades.
*   **Interface Amigável:** Desenvolvido com Streamlit para uma experiência de usuário intuitiva e responsiva.

---

## 3. Conceitos Científicos

### Efeito Acustoelástico

O efeito acustoelástico descreve a dependência da velocidade de propagação de ondas ultrassônicas no material com o estado de tensão aplicado. Em outras palavras, a velocidade do ultrassom muda quando o material está sob tensão. Essa mudança de velocidade é pequena, mas mensurável, e pode ser correlacionada com a tensão residual presente no material.

A relação fundamental é que a variação relativa da velocidade (Δv/v) é aproximadamente proporcional à tensão (σ):

`Δv/v = K * σ`

Onde `K` é a constante acustoelástica do material, que é específica para cada material, tipo de onda e direção de propagação.

### Fórmulas Matemáticas

#### Modo Longitudinal (TOF)

1.  **Cálculo da Velocidade (v):**
    `v = (2 * d) / TOF`
    Onde:
    *   `v`: Velocidade da onda longitudinal (m/s)
    *   `d`: Espessura do componente (m)
    *   `TOF`: Tempo de voo da onda (s)

2.  **Correção Térmica (v_corr):**
    `v_corr = v + α * (T_medida - T_referencia)`
    Onde:
    *   `v_corr`: Velocidade corrigida (m/s)
    *   `v`: Velocidade medida (m/s)
    *   `α`: Coeficiente térmico da velocidade ((m/s)/°C)
    *   `T_medida`: Temperatura na qual a medição foi realizada (°C)
    *   `T_referencia`: Temperatura de referência (°C)

3.  **Índice de Tensão Residual (Δv/v):**
    `Índice = (v_corr - v_ref) / v_ref`
    Onde:
    *   `v_ref`: Velocidade de referência em uma região livre de tensões (m/s)

#### Modo Cisalhante (Birefringência)

1.  **Velocidade Média (v_médio):**
    `v_médio = (v1 + v2) / 2`
    Onde:
    *   `v1`, `v2`: Velocidades das ondas cisalhantes polarizadas ortogonalmente (m/s)

2.  **Índice de Birefringência (Δv/v):**
    `Índice = (v1 - v2) / v_médio`
    Este índice é sensível a tensões cisalhantes e à orientação das tensões principais.

#### Conversão Qualitativa para Tensão (Opcional)

Se a constante acustoelástica `K` for fornecida:
`σ (MPa) ≈ Índice / K`

### Limitações e Considerações

⚠️ **Resultados Relativos:** O principal ponto a ser lembrado é que este método fornece um **índice relativo** de tensão. Ele indica variações de tensão em relação a um estado de referência (v_ref). Para obter valores absolutos de tensão em MPa, é crucial uma calibração rigorosa da constante acustoelástica `K` para o material específico e validação com técnicas absolutas.

*   **Microestrutura:** Fatores como textura cristalográfica, tamanho de grão, fases metalúrgicas e anisotropia do material podem influenciar a velocidade ultrassônica independentemente da tensão, introduzindo ruído ou vieses nos resultados.
*   **Temperatura:** A correção térmica é uma aproximação linear. Grandes variações de temperatura ou materiais com comportamento térmico complexo podem exigir modelos mais sofisticados.
*   **Estado de Tensão:** O efeito acustoelástico é mais simples de interpretar para estados de tensão uniaxial ou biaxial. Em estados de tensão triaxial complexos, a interpretação pode ser mais desafiadora.
*   **Profundidade de Análise:** Ondas longitudinais geralmente atravessam toda a espessura do componente, fornecendo uma média da tensão ao longo do caminho. Para tensões superficiais, outras técnicas (como ondas de superfície) seriam mais apropriadas.

---

## 4. Requisitos Técnicos

Para executar o Streamlit Residual Stress Analyzer, você precisará de:

*   **Python:** Versão 3.10 ou superior.
*   **Bibliotecas Python:**
    *   `streamlit` (para a interface web)
    *   `numpy` (para operações numéricas eficientes)
    *   `pandas` (para manipulação de dados tabulares)
    *   `scipy` (para interpolação e processamento de sinal, como a transformada de Hilbert para A-scan)
    *   `matplotlib` (para plotagem de gráficos e heatmaps)
    *   `seaborn` (para visualizações aprimoradas, embora `matplotlib` seja o principal para heatmaps aqui)
    *   `openpyxl` (para leitura de arquivos `.xlsx` e `.xls`)
*   **Requisitos de Sistema:**
    *   **RAM:** Mínimo de 4 GB (8 GB ou mais recomendado para grandes datasets).
    *   **Espaço em Disco:** Aproximadamente 100 MB para o código e dependências, mais espaço para seus arquivos de dados.
    *   **Processador:** Qualquer CPU moderna é suficiente.

---

## 5. Instalação

Siga os passos abaixo para configurar e instalar o aplicativo em seu sistema.

### Pré-requisitos

Certifique-se de ter o Python 3.10 ou superior instalado. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).

### Criação de Ambiente Virtual

É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto e evitar conflitos com outras instalações Python.

1.  **Navegue até o diretório do projeto:**
```bash
    cd /caminho/para/seu/projeto/streamlit-residual-stress-analyzer