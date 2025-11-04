"""
Validation script for PREVENT calculator
This script performs basic validation of the calculator logic
"""

def validate_calculator_structure():
    """Validate that the calculator module has correct structure"""
    print("Validating PREVENT Calculator structure...")
    
    # Check if file exists
    import os
    if not os.path.exists('prevent_calculator.py'):
        print("❌ prevent_calculator.py not found")
        return False
    
    print("✅ prevent_calculator.py exists")
    
    # Check if file has correct syntax
    try:
        with open('prevent_calculator.py', 'r') as f:
            code = f.read()
            compile(code, 'prevent_calculator.py', 'exec')
        print("✅ Python syntax is valid")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False
    
    # Check for required components
    required_components = [
        'class PREVENTCalculator',
        'def calculate_risk_score',
        'def _categorize_risk',
        'def get_recommendations'
    ]
    
    for component in required_components:
        if component in code:
            print(f"✅ Found: {component}")
        else:
            print(f"❌ Missing: {component}")
            return False
    
    # Check for required parameters in calculate_risk_score
    required_params = [
        'age', 'sex', 'race', 'total_cholesterol', 
        'hdl_cholesterol', 'sbp', 'on_bp_meds', 
        'diabetes', 'smoker'
    ]
    
    for param in required_params:
        if param in code:
            print(f"✅ Parameter: {param}")
        else:
            print(f"❌ Missing parameter: {param}")
            return False
    
    return True


def validate_app_structure():
    """Validate that the Streamlit app has correct structure"""
    print("\nValidating Streamlit App structure...")
    
    import os
    if not os.path.exists('app.py'):
        print("❌ app.py not found")
        return False
    
    print("✅ app.py exists")
    
    try:
        with open('app.py', 'r') as f:
            code = f.read()
            compile(code, 'app.py', 'exec')
        print("✅ Python syntax is valid")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False
    
    # Check for required Streamlit components
    required_components = [
        'import streamlit',
        'st.set_page_config',
        'st.title',
        'PREVENTCalculator',
        'calculate_risk_score'
    ]
    
    for component in required_components:
        if component in code:
            print(f"✅ Found: {component}")
        else:
            print(f"❌ Missing: {component}")
            return False
    
    return True


def validate_requirements():
    """Validate requirements.txt"""
    print("\nValidating requirements.txt...")
    
    import os
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    print("✅ requirements.txt exists")
    
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    required_packages = ['streamlit', 'pandas', 'numpy', 'plotly']
    
    for package in required_packages:
        if package in requirements:
            print(f"✅ Package: {package}")
        else:
            print(f"❌ Missing package: {package}")
            return False
    
    return True


def validate_documentation():
    """Validate documentation files"""
    print("\nValidating documentation...")
    
    import os
    
    # Check README
    if os.path.exists('README.md'):
        print("✅ README.md exists")
        with open('README.md', 'r') as f:
            content = f.read()
            if len(content) > 100:
                print("✅ README.md has content")
            else:
                print("⚠️ README.md is too short")
    else:
        print("❌ README.md not found")
        return False
    
    # Check .gitignore
    if os.path.exists('.gitignore'):
        print("✅ .gitignore exists")
    else:
        print("⚠️ .gitignore not found (optional)")
    
    return True


def main():
    """Run all validations"""
    print("=" * 60)
    print("PREVENT Calculator Validation")
    print("=" * 60)
    
    results = {
        'Calculator Structure': validate_calculator_structure(),
        'App Structure': validate_app_structure(),
        'Requirements': validate_requirements(),
        'Documentation': validate_documentation()
    }
    
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    for test, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test}: {status}")
    
    print("=" * 60)
    
    if all(results.values()):
        print("\n🎉 All validations passed!")
        print("\nNext steps:")
        print("1. Deploy to Streamlit Cloud")
        print("2. Test the application in browser")
        print("3. Share with medical professionals")
        return 0
    else:
        print("\n⚠️ Some validations failed. Please fix the issues above.")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
