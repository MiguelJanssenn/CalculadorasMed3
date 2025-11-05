import streamlit as st
import pandas as pd
from prevent_calculator import PREVENTCalculator
from calculators.gastro import FIB4Calculator, MELDCalculator, ChildPughCalculator
from calculators.nephro import eGFRCalculator, KtVCalculator
from calculators.endocrino import BMICalculator, HOMAIRCalculator, HOMABetaCalculator

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
        pd = st.session_state.patient_data
        
        # Helper function to check if required data is valid/realistic
        def has_valid_data(params_needed):
            """Check if the patient data has realistic values for required parameters"""
            for param, min_val in params_needed.items():
                val = pd.get(param)
                if isinstance(val, bool):
                    continue  # Booleans are always valid
                if val is None or val <= min_val:
                    return False, param
            return True, None
        
        # Helper function to get missing parameters message
        def get_missing_params_msg(params_needed):
            """Generate message for missing parameters"""
            missing = []
            param_labels = {
                'age': 'Idade', 'weight': 'Peso', 'height': 'Altura',
                'sbp': 'Pressão Arterial', 'total_chol': 'Colesterol Total',
                'hdl_chol': 'HDL Colesterol', 'creatinine': 'Creatinina',
                'egfr': 'eTFG', 'fasting_glucose': 'Glicemia de jejum',
                'fasting_insulin': 'Insulina de jejum', 'ast': 'AST',
                'alt': 'ALT', 'platelets': 'Plaquetas', 'bilirubin': 'Bilirrubina',
                'albumin': 'Albumina', 'inr': 'INR', 'hba1c': 'HbA1c'
            }
            for param, min_val in params_needed.items():
                val = pd.get(param)
                if isinstance(val, bool):
                    continue
                if val is None or val <= min_val:
                    missing.append(param_labels.get(param, param))
            return missing
        
        # Check calculator availability
        calc_availability = {
            'IMC': has_valid_data({'weight': 1.0, 'height': 50.0})[0],
            'HOMA-IR': has_valid_data({'fasting_glucose': 30, 'fasting_insulin': 0.1})[0],
            'HOMA-Beta': has_valid_data({'fasting_glucose': 30, 'fasting_insulin': 0.1})[0],
            'FIB-4': has_valid_data({'age': 1, 'ast': 1, 'alt': 1, 'platelets': 1})[0],
            'MELD': has_valid_data({'creatinine': 0.1, 'bilirubin': 0.1, 'inr': 0.8})[0],
            'Child-Pugh': has_valid_data({'bilirubin': 0.1, 'albumin': 1.0, 'inr': 0.8})[0],
            'eTFG': has_valid_data({'creatinine': 0.1, 'age': 1})[0],
            'Kt/V': has_valid_data({'weight': 1.0})[0],
            'PREVENT': has_valid_data({'age': 1, 'sbp': 70, 'total_chol': 50, 'hdl_chol': 10, 'egfr': 5})[0]
        }
        
        # Display availability summary
        ready_count = sum(calc_availability.values())
        total_count = len(calc_availability)
        
        st.markdown(f"""
        <div class="info-box">
        <strong>Status das Calculadoras:</strong> {ready_count} de {total_count} calculadoras podem ser executadas com os dados atuais<br>
        ✅ <strong>Prontas:</strong> {', '.join([k for k, v in calc_availability.items() if v])}<br>
        ⚠️ <strong>Faltam dados:</strong> {', '.join([k for k, v in calc_availability.items() if not v])}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ===== ENDOCRINOLOGY SECTION =====
        st.markdown("### 🩺 Endocrinologia")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Check availability
            is_available = calc_availability.get('IMC', False)
            status_badge = '<span class="status-badge status-ready">✅ Pronto</span>' if is_available else '<span class="status-badge status-missing">⚠️ Falta dados</span>'
            
            st.markdown(f"""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">📊</div>
                        <div>
                            <div class="calc-title">IMC {status_badge}</div>
                            <div class="calc-subtitle">Índice de Massa Corporal</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Check if data is valid
            is_valid, missing_param = has_valid_data({'weight': 1.0, 'height': 50.0})
            
            if not is_valid:
                missing = get_missing_params_msg({'weight': 1.0, 'height': 50.0})
                st.warning(f"⚠️ **Dados faltantes:** {', '.join(missing)}")
            else:
                try:
                    calculator = BMICalculator()
                    result = calculator.calculate(weight=pd['weight'], height=pd['height'])
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("IMC", result['bmi'])
                    with col_b:
                        st.metric("Classificação", result['classification'])
                    st.markdown(f"""
                        <div class="classification-box">
                            <strong>Risco:</strong> {result['risk']}
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        
        with col2:
            # Check availability
            is_available = calc_availability.get('HOMA-IR', False)
            status_badge = '<span class="status-badge status-ready">✅ Pronto</span>' if is_available else '<span class="status-badge status-missing">⚠️ Falta dados</span>'
            
            st.markdown(f"""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">🔬</div>
                        <div>
                            <div class="calc-title">HOMA-IR {status_badge}</div>
                            <div class="calc-subtitle">Resistência Insulínica</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Check if data is valid
            is_valid, missing_param = has_valid_data({'fasting_glucose': 30, 'fasting_insulin': 0.1})
            
            if not is_valid:
                missing = get_missing_params_msg({'fasting_glucose': 30, 'fasting_insulin': 0.1})
                st.warning(f"⚠️ **Dados faltantes:** {', '.join(missing)}")
            else:
                try:
                    calculator = HOMAIRCalculator()
                    result = calculator.calculate(
                        fasting_glucose=pd['fasting_glucose'],
                        fasting_insulin=pd['fasting_insulin']
                    )
                    st.metric("HOMA-IR", result['homa_ir'])
                    st.markdown(f"""
                        <div class="classification-box">
                            {result['interpretation']}
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        
        with col3:
            # Check availability
            is_available = calc_availability.get('HOMA-Beta', False)
            status_badge = '<span class="status-badge status-ready">✅ Pronto</span>' if is_available else '<span class="status-badge status-missing">⚠️ Falta dados</span>'
            
            st.markdown(f"""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">🧬</div>
                        <div>
                            <div class="calc-title">HOMA-Beta {status_badge}</div>
                            <div class="calc-subtitle">Função Beta Células</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Check if data is valid
            is_valid, missing_param = has_valid_data({'fasting_glucose': 30, 'fasting_insulin': 0.1})
            
            if not is_valid:
                missing = get_missing_params_msg({'fasting_glucose': 30, 'fasting_insulin': 0.1})
                st.warning(f"⚠️ **Dados faltantes:** {', '.join(missing)}")
            else:
                try:
                    calculator = HOMABetaCalculator()
                    result = calculator.calculate(
                        fasting_glucose=pd['fasting_glucose'],
                        fasting_insulin=pd['fasting_insulin']
                    )
                    st.metric("HOMA-Beta", f"{result['homa_beta']}%")
                    st.markdown(f"""
                        <div class="classification-box">
                            {result['interpretation']}
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        
        # ===== GASTROENTEROLOGY SECTION =====
        st.markdown("---")
        st.markdown("### 🍽️ Gastroenterologia")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Check availability
            is_available = calc_availability.get('FIB-4', False)
            status_badge = '<span class="status-badge status-ready">✅ Pronto</span>' if is_available else '<span class="status-badge status-missing">⚠️ Falta dados</span>'
            
            st.markdown(f"""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">🔍</div>
                        <div>
                            <div class="calc-title">FIB-4 {status_badge}</div>
                            <div class="calc-subtitle">Fibrose Hepática</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Check if data is valid
            is_valid, missing_param = has_valid_data({'age': 1, 'ast': 1, 'alt': 1, 'platelets': 1})
            
            if not is_valid:
                missing = get_missing_params_msg({'age': 1, 'ast': 1, 'alt': 1, 'platelets': 1})
                st.warning(f"⚠️ **Dados faltantes:** {', '.join(missing)}")
            else:
                try:
                    calculator = FIB4Calculator()
                    result = calculator.calculate(
                        age=pd['age'],
                        ast=pd['ast'],
                        alt=pd['alt'],
                        platelets=pd['platelets']
                    )
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Score FIB-4", result['score'])
                    with col_b:
                        st.metric("Risco", result['risk'])
                    st.markdown(f"""
                        <div class="classification-box">
                            {result['interpretation']}
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        
        with col2:
            # Check availability
            is_available = calc_availability.get('MELD', False)
            status_badge = '<span class="status-badge status-ready">✅ Pronto</span>' if is_available else '<span class="status-badge status-missing">⚠️ Falta dados</span>'
            
            st.markdown(f"""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">⚕️</div>
                        <div>
                            <div class="calc-title">MELD {status_badge}</div>
                            <div class="calc-subtitle">Gravidade Hepática</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Check if data is valid
            is_valid, missing_param = has_valid_data({'creatinine': 0.1, 'bilirubin': 0.1, 'inr': 0.8})
            
            if not is_valid:
                missing = get_missing_params_msg({'creatinine': 0.1, 'bilirubin': 0.1, 'inr': 0.8})
                st.warning(f"⚠️ **Dados faltantes:** {', '.join(missing)}")
            else:
                try:
                    calculator = MELDCalculator()
                    result = calculator.calculate(
                        creatinine=pd['creatinine'],
                        bilirubin=pd['bilirubin'],
                        inr=pd['inr'],
                        dialysis=pd['dialysis']
                    )
                    st.metric("Score MELD", result['score'])
                    st.markdown(f"""
                        <div class="classification-box">
                            {result['interpretation']}<br>
                            <strong>Mortalidade:</strong> {result['mortality']}
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        
        with col3:
            # Check availability
            is_available = calc_availability.get('Child-Pugh', False)
            status_badge = '<span class="status-badge status-ready">✅ Pronto</span>' if is_available else '<span class="status-badge status-missing">⚠️ Falta dados</span>'
            
            st.markdown(f"""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">🏥</div>
                        <div>
                            <div class="calc-title">Child-Pugh {status_badge}</div>
                            <div class="calc-subtitle">Classificação de Cirrose</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Child-Pugh requires additional inputs
            ascites = st.selectbox("Ascite", ["Ausente", "Leve", "Moderada/Grave"], key="cp_ascites")
            encephalopathy = st.selectbox("Encefalopatia", ["Ausente", "Grau 1-2", "Grau 3-4"], key="cp_enceph")
            
            # Check if data is valid
            is_valid, missing_param = has_valid_data({'bilirubin': 0.1, 'albumin': 1.0, 'inr': 0.8})
            
            if not is_valid:
                missing = get_missing_params_msg({'bilirubin': 0.1, 'albumin': 1.0, 'inr': 0.8})
                st.warning(f"⚠️ **Dados faltantes:** {', '.join(missing)}")
            else:
                try:
                    ascites_map = {"Ausente": "none", "Leve": "mild", "Moderada/Grave": "moderate_severe"}
                    enceph_map = {"Ausente": "none", "Grau 1-2": "grade_1_2", "Grau 3-4": "grade_3_4"}
                    
                    calculator = ChildPughCalculator()
                    result = calculator.calculate(
                        bilirubin=pd['bilirubin'],
                        albumin=pd['albumin'],
                        inr=pd['inr'],
                        ascites=ascites_map[ascites],
                        encephalopathy=enceph_map[encephalopathy]
                    )
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Score", result['score'])
                    with col_b:
                        st.metric("Classe", result['class'])
                    st.markdown(f"""
                        <div class="classification-box">
                            {result['interpretation']}
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        
        # ===== NEPHROLOGY SECTION =====
        st.markdown("---")
        st.markdown("### 💧 Nefrologia")
        col1, col2 = st.columns(2)
        
        with col1:
            # Check availability
            is_available = calc_availability.get('eTFG', False)
            status_badge = '<span class="status-badge status-ready">✅ Pronto</span>' if is_available else '<span class="status-badge status-missing">⚠️ Falta dados</span>'
            
            st.markdown(f"""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">🫘</div>
                        <div>
                            <div class="calc-title">eTFG {status_badge}</div>
                            <div class="calc-subtitle">Taxa de Filtração Glomerular</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Check if data is valid
            is_valid, missing_param = has_valid_data({'creatinine': 0.1, 'age': 1})
            
            if not is_valid:
                missing = get_missing_params_msg({'creatinine': 0.1, 'age': 1})
                st.warning(f"⚠️ **Dados faltantes:** {', '.join(missing)}")
            else:
                try:
                    sex_code = 'M' if pd['sex'] == "Masculino" else 'F'
                    calculator = eGFRCalculator()
                    result = calculator.calculate(
                        creatinine=pd['creatinine'],
                        age=pd['age'],
                        sex=sex_code
                    )
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("eTFG", f"{result['egfr']} mL/min/1.73m²")
                    with col_b:
                        st.metric("Estágio DRC", result['stage'])
                    st.markdown(f"""
                        <div class="classification-box">
                            {result['description']}
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        
        with col2:
            # Check availability
            is_available = calc_availability.get('Kt/V', False)
            status_badge = '<span class="status-badge status-ready">✅ Pronto</span>' if is_available else '<span class="status-badge status-missing">⚠️ Falta dados</span>'
            
            st.markdown(f"""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">💉</div>
                        <div>
                            <div class="calc-title">Kt/V {status_badge}</div>
                            <div class="calc-subtitle">Adequação da Diálise</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Kt/V requires additional dialysis-specific inputs
            # Only show if patient is on dialysis
            if not pd.get('dialysis', False):
                st.info("ℹ️ **Kt/V** é aplicável apenas para pacientes em diálise. Marque 'Em diálise' na aba de Dados do Paciente.")
            else:
                col_a, col_b = st.columns(2)
                with col_a:
                    pre_bun = st.number_input("BUN pré-diálise (mg/dL)", min_value=1, max_value=300, value=60, step=1, key="ktv_pre")
                    post_bun = st.number_input("BUN pós-diálise (mg/dL)", min_value=1, max_value=200, value=20, step=1, key="ktv_post")
                with col_b:
                    dialysis_time = st.number_input("Tempo de diálise (horas)", min_value=0.5, max_value=10.0, value=4.0, step=0.5, key="ktv_time")
                    ultrafiltration = st.number_input("Ultrafiltração (L)", min_value=0.0, max_value=10.0, value=2.0, step=0.1, key="ktv_uf")
                
                # Check if weight is valid
                is_valid, missing_param = has_valid_data({'weight': 1.0})
                
                if not is_valid:
                    st.warning(f"⚠️ **Dados faltantes:** Peso")
                else:
                    try:
                        calculator = KtVCalculator()
                        result = calculator.calculate(
                            pre_bun=pre_bun,
                            post_bun=post_bun,
                            dialysis_time=dialysis_time,
                            ultrafiltration=ultrafiltration,
                            post_weight=pd['weight']
                        )
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Kt/V", result['ktv'])
                        with col_b:
                            st.metric("Adequação", result['adequacy'])
                        st.markdown(f"""
                            <div class="classification-box">
                                <strong>Recomendação:</strong> {result['recommendation']}
                            </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")
        
        # ===== CARDIOLOGY SECTION =====
        st.markdown("---")
        st.markdown("### 🫀 Cardiologia")
        
        # Check availability
        is_available = calc_availability.get('PREVENT', False)
        status_badge = '<span class="status-badge status-ready">✅ Pronto</span>' if is_available else '<span class="status-badge status-missing">⚠️ Falta dados</span>'
        
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
        
        # Check if data is valid for PREVENT
        is_valid, missing_param = has_valid_data({
            'age': 1, 'sbp': 70, 'total_chol': 50, 'hdl_chol': 10, 'egfr': 5
        })
        
        if not is_valid:
            missing = get_missing_params_msg({
                'age': 1, 'sbp': 70, 'total_chol': 50, 'hdl_chol': 10, 'egfr': 5
            })
            st.warning(f"⚠️ **Dados faltantes:** {', '.join(missing)}")
        else:
            try:
                sex_code = 'M' if pd['sex'] == "Masculino" else 'F'
                calculator = PREVENTCalculator()
                
                # Only use uacr and hba1c if the checkboxes are checked
                uacr_value = pd.get('uacr') if pd.get('use_uacr', False) and pd.get('uacr', 0) > 0 else None
                hba1c_value = pd.get('hba1c') if pd.get('use_hba1c', False) and pd.get('hba1c', 0) > 0 else None
                
                results = calculator.calculate_risk_score(
                    age=pd['age'],
                    sex=sex_code,
                    race='other',
                    total_cholesterol=pd['total_chol'],
                    hdl_cholesterol=pd['hdl_chol'],
                    sbp=pd['sbp'],
                    on_bp_meds=pd['on_bp_meds'],
                    diabetes=pd['diabetes'],
                    smoker=pd['smoker'],
                    egfr=pd['egfr'],
                    uacr=uacr_value,
                    hba1c=hba1c_value
                )
                
                # Display overall risk category
                risk_class_map = {
                    'Baixo': 'risk-low',
                    'Limítrofe': 'risk-borderline',
                    'Intermediário': 'risk-intermediate',
                    'Alto': 'risk-high'
                }
                st.markdown(f"""
                    <div class="risk-box {risk_class_map[results['risk_category']]}">
                        Categoria de Risco Geral: {results['risk_category'].upper()}
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**📊 DCV Total**")
                    st.metric("10 anos", f"{results['total_cvd_10yr']}%")
                    st.metric("30 anos", f"{results['total_cvd_30yr']}%")
                
                with col2:
                    st.markdown("**🩺 DCVA (Aterosclerose)**")
                    st.metric("10 anos", f"{results['ascvd_10yr']}%")
                    st.metric("30 anos", f"{results['ascvd_30yr']}%")
                
                with col3:
                    st.markdown("**💔 Insuficiência Cardíaca**")
                    st.metric("10 anos", f"{results['hf_10yr']}%")
                    st.metric("30 anos", f"{results['hf_30yr']}%")
                
            except Exception as e:
                st.error(f"Erro ao calcular PREVENT: {str(e)}")


# ========== TAB 3: CARDIOLOGY ==========
with tabs[2]:
    st.header("🫀 Cardiologia")
    
    st.markdown("""
        <div class="calculator-card">
            <div class="calc-header">
                <div class="calc-icon">❤️</div>
                <div>
                    <div class="calc-title">PREVENT - Risco Cardiovascular (AHA)</div>
                    <div class="calc-subtitle">Cálculo Automático Ativo</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <strong>PREVENT (Predicting Risk of cardiovascular disease EVENTs)</strong><br>
    Calculadora oficial da American Heart Association para estimativa de risco cardiovascular.<br>
    Fornece três avaliações de risco: DCV Total, DCVA (Aterosclerose) e Insuficiência Cardíaca.<br><br>
    <em>Implementação fidedigna às equações oficiais AHA PREVENT (Circulation 2023).</em>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.patient_data:
        st.warning("⚠️ Por favor, preencha os dados do paciente na aba 'Dados do Paciente' primeiro.")
    else:
        try:
            pd = st.session_state.patient_data
            sex_code = 'M' if pd['sex'] == "Masculino" else 'F'
            
            calculator = PREVENTCalculator()
            
            # Only use uacr and hba1c if the checkboxes are checked
            uacr_value = pd.get('uacr') if pd.get('use_uacr', False) and pd.get('uacr', 0) > 0 else None
            hba1c_value = pd.get('hba1c') if pd.get('use_hba1c', False) and pd.get('hba1c', 0) > 0 else None
            
            results = calculator.calculate_risk_score(
                age=pd['age'],
                sex=sex_code,
                race='other',  # Default value
                total_cholesterol=pd['total_chol'],
                hdl_cholesterol=pd['hdl_chol'],
                sbp=pd['sbp'],
                on_bp_meds=pd['on_bp_meds'],
                diabetes=pd['diabetes'],
                smoker=pd['smoker'],
                egfr=pd['egfr'],
                uacr=uacr_value,
                hba1c=hba1c_value
            )
            
            # Display overall risk category
            risk_class_map = {
                'Baixo': 'risk-low',
                'Limítrofe': 'risk-borderline',
                'Intermediário': 'risk-intermediate',
                'Alto': 'risk-high'
            }
            st.markdown(f"""
                <div class="risk-box {risk_class_map[results['risk_category']]}">
                    Categoria de Risco Geral: {results['risk_category'].upper()}
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Section 1: Total CVD (Risco Geral)
            st.subheader("📊 Doença Cardiovascular Total (DCV)")
            st.markdown("*Risco de qualquer evento cardiovascular (infarto, AVC, insuficiência cardíaca, etc.)*")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Risco em 10 anos", f"{results['total_cvd_10yr']}%")
            with col2:
                st.metric("Risco em 30 anos", f"{results['total_cvd_30yr']}%")
            
            st.markdown("---")
            
            # Section 2: ASCVD (Aterosclerose)
            st.subheader("🩺 Doença Cardiovascular Aterosclerótica (DCVA)")
            st.markdown("*Risco de infarto do miocárdio ou AVC isquêmico*")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Risco em 10 anos", f"{results['ascvd_10yr']}%")
            with col2:
                st.metric("Risco em 30 anos", f"{results['ascvd_30yr']}%")
            
            st.markdown("---")
            
            # Section 3: Heart Failure
            st.subheader("💔 Insuficiência Cardíaca")
            st.markdown("*Risco de desenvolver insuficiência cardíaca congestiva*")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Risco em 10 anos", f"{results['hf_10yr']}%")
            with col2:
                st.metric("Risco em 30 anos", f"{results['hf_30yr']}%")
            
            st.markdown("---")
            
            # Clinical recommendations
            st.subheader("💊 Recomendações Clínicas")
            recommendations = calculator.get_recommendations(
                results['risk_category'], 
                results['total_cvd_10yr']
            )
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"**{i}.** {rec}")
            
            # Additional information about risk types
            st.markdown("---")
            st.info("""
            **Interpretação dos Resultados:**
            
            **DCV Total (Doença Cardiovascular Total):**
            - Inclui todos os eventos cardiovasculares: infarto, AVC, insuficiência cardíaca, morte cardiovascular
            - É o risco mais abrangente e útil para decisões sobre prevenção primária
            
            **DCVA (Doença Cardiovascular Aterosclerótica):**
            - Eventos causados por aterosclerose: infarto do miocárdio e AVC isquêmico
            - Importante para decisões sobre terapia antiplaquetária e estatinas
            
            **Insuficiência Cardíaca:**
            - Risco específico de desenvolver ICC
            - Útil para identificar pacientes que podem se beneficiar de controle mais rigoroso da PA e uso de IECA/BRA
            
            **Nota:** Estas estimativas são baseadas nas equações oficiais PREVENT da AHA (Circulation 2023),
            que incorporam função renal (eTFG) e marcadores metabólicos (uACR, HbA1c) para uma avaliação
            mais precisa do risco cardiovascular.
            """)
                
        except Exception as e:
            st.error(f"Erro ao calcular: {str(e)}")

# ========== TAB 4: GASTROENTEROLOGY ==========
with tabs[3]:
    st.header("🍽️ Gastroenterologia")
    
    calc_choice = st.selectbox(
        "Selecione a Calculadora:",
        ["FIB-4 - Fibrose Hepática", "MELD - Gravidade Hepática", "Child-Pugh - Cirrose"]
    )
    
    if not st.session_state.patient_data:
        st.warning("⚠️ Por favor, preencha os dados do paciente na aba 'Dados do Paciente' primeiro.")
    else:
        pd = st.session_state.patient_data
        
        if calc_choice == "FIB-4 - Fibrose Hepática":
            st.markdown("""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">🔍</div>
                        <div>
                            <div class="calc-title">FIB-4</div>
                            <div class="calc-subtitle">Avaliação de Fibrose Hepática - Cálculo Automático</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
            O FIB-4 é usado para avaliar a probabilidade de fibrose hepática avançada.
            </div>
            """, unsafe_allow_html=True)
            
            try:
                calculator = FIB4Calculator()
                result = calculator.calculate(
                    age=pd['age'],
                    ast=pd['ast'],
                    alt=pd['alt'],
                    platelets=pd['platelets']
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Score FIB-4", result['score'])
                with col2:
                    st.metric("Risco", result['risk'])
                
                st.info(f"**Interpretação:** {result['interpretation']}")
            except Exception as e:
                st.error(f"Erro ao calcular: {str(e)}")
        
        elif calc_choice == "MELD - Gravidade Hepática":
            st.markdown("""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">⚕️</div>
                        <div>
                            <div class="calc-title">MELD</div>
                            <div class="calc-subtitle">Model for End-Stage Liver Disease - Cálculo Automático</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
            O MELD é usado para priorização de transplante hepático e avaliação de gravidade.
            </div>
            """, unsafe_allow_html=True)
            
            try:
                calculator = MELDCalculator()
                result = calculator.calculate(
                    creatinine=pd['creatinine'],
                    bilirubin=pd['bilirubin'],
                    inr=pd['inr'],
                    dialysis=pd['dialysis']
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Score MELD", result['score'])
                with col2:
                    st.info(f"**{result['interpretation']}**")
                
                st.warning(f"**Mortalidade:** {result['mortality']}")
            except Exception as e:
                st.error(f"Erro ao calcular: {str(e)}")
        
        else:  # Child-Pugh
            st.markdown("""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">🏥</div>
                        <div>
                            <div class="calc-title">Child-Pugh</div>
                            <div class="calc-subtitle">Classificação de Cirrose - Cálculo Automático</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
            O Child-Pugh classifica a gravidade da cirrose hepática.
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                ascites = st.selectbox("Ascite", ["Ausente", "Leve", "Moderada/Grave"], key="gastro_ascites")
            with col2:
                encephalopathy = st.selectbox("Encefalopatia", ["Ausente", "Grau 1-2", "Grau 3-4"], key="gastro_enceph")
            
            try:
                # Map selections
                ascites_map = {"Ausente": "none", "Leve": "mild", "Moderada/Grave": "moderate_severe"}
                enceph_map = {"Ausente": "none", "Grau 1-2": "grade_1_2", "Grau 3-4": "grade_3_4"}
                
                calculator = ChildPughCalculator()
                result = calculator.calculate(
                    bilirubin=pd['bilirubin'],
                    albumin=pd['albumin'],
                    inr=pd['inr'],
                    ascites=ascites_map[ascites],
                    encephalopathy=enceph_map[encephalopathy]
                )
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Score", result['score'])
                with col2:
                    st.metric("Classe", result['class'])
                with col3:
                    st.info(f"**{result['interpretation']}**")
                
                st.markdown(f"**Sobrevida em 1 ano:** {result['survival_1_year']}")
                st.markdown(f"**Sobrevida em 2 anos:** {result['survival_2_year']}")
            except Exception as e:
                st.error(f"Erro ao calcular: {str(e)}")

# ========== TAB 5: NEPHROLOGY ==========
with tabs[4]:
    st.header("💧 Nefrologia")
    
    calc_choice = st.selectbox(
        "Selecione a Calculadora:",
        ["eTFG - Taxa de Filtração Glomerular", "Kt/V - Adequação da Diálise"],
        key="nephro_choice"
    )
    
    if not st.session_state.patient_data:
        st.warning("⚠️ Por favor, preencha os dados do paciente na aba 'Dados do Paciente' primeiro.")
    else:
        pd = st.session_state.patient_data
        
        if calc_choice == "eTFG - Taxa de Filtração Glomerular":
            st.markdown("""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">🫘</div>
                        <div>
                            <div class="calc-title">eTFG</div>
                            <div class="calc-subtitle">Estimativa da Taxa de Filtração Glomerular - Cálculo Automático</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
            Cálculo usando equação CKD-EPI 2021 (sem ajuste racial).
            </div>
            """, unsafe_allow_html=True)
            
            try:
                sex_code = 'M' if pd['sex'] == "Masculino" else 'F'
                
                calculator = eGFRCalculator()
                result = calculator.calculate(
                    creatinine=pd['creatinine'],
                    age=pd['age'],
                    sex=sex_code
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("eTFG", f"{result['egfr']} mL/min/1.73m²")
                with col2:
                    st.metric("Estágio DRC", result['stage'])
                
                st.info(f"**{result['description']}**")
            except Exception as e:
                st.error(f"Erro ao calcular: {str(e)}")
        
        else:  # Kt/V
            st.markdown("""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">💉</div>
                        <div>
                            <div class="calc-title">Kt/V</div>
                            <div class="calc-subtitle">Adequação da Diálise - Cálculo Automático</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
            Avalia a adequação da hemodiálise usando fórmula de Daugirdas II.
            </div>
            """, unsafe_allow_html=True)
            
            # Only show if patient is on dialysis
            if not pd.get('dialysis', False):
                st.warning("⚠️ **Kt/V** é aplicável apenas para pacientes em diálise. Marque 'Em diálise' na aba de Dados do Paciente para habilitar este cálculo.")
            else:
                col1, col2, col3 = st.columns(3)
                with col1:
                    pre_bun = st.number_input("BUN pré-diálise (mg/dL)", min_value=1, max_value=300, value=60, step=1, key="nephro_pre_bun")
                    post_bun = st.number_input("BUN pós-diálise (mg/dL)", min_value=1, max_value=200, value=20, step=1, key="nephro_post_bun")
                with col2:
                    dialysis_time = st.number_input("Tempo de diálise (horas)", min_value=0.5, max_value=10.0, value=4.0, step=0.5, key="nephro_time")
                with col3:
                    ultrafiltration = st.number_input("Ultrafiltração (L)", min_value=0.0, max_value=10.0, value=2.0, step=0.1, key="nephro_uf")
                
                try:
                    calculator = KtVCalculator()
                    result = calculator.calculate(
                        pre_bun=pre_bun,
                        post_bun=post_bun,
                        dialysis_time=dialysis_time,
                        ultrafiltration=ultrafiltration,
                        post_weight=pd['weight']
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Kt/V", result['ktv'])
                    with col2:
                        st.metric("Adequação", result['adequacy'])
                    
                    st.info(f"**Recomendação:** {result['recommendation']}")
                except Exception as e:
                    st.error(f"Erro ao calcular: {str(e)}")

# ========== TAB 6: ENDOCRINOLOGY ==========
with tabs[5]:
    st.header("🩺 Endocrinologia")
    
    calc_choice = st.selectbox(
        "Selecione a Calculadora:",
        ["IMC - Índice de Massa Corporal", "HOMA-IR - Resistência Insulínica", "HOMA-Beta - Função Beta Células"],
        key="endo_choice"
    )
    
    if not st.session_state.patient_data:
        st.warning("⚠️ Por favor, preencha os dados do paciente na aba 'Dados do Paciente' primeiro.")
    else:
        pd = st.session_state.patient_data
        
        if calc_choice == "IMC - Índice de Massa Corporal":
            st.markdown("""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">📊</div>
                        <div>
                            <div class="calc-title">IMC</div>
                            <div class="calc-subtitle">Índice de Massa Corporal - Cálculo Automático</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
            Classificação de peso corporal segundo OMS.
            </div>
            """, unsafe_allow_html=True)
            
            try:
                calculator = BMICalculator()
                result = calculator.calculate(
                    weight=pd['weight'],
                    height=pd['height']
                )
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("IMC", result['bmi'])
                with col2:
                    st.metric("Classificação", result['classification'])
                with col3:
                    st.metric("Risco", result['risk'])
            except Exception as e:
                st.error(f"Erro ao calcular: {str(e)}")
        
        elif calc_choice == "HOMA-IR - Resistência Insulínica":
            st.markdown("""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">🔬</div>
                        <div>
                            <div class="calc-title">HOMA-IR</div>
                            <div class="calc-subtitle">Avaliação de Resistência Insulínica - Cálculo Automático</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
            Modelo homeostático para avaliar resistência à insulina.
            </div>
            """, unsafe_allow_html=True)
            
            try:
                calculator = HOMAIRCalculator()
                result = calculator.calculate(
                    fasting_glucose=pd['fasting_glucose'],
                    fasting_insulin=pd['fasting_insulin']
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("HOMA-IR", result['homa_ir'])
                with col2:
                    st.info(f"**{result['interpretation']}**")
                
                st.markdown(f"**Recomendação:** {result['recommendation']}")
            except Exception as e:
                st.error(f"Erro ao calcular: {str(e)}")
        
        else:  # HOMA-Beta
            st.markdown("""
                <div class="calculator-card">
                    <div class="calc-header">
                        <div class="calc-icon">🧬</div>
                        <div>
                            <div class="calc-title">HOMA-Beta</div>
                            <div class="calc-subtitle">Avaliação da Função das Células Beta - Cálculo Automático</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
            Modelo homeostático para avaliar função pancreática (células beta).
            </div>
            """, unsafe_allow_html=True)
            
            try:
                calculator = HOMABetaCalculator()
                result = calculator.calculate(
                    fasting_glucose=pd['fasting_glucose'],
                    fasting_insulin=pd['fasting_insulin']
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("HOMA-Beta", f"{result['homa_beta']}%")
                with col2:
                    st.info(f"**{result['interpretation']}**")
                
                st.markdown(f"**Recomendação:** {result['recommendation']}")
            except Exception as e:
                st.error(f"Erro ao calcular: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>Calculadoras Médicas - Plataforma Integrada de Apoio à Decisão Clínica</strong></p>
    <p>Desenvolvido para profissionais de saúde | Versão 2.0</p>
</div>
""", unsafe_allow_html=True)
