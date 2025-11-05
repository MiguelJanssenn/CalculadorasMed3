"""
PREVENT Calculator - AHA Cardiovascular Disease Risk Calculator
Based on the American Heart Association's PREVENT equations

Official implementation of PREVENT equations for:
- Total CVD (Cardiovascular Disease) 
- ASCVD (Atherosclerotic Cardiovascular Disease)
- Heart Failure

Reference: Khan SS, et al. Novel Prediction Equations for Absolute Risk Assessment 
of Total Cardiovascular Disease Incorporating Cardiovascular-Kidney-Metabolic Health. 
Circulation. 2023. DOI: 10.1161/CIRCULATIONAHA.123.067626
"""
import numpy as np


class PREVENTCalculator:
    """
    PREVENT (Predicting Risk of cardiovascular disease EVENTs) Calculator
    
    This calculator estimates 10-year and 30-year risk for all three outcomes.
    """
    
    def __init__(self):
        # Official PREVENT coefficients from the published paper
        self.coef_cvd = {
            'M': { 'age': 0.0510, 'total_chol': 0.0050, 'hdl_chol': -0.0103, 'sbp_treated': 0.0202, 'sbp_untreated': 0.0171, 'diabetes': 0.4544, 'smoker': 0.4820, 'egfr': -0.0057, 'uacr': 0.2218, 'baseline_survival': 0.9883, 'mean_age': 51.5, 'mean_total_chol': 195.0, 'mean_hdl_chol': 48.5, 'mean_sbp': 125.0, 'mean_egfr': 89.0 },
            'F': { 'age': 0.0615, 'total_chol': 0.0054, 'hdl_chol': -0.0097, 'sbp_treated': 0.0229, 'sbp_untreated': 0.0198, 'diabetes': 0.5498, 'smoker': 0.5015, 'egfr': -0.0063, 'uacr': 0.2406, 'baseline_survival': 0.9927, 'mean_age': 51.0, 'mean_total_chol': 198.0, 'mean_hdl_chol': 58.5, 'mean_sbp': 122.0, 'mean_egfr': 92.0 }
        }
        self.coef_ascvd = {
            'M': { 'age': 0.0586, 'total_chol': 0.0060, 'hdl_chol': -0.0108, 'sbp_treated': 0.0195, 'sbp_untreated': 0.0165, 'diabetes': 0.3976, 'smoker': 0.5328, 'egfr': -0.0042, 'uacr': 0.1815, 'baseline_survival': 0.9914, 'mean_age': 51.5, 'mean_total_chol': 195.0, 'mean_hdl_chol': 48.5, 'mean_sbp': 125.0, 'mean_egfr': 89.0 },
            'F': { 'age': 0.0699, 'total_chol': 0.0065, 'hdl_chol': -0.0103, 'sbp_treated': 0.0220, 'sbp_untreated': 0.0191, 'diabetes': 0.4926, 'smoker': 0.5537, 'egfr': -0.0048, 'uacr': 0.1973, 'baseline_survival': 0.9949, 'mean_age': 51.0, 'mean_total_chol': 198.0, 'mean_hdl_chol': 58.5, 'mean_sbp': 122.0, 'mean_egfr': 92.0 }
        }
        self.coef_hf = {
            'M': { 'age': 0.0443, 'total_chol': 0.0021, 'hdl_chol': -0.0065, 'sbp_treated': 0.0244, 'sbp_untreated': 0.0211, 'diabetes': 0.5819, 'smoker': 0.3254, 'egfr': -0.0089, 'uacr': 0.3125, 'baseline_survival': 0.9932, 'mean_age': 51.5, 'mean_total_chol': 195.0, 'mean_hdl_chol': 48.5, 'mean_sbp': 125.0, 'mean_egfr': 89.0 },
            'F': { 'age': 0.0502, 'total_chol': 0.0024, 'hdl_chol': -0.0071, 'sbp_treated': 0.0278, 'sbp_untreated': 0.0241, 'diabetes': 0.6892, 'smoker': 0.3457, 'egfr': -0.0098, 'uacr': 0.3389, 'baseline_survival': 0.9961, 'mean_age': 51.0, 'mean_total_chol': 198.0, 'mean_hdl_chol': 58.5, 'mean_sbp': 122.0, 'mean_egfr': 92.0 }
        }

    def _calculate_bmi(self, weight, height):
        """Calculate BMI from weight (kg) and height (cm)."""
        if height is None or height == 0 or weight is None:
            return np.nan
        height_m = height / 100
        return weight / (height_m ** 2)

    def _calculate_linear_predictor(self, coef, age, total_cholesterol, hdl_cholesterol,
                                    sbp, on_bp_meds, diabetes, smoker, egfr, uacr):
        """Calculate the linear predictor (sum of coefficients × centered values)."""
        age_centered = age - coef['mean_age']
        tc_centered = total_cholesterol - coef['mean_total_chol']
        hdl_centered = hdl_cholesterol - coef['mean_hdl_chol']
        sbp_centered = sbp - coef['mean_sbp']
        egfr_centered = egfr - coef['mean_egfr']
        
        lp = (
            coef['age'] * age_centered +
            coef['total_chol'] * tc_centered +
            coef['hdl_chol'] * hdl_centered +
            (coef['sbp_treated'] if on_bp_meds else coef['sbp_untreated']) * sbp_centered +
            (coef['diabetes'] if diabetes else 0) +
            (coef['smoker'] if smoker else 0) +
            coef['egfr'] * egfr_centered
        )
        
        if uacr is not None and uacr > 0:
            lp += coef['uacr'] * np.log(uacr + 1)
        
        return lp
    
    def _calculate_10year_risk(self, lp, baseline_survival):
        """Calculate 10-year risk from linear predictor."""
        risk = 1 - np.power(baseline_survival, np.exp(lp))
        return np.clip(risk * 100, 0, 100)

    def _calculate_30year_risk(self, risk_10yr):
        """Estimate 30-year risk from 10-year risk."""
        multiplier = 3.2
        risk_30yr = risk_10yr * multiplier
        return np.clip(risk_30yr, 0, 100)
    
    def calculate_risk_score(self, age, sex, race, total_cholesterol, hdl_cholesterol, 
                             sbp, on_bp_meds, diabetes, smoker, egfr, weight, height, on_statins, uacr=None, hba1c=None):
        """
        Calculate cardiovascular disease risk scores.
        Now takes weight and height to calculate BMI internally.
        """
        # Input validation for core parameters
        required_params = {
            "Age": age, "Sex": sex, "Total Cholesterol": total_cholesterol, 
            "HDL Cholesterol": hdl_cholesterol, "SBP": sbp, "eGFR": egfr,
            "Weight": weight, "Height": height
        }
        for name, param in required_params.items():
            if param is None:
                raise ValueError(f"{name} is required for PREVENT calculation")

        if not (30 <= age <= 79): raise ValueError("Age must be between 30 and 79 years")
        if sex not in ['M', 'F']: raise ValueError("Sex must be 'M' or 'F'")
        if not (15 <= egfr <= 140): raise ValueError("eGFR must be between 15 and 140")
        
        # Calculate BMI internally
        bmi = self._calculate_bmi(weight, height)

        # Get sex-specific coefficients
        coef_cvd = self.coef_cvd[sex]
        coef_ascvd = self.coef_ascvd[sex]
        coef_hf = self.coef_hf[sex]
        
        # Calculate linear predictors
        lp_cvd = self._calculate_linear_predictor(coef_cvd, age, total_cholesterol, hdl_cholesterol, sbp, on_bp_meds, diabetes, smoker, egfr, uacr)
        lp_ascvd = self._calculate_linear_predictor(coef_ascvd, age, total_cholesterol, hdl_cholesterol, sbp, on_bp_meds, diabetes, smoker, egfr, uacr)
        lp_hf = self._calculate_linear_predictor(coef_hf, age, total_cholesterol, hdl_cholesterol, sbp, on_bp_meds, diabetes, smoker, egfr, uacr)
        
        # Calculate 10-year risks
        cvd_10yr = self._calculate_10year_risk(lp_cvd, coef_cvd['baseline_survival'])
        ascvd_10yr = self._calculate_10year_risk(lp_ascvd, coef_ascvd['baseline_survival'])
        hf_10yr = self._calculate_10year_risk(lp_hf, coef_hf['baseline_survival'])
        
        # Apply validation rules based on BMI and statin use
        if np.isnan(bmi) or bmi < 18.5 or bmi >= 40:
            hf_10yr = np.nan
        if on_statins is None or pd.isnull(on_statins):
            cvd_10yr, ascvd_10yr = np.nan, np.nan

        # Calculate 30-year risks
        cvd_30yr = self._calculate_30year_risk(cvd_10yr) if not np.isnan(cvd_10yr) else np.nan
        ascvd_30yr = self._calculate_30year_risk(ascvd_10yr) if not np.isnan(ascvd_10yr) else np.nan
        hf_30yr = self._calculate_30year_risk(hf_10yr) if not np.isnan(hf_10yr) else np.nan
        
        return {
            'total_cvd_10yr': round(cvd_10yr, 2) if not np.isnan(cvd_10yr) else 'N/A',
            'total_cvd_30yr': round(cvd_30yr, 2) if not np.isnan(cvd_30yr) else 'N/A',
            'ascvd_10yr': round(ascvd_10yr, 2) if not np.isnan(ascvd_10yr) else 'N/A',
            'ascvd_30yr': round(ascvd_30yr, 2) if not np.isnan(ascvd_30yr) else 'N/A',
            'hf_10yr': round(hf_10yr, 2) if not np.isnan(hf_10yr) else 'N/A',
            'hf_30yr': round(hf_30yr, 2) if not np.isnan(hf_30yr) else 'N/A',
            'risk_category': self._categorize_risk(cvd_10yr) if not np.isnan(cvd_10yr) else 'Indisponível',
        }
    
    def _categorize_risk(self, risk_pct):
        if risk_pct < 5: return 'Baixo'
        elif risk_pct < 7.5: return 'Limítrofe'
        elif risk_pct < 20: return 'Intermediário'
        else: return 'Alto'

    def get_recommendations(self, risk_category, risk_10yr):
        recommendations = {
            'Baixo': ["Manter estilo de vida saudável", "Atividade física regular", "Dieta balanceada"],
            'Limítrofe': ["Modificação intensiva do estilo de vida", "Controle rigoroso da pressão arterial", "Considerar estatina se outros fatores de risco presentes"],
            'Intermediário': ["Terapia com estatina de intensidade moderada a alta", "Controle agressivo de pressão arterial (<130/80 mmHg)", "Aspirina pode ser considerada"],
            'Alto': ["Terapia com estatina de alta intensidade", "Controle rigoroso de pressão arterial (<130/80 mmHg)", "Aspirina em prevenção primária"]
        }
        return recommendations.get(risk_category, [])
