Aqui está o arquivo README.md completo e detalhado para o seu projeto, conforme solicitado:

`markdown
🔊 Streamlit Residual Stress Analyzer

!Python Version
!Streamlit Version
!License
!Status

📝 Índice

1.  Descrição Geral
2.  Características Principais
3.  Conceitos Científicos
    *   Efeito Acustoelástico
    *   Fórmulas Matemáticas
    *   Limitações e Considerações
4.  Requisitos Técnicos
5.  Instalação
    *   Pré-requisitos
    *   Criação de Ambiente Virtual
    *   Instalação das Dependências
6.  Estrutura do Projeto
7.  Guia de Uso
    *   Como Executar o Aplicativo
    *   Visão Geral da Interface
    *   Guia Passo a Passo
8.  Formatos de Entrada
    *   CSV/Excel
    *   NPY/NPZ (A-scan)
    *   Exemplos de Dados
9.  Modos de Operação
    *   Modo Longitudinal (TOF)
    *   Modo Cisalhante (Birefringência)
    *   Dados Sintéticos de Teste
10. Parâmetros de Configuração
    *   Modo de Medição
    *   Espessura do Componente
    *   Velocidade de Referência (v_ref)
    *   Constante Acustoelástica K
    *   Correção Térmica
    *   Gate(s) de Tempo (para A-scan)
    *   Passo da Malha
    *   Colormap e Normalização
11. Processamento de Dados
    *   Fluxo de Processamento
    *   Cálculos Realizados
    *   Interpolação e Grade
12. Visualizações
    *   Heatmap do Índice de Tensão
    *   Histogramas e Estatísticas
13. Exportações
    *   Heatmap (PNG)
    *   Dados Processados (CSV)
    *   Relatório Sumarizado (TXT/Markdown)
14. Exemplos Práticos
    *   Exemplo com Dados Sintéticos
    *   Exemplo com Dados Reais
    *   Interpretação de Resultados
15. Validação e Calibração
    *   Validação de Resultados
    *   Calibração da Constante K
    *   Boas Práticas
16. Troubleshooting
    *   Problemas Comuns
    *   FAQ
17. Limitações
    *   Limitações do Método Acustoelástico
    *   Limitações do Software
18. Contribuindo
19. Licença
20. Referências
21. Contato e Suporte
22. Changelog

---

1. Descrição Geral

O Streamlit Residual Stress Analyzer é um aplicativo web interativo desenvolvido em Python usando o framework Streamlit. Ele permite a visualização e análise de tensões residuais relativas em materiais metálicos, utilizando dados de ultrassom (mapas C-scan ou matrizes de A-scan) e o princípio do efeito acustoelástico.

O objetivo principal é transformar leituras de tempo de voo (TOF) ou velocidades de ondas cisalhantes em mapas de calor de "índice de tensão residual" (Δv/v ou birefringência), oferecendo ferramentas para calibração, correção térmica e exportação de resultados e relatórios.

⚠️ Aviso Importante: Os resultados gerados por este aplicativo são RELATIVOS. A obtenção de valores absolutos de tensão residual requer calibração externa e validação com técnicas complementares (como difração de raios-X ou furo incremental).

---

2. Características Principais

✨ Funcionalidades Essenciais:

*   Upload Flexível de Dados: Suporte a arquivos CSV/Excel para dados de C-scan (TOF, v1, v2).
*   Modos de Análise:
    *   Longitudinal (TOF): Calcula Δv/v a partir do tempo de voo.
    *   Cisalhante (Birefringência): Calcula birefringência a partir de velocidades de polarizações ortogonais (v1, v2).
*   Correções Avançadas:
    *   Correção Térmica: Ajusta a velocidade ultrassônica com base na temperatura.
    *   Velocidade de Referência (v_ref): Definição manual ou por seleção de Região de Interesse (ROI) nos dados.
*   Visualização Intuitiva:
    *   Heatmaps: Mapas de calor do índice de tensão residual com colormaps configuráveis.
    *   Histogramas: Distribuição estatística do índice de tensão.
    *   Estatísticas: Média, desvio padrão, mínimo, máximo do índice.
*   Estimativa Quantitativa (Opcional): Conversão do índice Δv/v para tensão (MPa) usando uma constante acustoelástica (K) fornecida pelo usuário, com os devidos avisos de limitação.
*   Exportação de Resultados:
    *   PNG: Imagem do heatmap.
    *   CSV: Dados processados e interpolados.
    *   Relatório: Sumário detalhado em formato TXT/Markdown com parâmetros e estatísticas.
*   Dados Sintéticos: Geração de um dataset sintético para testes rápidos da interface e funcionalidades.
*   Interface Amigável: Desenvolvido com Streamlit para uma experiência de usuário intuitiva e responsiva.

---

3. Conceitos Científicos

Efeito Acustoelástico

O efeito acustoelástico descreve a dependência da velocidade de propagação de ondas ultrassônicas no material com o estado de tensão aplicado. Em outras palavras, a velocidade do ultrassom muda quando o material está sob tensão. Essa mudança de velocidade é pequena, mas mensurável, e pode ser correlacionada com a tensão residual presente no material.

A relação fundamental é que a variação relativa da velocidade (Δv/v) é aproximadamente proporcional à tensão (σ):

Δv/v = K * σ

Onde K é a constante acustoelástica do material, que é específica para cada material, tipo de onda e direção de propagação.

Fórmulas Matemáticas

Modo Longitudinal (TOF)

1.  Cálculo da Velocidade (v):
    v = (2 * d) / TOF
    Onde:
    *   v: Velocidade da onda longitudinal (m/s)
    *   d: Espessura do componente (m)
    *   TOF: Tempo de voo da onda (s)

2.  Correção Térmica (v_corr):
    v_corr = v + α * (T_medida - T_referencia)
    Onde:
    *   v_corr: Velocidade corrigida (m/s)
    *   v: Velocidade medida (m/s)
    *   α: Coeficiente térmico da velocidade ((m/s)/°C)
    *   T_medida: Temperatura na qual a medição foi realizada (°C)
    *   T_referencia: Temperatura de referência (°C)

3.  Índice de Tensão Residual (Δv/v):
    Índice = (v_corr - v_ref) / v_ref
    Onde:
    *   v_ref: Velocidade de referência em uma região livre de tensões (m/s)

Modo Cisalhante (Birefringência)

1.  Velocidade Média (v_médio):
    v_médio = (v1 + v2) / 2
    Onde:
    *   v1, v2: Velocidades das ondas cisalhantes polarizadas ortogonalmente (m/s)

2.  Índice de Birefringência (Δv/v):
    Índice = (v1 - v2) / v_médio
    Este índice é sensível a tensões cisalhantes e à orientação das tensões principais.

Conversão Qualitativa para Tensão (Opcional)

Se a constante acustoelástica K for fornecida:
σ (MPa) ≈ Índice / K

Limitações e Considerações

⚠️ Resultados Relativos: O principal ponto a ser lembrado é que este método fornece um índice relativo de tensão. Ele indica variações de tensão em relação a um estado de referência (v_ref). Para obter valores absolutos de tensão em MPa, é crucial uma calibração rigorosa da constante acustoelástica K para o material específico e validação com técnicas absolutas.

*   Microestrutura: Fatores como textura cristalográfica, tamanho de grão, fases metalúrgicas e anisotropia do material podem influenciar a velocidade ultrassônica independentemente da tensão, introduzindo ruído ou vieses nos resultados.
*   Temperatura: A correção térmica é uma aproximação linear. Grandes variações de temperatura ou materiais com comportamento térmico complexo podem exigir modelos mais sofisticados.
*   Estado de Tensão: O efeito acustoelástico é mais simples de interpretar para estados de tensão uniaxial ou biaxial. Em estados de tensão triaxial complexos, a interpretação pode ser mais desafiadora.
*   Profundidade de Análise: Ondas longitudinais geralmente atravessam toda a espessura do componente, fornecendo uma média da tensão ao longo do caminho. Para tensões superficiais, outras técnicas (como ondas de superfície) seriam mais apropriadas.

---

4. Requisitos Técnicos

Para executar o Streamlit Residual Stress Analyzer, você precisará de:

*   Python: Versão 3.10 ou superior.
*   Bibliotecas Python:
    *   streamlit (para a interface web)
    *   numpy (para operações numéricas eficientes)
    *   pandas (para manipulação de dados tabulares)
    *   scipy (para interpolação e processamento de sinal, como a transformada de Hilbert para A-scan)
    *   matplotlib (para plotagem de gráficos e heatmaps)
    *   seaborn (para visualizações aprimoradas, embora matplotlib seja o principal para heatmaps aqui)
    *   openpyxl (para leitura de arquivos .xlsx e .xls)
*   Requisitos de Sistema:
    *   RAM: Mínimo de 4 GB (8 GB ou mais recomendado para grandes datasets).
    *   Espaço em Disco: Aproximadamente 100 MB para o código e dependências, mais espaço para seus arquivos de dados.
    *   Processador: Qualquer CPU moderna é suficiente.

---

5. Instalação

Siga os passos abaixo para configurar e instalar o aplicativo em seu sistema.

Pré-requisitos

Certifique-se de ter o Python 3.10 ou superior instalado. Você pode baixá-lo em python.org.

Criação de Ambiente Virtual

É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto e evitar conflitos com outras instalações Python.

1.  Navegue até o diretório do projeto:
    `bash
    cd /caminho/para/seu/projeto/streamlit-residual-stress-analyzer
    `

2.  Crie o ambiente virtual:
    `bash
    python -m venv .venv
    `

3.  Ative o ambiente virtual:
    *   Windows:
        `bash
        .venv\Scripts\activate
        `
    *   macOS/Linux:
        `bash
        source .venv/bin/activate
        `
    Você verá (.venv) no início da linha de comando, indicando que o ambiente virtual está ativo.

Instalação das Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias usando o arquivo requirements.txt fornecido:

`bash
pip install -r requirements.txt
`

---

6. Estrutura do Projeto

O projeto é organizado da seguinte forma:

`
streamlit-residual-stress-analyzer/
├── streamlit_app.py          # Código principal do aplicativo Streamlit
├── requirements.txt          # Lista de dependências Python
└── data/                     # (Opcional) Diretório para armazenar arquivos de dados de exemplo
    ├── example_longitudinal.csv  # Exemplo de dados para modo longitudinal
    └── example_shear.csv         # Exemplo de dados para modo cisalhante
`

*   streamlit_app.py: Contém todo o código-fonte do aplicativo Streamlit, incluindo a interface do usuário, lógica de processamento de dados, cálculos acustoelásticos e funções de visualização/exportação.
*   requirements.txt: Lista todas as bibliotecas Python necessárias para o projeto, garantindo que você possa reproduzir o ambiente de desenvolvimento.
*   data/: Este diretório é sugerido para armazenar seus arquivos de dados de entrada (CSV, Excel, etc.) e pode conter exemplos para facilitar o teste.

---

7. Guia de Uso

Como Executar o Aplicativo

1.  Ative seu ambiente virtual (se ainda não estiver ativo).
2.  Navegue até o diretório do projeto onde streamlit_app.py está localizado.
3.  Execute o aplicativo Streamlit com o seguinte comando:

    `bash
    streamlit run streamlit_app.py
    `

    Seu navegador web padrão deve abrir automaticamente uma nova aba com o aplicativo em http://localhost:8501. Se não abrir, copie e cole o endereço no seu navegador.

Visão Geral da Interface

O aplicativo é dividido em duas áreas principais:

*   Barra Lateral (Sidebar): Localizada à esquerda, contém todos os parâmetros de configuração e controle para a análise (modo de medição, espessura, referências, correções, etc.).
*   Área Principal: Ocupa a maior parte da tela e é onde você fará o upload dos dados, visualizará os heatmaps, histogramas e estatísticas, e encontrará as opções de exportação.

Guia Passo a Passo

1.  Iniciar o Aplicativo:
    *   Execute streamlit run streamlit_app.py no terminal.

2.  Carregar Dados:
    *   Na área principal, você tem duas opções:
        *   "Upload de Arquivo": Clique em "Selecione arquivo CSV ou Excel" para carregar seus próprios dados. Certifique-se de que o arquivo esteja no formato correto (veja Formatos de Entrada).
        *   "Dados Sintéticos de Teste": Use esta aba para gerar um dataset de exemplo rapidamente. Ajuste os "Pontos em X", "Pontos em Y" e "Nível de ruído" e clique em "🎲 Gerar Dados Sintéticos". Isso é ótimo para testar a interface sem dados reais.
    *   Após o upload/geração, uma prévia dos dados será exibida.

    (Screenshot: Área de upload de dados com prévia de um CSV)

3.  Configurar Parâmetros na Barra Lateral:
    *   Modo de Medição: Escolha entre "Longitudinal (TOF)" ou "Cisalhante (birefringência)" de acordo com seus dados.
    *   Espessura do Componente (mm): Insira a espessura da peça.
    *   Velocidade de Referência (v_ref):
        *   "Valor numérico": Digite um valor de v_ref conhecido.
        *   "ROI (região de interesse)": Seus dados serão carregados primeiro. Depois, na área principal, aparecerão sliders para definir x_min/max e y_min/max para selecionar uma região. A média da velocidade nesta ROI será usada como v_ref.
    *   Constante Acustoelástica K (Opcional): Marque a caixa e insira um valor de K se desejar uma estimativa semi-quantitativa da tensão em MPa.
    *   Correção Térmica (Opcional): Marque a caixa, insira o coeficiente térmico, temperatura de referência e temperatura medida para aplicar a correção.
    *   Passo da Malha (mm): Define a resolução da grade para a interpolação do heatmap.
    *   Colormap e Normalização: Escolha o esquema de cores e ajuste os percentis mínimo/máximo para a escala de cores do heatmap.

    (Screenshot: Barra lateral com parâmetros configurados)

4.  Visualizar Resultados:
    *   Após carregar os dados e configurar os parâmetros, o aplicativo processará automaticamente e exibirá:
        *   Estatísticas: Média, desvio padrão, mínimo e máximo do índice de tensão.
        *   Heatmap do Índice de Tensão: Um mapa de calor mostrando a distribuição espacial do índice de tensão.
        *   Histograma da Distribuição: Um gráfico da frequência dos valores do índice de tensão.

    (Screenshot: Heatmap e histograma exibidos na área principal)

5.  Exportar Resultados:
    *   Na seção "Exportar Resultados", você encontrará botões para:
        *   📷 Baixar Heatmap (PNG): Salva a imagem do mapa de calor.
        *   📊 Baixar Dados (CSV): Exporta os dados processados, incluindo o índice de tensão calculado.
        *   📄 Baixar Relatório (TXT): Gera um relatório sumarizado com todos os parâmetros usados e estatísticas.
    *   Você também pode clicar em "👁️ Visualizar Relatório" para ver o conteúdo do relatório diretamente no aplicativo.

    (Screenshot: Seção de exportação com botões)

---

8. Formatos de Entrada

O aplicativo suporta arquivos CSV e Excel para dados de C-scan. O suporte para arquivos NPY/NPZ (cubos A-scan) é um recurso avançado planejado.

CSV/Excel

Os arquivos CSV ou Excel devem conter colunas específicas dependendo do modo de medição selecionado. As coordenadas x e y devem estar em milímetros (mm).

Modo Longitudinal (TOF)

*   Colunas Obrigatórias:
    *   x: Coordenada X do ponto de medição (mm)
    *   y: Coordenada Y do ponto de medição (mm)
    *   tof_us: Tempo de voo da onda ultrassônica (microssegundos, µs)

*   Exemplo de CSV:
    `csv
    x,y,tof_us
    0.0,0.0,3.3898
    1.0,0.0,3.3901
    2.0,0.0,3.3905
    ...
    `

Modo Cisalhante (Birefringência)

*   Colunas Obrigatórias:
    *   x: Coordenada X do ponto de medição (mm)
    *   y: Coordenada Y do ponto de medição (mm)
    *   v1: Velocidade da onda cisalhante na primeira polarização (m/s)
    *   v2: Velocidade da onda cisalhante na segunda polarização (m/s)

*   Exemplo de CSV:
    `csv
    x,y,v1,v2
    0.0,0.0,3200.5,3198.2
    1.0,0.0,3201.0,3198.5
    2.0,0.0,3201.3,3198.8
    ...
    `

NPY/NPZ (A-scan)

(Este recurso é mencionado nos requisitos, mas a implementação completa de processamento de A-scan (Hilbert Transform, gate de tempo) não está totalmente desenvolvida no código atual. A estrutura esperada seria para futuras implementações.)

*   Formato Esperado:
    *   Um arquivo .npy ou .npz contendo:
        *   Um array NumPy 3D (data_cube) com shape [ny, nx, nt], onde ny é o número de pontos em Y, nx é o número de pontos em X, e nt é o número de amostras de tempo por A-scan.
        *   Um array NumPy 1D (time_vector) com nt elementos, representando os valores de tempo para cada amostra.

Exemplos de Dados

Você pode criar um diretório data/ na raiz do projeto e salvar arquivos CSV de exemplo para testar. O aplicativo também oferece a opção de gerar dados sintéticos diretamente na interface.

---

9. Modos de Operação

O aplicativo oferece dois modos principais de análise, selecionáveis na barra lateral.

Modo Longitudinal (TOF)

*   Princípio: Baseia-se na medição do Tempo de Voo (TOF) de uma onda ultrassônica longitudinal através da espessura do material. A velocidade é calculada a partir do TOF e da espessura. Variações na velocidade são correlacionadas com as tensões residuais.
*   Dados de Entrada: Requer as colunas x, y e tof_us.
*   Saída: Heatmap e estatísticas do índice (v - v_ref) / v_ref.

Modo Cisalhante (Birefringência)

*   Princípio: Utiliza ondas ultrassônicas cisalhantes polarizadas em duas direções ortogonais. A diferença de velocidade entre essas duas polarizações (birefringência) é sensível à anisotropia induzida por tensões residuais.
*   Dados de Entrada: Requer as colunas x, y, v1 e v2 (velocidades das duas polarizações).
*   Saída: Heatmap e estatísticas do índice (v1 - v2) / v_médio.

Dados Sintéticos de Teste

*   Propósito: Permite gerar um conjunto de dados simulados com um gradiente de tensão suave e ruído. Ideal para testar a funcionalidade do aplicativo, a interface do usuário e as opções de visualização sem a necessidade de carregar arquivos reais.
*   Configuração: Ajuste o número de pontos em X e Y, e o nível de ruído para criar diferentes cenários de teste.

---

10. Parâmetros de Configuração

Todos os parâmetros de configuração são ajustados na barra lateral (sidebar) do aplicativo.

Modo de Medição

*   Opções: "Longitudinal (TOF)", "Cisalhante (birefringência)".
*   Descrição: Define qual algoritmo de cálculo de índice de tensão será utilizado, impactando as colunas de entrada esperadas.

Espessura do Componente (mm)

*   Tipo: Numérico (float).
*   Descrição: A espessura da peça em milímetros. Essencial para converter TOF em velocidade no modo longitudinal.
*   Dica: Certifique-se de que esta é a espessura real do caminho percorrido pela onda.

Velocidade de Referência (v_ref)

*   Métodos:
    *   "Valor numérico": Insira um valor de velocidade (m/s) conhecido para uma região livre de tensões do material.
    *   "ROI (região de interesse)": Após carregar os dados, sliders aparecerão na área principal para que você defina uma caixa delimitadora (x_min/max, y_min/max). A média da velocidade dentro desta ROI será calculada e usada como v_ref.
*   Descrição: A velocidade ultrassônica do material em um estado livre de tensões. É o ponto de referência para calcular a variação relativa de velocidade (Δv/v).
*   Dica de Calibração: Idealmente, v_ref deve ser obtido de uma amostra do mesmo material, com a mesma microestrutura, mas sem tensões residuais.

Constante Acustoelástica K (Opcional)

*   Tipo: Numérico (float).
*   Descrição: Se fornecida, permite uma estimativa semi-quantitativa da tensão residual em MPa (σ ≈ Δv/v / K).
*   Valores Típicos: Para aços, K pode variar de 1e-5 a 1e-4 (MPa⁻¹).
*   Dica de Calibração: A constante K é altamente dependente do material, tipo de onda, direção de propagação e microestrutura. Deve ser determinada experimentalmente para cada material e condição específica, por exemplo, aplicando tensões conhecidas a amostras.

Correção Térmica (Opcional)

*   Parâmetros:
    *   Coeficiente térmico ((m/s)/°C): Taxa de variação da velocidade com a temperatura. Típico para aço: -0.9 (m/s)/°C.
    *   Temperatura de referência (°C): Temperatura na qual a constante acustoelástica K foi determinada ou uma temperatura ambiente padrão.
    *   Temperatura da medição (°C): Temperatura real do componente durante a medição ultrassônica.
*   Descrição: Compensa as variações de velocidade ultrassônica causadas por diferenças de temperatura entre a medição e a referência.

Gate(s) de Tempo (para A-scan)

(Este parâmetro é relevante para o processamento de dados A-scan, que é um recurso avançado e não totalmente implementado na versão atual do código. No futuro, seria usado para definir a janela de tempo onde o eco de interesse (ex: eco de fundo) deve ser detectado.)

Passo da Malha (mm)

*   Tipo: Numérico (float).
*   Descrição: Define a resolução da grade para a interpolação dos dados antes de gerar o heatmap. Um valor menor resulta em um mapa mais detalhado, mas pode aumentar o tempo de processamento.
*   Dica: Escolha um passo que seja razoável em relação ao espaçamento dos seus pontos de medição.

Colormap e Normalização

*   Colormap: Selecione um esquema de cores para o heatmap (ex: viridis, coolwarm, inferno). coolwarm ou RdBu_r são bons para visualizar variações em torno de um ponto central (zero).
*   Percentil Mínimo/Máximo: Ajusta a faixa de cores do heatmap. Por exemplo, definir 1% e 99% ignora os 1% menores e 1% maiores valores, que podem ser ruído, melhorando o contraste visual para a maioria dos dados.

---

11. Processamento de Dados

O aplicativo segue um fluxo de processamento lógico para transformar os dados brutos em um mapa de tensões residuais.

Fluxo de Processamento

1.  Upload/Geração de Dados: Carregamento do arquivo CSV/Excel ou geração de dados sintéticos.
2.  Validação de Colunas: Verifica se as colunas necessárias (x, y, tof_us ou v1, v2) estão presentes.
3.  Cálculo de Velocidade (Modo Longitudinal): Converte tof_us em velocidade (m/s) usando a espessura_mm.
4.  Correção Térmica (Opcional): Aplica o ajuste de temperatura à velocidade calculada.
5.  Definição de v_ref: Obtém a velocidade de referência (manual ou via ROI).
6.  Cálculo do Índice de Tensão:
    *   Longitudinal: (v_corr - v_ref) / v_ref
    *   Cisalhante: (v1 - v2) / v_médio
7.  Interpolação: Transforma os dados esparsos em uma grade regular para o heatmap.
8.  Visualização: Gera heatmap, histograma e estatísticas.

Cálculos Realizados

As fórmulas detalhadas para cálculo de velocidade, correção térmica e índices de tensão/birefringência podem ser encontradas na seção Conceitos Científicos.

Interpolação e Grade

Os dados de ultrassom são frequentemente coletados em pontos discretos. Para criar um heatmap contínuo, o aplicativo utiliza interpolação:

*   Método: scipy.interpolate.griddata com o método cubic é usado para interpolar os valores do índice de tensão em uma grade regular.
*   Resolução: A resolução da grade é controlada pelo parâmetro "Passo da malha (mm)" na barra lateral.
*   Extrapolação: Pontos fora da área de dados original são preenchidos com NaN (Not a Number) para evitar extrapolações enganosas.
*   Aspect Ratio: O heatmap é plotado com aspect='equal' para garantir que as dimensões X e Y sejam representadas corretamente em escala.

---

12. Visualizações

O aplicativo oferece visualizações claras para interpretar os resultados da análise de tensões residuais.

Heatmap do Índice de Tensão

*   Descrição: Um mapa de calor 2D que exibe a distribuição espacial do índice de tensão residual (Δv/v ou birefringência) sobre a área escaneada.
*   Eixos: As coordenadas X e Y são plotadas em milímetros (mm).
*   Escala de Cores: A legenda de cores indica os valores do índice de tensão. Você pode personalizar o Colormap e a Normalização (Percentis) na barra lateral para otimizar a visualização.
*   Interpretação: Regiões com cores mais quentes (ex: vermelho em coolwarm) podem indicar tensões de compressão ou tração mais elevadas (dependendo da calibração e do sinal), enquanto cores mais frias (ex: azul) indicam o oposto ou regiões de menor tensão.

    (Screenshot: Exemplo de heatmap com legenda de cores)

Histogramas e Estatísticas

*   Histograma: Um gráfico de barras que mostra a distribuição de frequência dos valores do índice de tensão. Ajuda a entender a dispersão dos dados e identificar valores atípicos. A média e a mediana são indicadas por linhas tracejadas.
*   Estatísticas: Uma seção com métricas chave:
    *   Média: Valor médio do índice de tensão.
    *   Desvio Padrão: Medida da dispersão dos dados.
    *   Mínimo: Menor valor do índice.
    *   Máximo: Maior valor do índice.
    *   Se K for fornecido, uma estimativa da tensão média e variação em MPa também será exibida.

    (Screenshot: Exemplo de histograma com estatísticas)

---

13. Exportações

Os resultados da análise podem ser exportados em diferentes formatos para relatórios, análises adicionais ou arquivamento.

Heatmap (PNG)

*   Formato: Imagem PNG de alta resolução (300 dpi).
*   Conteúdo: O mapa de calor gerado, incluindo eixos, título e legenda de cores.
*   Uso: Ideal para inclusão em relatórios, apresentações ou documentação visual.

Dados Processados (CSV)

*   Formato: Arquivo CSV (Comma Separated Values).
*   Conteúdo: Contém todas as colunas dos dados de entrada, mais as colunas calculadas durante o processamento (ex: velocidade, indice_tensao).
*   Uso: Pode ser importado em softwares de planilha (Excel, Google Sheets) ou outras ferramentas de análise de dados para processamento posterior.

Relatório Sumarizado (TXT/Markdown)

*   Formato: Arquivo de texto simples (.txt) ou Markdown.
*   Conteúdo: Um relatório detalhado que inclui:
    *   Data e hora da análise.
    *   Todos os parâmetros de configuração utilizados.
    *   Estatísticas completas do índice de tensão (média, desvio padrão, min, max, percentis).
    *   Estimativa semi-quantitativa de tensão em MPa (se K foi fornecido).
    *   Notas importantes e limitações do método acustoelástico.
*   Uso: Serve como um registro completo da análise, garantindo a rastreabilidade dos parâmetros e resultados. Pode ser facilmente copiado e colado em documentos ou sistemas de gerenciamento de dados.

---

14. Exemplos Práticos

Exemplo com Dados Sintéticos

1.  Inicie o aplicativo (streamlit run streamlit_app.py).
2.  Na área principal, selecione a aba "Dados Sintéticos de Teste".
3.  Ajuste os parâmetros Pontos em X, Pontos em Y e Nível de ruído (ex: 50, 40, 0.02).
4.  Clique em "🎲 Gerar Dados Sintéticos". Uma tabela com os dados gerados aparecerá.
5.  Na barra lateral, selecione "Longitudinal (TOF)" como modo de medição.
6.  Defina a Espessura do componente para 10.0 mm.
7.  Em "Velocidade de Referência", escolha "Valor numérico" e defina v_ref para 5900.0 m/s.
8.  Observe o heatmap e o histograma gerados. Você deverá ver um gradiente de tensão simulado e as estatísticas correspondentes.
9.  Experimente ajustar o Colormap e os Percentis para ver como a visualização muda.
10. Clique nos botões de exportação para salvar o heatmap, os dados e o relatório.

Exemplo com Dados Reais

1.  Prepare seu arquivo de dados (CSV ou Excel) no formato correto (veja Formatos de Entrada). Por exemplo, um CSV com x,y,tof_us.
2.  Inicie o aplicativo (streamlit run streamlit_app.py).
3.  Na área principal, selecione a aba "Upload de Arquivo".
4.  Clique em "Selecione arquivo CSV ou Excel" e carregue seu arquivo.
5.  Na barra lateral, configure os parâmetros de acordo com suas medições:
    *   Modo de Medição: Escolha "Longitudinal (TOF)" ou "Cisalhante (birefringência)".
    *   Espessura do Componente: Insira a espessura real da sua peça.
    *   Velocidade de Referência:
        *   Se você tiver um valor conhecido para uma região sem tensão, use "Valor numérico".
        *   Caso contrário, escolha "ROI (região de interesse)". Após o carregamento, ajuste os sliders na área principal para selecionar uma área da peça que você sabe estar livre de tensões.
    *   Correção Térmica: Se suas medições foram feitas em temperaturas diferentes da referência, ative e configure a correção.
    *   Constante Acustoelástica K: Se você tiver um valor de K para seu material, insira-o para obter uma estimativa em MPa.
6.  Analise os heatmaps, histogramas e estatísticas.
7.  Exporte os resultados para documentação.

Interpretação de Resultados

*   Heatmap: Procure por padrões de cores. Regiões com cores contrastantes (ex: vermelho vs. azul) indicam gradientes de tensão. Uma distribuição uniforme de cores pode sugerir um estado de tensão homogêneo ou uma peça livre de tensões (se o v_ref for bem escolhido).
*   Histograma: Uma distribuição estreita e centrada perto de zero (para Δv/v) indica pouca variação de tensão. Uma distribuição larga ou com múltiplos picos pode sugerir regiões com diferentes estados de tensão.
*   Estatísticas: A média do índice dá uma ideia do nível geral de tensão. O desvio padrão indica a variabilidade. Valores mínimos e máximos mostram a faixa de tensões presentes.

---

15. Validação e Calibração

Validação de Resultados

A validação é crucial para garantir a confiabilidade das suas análises. Como o método acustoelástico é relativo, é altamente recomendável comparar os resultados com técnicas absolutas em pontos críticos da peça:

*   Difração de Raios-X (XRD): Fornece medições de tensão residual na superfície com alta precisão.
*   Furo Incremental (Hole-Drilling): Mede a tensão residual em profundidade, liberando material e medindo a deformação resultante.
*   Outras Técnicas: Como o método de corte (slitting method) ou o método de contorno (contour method) para tensões em profundidade.

Calibração da Constante K

A constante acustoelástica K é o fator de proporcionalidade entre a variação relativa de velocidade e a tensão. Sua determinação precisa é fundamental para converter o índice Δv/v em valores de tensão em MPa.

*   Método: Geralmente, K é determinado experimentalmente aplicando tensões conhecidas (uniaxial, biaxial) a amostras do material de interesse e medindo a variação correspondente na velocidade ultrassônica.
*   Fatores: K varia com o material, tipo de onda (longitudinal, cisalhante), direção de propagação e polarização, e microestrutura.

Boas Práticas

*   Caracterização do Material: Conheça bem o seu material (composição, tratamento térmico, microestrutura).
*   Controle de Temperatura: Mantenha a temperatura da peça e do transdutor o mais estável possível durante as medições.
*   Superfície: Garanta uma superfície limpa e lisa para um bom acoplamento ultrassônico.
*   Repetibilidade: Realize medições repetidas para avaliar a precisão e a repetibilidade dos seus dados.

---

16. Troubleshooting

Problemas Comuns

*   "Erro ao carregar arquivo":
    *   Causa: Formato de arquivo incorreto, colunas ausentes ou nomes de colunas errados.
    *   Solução: Verifique se o arquivo é CSV ou Excel e se contém as colunas x, y, tof_us (para longitudinal) ou x, y, v1, v2 (para cisalhante). Verifique a ortografia dos nomes das colunas.
*   Heatmap vazio ou com muitos NaNs:
    *   Causa: Dados de entrada insuficientes, valores NaN no índice de tensão, ou problemas na interpolação.
    *   Solução: Verifique se há valores NaN nas colunas de entrada. Ajuste o "Passo da malha" na barra lateral. Certifique-se de que há pontos de dados suficientes para a interpolação.
*   Valores do índice de tensão muito pequenos ou muito grandes:
    *   Causa: v_ref incorreto, erro na espessura_mm, ou unidades inconsistentes.
    *   Solução: Revise v_ref e espessura_mm. Certifique-se de que tof_us está em microssegundos e espessura_mm em milímetros.
*   Aplicativo não inicia:
    *   Causa: Ambiente virtual não ativado, dependências não instaladas, ou erro de sintaxe no streamlit_app.py.
    *   Solução: Ative o ambiente virtual (source .venv/bin/activate ou .venv\Scripts\activate). Execute pip install -r requirements.txt. Verifique o terminal para mensagens de erro do Python.

FAQ

*   "Por que os valores do meu heatmap são tão pequenos (ex: 1e-4)?"
       O índice Δv/v é uma variação relativa* de velocidade, que geralmente é uma fração muito pequena da velocidade total. Valores na ordem de 10⁻⁴ a 10⁻³ são comuns e esperados para tensões residuais.
*   "Posso usar este aplicativo para medir tensões absolutas?"
       Não diretamente. O aplicativo fornece um índice relativo. Para tensões absolutas, você precisa* calibrar a constante acustoelástica K para o seu material e validar com técnicas absolutas. O aplicativo oferece uma estimativa se K for fornecido, mas com ressalvas.
*   "Como posso melhorar a qualidade do meu heatmap?"
    *   Aumente a densidade dos pontos de medição.
    *   Reduza o "Passo da malha" (mas cuidado com o tempo de processamento).
    *   Ajuste os Percentis do colormap para focar na faixa de valores mais relevantes.
    *   Garanta dados de entrada limpos e sem ruído excessivo.

---

17. Limitações

Limitações do Método Acustoelástico

*   Natureza Relativa: Não mede tensões absolutas diretamente.
*   Sensibilidade à Microestrutura: Textura, tamanho de grão, fases podem mascarar ou confundir o sinal de tensão.
*   Anisotropia: Materiais intrinsecamente anisotrópicos (ex: laminados) podem complicar a interpretação.
*   Profundidade: Ondas longitudinais fornecem uma média da tensão ao longo do caminho. Não é ideal para perfis de tensão em profundidade sem técnicas avançadas.
*   Calibração de K: A constante acustoelástica é material-dependente e pode variar com a temperatura e o estado de tensão.

Limitações do Software

*   Processamento A-scan: A funcionalidade de processamento de A-scan (Hilbert Transform, gate de tempo) é básica e não totalmente implementada na versão atual.
*   Sem Visualização 3D: O aplicativo foca em mapas 2D (C-scan). Não há suporte para visualização de perfis de tensão em profundidade.
*   Interpolação: griddata é um método geral. Para dados muito esparsos ou com geometrias complexas, pode não ser ideal.
*   Interface: Embora funcional, a interface é baseada em Streamlit e pode não ter a mesma flexibilidade ou recursos de softwares de análise dedicados.

---

18. Contribuindo

Contribuições são bem-vindas! Se você tiver ideias para melhorias, detetar bugs ou quiser adicionar novas funcionalidades, sinta-se à vontade para:

1.  Abrir uma Issue: Para relatar bugs ou sugerir novas funcionalidades.
2.  Forkar o Repositório: Crie um fork do projeto.
3.  Criar uma Branch: Desenvolva suas alterações em uma nova branch (git checkout -b feature/sua-feature).
4.  Commitar suas Alterações: Faça commits claros e descritivos.
5.  Abrir um Pull Request: Envie um Pull Request para a branch main do projeto original.

---

19. Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE na raiz do repositório para mais detalhes.

---

20. Referências

Para aprofundar seus conhecimentos sobre o efeito acustoelástico e medição de tensões residuais via ultrassom:

*   Livros:
    *   "Nondestructive Evaluation: Theory, Techniques, and Applications" por Peter J. Shull.
    *   "Ultrasonic Nondestructive Testing" por J. Krautkrämer e H. Krautkrämer.
*   Artigos Científicos: Pesquise por termos como "acoustoelasticity", "ultrasonic stress measurement", "residual stress NDE".
*   Normas Técnicas:
    *   ASTM E2821: Standard Practice for Measurement of Residual Stress by the Acoustoelastic Method.

---

21. Contato e Suporte

Para dúvidas, sugestões ou suporte, por favor, utilize os seguintes canais:

*   GitHub Issues: [Link para as Issues do seu repositório GitHub]
*   Email: [Seu Email de Contato] (opcional)

---

22. Changelog

v1.0 (2023-10-27)

*   Lançamento inicial do Streamlit Residual Stress Analyzer.
*   Suporte para modos Longitudinal (TOF) e Cisalhante (birefringência).
*   Upload de dados CSV/Excel.
*   Correção térmica e definição de v_ref (manual ou por ROI).
*   Heatmaps, histogramas e estatísticas.
*   Exportação para PNG, CSV e relatório TXT/Markdown.
*   Geração de dados sintéticos para teste.
*   Documentação completa no README.md.
`