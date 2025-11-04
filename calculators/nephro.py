"""
Nephrology Calculators
Contains eGFR and Kt/V calculators
"""
import numpy as np


class eGFRCalculator:
    """
    eGFR Calculator using CKD-EPI 2021 equation (race-free)
    """
    
    def calculate(self, creatinine, age, sex):
        """
        Calculate eGFR using CKD-EPI 2021 equation
        
        Parameters:
        - creatinine: Serum creatinine (mg/dL)
        - age: Age in years
        - sex: 'M' for Male, 'F' for Female
        
        Returns:
        - Dictionary with eGFR and CKD stage
        """
        if sex == 'F':
            kappa = 0.7
            alpha = -0.241
            if creatinine <= kappa:
                egfr = 142 * (creatinine / kappa) ** alpha * 0.9938 ** age * 1.012
            else:
                egfr = 142 * (creatinine / kappa) ** (-1.200) * 0.9938 ** age * 1.012
        else:  # Male
            kappa = 0.9
            alpha = -0.302
            if creatinine <= kappa:
                egfr = 142 * (creatinine / kappa) ** alpha * 0.9938 ** age
            else:
                egfr = 142 * (creatinine / kappa) ** (-1.200) * 0.9938 ** age
        
        # Determine CKD stage
        if egfr >= 90:
            stage = "G1 (Normal ou aumentada)"
            description = "TFG normal ou aumentada"
        elif egfr >= 60:
            stage = "G2 (Levemente diminuída)"
            description = "Leve redução da TFG"
        elif egfr >= 45:
            stage = "G3a (Leve a moderadamente diminuída)"
            description = "Redução leve a moderada da TFG"
        elif egfr >= 30:
            stage = "G3b (Moderada a gravemente diminuída)"
            description = "Redução moderada a grave da TFG"
        elif egfr >= 15:
            stage = "G4 (Gravemente diminuída)"
            description = "Redução grave da TFG"
        else:
            stage = "G5 (Falência renal)"
            description = "Falência renal"
        
        return {
            'egfr': round(egfr, 1),
            'stage': stage,
            'description': description
        }


class KtVCalculator:
    """
    Kt/V Calculator for hemodialysis adequacy
    """
    
    def calculate(self, pre_bun, post_bun, dialysis_time, ultrafiltration, post_weight):
        """
        Calculate Kt/V using Daugirdas II formula
        
        Parameters:
        - pre_bun: Pre-dialysis BUN (mg/dL)
        - post_bun: Post-dialysis BUN (mg/dL)
        - dialysis_time: Dialysis session time (hours)
        - ultrafiltration: Ultrafiltration volume (liters)
        - post_weight: Post-dialysis weight (kg)
        
        Returns:
        - Dictionary with Kt/V and adequacy assessment
        """
        if pre_bun <= 0 or post_bun <= 0:
            raise ValueError("BUN pré e pós devem ser maiores que zero")
        
        # Daugirdas II formula
        r = post_bun / pre_bun
        
        ktv = -np.log(r - 0.008 * dialysis_time) + (4 - 3.5 * r) * (ultrafiltration / post_weight)
        
        # Assessment
        if ktv >= 1.4:
            adequacy = "Adequada"
            recommendation = "Diálise adequada segundo guidelines KDOQI"
        elif ktv >= 1.2:
            adequacy = "Limítrofe"
            recommendation = "Considerar otimização dos parâmetros de diálise"
        else:
            adequacy = "Inadequada"
            recommendation = "Ajuste urgente necessário - aumentar tempo ou fluxo"
        
        return {
            'ktv': round(ktv, 2),
            'adequacy': adequacy,
            'recommendation': recommendation
        }
