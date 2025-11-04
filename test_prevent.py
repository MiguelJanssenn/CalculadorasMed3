"""
Unit tests for PREVENT Calculator
Tests the cardiovascular risk calculation logic
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from prevent_calculator import PREVENTCalculator
    IMPORTS_AVAILABLE = True
except ImportError:
    IMPORTS_AVAILABLE = False
    print("Warning: Cannot import dependencies. Tests will be skipped.")


@unittest.skipUnless(IMPORTS_AVAILABLE, "Dependencies not available")
class TestPREVENTCalculator(unittest.TestCase):
    """Test cases for PREVENT Calculator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calculator = PREVENTCalculator()
    
    def test_basic_calculation(self):
        """Test basic risk calculation"""
        result = self.calculator.calculate_risk_score(
            age=55,
            sex='M',
            race='white',
            total_cholesterol=200,
            hdl_cholesterol=50,
            sbp=120,
            on_bp_meds=False,
            diabetes=False,
            smoker=False
        )
        
        self.assertIn('10_year_risk', result)
        self.assertIn('30_year_risk', result)
        self.assertIn('risk_category', result)
        self.assertGreaterEqual(result['10_year_risk'], 0)
        self.assertLessEqual(result['10_year_risk'], 100)
    
    def test_high_risk_patient(self):
        """Test calculation for high-risk patient"""
        result = self.calculator.calculate_risk_score(
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
        
        # High risk patients should have higher risk scores
        self.assertGreater(result['10_year_risk'], 5)
        self.assertIn(result['risk_category'], ['Intermediário', 'Alto'])
    
    def test_low_risk_patient(self):
        """Test calculation for low-risk patient"""
        result = self.calculator.calculate_risk_score(
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
        
        # Low risk patients should have lower risk scores
        self.assertLess(result['10_year_risk'], 20)
    
    def test_age_validation(self):
        """Test age validation"""
        with self.assertRaises(ValueError):
            self.calculator.calculate_risk_score(
                age=35,  # Too young
                sex='M',
                race='white',
                total_cholesterol=200,
                hdl_cholesterol=50,
                sbp=120,
                on_bp_meds=False,
                diabetes=False,
                smoker=False
            )
        
        with self.assertRaises(ValueError):
            self.calculator.calculate_risk_score(
                age=85,  # Too old
                sex='M',
                race='white',
                total_cholesterol=200,
                hdl_cholesterol=50,
                sbp=120,
                on_bp_meds=False,
                diabetes=False,
                smoker=False
            )
    
    def test_sex_validation(self):
        """Test sex validation"""
        with self.assertRaises(ValueError):
            self.calculator.calculate_risk_score(
                age=55,
                sex='X',  # Invalid sex
                race='white',
                total_cholesterol=200,
                hdl_cholesterol=50,
                sbp=120,
                on_bp_meds=False,
                diabetes=False,
                smoker=False
            )
    
    def test_with_egfr(self):
        """Test calculation with eGFR"""
        result = self.calculator.calculate_risk_score(
            age=55,
            sex='M',
            race='white',
            total_cholesterol=200,
            hdl_cholesterol=50,
            sbp=120,
            on_bp_meds=False,
            diabetes=False,
            smoker=False,
            egfr=45  # Reduced kidney function
        )
        
        self.assertIn('10_year_risk', result)
        # Risk should be calculated successfully with eGFR
        self.assertGreaterEqual(result['10_year_risk'], 0)
    
    def test_risk_categorization(self):
        """Test risk categorization logic"""
        self.assertEqual(self.calculator._categorize_risk(3), 'Baixo')
        self.assertEqual(self.calculator._categorize_risk(6), 'Limítrofe')
        self.assertEqual(self.calculator._categorize_risk(15), 'Intermediário')
        self.assertEqual(self.calculator._categorize_risk(25), 'Alto')
    
    def test_recommendations(self):
        """Test that recommendations are provided"""
        recommendations = self.calculator.get_recommendations('Alto', 25)
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        recommendations = self.calculator.get_recommendations('Baixo', 3)
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)


if __name__ == '__main__':
    if IMPORTS_AVAILABLE:
        unittest.main()
    else:
        print("Skipping tests - dependencies not available")
