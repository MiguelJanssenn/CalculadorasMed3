import streamlit as st
import pandas as pd
from prevent_calculator import PREVENTCalculator

# Page configuration
st.set_page_config(
    page_title="Calculadoras Médicas",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .risk-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .risk-low {
        background-color: #D4EDDA;
        color: #155724;
        border: 2px solid #C3E6CB;
    }
    .risk-borderline {
        background-color: #FFF3CD;
        color: #856404;
        border: 2px solid #FFEEBA;
    }
    .risk-intermediate {
        background-color: #FFE5CC;
        color: #CC5500;
        border: 2px solid #FFD4A3;
    }
    .risk-high {
        background-color: #F8D7DA;
        color: #721C24;
        border: 2px solid #F5C6CB;
    }
    .metric-card {
        background-color: #F0F2F6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    h1 {
        color: #FF4B4B;
    }
    h2 {
        color: #0E1117;
        border-bottom: 2px solid #FF4B4B;
        padding-bottom: 0.5rem;
    }
    .info-box {
        background-color: #E7F3FF;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0066CC;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("⚕️ Calculadoras Médicas")
st.markdown("### Plataforma de Scores e Calculadoras para Prática Médica")

# Sidebar for navigation
st.sidebar.title("📋 Menu")
calculator_choice = st.sidebar.selectbox(
    "Selecione a Calculadora:",
    ["PREVENT - Risco Cardiovascular (AHA)"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Sobre esta plataforma:**

Ferramenta desenvolvida para auxiliar profissionais de saúde na avaliação rápida e precisa de scores e calculadoras médicas durante o atendimento clínico.

**Uso:**
1. Selecione a calculadora desejada
2. Preencha os dados do paciente
3. Obtenha resultados instantâneos
4. Visualize recomendações clínicas
""")

# Main content based on selection
if calculator_choice == "PREVENT - Risco Cardiovascular (AHA)":
    st.header("🫀 Calculadora PREVENT")
    st.markdown("""
    <div class="info-box">
    <strong>PREVENT (Predicting Risk of cardiovascular disease EVENTs)</strong><br>
    Calculadora da American Heart Association para estimativa de risco cardiovascular em 10 e 30 anos.
    Útil para decisões sobre prevenção primária de doenças cardiovasculares.
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dados Demográficos")
        age = st.number_input("Idade (anos)", min_value=40, max_value=79, value=55, step=1)
        sex = st.selectbox("Sexo", ["Masculino", "Feminino"])
        race = st.selectbox("Raça/Etnia", [
            "Branco",
            "Negro",
            "Hispânico",
            "Asiático",
            "Outro"
        ])
        
        st.subheader("Fatores de Risco")
        diabetes = st.checkbox("Diabetes")
        smoker = st.checkbox("Fumante atual")
        on_bp_meds = st.checkbox("Em uso de anti-hipertensivos")
    
    with col2:
        st.subheader("Dados Laboratoriais")
        total_chol = st.number_input(
            "Colesterol Total (mg/dL)", 
            min_value=100, 
            max_value=400, 
            value=200,
            step=1
        )
        hdl_chol = st.number_input(
            "HDL Colesterol (mg/dL)", 
            min_value=20, 
            max_value=100, 
            value=50,
            step=1
        )
        sbp = st.number_input(
            "Pressão Arterial Sistólica (mmHg)", 
            min_value=90, 
            max_value=200, 
            value=120,
            step=1
        )
        
        egfr_check = st.checkbox("Incluir eGFR na avaliação")
        egfr = None
        if egfr_check:
            egfr = st.number_input(
                "eGFR (mL/min/1.73m²)", 
                min_value=15, 
                max_value=120, 
                value=90,
                step=1
            )
    
    # Calculate button
    st.markdown("---")
    if st.button("🔬 Calcular Risco Cardiovascular"):
        try:
            # Convert inputs
            sex_code = 'M' if sex == "Masculino" else 'F'
            race_map = {
                "Branco": "white",
                "Negro": "black",
                "Hispânico": "hispanic",
                "Asiático": "asian",
                "Outro": "other"
            }
            race_code = race_map[race]
            
            # Create calculator instance and calculate
            calculator = PREVENTCalculator()
            results = calculator.calculate_risk_score(
                age=age,
                sex=sex_code,
                race=race_code,
                total_cholesterol=total_chol,
                hdl_cholesterol=hdl_chol,
                sbp=sbp,
                on_bp_meds=on_bp_meds,
                diabetes=diabetes,
                smoker=smoker,
                egfr=egfr
            )
            
            # Display results
            st.markdown("---")
            st.subheader("📊 Resultados")
            
            # Create metrics in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Risco em 10 anos",
                    value=f"{results['10_year_risk']}%"
                )
            
            with col2:
                st.metric(
                    label="Risco em 30 anos",
                    value=f"{results['30_year_risk']}%"
                )
            
            with col3:
                st.metric(
                    label="Categoria de Risco",
                    value=results['risk_category']
                )
            
            # Risk visualization
            risk_category = results['risk_category']
            risk_class_map = {
                'Baixo': 'risk-low',
                'Limítrofe': 'risk-borderline',
                'Intermediário': 'risk-intermediate',
                'Alto': 'risk-high'
            }
            
            st.markdown(f"""
                <div class="risk-box {risk_class_map[risk_category]}">
                    Categoria de Risco: {risk_category.upper()}
                </div>
            """, unsafe_allow_html=True)
            
            # Recommendations
            st.markdown("---")
            st.subheader("💊 Recomendações Clínicas")
            
            recommendations = calculator.get_recommendations(
                risk_category, 
                results['10_year_risk']
            )
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"**{i}.** {rec}")
            
            # Additional information
            st.markdown("---")
            st.info("""
            **Nota Importante:**
            
            Esta calculadora é uma ferramenta de auxílio à decisão clínica e não substitui o julgamento médico. 
            Os resultados devem ser interpretados no contexto clínico completo do paciente. 
            
            Considere fatores adicionais como:
            - História familiar de doença cardiovascular precoce
            - Condições inflamatórias crônicas
            - Escore de cálcio coronário
            - Biomarcadores cardiovasculares (PCR-us, Lp(a))
            """)
            
        except ValueError as e:
            st.error(f"Erro ao calcular: {str(e)}")
        except Exception as e:
            st.error(f"Erro inesperado: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>Calculadoras Médicas - Plataforma de Apoio à Decisão Clínica</strong></p>
    <p>Desenvolvido para profissionais de saúde | Versão 1.0</p>
</div>
""", unsafe_allow_html=True)
