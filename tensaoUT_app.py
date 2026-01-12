"""
APLICATIVO STREAMLIT: ANÁLISE DE TENSÕES RESIDUAIS VIA ULTRASSOM
Baseado no Efeito Acustoelástico

Conceito: A velocidade de propagação de ondas ultrassônicas em sólidos varia
com o estado de tensão do material. Δv/v ∝ σ (proporcional à tensão residual).

IMPORTANTE: Este método fornece valores RELATIVOS. Calibração absoluta requer
técnicas complementares (difração de raios-X, furo incremental).
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import griddata
from scipy.signal import hilbert
from io import BytesIO
import base64

# Configuração da página
st.set_page_config(
    page_title="Análise de Tensões Residuais - Ultrassom",
    page_icon="🔊",
    layout="wide"
)

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

@st.cache_data
def gerar_dados_sinteticos(nx=50, ny=40, noise_level=0.02):
    """
    Gera dataset sintético com gradiente suave de índice de tensão
    Útil para testar a interface sem dados reais
    """
    x = np.linspace(0, 100, nx)  # mm
    y = np.linspace(0, 80, ny)   # mm
    X, Y = np.meshgrid(x, y)
    
    # Gradiente radial de tensão simulado
    center_x, center_y = 50, 40
    dist = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
    idx_base = 0.001 * (1 - dist / 60)  # Varia de ~0.001 a ~0
    
    # Adicionar ruído
    idx = idx_base + noise_level * np.random.randn(*idx_base.shape)
    
    # Converter para TOF (assumindo v_ref = 5900 m/s, espessura = 10 mm)
    v_ref = 5900
    d = 0.01  # 10 mm em metros
    v = v_ref * (1 + idx)
    tof_us = (2 * d / v) * 1e6  # TOF em microssegundos
    
    # Criar DataFrame
    df = pd.DataFrame({
        'x': X.flatten(),
        'y': Y.flatten(),
        'tof_us': tof_us.flatten(),
           'v1': (v * 0.5 + 50 * np.random.randn(*v.shape)).flatten(),  # Para modo cisalhante
           'v2': (v * 0.5 - 50 * np.random.randn(*v.shape)).flatten()
    })
    
    return df

def calcular_velocidade_longitudinal(tof_us, espessura_mm):
    """
    Converte TOF (tempo de voo) em velocidade ultrassônica
    v = 2*d / TOF
    
    Args:
        tof_us: tempo de voo em microssegundos
        espessura_mm: espessura da peça em milímetros
    
    Returns:
        velocidade em m/s
    """
    d_m = espessura_mm / 1000.0  # mm → m
    tof_s = tof_us / 1e6  # μs → s
    
    with np.errstate(divide='ignore', invalid='ignore'):
        v = (2 * d_m) / tof_s
        v[~np.isfinite(v)] = np.nan
    
    return v

def aplicar_correcao_termica(v, temp_medida, temp_ref, coef_termico):
    """
    Corrige variação de velocidade devido à temperatura
    v_corr = v + α * (T - T_ref)
    
    Args:
        v: velocidade medida (m/s)
        temp_medida: temperatura da medição (°C)
        temp_ref: temperatura de referência (°C)
        coef_termico: coeficiente α em (m/s)/°C
    
    Returns:
        velocidade corrigida
    """
    return v + coef_termico * (temp_medida - temp_ref)

def calcular_indice_tensao(v, v_ref):
    """
    Calcula índice relativo de tensão: (v - v_ref) / v_ref
    
    Este índice é proporcional à tensão residual pelo efeito acustoelástico:
    σ ≈ (Δv/v) / K, onde K é a constante acustoelástica do material
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        idx = (v - v_ref) / v_ref
        idx[~np.isfinite(idx)] = np.nan
    
    return idx

def calcular_birefringencia(v1, v2):
    """
    Calcula índice de birrefringência para ondas cisalhantes
    idx = (v1 - v2) / v_médio
    
    Sensível a tensões cisalhantes e principais
    """
    v_medio = (v1 + v2) / 2
    with np.errstate(divide='ignore', invalid='ignore'):
        idx = (v1 - v2) / v_medio
        idx[~np.isfinite(idx)] = np.nan
    
    return idx

def interpolar_grade(df, coluna_valor):
    """
    Interpola dados irregulares em grade regular para plotagem
    """
    x = df['x'].values
    y = df['y'].values
    z = df[coluna_valor].values
    
    # Remover NaNs
    mask = np.isfinite(z)
    x, y, z = x[mask], y[mask], z[mask]
    
    if len(x) < 3:
        return None, None, None, None
    
    # Criar grade regular
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
    
    nx = int((x_max - x_min) / st.session_state.get('passo_malha', 1.0)) + 1
    ny = int((y_max - y_min) / st.session_state.get('passo_malha', 1.0)) + 1
    
    xi = np.linspace(x_min, x_max, min(nx, 500))
    yi = np.linspace(y_min, y_max, min(ny, 500))
    Xi, Yi = np.meshgrid(xi, yi)
    
    # Interpolação
    Zi = griddata((x, y), z, (Xi, Yi), method='cubic', fill_value=np.nan)
    
    return Xi, Yi, Zi, (x_min, x_max, y_min, y_max)

def plotar_heatmap(Xi, Yi, Zi, titulo, colormap, vmin_percentil, vmax_percentil):
    """
    Cria heatmap profissional do índice de tensão
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Calcular limites de cor baseados em percentis
    z_flat = Zi[np.isfinite(Zi)]
    if len(z_flat) > 0:
        vmin = np.percentile(z_flat, vmin_percentil)
        vmax = np.percentile(z_flat, vmax_percentil)
    else:
        vmin, vmax = -0.001, 0.001
    
    # Plot
    im = ax.pcolormesh(Xi, Yi, Zi, cmap=colormap, shading='auto',
                       vmin=vmin, vmax=vmax)
    
    cbar = plt.colorbar(im, ax=ax, label='Índice de Tensão (Δv/v)')
    
    # Formatação
    ax.set_xlabel('Posição X (mm)', fontsize=12)
    ax.set_ylabel('Posição Y (mm)', fontsize=12)
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def criar_histograma(dados, titulo):
    """
    Cria histograma da distribuição do índice
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    
    dados_limpos = dados[np.isfinite(dados)]
    if len(dados_limpos) > 0:
        ax.hist(dados_limpos, bins=50, edgecolor='black', alpha=0.7)
        ax.axvline(np.mean(dados_limpos), color='red', linestyle='--', 
                   linewidth=2, label=f'Média: {np.mean(dados_limpos):.2e}')
        ax.axvline(np.median(dados_limpos), color='green', linestyle='--',
                   linewidth=2, label=f'Mediana: {np.median(dados_limpos):.2e}')
    
    ax.set_xlabel('Índice de Tensão (Δv/v)', fontsize=12)
    ax.set_ylabel('Frequência', fontsize=12)
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def gerar_relatorio(df_resultados, parametros):
    """
    Gera relatório em texto/markdown com sumário da análise
    """
    idx_col = 'indice_tensao'
    if idx_col not in df_resultados.columns:
        return "Erro: coluna de índice não encontrada"
    
    idx = df_resultados[idx_col].values
    idx_limpo = idx[np.isfinite(idx)]
    
    relatorio = f"""
# RELATÓRIO DE ANÁLISE DE TENSÕES RESIDUAIS - ULTRASSOM
**Data:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## PARÂMETROS DA ANÁLISE

- **Modo de medição:** {parametros.get('modo', 'N/A')}
- **Espessura da peça:** {parametros.get('espessura_mm', 'N/A')} mm
- **Velocidade de referência:** {parametros.get('v_ref', 'N/A')} m/s
- **Correção térmica:** {parametros.get('correcao_termica', 'Não aplicada')}
- **Constante acustoelástica K:** {parametros.get('K', 'Não informada')}
- **Colormap:** {parametros.get('colormap', 'viridis')}
- **Total de pontos:** {len(df_resultados)}

---

## ESTATÍSTICAS DO ÍNDICE DE TENSÃO (Δv/v)

- **Média:** {np.mean(idx_limpo):.6e}
- **Desvio padrão:** {np.std(idx_limpo):.6e}
- **Mediana:** {np.median(idx_limpo):.6e}
- **Mínimo:** {np.min(idx_limpo):.6e}
- **Máximo:** {np.max(idx_limpo):.6e}
- **Percentil 5%:** {np.percentile(idx_limpo, 5):.6e}
- **Percentil 95%:** {np.percentile(idx_limpo, 95):.6e}

---

## ESTIMATIVA SEMI-QUANTITATIVA DE TENSÃO
"""
    
    if parametros.get('K') and parametros['K'] > 0:
        K = parametros['K']
        sigma_media = np.mean(idx_limpo) / K
        sigma_std = np.std(idx_limpo) / K
        relatorio += f"""
**Utilizando σ ≈ (Δv/v) / K:**

- **Tensão média estimada:** {sigma_media:.2f} MPa
- **Variação (±1σ):** ±{sigma_std:.2f} MPa

⚠️ **ATENÇÃO:** Esta é uma estimativa QUALITATIVA. A conversão exata requer:
1. Calibração experimental da constante K para o material específico
2. Validação com técnicas absolutas (difração de raios-X, furo incremental)
3. Consideração do estado multiaxial de tensões
"""
    else:
        relatorio += """
⚠️ **Constante K não fornecida.** Resultados permanecem em unidades relativas (Δv/v).
Para conversão em MPa, determine K experimentalmente para seu material.
"""
    
    relatorio += f"""
---

## NOTAS E LIMITAÇÕES

1. **Método relativo:** O efeito acustoelástico fornece variações relativas de tensão.
   Tensões absolutas requerem estado de referência conhecido (livre de tensões).

2. **Influência da microestrutura:** Textura cristalográfica, tamanho de grão e fases
   metalúrgicas afetam a velocidade ultrassônica independentemente da tensão.

3. **Temperatura:** Correções térmicas são lineares apenas em pequenos intervalos.
   Variações significativas de temperatura exigem caracterização mais detalhada.

4. **Profundidade de análise:** Ondas longitudinais sampleiam toda a espessura.
   Para tensões superficiais, considere ondas de superfície (Rayleigh).

5. **Calibração:** Sempre que possível, valide resultados com técnica independente
   em pontos selecionados (ex: difração de raios-X).

---

**Software:** Streamlit Residual Stress Analyzer v1.0
**Método:** Análise acustoelástica de velocidade ultrassônica
"""
    
    return relatorio

# ============================================================================
# INTERFACE STREAMLIT
# ============================================================================

st.title("🔊 Análise de Tensões Residuais via Ultrassom")
st.markdown("*Baseado no Efeito Acustoelástico*")

st.info("""
**Conceito:** A velocidade de ondas ultrassônicas varia com o estado de tensão do material.
Este app calcula o índice relativo **Δv/v** proporcional à tensão residual.

⚠️ **Resultados são RELATIVOS** - Calibração absoluta requer técnicas complementares (XRD, furo incremental).
""")

# ============================================================================
# SIDEBAR - PARÂMETROS
# ============================================================================

st.sidebar.header("⚙️ Parâmetros de Análise")

# Modo de medição
modo = st.sidebar.selectbox(
    "Modo de medição",
    ["Longitudinal (TOF)", "Cisalhante (birefringência)"],
    help="Longitudinal: mede tempo de voo (TOF) de ondas longitudinais. Cisalhante: mede diferença de velocidade entre polarizações."
)

# Espessura
espessura_mm = st.sidebar.number_input(
    "Espessura do componente (mm)",
    min_value=0.1,
    max_value=500.0,
    value=10.0,
    step=0.1,
    help="Espessura da peça na direção de propagação da onda"
)

# Velocidade de referência
st.sidebar.subheader("Velocidade de Referência")
metodo_ref = st.sidebar.radio(
    "Método de definição",
    ["Valor numérico", "ROI (região de interesse)"],
    help="Defina v_ref manualmente ou selecione região nos dados"
)

if metodo_ref == "Valor numérico":
    v_ref_manual = st.sidebar.number_input(
        "v_ref (m/s)",
        min_value=1000.0,
        max_value=10000.0,
        value=5900.0,
        step=10.0,
        help="Velocidade em região livre de tensões ou referência conhecida"
    )
else:
    st.sidebar.markdown("*ROI será definido após carregar dados*")
    v_ref_manual = None

# Constante acustoelástica
st.sidebar.subheader("Constante Acustoelástica (Opcional)")
usar_K = st.sidebar.checkbox("Fornecer constante K para estimativa quantitativa")
if usar_K:
    K_val = st.sidebar.number_input(
        "Constante K",
        min_value=0.0,
        max_value=1.0,
        value=0.00001,
        format="%.8f",
        help="σ (MPa) ≈ (Δv/v) / K. Valor típico: 1e-5 a 1e-4 para aços"
    )
else:
    K_val = None

# Correção térmica
st.sidebar.subheader("Correção Térmica (Opcional)")
usar_temp = st.sidebar.checkbox("Aplicar correção de temperatura")
if usar_temp:
    coef_termico = st.sidebar.number_input(
        "Coeficiente térmico ((m/s)/°C)",
        value=-0.9,
        step=0.1,
        format="%.2f",
        help="Típico para aço: -0.9 m/s/°C"
    )
    temp_ref = st.sidebar.number_input("Temperatura de referência (°C)", value=20.0, step=1.0)
    temp_medida = st.sidebar.number_input("Temperatura da medição (°C)", value=20.0, step=1.0)
else:
    coef_termico = 0.0
    temp_ref = 20.0
    temp_medida = 20.0

# Visualização
st.sidebar.subheader("Visualização")
passo_malha = st.sidebar.number_input(
    "Passo da malha (mm)",
    min_value=0.1,
    max_value=10.0,
    value=1.0,
    step=0.1,
    help="Resolução da interpolação para heatmap"
)
st.session_state['passo_malha'] = passo_malha

colormap = st.sidebar.selectbox(
    "Colormap",
    ["viridis", "coolwarm", "inferno", "plasma", "seismic", "RdBu_r"],
    help="Esquema de cores do mapa de calor"
)

vmin_percentil = st.sidebar.slider("Percentil mínimo colormap", 0, 50, 1)
vmax_percentil = st.sidebar.slider("Percentil máximo colormap", 50, 100, 99)

# ============================================================================
# ÁREA PRINCIPAL - UPLOAD E PROCESSAMENTO
# ============================================================================


st.header("📂 Carregamento de Dados")

# Adiciona uma aba para o README
tab1, tab2, tab3 = st.tabs(["Upload de Arquivo", "Dados Sintéticos de Teste", "README"])

with tab1:
    st.markdown("""
    **Formato esperado (CSV ou Excel):**
    - Modo Longitudinal: colunas `x`, `y`, `tof_us` (tempo de voo em microssegundos)
    - Modo Cisalhante: colunas `x`, `y`, `v1`, `v2` (velocidades em m/s)
    - Coordenadas x, y em milímetros
    """)
    
    uploaded_file = st.file_uploader(
        "Selecione arquivo CSV ou Excel",
        type=['csv', 'xlsx', 'xls'],
        help="Arquivo com dados de varredura ultrassônica"
    )
    
    df_original = None
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_original = pd.read_csv(uploaded_file)
            else:
                df_original = pd.read_excel(uploaded_file)
            
            st.success(f"✅ Arquivo carregado: {len(df_original)} pontos")
            st.dataframe(df_original.head(10), use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao carregar arquivo: {str(e)}")

with tab2:
    st.markdown("**Gerar dataset sintético para testar a interface**")

with tab3:
    try:
        with open("readme.md", encoding="utf-8") as f:
            readme_content = f.read()
        st.markdown(readme_content, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Não foi possível carregar o README: {e}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        nx_sint = st.number_input("Pontos em X", 20, 100, 50)
    with col2:
        ny_sint = st.number_input("Pontos em Y", 20, 100, 40)
    with col3:
        noise = st.slider("Nível de ruído", 0.0, 0.1, 0.02, 0.01)
    
    if st.button("🎲 Gerar Dados Sintéticos"):
        df_original = gerar_dados_sinteticos(nx_sint, ny_sint, noise)
        st.success(f"✅ Dataset sintético gerado: {len(df_original)} pontos")
        st.dataframe(df_original.head(10), use_container_width=True)
        
        # Botão de download
        csv = df_original.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Baixar CSV de Exemplo",
            csv,
            "dados_sinteticos.csv",
            "text/csv"
        )

# ============================================================================
# PROCESSAMENTO E VISUALIZAÇÃO
# ============================================================================

if df_original is not None and len(df_original) > 0:
    
    st.header("🔬 Processamento e Análise")
    
    # Verificar colunas necessárias
    colunas_obrigatorias = ['x', 'y']
    if modo == "Longitudinal (TOF)":
        colunas_obrigatorias.append('tof_us')
    else:
        colunas_obrigatorias.extend(['v1', 'v2'])
    
    colunas_faltantes = set(colunas_obrigatorias) - set(df_original.columns)
    
    if colunas_faltantes:
        st.error(f"❌ Colunas faltantes no arquivo: {colunas_faltantes}")
        st.stop()
    
    # Criar cópia para processamento
    df = df_original.copy()
    
    # ========================================================================
    # PROCESSAMENTO ESPECÍFICO POR MODO
    # ========================================================================
    
    if modo == "Longitudinal (TOF)":
        st.subheader("Modo Longitudinal - Análise de TOF")
        
        # Calcular velocidade
        with st.spinner("Calculando velocidades..."):
            df['velocidade'] = calcular_velocidade_longitudinal(
                df['tof_us'].values,
                espessura_mm
            )
        
        # Correção térmica
        if usar_temp and abs(temp_medida - temp_ref) > 0.1:
            df['velocidade'] = aplicar_correcao_termica(
                df['velocidade'].values,
                temp_medida,
                temp_ref,
                coef_termico
            )
            st.info(f"✓ Correção térmica aplicada: ΔT = {temp_medida - temp_ref:.1f}°C")
        
        # Definir v_ref
        if metodo_ref == "ROI (região de interesse)":
            st.subheader("🎯 Seleção de Região de Referência (ROI)")
            
            col1, col2 = st.columns(2)
            with col1:
                x_min_roi = st.slider("X mínimo (mm)", 
                                      float(df['x'].min()), 
                                      float(df['x'].max()), 
                                      float(df['x'].min()))
                x_max_roi = st.slider("X máximo (mm)", 
                                      float(df['x'].min()), 
                                      float(df['x'].max()), 
                                      float(df['x'].max()))
            with col2:
                y_min_roi = st.slider("Y mínimo (mm)", 
                                      float(df['y'].min()), 
                                      float(df['y'].max()), 
                                      float(df['y'].min()))
                y_max_roi = st.slider("Y máximo (mm)", 
                                      float(df['y'].min()), 
                                      float(df['y'].max()), 
                                      float(df['y'].max()))
            
            # Filtrar ROI
            mask_roi = (
                (df['x'] >= x_min_roi) & (df['x'] <= x_max_roi) &
                (df['y'] >= y_min_roi) & (df['y'] <= y_max_roi)
            )
            df_roi = df[mask_roi]
            
            if len(df_roi) > 0:
                v_ref = np.nanmean(df_roi['velocidade'])
                st.success(f"✓ v_ref calculado do ROI: {v_ref:.2f} m/s ({len(df_roi)} pontos)")
            else:
                st.warning("⚠️ ROI vazio, usando valor padrão")
                v_ref = 5900.0
        else:
            v_ref = v_ref_manual
            st.info(f"✓ v_ref definido manualmente: {v_ref:.2f} m/s")
        
        # Calcular índice de tensão
        df['indice_tensao'] = calcular_indice_tensao(df['velocidade'].values, v_ref)
        
    else:  # Modo Cisalhante
        st.subheader("Modo Cisalhante - Análise de Birefringência")
        
        # Calcular birefringência
        with st.spinner("Calculando birefringência..."):
            df['indice_tensao'] = calcular_birefringencia(
                df['v1'].values,
                df['v2'].values
            )
        
        v_ref = np.nanmean((df['v1'] + df['v2']) / 2)
        st.info(f"✓ Velocidade média cisalhante: {v_ref:.2f} m/s")
    
    # ========================================================================
    # VISUALIZAÇÕES
    # ========================================================================
    
    st.header("📊 Visualizações")
    
    # Estatísticas
    idx_clean = df['indice_tensao'].values
    idx_clean = idx_clean[np.isfinite(idx_clean)]
    
    if len(idx_clean) > 0:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Média (Δv/v)", f"{np.mean(idx_clean):.2e}")
        with col2:
            st.metric("Desvio Padrão", f"{np.std(idx_clean):.2e}")
        with col3:
            st.metric("Mínimo", f"{np.min(idx_clean):.2e}")
        with col4:
            st.metric("Máximo", f"{np.max(idx_clean):.2e}")
        
        if usar_K and K_val:
            st.info(f"""
            **Estimativa de tensão (σ ≈ Δv/v / K):**
            - Média: **{np.mean(idx_clean)/K_val:.2f} MPa**
            - Variação: ±{np.std(idx_clean)/K_val:.2f} MPa
            
            ⚠️ Valores qualitativos - requerem calibração experimental
            """)
    
    # Heatmap
    st.subheader("🌡️ Mapa de Calor do Índice de Tensão")
    
    with st.spinner("Interpolando dados e gerando mapa..."):
        Xi, Yi, Zi, limites = interpolar_grade(df, 'indice_tensao')
        
        if Xi is not None:
            fig_heatmap = plotar_heatmap(
                Xi, Yi, Zi,
                f"Índice de Tensão Residual - {modo}",
                colormap,
                vmin_percentil,
                vmax_percentil
            )
            st.pyplot(fig_heatmap)
        else:
            st.error("Não foi possível interpolar os dados. Verifique qualidade dos dados.")
    
    # Histograma
    st.subheader("📈 Distribuição do Índice")
    
    fig_hist = criar_histograma(
        df['indice_tensao'].values,
        "Distribuição do Índice de Tensão (Δv/v)"
    )
    st.pyplot(fig_hist)
    
    # ========================================================================
    # EXPORTAÇÕES
    # ========================================================================
    
    st.header("💾 Exportar Resultados")
    
    col1, col2, col3 = st.columns(3)
    
    # Exportar PNG do Heatmap
    with col1:
        if Xi is not None:
            buf_png = BytesIO()
            fig_heatmap.savefig(buf_png, format='png', dpi=300, bbox_inches='tight')
            buf_png.seek(0)
            
            st.download_button(
                label="📷 Baixar Heatmap (PNG)",
                data=buf_png,
                file_name="heatmap_tensao_residual.png",
                mime="image/png"
            )
    
    # Exportar CSV
    with col2:
        csv_export = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Baixar Dados (CSV)",
            data=csv_export,
            file_name="resultados_tensao_residual.csv",
            mime="text/csv"
        )
    
    # Exportar Relatório
    with col3:
        parametros_relatorio = {
            'modo': modo,
            'espessura_mm': espessura_mm,
            'v_ref': v_ref,
            'correcao_termica': f"{coef_termico:.2f} (m/s)/°C" if usar_temp else "Não aplicada",
            'K': K_val,
            'colormap': colormap
        }
        
        relatorio_texto = gerar_relatorio(df, parametros_relatorio)
        
        st.download_button(
            label="📄 Baixar Relatório (TXT)",
            data=relatorio_texto.encode('utf-8'),
            file_name="relatorio_tensao_residual.txt",
            mime="text/plain"
        )
    
    # Mostrar preview do relatório
    with st.expander("👁️ Visualizar Relatório"):
        st.markdown(relatorio_texto)

else:
    st.warning("⬆️ Carregue um arquivo de dados ou gere dados sintéticos para começar a análise")

# ========================================================================
# RODAPÉ
# ========================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    <p><strong>Streamlit Residual Stress Analyzer v1.0</strong></p>
    <p>Baseado no efeito acustoelástico | Desenvolvido com Python & Streamlit</p>
    <p>⚠️ Ferramenta para análise qualitativa - Sempre valide resultados com técnicas complementares</p>
</div>
""", unsafe_allow_html=True)