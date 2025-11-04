"""
Gastroenterology Calculators
Contains FIB-4, MELD, and Child-Pugh calculators
"""
import numpy as np


class FIB4Calculator:
    """
    FIB-4 Calculator for liver fibrosis assessment
    Formula: FIB-4 = (Age × AST) / (Platelet count × √ALT)
    """
    
    def calculate(self, age, ast, alt, platelets):
        """
        Calculate FIB-4 score
        
        Parameters:
        - age: Age in years
        - ast: AST (U/L)
        - alt: ALT (U/L)
        - platelets: Platelet count (×10^9/L)
        
        Returns:
        - Dictionary with FIB-4 score and interpretation
        """
        if platelets <= 0 or alt <= 0:
            raise ValueError("Plaquetas e ALT devem ser maiores que zero")
        
        fib4_score = (age * ast) / (platelets * np.sqrt(alt))
        
        # Interpretation
        if fib4_score < 1.45:
            interpretation = "F0-F1 (Baixa probabilidade de fibrose avançada)"
            risk = "Baixo"
        elif fib4_score <= 3.25:
            interpretation = "Indeterminado (Considerar outros métodos)"
            risk = "Intermediário"
        else:
            interpretation = "F3-F4 (Alta probabilidade de fibrose avançada)"
            risk = "Alto"
        
        return {
            'score': round(fib4_score, 2),
            'interpretation': interpretation,
            'risk': risk
        }


class MELDCalculator:
    """
    MELD Score Calculator (Model for End-Stage Liver Disease)
    Used for liver transplant prioritization
    """
    
    def calculate(self, creatinine, bilirubin, inr, dialysis=False):
        """
        Calculate MELD score
        
        Parameters:
        - creatinine: Serum creatinine (mg/dL)
        - bilirubin: Total bilirubin (mg/dL)
        - inr: International Normalized Ratio
        - dialysis: Boolean - on dialysis (treated as creatinine = 4)
        
        Returns:
        - Dictionary with MELD score and interpretation
        """
        # Set minimum values to avoid log errors
        creatinine = max(1.0, creatinine)
        bilirubin = max(1.0, bilirubin)
        inr = max(1.0, inr)
        
        # If on dialysis, creatinine is set to 4
        if dialysis:
            creatinine = 4.0
        
        # MELD formula
        meld_score = 3.78 * np.log(bilirubin) + 11.2 * np.log(inr) + 9.57 * np.log(creatinine) + 6.43
        
        # Round to integer and cap at 40
        meld_score = min(40, max(6, int(round(meld_score))))
        
        # Interpretation
        if meld_score < 10:
            interpretation = "Doença hepática compensada"
            mortality = "<2% mortalidade em 3 meses"
        elif meld_score < 20:
            interpretation = "Doença hepática moderada"
            mortality = "6-20% mortalidade em 3 meses"
        elif meld_score < 30:
            interpretation = "Doença hepática grave"
            mortality = "20-50% mortalidade em 3 meses"
        else:
            interpretation = "Doença hepática muito grave"
            mortality = ">50% mortalidade em 3 meses"
        
        return {
            'score': meld_score,
            'interpretation': interpretation,
            'mortality': mortality
        }


class ChildPughCalculator:
    """
    Child-Pugh Score Calculator for cirrhosis severity
    """
    
    def calculate(self, bilirubin, albumin, inr, ascites, encephalopathy):
        """
        Calculate Child-Pugh score
        
        Parameters:
        - bilirubin: Total bilirubin (mg/dL)
        - albumin: Serum albumin (g/dL)
        - inr: International Normalized Ratio
        - ascites: 'none', 'mild', 'moderate_severe'
        - encephalopathy: 'none', 'grade_1_2', 'grade_3_4'
        
        Returns:
        - Dictionary with Child-Pugh score and class
        """
        score = 0
        
        # Bilirubin points
        if bilirubin < 2:
            score += 1
        elif bilirubin <= 3:
            score += 2
        else:
            score += 3
        
        # Albumin points
        if albumin > 3.5:
            score += 1
        elif albumin >= 2.8:
            score += 2
        else:
            score += 3
        
        # INR points
        if inr < 1.7:
            score += 1
        elif inr <= 2.3:
            score += 2
        else:
            score += 3
        
        # Ascites points
        ascites_map = {'none': 1, 'mild': 2, 'moderate_severe': 3}
        score += ascites_map.get(ascites, 1)
        
        # Encephalopathy points
        enceph_map = {'none': 1, 'grade_1_2': 2, 'grade_3_4': 3}
        score += enceph_map.get(encephalopathy, 1)
        
        # Determine class
        if score <= 6:
            child_class = "A"
            interpretation = "Doença hepática bem compensada"
            survival_1yr = "100%"
            survival_2yr = "85%"
        elif score <= 9:
            child_class = "B"
            interpretation = "Função hepática significativamente comprometida"
            survival_1yr = "80%"
            survival_2yr = "60%"
        else:
            child_class = "C"
            interpretation = "Doença hepática descompensada"
            survival_1yr = "45%"
            survival_2yr = "35%"
        
        return {
            'score': score,
            'class': child_class,
            'interpretation': interpretation,
            'survival_1_year': survival_1yr,
            'survival_2_year': survival_2yr
        }
