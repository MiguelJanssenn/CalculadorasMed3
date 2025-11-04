"""
Example usage of PREVENT Calculator
Demonstrates how to use the calculator with different patient scenarios
"""

try:
    from prevent_calculator import PREVENTCalculator
    IMPORTS_AVAILABLE = True
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install -r requirements.txt")
    IMPORTS_AVAILABLE = False
    exit(1)


def example_low_risk_patient():
    """Example: Low risk patient"""
    print("\n" + "="*60)
    print("Exemplo 1: Paciente de Baixo Risco")
    print("="*60)
    
    calculator = PREVENTCalculator()
    
    # Patient data
    print("\nDados do Paciente:")
    print("- Mulher, 45 anos, branca")
    print("- Colesterol total: 160 mg/dL")
    print("- HDL: 70 mg/dL")
    print("- PA: 110/70 mmHg")
    print("- Não usa anti-hipertensivos")
    print("- Não diabética")
    print("- Não fumante")
    
    result = calculator.calculate_risk_score(
        age=45,
        sex='F',
        race='white',
        total_cholesterol=160,
        hdl_cholesterol=70,
        sbp=110,
        on_bp_meds=False,
        diabetes=False,
        smoker=False
    )
    
    print("\nResultados:")
    print(f"- Risco em 10 anos: {result['10_year_risk']}%")
    print(f"- Risco em 30 anos: {result['30_year_risk']}%")
    print(f"- Categoria: {result['risk_category']}")
    
    print("\nRecomendações:")
    recommendations = calculator.get_recommendations(result['risk_category'], result['10_year_risk'])
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")


def example_high_risk_patient():
    """Example: High risk patient"""
    print("\n" + "="*60)
    print("Exemplo 2: Paciente de Alto Risco")
    print("="*60)
    
    calculator = PREVENTCalculator()
    
    # Patient data
    print("\nDados do Paciente:")
    print("- Homem, 70 anos, branco")
    print("- Colesterol total: 280 mg/dL")
    print("- HDL: 35 mg/dL")
    print("- PA: 160/95 mmHg")
    print("- Em uso de anti-hipertensivos")
    print("- Diabético")
    print("- Fumante")
    
    result = calculator.calculate_risk_score(
        age=70,
        sex='M',
        race='white',
        total_cholesterol=280,
        hdl_cholesterol=35,
        sbp=160,
        on_bp_meds=True,
        diabetes=True,
        smoker=True
    )
    
    print("\nResultados:")
    print(f"- Risco em 10 anos: {result['10_year_risk']}%")
    print(f"- Risco em 30 anos: {result['30_year_risk']}%")
    print(f"- Categoria: {result['risk_category']}")
    
    print("\nRecomendações:")
    recommendations = calculator.get_recommendations(result['risk_category'], result['10_year_risk'])
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")


def example_intermediate_risk_patient():
    """Example: Intermediate risk patient"""
    print("\n" + "="*60)
    print("Exemplo 3: Paciente de Risco Intermediário")
    print("="*60)
    
    calculator = PREVENTCalculator()
    
    # Patient data
    print("\nDados do Paciente:")
    print("- Homem, 55 anos, hispânico")
    print("- Colesterol total: 220 mg/dL")
    print("- HDL: 45 mg/dL")
    print("- PA: 140/90 mmHg")
    print("- Não usa anti-hipertensivos")
    print("- Diabético")
    print("- Não fumante")
    
    result = calculator.calculate_risk_score(
        age=55,
        sex='M',
        race='hispanic',
        total_cholesterol=220,
        hdl_cholesterol=45,
        sbp=140,
        on_bp_meds=False,
        diabetes=True,
        smoker=False
    )
    
    print("\nResultados:")
    print(f"- Risco em 10 anos: {result['10_year_risk']}%")
    print(f"- Risco em 30 anos: {result['30_year_risk']}%")
    print(f"- Categoria: {result['risk_category']}")
    
    print("\nRecomendações:")
    recommendations = calculator.get_recommendations(result['risk_category'], result['10_year_risk'])
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")


def example_with_kidney_disease():
    """Example: Patient with reduced kidney function"""
    print("\n" + "="*60)
    print("Exemplo 4: Paciente com Função Renal Reduzida")
    print("="*60)
    
    calculator = PREVENTCalculator()
    
    # Patient data
    print("\nDados do Paciente:")
    print("- Homem, 62 anos, negro")
    print("- Colesterol total: 200 mg/dL")
    print("- HDL: 50 mg/dL")
    print("- PA: 135/85 mmHg")
    print("- Em uso de anti-hipertensivos")
    print("- Não diabético")
    print("- Não fumante")
    print("- eGFR: 45 mL/min/1.73m²")
    
    result = calculator.calculate_risk_score(
        age=62,
        sex='M',
        race='black',
        total_cholesterol=200,
        hdl_cholesterol=50,
        sbp=135,
        on_bp_meds=True,
        diabetes=False,
        smoker=False,
        egfr=45
    )
    
    print("\nResultados:")
    print(f"- Risco em 10 anos: {result['10_year_risk']}%")
    print(f"- Risco em 30 anos: {result['30_year_risk']}%")
    print(f"- Categoria: {result['risk_category']}")
    
    print("\nRecomendações:")
    recommendations = calculator.get_recommendations(result['risk_category'], result['10_year_risk'])
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")
    
    print("\nNota: A função renal reduzida aumenta o risco cardiovascular.")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("PREVENT Calculator - Exemplos de Uso")
    print("="*60)
    
    if not IMPORTS_AVAILABLE:
        return
    
    # Run all examples
    example_low_risk_patient()
    example_high_risk_patient()
    example_intermediate_risk_patient()
    example_with_kidney_disease()
    
    print("\n" + "="*60)
    print("Todos os exemplos foram executados com sucesso!")
    print("="*60)
    print("\nPara usar a interface gráfica, execute:")
    print("  streamlit run app.py")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
