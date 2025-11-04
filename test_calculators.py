"""
Unit tests for additional calculators
"""
import unittest
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from calculators.gastro import FIB4Calculator, MELDCalculator, ChildPughCalculator
    from calculators.nephro import eGFRCalculator, KtVCalculator
    from calculators.endocrino import BMICalculator, HOMAIRCalculator, HOMABetaCalculator
    IMPORTS_AVAILABLE = True
except ImportError as e:
    IMPORTS_AVAILABLE = False
    print(f"Warning: Cannot import dependencies. Tests will be skipped. Error: {e}")


@unittest.skipUnless(IMPORTS_AVAILABLE, "Dependencies not available")
class TestGastroCalculators(unittest.TestCase):
    """Test cases for Gastroenterology Calculators"""
    
    def test_fib4_calculator(self):
        """Test FIB-4 calculation"""
        calc = FIB4Calculator()
        result = calc.calculate(age=50, ast=40, alt=35, platelets=200)
        
        self.assertIn('score', result)
        self.assertIn('risk', result)
        self.assertGreater(result['score'], 0)
    
    def test_meld_calculator(self):
        """Test MELD calculation"""
        calc = MELDCalculator()
        result = calc.calculate(creatinine=1.5, bilirubin=2.0, inr=1.2)
        
        self.assertIn('score', result)
        self.assertGreaterEqual(result['score'], 6)
        self.assertLessEqual(result['score'], 40)
    
    def test_childpugh_calculator(self):
        """Test Child-Pugh calculation"""
        calc = ChildPughCalculator()
        result = calc.calculate(
            bilirubin=1.5,
            albumin=3.8,
            inr=1.2,
            ascites='none',
            encephalopathy='none'
        )
        
        self.assertIn('score', result)
        self.assertIn('class', result)
        self.assertIn(result['class'], ['A', 'B', 'C'])


@unittest.skipUnless(IMPORTS_AVAILABLE, "Dependencies not available")
class TestNephroCalculators(unittest.TestCase):
    """Test cases for Nephrology Calculators"""
    
    def test_egfr_calculator(self):
        """Test eGFR calculation"""
        calc = eGFRCalculator()
        result = calc.calculate(creatinine=1.0, age=50, sex='M')
        
        self.assertIn('egfr', result)
        self.assertIn('stage', result)
        self.assertGreater(result['egfr'], 0)
    
    def test_ktv_calculator(self):
        """Test Kt/V calculation"""
        calc = KtVCalculator()
        result = calc.calculate(
            pre_bun=60,
            post_bun=20,
            dialysis_time=4.0,
            ultrafiltration=2.0,
            post_weight=70
        )
        
        self.assertIn('ktv', result)
        self.assertIn('adequacy', result)
        self.assertGreater(result['ktv'], 0)


@unittest.skipUnless(IMPORTS_AVAILABLE, "Dependencies not available")
class TestEndocrinoCalculators(unittest.TestCase):
    """Test cases for Endocrinology Calculators"""
    
    def test_bmi_calculator(self):
        """Test BMI calculation"""
        calc = BMICalculator()
        result = calc.calculate(weight=70, height=170)
        
        self.assertIn('bmi', result)
        self.assertIn('classification', result)
        self.assertGreater(result['bmi'], 0)
    
    def test_homa_ir_calculator(self):
        """Test HOMA-IR calculation"""
        calc = HOMAIRCalculator()
        result = calc.calculate(fasting_glucose=100, fasting_insulin=10)
        
        self.assertIn('homa_ir', result)
        self.assertIn('interpretation', result)
        self.assertGreater(result['homa_ir'], 0)
    
    def test_homa_beta_calculator(self):
        """Test HOMA-Beta calculation"""
        calc = HOMABetaCalculator()
        result = calc.calculate(fasting_glucose=100, fasting_insulin=10)
        
        self.assertIn('homa_beta', result)
        self.assertIn('interpretation', result)
        self.assertGreaterEqual(result['homa_beta'], 0)


if __name__ == '__main__':
    if IMPORTS_AVAILABLE:
        unittest.main()
    else:
        print("Skipping tests - dependencies not available")
