"""
PREVENT Calculator - AHA Cardiovascular Disease Risk Calculator
Based on the American Heart Association's PREVENT equations

NOTE: This implementation uses simplified coefficients for demonstration purposes.
For clinical use, coefficients should be validated against the official AHA PREVENT
equations published in Circulation (2023). The actual PREVENT equations include
race-specific and more refined coefficients.

Reference: Khan SS, et al. Novel Prediction Equations for Absolute Risk Assessment 
of Total Cardiovascular Disease Incorporating Cardiovascular-Kidney-Metabolic Health. 
Circulation. 2023.
"""
import numpy as np


class PREVENTCalculator:
    """
    PREVENT (Predicting Risk of cardiovascular disease EVENTs) Calculator
    
    This calculator estimates 10-year and 30-year risk of cardiovascular disease
    based on the American Heart Association's PREVENT equations.
    """
    
    def __init__(self):
        self.baseline_survival_10yr = 0.9656  # Example baseline - adjust based on specific model
        self.baseline_survival_30yr = 0.8523  # Example baseline - adjust based on specific model
    
    def calculate_risk_score(self, age, sex, race, total_cholesterol, hdl_cholesterol, 
                            sbp, on_bp_meds, diabetes, smoker, egfr, uacr=None, hba1c=None):
        """
        Calculate cardiovascular disease risk score
        
        Parameters:
        - age: Age in years (40-79)
        - sex: 'M' for Male, 'F' for Female
        - race: 'white', 'black', 'hispanic', 'asian', 'other' (for future use with race-specific coefficients)
        - total_cholesterol: Total cholesterol in mg/dL
        - hdl_cholesterol: HDL cholesterol in mg/dL
        - sbp: Systolic blood pressure in mmHg
        - on_bp_meds: Boolean - on blood pressure medication
        - diabetes: Boolean - has diabetes
        - smoker: Boolean - current smoker
        - egfr: eGFR value (mL/min/1.73m²) - REQUIRED for PREVENT calculation
        - uacr: Urine albumin-to-creatinine ratio (mg/g) - optional
        - hba1c: HbA1c percentage (%) - optional
        
        Returns:
        - Dictionary with 10-year and 30-year risk percentages
        
        Note: Race parameter is included for interface compatibility and future 
        implementation of race-specific coefficients as per AHA PREVENT equations.
        Current implementation uses sex-specific coefficients only.
        """
        
        # Input validation
        if not (40 <= age <= 79):
            raise ValueError("Age must be between 40 and 79 years")
        
        if sex not in ['M', 'F']:
            raise ValueError("Sex must be 'M' or 'F'")
        
        if egfr is None:
            raise ValueError("eGFR is required for PREVENT calculation")
        
        # Calculate log-transformed values
        ln_age = np.log(age)
        ln_total_chol = np.log(total_cholesterol)
        ln_hdl = np.log(hdl_cholesterol)
        ln_sbp = np.log(sbp)
        
        # Coefficients based on Framingham-like equations adapted for PREVENT
        # NOTE: These are simplified coefficients for demonstration. In production,
        # use the official AHA PREVENT equation coefficients from the published paper.
        # Official coefficients vary by sex, race/ethnicity, and are continuously updated.
        
        if sex == 'M':
            # Male coefficients (simplified example values)
            coef_ln_age = 3.06
            coef_ln_total_chol = 1.12
            coef_ln_hdl = -0.93
            coef_ln_sbp_treated = 1.93 if on_bp_meds else 0
            coef_ln_sbp_untreated = 1.99 if not on_bp_meds else 0
            coef_smoker = 0.65 if smoker else 0
            coef_diabetes = 0.57 if diabetes else 0
        else:
            # Female coefficients (simplified example values)
            coef_ln_age = 2.32
            coef_ln_total_chol = 1.20
            coef_ln_hdl = -0.70
            coef_ln_sbp_treated = 2.82 if on_bp_meds else 0
            coef_ln_sbp_untreated = 2.76 if not on_bp_meds else 0
            coef_smoker = 0.52 if smoker else 0
            coef_diabetes = 0.77 if diabetes else 0
        
        # Calculate individual sums
        sum_coefficients = (
            coef_ln_age * ln_age +
            coef_ln_total_chol * ln_total_chol +
            coef_ln_hdl * ln_hdl +
            (coef_ln_sbp_treated if on_bp_meds else coef_ln_sbp_untreated) * ln_sbp +
            coef_smoker +
            coef_diabetes
        )
        
        # Enhanced risk with eGFR (now mandatory)
        if egfr < 60:
            # Add risk for reduced kidney function
            sum_coefficients += 0.35
        
        # Optional: Add risk adjustment for uACR if provided
        if uacr is not None and uacr > 30:
            # Add risk for albuminuria
            sum_coefficients += 0.25
        
        # Optional: Add risk adjustment for HbA1c if provided
        if hba1c is not None and hba1c > 6.5:
            # Add risk for elevated HbA1c
            sum_coefficients += 0.20
        
        # Calculate 10-year risk
        risk_10yr = 1 - np.power(self.baseline_survival_10yr, np.exp(sum_coefficients - 26.1))
        
        # Calculate 30-year risk (with adjusted baseline)
        risk_30yr = 1 - np.power(self.baseline_survival_30yr, np.exp(sum_coefficients - 26.1))
        
        # Convert to percentage and ensure bounds
        risk_10yr_pct = np.clip(risk_10yr * 100, 0, 100)
        risk_30yr_pct = np.clip(risk_30yr * 100, 0, 100)
        
        return {
            '10_year_risk': round(risk_10yr_pct, 2),
            '30_year_risk': round(risk_30yr_pct, 2),
            'risk_category': self._categorize_risk(risk_10yr_pct)
        }
    
    def _categorize_risk(self, risk_pct):
        """Categorize risk based on percentage"""
        if risk_pct < 5:
            return 'Baixo'
        elif risk_pct < 7.5:
            return 'Limítrofe'
        elif risk_pct < 20:
            return 'Intermediário'
        else:
            return 'Alto'
    
    def get_recommendations(self, risk_category, risk_10yr):
        """
        Get clinical recommendations based on risk category
        """
        recommendations = {
            'Baixo': [
                "Manter estilo de vida saudável",
                "Atividade física regular",
                "Dieta balanceada",
                "Monitoramento periódico dos fatores de risco"
            ],
            'Limítrofe': [
                "Modificação intensiva do estilo de vida",
                "Controle rigoroso da pressão arterial",
                "Considerar estatina se outros fatores de risco presentes",
                "Avaliação cardiovascular periódica"
            ],
            'Intermediário': [
                "Terapia com estatina de intensidade moderada a alta",
                "Controle agressivo de pressão arterial (<130/80 mmHg)",
                "Aspirina pode ser considerada",
                "Modificação intensiva do estilo de vida",
                "Avaliação de escore de cálcio coronário se decisão incerta"
            ],
            'Alto': [
                "Terapia com estatina de alta intensidade",
                "Controle rigoroso de pressão arterial (<130/80 mmHg)",
                "Aspirina em prevenção primária",
                "Modificação intensiva do estilo de vida",
                "Considerar outras terapias (ezetimiba, inibidores PCSK9)",
                "Acompanhamento cardiológico próximo"
            ]
        }
        
        return recommendations.get(risk_category, [])
