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
    .info-box {
        background-color: #E7F3FF;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0066CC;
        margin: 1rem 0;
    }
    .data-saved {
        background-color: #D4EDDA;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28A745;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for patient data
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}

# Title
st.title("⚕️ Calculadoras Médicas")
st.markdown("### Plataforma Integrada de Scores e Calculadoras para Prática Médica")

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
    
    with col1:
        st.subheader("Dados Demográficos")
        age = st.number_input("Idade (anos)", min_value=1, max_value=120, 
                             value=st.session_state.patient_data.get('age', 55), step=1)
        sex = st.selectbox("Sexo", ["Masculino", "Feminino"],
                          index=0 if st.session_state.patient_data.get('sex') == 'Masculino' else 1)
        weight = st.number_input("Peso (kg)", min_value=1.0, max_value=300.0,
                                value=st.session_state.patient_data.get('weight', 70.0), step=0.1)
        height = st.number_input("Altura (cm)", min_value=50.0, max_value=250.0,
                                value=st.session_state.patient_data.get('height', 170.0), step=0.1)
        
        st.subheader("História Clínica")
        diabetes = st.checkbox("Diabetes", value=st.session_state.patient_data.get('diabetes', False))
        smoker = st.checkbox("Fumante atual", value=st.session_state.patient_data.get('smoker', False))
        on_bp_meds = st.checkbox("Uso de anti-hipertensivos", 
                                value=st.session_state.patient_data.get('on_bp_meds', False))
        dialysis = st.checkbox("Em diálise", value=st.session_state.patient_data.get('dialysis', False))
    
    with col2:
        st.subheader("Dados Vitais")
        sbp = st.number_input("Pressão Arterial Sistólica (mmHg)", min_value=70, max_value=250,
                             value=st.session_state.patient_data.get('sbp', 120), step=1)
        
        st.subheader("Lipidograma")
        total_chol = st.number_input("Colesterol Total (mg/dL)", min_value=50, max_value=500,
                                    value=st.session_state.patient_data.get('total_chol', 200), step=1)
        hdl_chol = st.number_input("HDL Colesterol (mg/dL)", min_value=10, max_value=150,
                                  value=st.session_state.patient_data.get('hdl_chol', 50), step=1)
        
        st.subheader("Função Renal")
        creatinine = st.number_input("Creatinina sérica (mg/dL)", min_value=0.1, max_value=20.0,
                                    value=st.session_state.patient_data.get('creatinine', 1.0), step=0.1)
        egfr = st.number_input("eTFG (mL/min/1.73m²)", min_value=5, max_value=150,
                              value=st.session_state.patient_data.get('egfr', 90), step=1)
        uacr = st.number_input("RACu - Relação Albumina/Creatinina Urinária (mg/g)", 
                              min_value=0.0, max_value=5000.0,
                              value=st.session_state.patient_data.get('uacr', 0.0), step=1.0)
    
    with col3:
        st.subheader("Glicemia e Insulina")
        fasting_glucose = st.number_input("Glicemia de jejum (mg/dL)", min_value=30, max_value=600,
                                         value=st.session_state.patient_data.get('fasting_glucose', 100), step=1)
        hba1c = st.number_input("HbA1c (%)", min_value=3.0, max_value=20.0,
                               value=st.session_state.patient_data.get('hba1c', 5.5), step=0.1)
        fasting_insulin = st.number_input("Insulina de jejum (μU/mL)", min_value=0.1, max_value=300.0,
                                         value=st.session_state.patient_data.get('fasting_insulin', 10.0), step=0.1)
        
        st.subheader("Função Hepática")
        ast = st.number_input("AST (U/L)", min_value=1, max_value=1000,
                            value=st.session_state.patient_data.get('ast', 30), step=1)
        alt = st.number_input("ALT (U/L)", min_value=1, max_value=1000,
                            value=st.session_state.patient_data.get('alt', 30), step=1)
        bilirubin = st.number_input("Bilirrubina total (mg/dL)", min_value=0.1, max_value=50.0,
                                   value=st.session_state.patient_data.get('bilirubin', 1.0), step=0.1)
        albumin = st.number_input("Albumina (g/dL)", min_value=1.0, max_value=6.0,
                                 value=st.session_state.patient_data.get('albumin', 4.0), step=0.1)
        inr = st.number_input("INR", min_value=0.8, max_value=10.0,
                            value=st.session_state.patient_data.get('inr', 1.0), step=0.1)
        platelets = st.number_input("Plaquetas (×10⁹/L)", min_value=1, max_value=1000,
                                   value=st.session_state.patient_data.get('platelets', 200), step=1)
    
    st.markdown("---")
    if st.button("💾 Salvar Dados do Paciente", type="primary"):
        st.session_state.patient_data = {
            'age': age,
            'sex': sex,
            'weight': weight,
            'height': height,
            'diabetes': diabetes,
            'smoker': smoker,
            'on_bp_meds': on_bp_meds,
            'dialysis': dialysis,
            'sbp': sbp,
            'total_chol': total_chol,
            'hdl_chol': hdl_chol,
            'creatinine': creatinine,
            'egfr': egfr,
            'uacr': uacr,
            'fasting_glucose': fasting_glucose,
            'hba1c': hba1c,
            'fasting_insulin': fasting_insulin,
            'ast': ast,
            'alt': alt,
            'bilirubin': bilirubin,
            'albumin': albumin,
            'inr': inr,
            'platelets': platelets
        }
        st.markdown("""
        <div class="data-saved">
        ✅ <strong>Dados salvos com sucesso!</strong><br>
        Os dados do paciente agora estão disponíveis para todas as calculadoras.
        </div>
        """, unsafe_allow_html=True)

# ========== TAB 2: ALL CALCULATORS ==========
with tabs[1]:
    st.header("🏥 Todas as Calculadoras")
    st.markdown("Selecione uma calculadora abaixo para realizar o cálculo com os dados do paciente.")
    
    if not st.session_state.patient_data:
        st.warning("⚠️ Por favor, preencha os dados do paciente na aba 'Dados do Paciente' primeiro.")
    
    # Organize calculators by specialty
    st.subheader("🫀 Cardiologia")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("PREVENT - Risco Cardiovascular"):
            st.session_state.selected_calculator = 'prevent'
    
    st.markdown("---")
    st.subheader("🍽️ Gastroenterologia")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("FIB-4 - Fibrose Hepática"):
            st.session_state.selected_calculator = 'fib4'
    with col2:
        if st.button("MELD - Gravidade Hepática"):
            st.session_state.selected_calculator = 'meld'
    with col3:
        if st.button("Child-Pugh - Cirrose"):
            st.session_state.selected_calculator = 'childpugh'
    
    st.markdown("---")
    st.subheader("💧 Nefrologia")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("eTFG - Taxa de Filtração Glomerular"):
            st.session_state.selected_calculator = 'egfr'
    with col2:
        if st.button("Kt/V - Adequação da Diálise"):
            st.session_state.selected_calculator = 'ktv'
    
    st.markdown("---")
    st.subheader("🩺 Endocrinologia")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("IMC - Índice de Massa Corporal"):
            st.session_state.selected_calculator = 'bmi'
    with col2:
        if st.button("HOMA-IR - Resistência Insulínica"):
            st.session_state.selected_calculator = 'homa_ir'
    with col3:
        if st.button("HOMA-Beta - Função das Células Beta"):
            st.session_state.selected_calculator = 'homa_beta'

# ========== TAB 3: CARDIOLOGY ==========
with tabs[2]:
    st.header("🫀 Cardiologia")
    
    st.subheader("PREVENT - Risco Cardiovascular (AHA)")
    st.markdown("""
    <div class="info-box">
    <strong>PREVENT (Predicting Risk of cardiovascular disease EVENTs)</strong><br>
    Calculadora da American Heart Association para estimativa de risco cardiovascular em 10 e 30 anos.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔬 Calcular Risco Cardiovascular", key="prevent_calc"):
        if not st.session_state.patient_data:
            st.error("❌ Por favor, preencha os dados do paciente primeiro.")
        else:
            try:
                pd = st.session_state.patient_data
                sex_code = 'M' if pd['sex'] == "Masculino" else 'F'
                
                calculator = PREVENTCalculator()
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
                    uacr=pd.get('uacr') if pd.get('uacr', 0) > 0 else None,
                    hba1c=pd.get('hba1c') if pd.get('hba1c', 0) > 0 else None
                )
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Risco em 10 anos", f"{results['10_year_risk']}%")
                with col2:
                    st.metric("Risco em 30 anos", f"{results['30_year_risk']}%")
                with col3:
                    st.metric("Categoria", results['risk_category'])
                
                risk_class_map = {
                    'Baixo': 'risk-low',
                    'Limítrofe': 'risk-borderline',
                    'Intermediário': 'risk-intermediate',
                    'Alto': 'risk-high'
                }
                st.markdown(f"""
                    <div class="risk-box {risk_class_map[results['risk_category']]}">
                        Categoria de Risco: {results['risk_category'].upper()}
                    </div>
                """, unsafe_allow_html=True)
                
                st.subheader("💊 Recomendações Clínicas")
                recommendations = calculator.get_recommendations(
                    results['risk_category'], 
                    results['10_year_risk']
                )
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"**{i}.** {rec}")
                    
            except Exception as e:
                st.error(f"Erro ao calcular: {str(e)}")

# ========== TAB 4: GASTROENTEROLOGY ==========
with tabs[3]:
    st.header("🍽️ Gastroenterologia")
    
    calc_choice = st.selectbox(
        "Selecione a Calculadora:",
        ["FIB-4 - Fibrose Hepática", "MELD - Gravidade Hepática", "Child-Pugh - Cirrose"]
    )
    
    if calc_choice == "FIB-4 - Fibrose Hepática":
        st.subheader("FIB-4 - Avaliação de Fibrose Hepática")
        st.markdown("""
        <div class="info-box">
        O FIB-4 é usado para avaliar a probabilidade de fibrose hepática avançada.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔬 Calcular FIB-4", key="fib4_calc"):
            if not st.session_state.patient_data:
                st.error("❌ Por favor, preencha os dados do paciente primeiro.")
            else:
                try:
                    pd = st.session_state.patient_data
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
        st.subheader("MELD - Model for End-Stage Liver Disease")
        st.markdown("""
        <div class="info-box">
        O MELD é usado para priorização de transplante hepático e avaliação de gravidade.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔬 Calcular MELD", key="meld_calc"):
            if not st.session_state.patient_data:
                st.error("❌ Por favor, preencha os dados do paciente primeiro.")
            else:
                try:
                    pd = st.session_state.patient_data
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
        st.subheader("Child-Pugh - Classificação de Cirrose")
        st.markdown("""
        <div class="info-box">
        O Child-Pugh classifica a gravidade da cirrose hepática.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            ascites = st.selectbox("Ascite", ["Ausente", "Leve", "Moderada/Grave"])
        with col2:
            encephalopathy = st.selectbox("Encefalopatia", ["Ausente", "Grau 1-2", "Grau 3-4"])
        
        if st.button("🔬 Calcular Child-Pugh", key="childpugh_calc"):
            if not st.session_state.patient_data:
                st.error("❌ Por favor, preencha os dados do paciente primeiro.")
            else:
                try:
                    pd = st.session_state.patient_data
                    
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
    
    if calc_choice == "eTFG - Taxa de Filtração Glomerular":
        st.subheader("eTFG - Estimativa da Taxa de Filtração Glomerular")
        st.markdown("""
        <div class="info-box">
        Cálculo usando equação CKD-EPI 2021 (sem ajuste racial).
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔬 Calcular eTFG", key="egfr_calc"):
            if not st.session_state.patient_data:
                st.error("❌ Por favor, preencha os dados do paciente primeiro.")
            else:
                try:
                    pd = st.session_state.patient_data
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
        st.subheader("Kt/V - Adequação da Diálise")
        st.markdown("""
        <div class="info-box">
        Avalia a adequação da hemodiálise usando fórmula de Daugirdas II.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            pre_bun = st.number_input("BUN pré-diálise (mg/dL)", min_value=1, max_value=300, value=60, step=1)
            post_bun = st.number_input("BUN pós-diálise (mg/dL)", min_value=1, max_value=200, value=20, step=1)
        with col2:
            dialysis_time = st.number_input("Tempo de diálise (horas)", min_value=0.5, max_value=10.0, value=4.0, step=0.5)
        with col3:
            ultrafiltration = st.number_input("Ultrafiltração (L)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
        
        if st.button("🔬 Calcular Kt/V", key="ktv_calc"):
            if not st.session_state.patient_data:
                st.error("❌ Por favor, preencha os dados do paciente primeiro.")
            else:
                try:
                    pd = st.session_state.patient_data
                    
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
    
    if calc_choice == "IMC - Índice de Massa Corporal":
        st.subheader("IMC - Índice de Massa Corporal")
        st.markdown("""
        <div class="info-box">
        Classificação de peso corporal segundo OMS.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔬 Calcular IMC", key="bmi_calc"):
            if not st.session_state.patient_data:
                st.error("❌ Por favor, preencha os dados do paciente primeiro.")
            else:
                try:
                    pd = st.session_state.patient_data
                    
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
        st.subheader("HOMA-IR - Avaliação de Resistência Insulínica")
        st.markdown("""
        <div class="info-box">
        Modelo homeostático para avaliar resistência à insulina.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔬 Calcular HOMA-IR", key="homa_ir_calc"):
            if not st.session_state.patient_data:
                st.error("❌ Por favor, preencha os dados do paciente primeiro.")
            else:
                try:
                    pd = st.session_state.patient_data
                    
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
        st.subheader("HOMA-Beta - Avaliação da Função das Células Beta")
        st.markdown("""
        <div class="info-box">
        Modelo homeostático para avaliar função pancreática (células beta).
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔬 Calcular HOMA-Beta", key="homa_beta_calc"):
            if not st.session_state.patient_data:
                st.error("❌ Por favor, preencha os dados do paciente primeiro.")
            else:
                try:
                    pd = st.session_state.patient_data
                    
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
