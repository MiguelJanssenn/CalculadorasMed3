"""
Endocrinology Calculators
Contains BMI, HOMA-IR, and HOMA-beta calculators
"""
import numpy as np


class BMICalculator:
    """
    BMI (Body Mass Index) Calculator
    """
    
    def calculate(self, weight, height):
        """
        Calculate BMI
        
        Parameters:
        - weight: Weight in kg
        - height: Height in cm
        
        Returns:
        - Dictionary with BMI and classification
        """
        if height <= 0 or weight <= 0:
            raise ValueError("Peso e altura devem ser maiores que zero")
        
        # Convert height to meters
        height_m = height / 100
        
        # Calculate BMI
        bmi = weight / (height_m ** 2)
        
        # WHO Classification
        if bmi < 18.5:
            classification = "Baixo peso"
            risk = "Baixo"
        elif bmi < 25:
            classification = "Peso normal"
            risk = "Normal"
        elif bmi < 30:
            classification = "Sobrepeso"
            risk = "Aumentado"
        elif bmi < 35:
            classification = "Obesidade Grau I"
            risk = "Moderado"
        elif bmi < 40:
            classification = "Obesidade Grau II"
            risk = "Alto"
        else:
            classification = "Obesidade Grau III"
            risk = "Muito Alto"
        
        return {
            'bmi': round(bmi, 1),
            'classification': classification,
            'risk': risk
        }


class HOMAIRCalculator:
    """
    HOMA-IR Calculator (Homeostatic Model Assessment for Insulin Resistance)
    """
    
    def calculate(self, fasting_glucose, fasting_insulin):
        """
        Calculate HOMA-IR
        
        Parameters:
        - fasting_glucose: Fasting glucose (mg/dL)
        - fasting_insulin: Fasting insulin (μU/mL)
        
        Returns:
        - Dictionary with HOMA-IR and interpretation
        """
        if fasting_glucose <= 0 or fasting_insulin <= 0:
            raise ValueError("Glicemia e insulina devem ser maiores que zero")
        
        # HOMA-IR formula
        homa_ir = (fasting_glucose * fasting_insulin) / 405
        
        # Interpretation
        if homa_ir < 2.5:
            interpretation = "Normal"
            recommendation = "Sem resistência insulínica significativa"
        elif homa_ir < 3.8:
            interpretation = "Resistência insulínica leve"
            recommendation = "Considerar modificações do estilo de vida"
        else:
            interpretation = "Resistência insulínica significativa"
            recommendation = "Avaliação endocrinológica e intervenção terapêutica"
        
        return {
            'homa_ir': round(homa_ir, 2),
            'interpretation': interpretation,
            'recommendation': recommendation
        }


class HOMABetaCalculator:
    """
    HOMA-Beta Calculator (Homeostatic Model Assessment for Beta Cell Function)
    """
    
    def calculate(self, fasting_glucose, fasting_insulin):
        """
        Calculate HOMA-Beta
        
        Parameters:
        - fasting_glucose: Fasting glucose (mg/dL)
        - fasting_insulin: Fasting insulin (μU/mL)
        
        Returns:
        - Dictionary with HOMA-Beta and interpretation
        """
        if fasting_glucose <= 0 or fasting_insulin <= 0:
            raise ValueError("Glicemia e insulina devem ser maiores que zero")
        
        # Convert glucose from mg/dL to mmol/L for formula
        glucose_mmol = fasting_glucose / 18
        
        # HOMA-Beta formula
        homa_beta = (20 * fasting_insulin) / (glucose_mmol - 3.5)
        
        # Ensure positive value
        homa_beta = max(0, homa_beta)
        
        # Interpretation (normal range: 50-150%)
        if homa_beta < 50:
            interpretation = "Função de células beta reduzida"
            recommendation = "Avaliação para possível insuficiência pancreática"
        elif homa_beta <= 150:
            interpretation = "Função de células beta normal"
            recommendation = "Função pancreática preservada"
        else:
            interpretation = "Função de células beta aumentada"
            recommendation = "Pode indicar hiperinsulinemia compensatória"
        
        return {
            'homa_beta': round(homa_beta, 1),
            'interpretation': interpretation,
            'recommendation': recommendation
        }
