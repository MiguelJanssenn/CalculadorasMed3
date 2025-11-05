import streamlit as st
import pandas as pd
from prevent_calculator import PREVENTCalculator
from calculators.gastro import FIB4Calculator, MELDCalculator, ChildPughCalculator
from calculators.nephro import eGFRCalculator, KtVCalculator
from calculators.endocrino import BMICalculator, HOMAIRCalculator, HOMABetaCalculator

# Helper function to get optional PREVENT parameters
def get_prevent_optional_params(patient_data):
    """Get UACR and HbA1c values if checkboxes are checked and values are valid"""
    uacr_value = patient_data.get('uacr') if patient_data.get('use_uacr', False) and patient_data.get('uacr', 0) > 0 else None
    hba1c_value = patient_data.get('hba1c') if patient_data.get('use_hba1c', False) and patient_data.get('hba1c', 0) > 0 else None
    return uacr_value, hba1c_value

# Page configuration
st.set_page_config(
    page_title="Calculadoras Médicas",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dashboard design
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Calculator Card Styling */
    .calculator-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid #e1e8ed;
        transition: all 0.3s ease;
    }
    .calculator-card:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    .calc-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .calc-icon {
        font-size: 2rem;
        margin-right: 0.75rem;
    }
    
    .calc-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1a1a1a;
        margin: 0;
    }
    
    .calc-subtitle {
        font-size: 0.875rem;
        color: #666;
        margin: 0;
    }
    
    .result-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    /* Classification box inside cards */
    .classification-box {
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 8px;
        margin-top: 0.5rem;
        font-size: 0.875rem;
        border-left: 3px solid #667eea;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    .status-ready {
        background: #d4edda;
        color: #155724;
    }
    .status-missing {
        background: #fff3cd;
        color: #856404;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .risk-box {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        font-size: 1rem;
        font-weight: bold;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .risk-low {
        background: linear-gradient(135deg, #D4EDDA 0%, #a8e6cf 100%);
        color: #155724;
        border: 2px solid #C3E6CB;
    }
    .risk-borderline {
        background: linear-gradient(135deg, #FFF3CD 0%, #ffeaa7 100%);
        color: #856404;
        border: 2px solid #FFEEBA;
    }
    .risk-intermediate {
        background: linear-gradient(135deg, #FFE5CC 0%, #fdcb6e 100%);
        color: #CC5500;
        border: 2px solid #FFD4A3;
    }
    .risk-high {
        background: linear-gradient(135deg, #F8D7DA 0%, #fab1a0 100%);
        color: #721C24;
        border: 2px solid #F5C6CB;
    }
    .info-box {
        background: linear-gradient(135deg, #E7F3FF 0%, #a8daff 100%);
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #0066CC;
        margin: 1rem 0;
    }
    .data-saved {
        background: linear-gradient(135deg, #D4EDDA 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #28A745;
        margin: 1rem 0;
    }
    
    /* Dashboard Grid */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    /* Metric styling */
    .metric-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .auto-calc-badge {
        display: inline-block;
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    /* Fix metric font sizes to prevent overflow */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.75rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for patient data
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}

# Title
st.title("⚕️ Calculadoras Médicas")
st.markdown("### Plataforma Integrada de Scores e Calculadoras para Prática Médica")
st.markdown('<span class="auto-calc-badge">✨ Cálculo Automático Ativo</span>', unsafe_allow_html=True)

# Tabs for navigation
tabs = st.tabs([
    "📋 Dados do Paciente",
    "🏥 Todas as Calculadoras",
    "🫀 Cardiologia",
    "🍽️ Gastroenterologia",
    "💧 Nefrologia",
    "🩺 Endocrinologia"
])

# ========== TAB 1: PATIENT DATA ==========
with tabs[0]:
    st.header("📋 Dados do Paciente")
    st.markdown("""
    <div class="info-box">
    <strong>Central de Dados</strong><br>
    Preencha os dados do paciente aqui. Estes dados serão utilizados automaticamente 
    por todas as calculadoras disponíveis na plataforma.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # Helper function to create optional numeric inputs
    def optional_number_input(label, key, default_value="", help_text=None):
        """Create a text input that accepts numbers or empty values"""
        stored_value = st.session_state.patient_data.get(key, default_value)
        if stored_value == "" or stored_value is None:
            display_value = ""
        else:
            display_value = str(stored_value)
        
        value = st.text_input(label, value=display_value, help=help_text, key=f"input_{key}")
        
        if value == "":
            return None
        try:
            # Try to convert to float
            return float(value)
        except ValueError:
            st.error(f"'{label}' deve ser um número válido")
            return None
    
    with col1:
        st.subheader("Dados Demográficos")
        # Note: Campos agora podem ficar vazios
        age = optional_number_input("Idade (anos)", "age", help_text="Deixe vazio se não disponível")
        sex = st.selectbox("Sexo", ["Masculino", "Feminino"],
                          index=0 if st.session_state.patient_data.get('sex') == 'Masculino' else 1)
        weight = optional_number_input("Peso (kg)", "weight", help_text="Deixe vazio se não disponível")
        height = optional_number_input("Altura (cm)", "height", help_text="Deixe vazio se não disponível")
        
        st.subheader("História Clínica")
        diabetes = st.checkbox("Diabetes", value=st.session_state.patient_data.get('diabetes', False))
        smoker = st.checkbox("Fumante atual", value=st.session_state.patient_data.get('smoker', False))
        on_bp_meds = st.checkbox("Uso de anti-hipertensivos", 
                                value=st.session_state.patient_data.get('on_bp_meds', False))
        on_statins = st.checkbox("Uso de estatinas", 
                                value=st.session_state.patient_data.get('on_statins', False))
        dialysis = st.checkbox("Em diálise", value=st.session_state.patient_data.get('dialysis', False))
    
    with col2:
        st.subheader("Dados Vitais")
        sbp = optional_number_input("Pressão Arterial Sistólica (mmHg)", "sbp", help_text="Deixe vazio se não disponível")
        
        st.subheader("Lipidograma")
        total_chol = optional_number_input("Colesterol Total (mg/dL)", "total_chol", help_text="Deixe vazio se não disponível")
        hdl_chol = optional_number_input("HDL Colesterol (mg/dL)", "hdl_chol", help_text="Deixe vazio se não disponível")
        
        st.subheader("Função Renal")
        creatinine = optional_number_input("Creatinina sérica (mg/dL)", "creatinine", help_text="Deixe vazio se não disponível")
        egfr = optional_number_input("eTFG (mL/min/1.73m²)", "egfr", help_text="Deixe vazio se não disponível")
        uacr = optional_number_input("RACu - Relação Albumina/Creatinina Urinária (mg/g)", "uacr", help_text="Deixe vazio se não disponível")
        use_uacr = st.checkbox("Usar RACu no cálculo PREVENT", 
                              value=st.session_state.patient_data.get('use_uacr', False),
                              help="Marque para incluir RACu no cálculo do risco cardiovascular")
    
    with col3:
        st.subheader("Glicemia e Insulina")
        fasting_glucose = optional_number_input("Glicemia de jejum (mg/dL)", "fasting_glucose", help_text="Deixe vazio se não disponível")
        hba1c = optional_number_input("HbA1c (%)", "hba1c", help_text="Deixe vazio se não disponível")
        use_hba1c = st.checkbox("Usar HbA1c no cálculo PREVENT", 
                               value=st.session_state.patient_data.get('use_hba1c', False),
                               help="Marque para incluir HbA1c no cálculo do risco cardiovascular")
        fasting_insulin = optional_number_input("Insulina de jejum (μU/mL)", "fasting_insulin", help_text="Deixe vazio se não disponível")
        
        st.subheader("Função Hepática")
        ast = optional_number_input("AST (U/L)", "ast", help_text="Deixe vazio se não disponível")
        alt = optional_number_input("ALT (U/L)", "alt", help_text="Deixe vazio se não disponível")
        bilirubin = optional_number_input("Bilirrubina total (mg/dL)", "bilirubin", help_text="Deixe vazio se não disponível")
        albumin = optional_number_input("Albumina (g/dL)", "albumin", help_text="Deixe vazio se não disponível")
        inr = optional_number_input("INR", "inr", help_text="Deixe vazio se não disponível")
        platelets = optional_number_input("Plaquetas (×10⁹/L)", "platelets", help_text="Deixe vazio se não disponível")
    
    # Automatically save data to session state as user inputs
    st.session_state.patient_data = {
        'age': age,
        'sex': sex,
        'weight': weight,
        'height': height,
        'diabetes': diabetes,
        'smoker': smoker,
        'on_bp_meds': on_bp_meds,
        'on_statins': on_statins,
        'dialysis': dialysis,
        'sbp': sbp,
        'total_chol': total_chol,
        'hdl_chol': hdl_chol,
        'creatinine': creatinine,
        'egfr': egfr,
        'uacr': uacr,
        'use_uacr': use_uacr,
        'fasting_glucose': fasting_glucose,
        'hba1c': hba1c,
        'use_hba1c': use_hba1c,
        'fasting_insulin': fasting_insulin,
        'ast': ast,
        'alt': alt,
        'bilirubin': bilirubin,
        'albumin': albumin,
        'inr': inr,
        'platelets': platelets
    }
    
    st.markdown("---")
    st.markdown("""
    <div class="data-saved">
    ✅ <strong>Dados salvos automaticamente!</strong><br>
    Os dados do paciente são atualizados em tempo real e estão disponíveis para todas as calculadoras.
    </div>
    """, unsafe_allow_html=True)

# ========== TAB 2: ALL CALCULATORS DASHBOARD ==========
with tabs[1]:
    st.header("🏥 Dashboard - Todas as Calculadoras")
    st.markdown("**Resultados calculados automaticamente com base nos dados do paciente**")
    
    if not st.session_state.patient_data:
        st.warning("⚠️ Por favor, preencha os dados do paciente na aba 'Dados do Paciente' primeiro.")
    else:
        pd_data = st.session_state.patient_data
        
        # Helper function to check if required data is valid/realistic
        def has_valid_data(params_needed):
            """Check if the patient data has realistic values for required parameters"""
            for param in params_needed:
                val = pd_data.get(param)
                if isinstance(val, bool): continue
                if val is None or val <= 0: return False
            return True
        
        # Check calculator availability
        calc_availability = {
            'IMC': has_valid_data(['weight', 'height']),
            'HOMA-IR': has_valid_data(['fasting_glucose', 'fasting_insulin']),
            'HOMA-Beta': has_valid_data(['fasting_glucose', 'fasting_insulin']),
            'FIB-4': has_valid_data(['age', 'ast', 'alt', 'platelets']),
            'MELD': has_valid_data(['creatinine', 'bilirubin', 'inr']),
            'Child-Pugh': has_valid_data(['bilirubin', 'albumin', 'inr']),
            'eTFG': has_valid_data(['creatinine', 'age']),
            'Kt/V': has_valid_data(['weight']),
            'PREVENT': has_valid_data(['age', 'sbp', 'total_chol', 'hdl_chol', 'egfr', 'weight', 'height'])
        }
        
        # ... (O restante do arquivo não precisa de alteração, mas será incluído para completude) ...
        st.markdown("### 🫀 Cardiologia")
        # Check availability
        is_available = calc_availability.get('PREVENT', False)
        status_badge = '<span class="status-badge status-ready">✅ Pronto</span>' if is_available else '<span class="status-badge status-missing">⚠️ Faltam dados</span>'
        
        st.markdown(f"""
            <div class="calculator-card">
                <div class="calc-header">
                    <div class="calc-icon">❤️</div>
                    <div>
                        <div class="calc-title">PREVENT {status_badge}</div>
                        <div class="calc-subtitle">Risco Cardiovascular (AHA)</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if not is_available:
            st.warning(f"⚠️ **Dados faltantes para PREVENT.** Verifique idade, PA, colesterol, TFG, peso e altura.")
        else:
            try:
                sex_code = 'F' if pd_data['sex'] == "Feminino" else 'M'
                calculator = PREVENTCalculator()
                
                uacr_value, hba1c_value = get_prevent_optional_params(pd_data)
                
                results = calculator.calculate_risk_score(
                    age=pd_data['age'],
                    sex=sex_code,
                    total_cholesterol=pd_data['total_chol'],
                    hdl_cholesterol=pd_data['hdl_chol'],
                    sbp=pd_data['sbp'],
                    on_bp_meds=pd_data['on_bp_meds'],
                    diabetes=pd_data['diabetes'],
                    smoker=pd_data['smoker'],
                    egfr=pd_data['egfr'],
                    weight=pd_data['weight'],
                    height=pd_data['height'],
                    on_statins=pd_data['on_statins'],
                    uacr=uacr_value,
                    hba1c=hba1c_value
                )
                
                risk_category = results.get('risk_category', 'Indisponível')
                risk_class_map = {'Baixo': 'risk-low', 'Limítrofe': 'risk-borderline', 'Intermediário': 'risk-intermediate', 'Alto': 'risk-high'}
                st.markdown(f"""
                    <div class="risk-box {risk_class_map.get(risk_category, 'risk-intermediate')}">
                        Categoria de Risco Geral: {risk_category.upper()}
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("DCV Total 10a", f"{results['total_cvd_10yr']}%" if results['total_cvd_10yr'] != 'N/A' else 'N/A')
                with col2:
                    st.metric("DCVA 10a", f"{results['ascvd_10yr']}%" if results['ascvd_10yr'] != 'N/A' else 'N/A')
                with col3:
                    st.metric("IC 10a", f"{results['hf_10yr']}%" if results['hf_10yr'] != 'N/A' else 'N/A')
                
            except Exception as e:
                st.error(f"Erro ao calcular PREVENT: {str(e)}")

# ========== TAB 3: CARDIOLOGY ==========
with tabs[2]:
    st.header("🫀 Cardiologia")
    
    st.markdown("""
    <div class="info-box">
    <strong>PREVENT (Predicting Risk of cardiovascular disease EVENTs)</strong><br>
    Calculadora oficial da American Heart Association para estimativa de risco cardiovascular, implementada com as fórmulas originais validadas.
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.patient_data or not has_valid_data(['age', 'sbp', 'total_chol', 'hdl_chol', 'egfr', 'weight', 'height']):
        st.warning("⚠️ Por favor, preencha todos os dados necessários na aba 'Dados do Paciente' para calcular o risco PREVENT.")
    else:
        try:
            pd_data = st.session_state.patient_data
            sex_code = 'F' if pd_data['sex'] == "Feminino" else 'M'
            
            calculator = PREVENTCalculator()
            uacr_value, hba1c_value = get_prevent_optional_params(pd_data)
            
            results = calculator.calculate_risk_score(
                age=pd_data.get('age'),
                sex=sex_code,
                total_cholesterol=pd_data.get('total_chol'),
                hdl_cholesterol=pd_data.get('hdl_chol'),
                sbp=pd_data.get('sbp'),
                on_bp_meds=pd_data.get('on_bp_meds'),
                diabetes=pd_data.get('diabetes'),
                smoker=pd_data.get('smoker'),
                egfr=pd_data.get('egfr'),
                weight=pd_data.get('weight'),
                height=pd_data.get('height'),
                on_statins=pd_data.get('on_statins'),
                uacr=uacr_value,
                hba1c=hba1c_value
            )
            
            risk_category = results.get('risk_category', 'Indisponível')
            risk_class_map = {'Baixo': 'risk-low', 'Limítrofe': 'risk-borderline', 'Intermediário': 'risk-intermediate', 'Alto': 'risk-high'}
            st.markdown(f"""
                <div class="risk-box {risk_class_map.get(risk_category, 'risk-intermediate')}">
                    Categoria de Risco Geral: {risk_category.upper()}
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("DCV Total 10 anos", f"{results['total_cvd_10yr']}%" if results['total_cvd_10yr'] != 'N/A' else 'N/A')
            with col2:
                st.metric("DCVA 10 anos", f"{results['ascvd_10yr']}%" if results['ascvd_10yr'] != 'N/A' else 'N/A')
            with col3:
                st.metric("IC 10 anos", f"{results['hf_10yr']}%" if results['hf_10yr'] != 'N/A' else 'N/A')
                
        except Exception as e:
            st.error(f"Erro ao calcular: {str(e)}")

# ... (O restante das abas permanece o mesmo) ...
