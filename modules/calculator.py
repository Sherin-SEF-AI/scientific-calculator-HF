"""
Basic Calculator Module
Handles fundamental arithmetic operations and basic mathematical functions
"""

import math
import operator
from typing import Union, List, Dict, Any
import numpy as np


class BasicCalculator:
    """Basic calculator with fundamental operations"""
    
    def __init__(self):
        self.history = []
        self.memory = {}
        self.constants = {
            'π': math.pi,
            'e': math.e,
            'phi': (1 + math.sqrt(5)) / 2,  # Golden ratio
            'c': 299792458,  # Speed of light (m/s)
            'h': 6.62607015e-34,  # Planck constant
            'k': 1.380649e-23,  # Boltzmann constant
        }
    
    def calculate(self, expression: str) -> Dict[str, Any]:
        """
        Calculate mathematical expression safely
        
        Args:
            expression: Mathematical expression as string
            
        Returns:
            Dictionary with result, status, and metadata
        """
        try:
            # Replace constants
            for const_name, const_value in self.constants.items():
                expression = expression.replace(const_name, str(const_value))
            
            # Safe evaluation with limited operations
            allowed_names = {
                "__builtins__": {},
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, "sqrt": math.sqrt,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "asin": math.asin, "acos": math.acos, "atan": math.atan,
                "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
                "log": math.log, "log10": math.log10, "exp": math.exp,
                "floor": math.floor, "ceil": math.ceil, "factorial": math.factorial,
                "pi": math.pi, "e": math.e,
            }
            
            result = eval(expression, allowed_names)
            
            # Add to history
            self.history.append({
                'expression': expression,
                'result': result,
                'timestamp': __import__('datetime').datetime.now().isoformat()
            })
            
            return {
                'result': result,
                'status': 'success',
                'expression': expression,
                'formatted_result': self._format_result(result)
            }
            
        except Exception as e:
            return {
                'result': None,
                'status': 'error',
                'error': str(e),
                'expression': expression
            }
    
    def _format_result(self, result: Any) -> str:
        """Format result for display"""
        if isinstance(result, (int, float)):
            if abs(result) > 1e10 or (abs(result) < 1e-10 and result != 0):
                return f"{result:.6e}"
            elif isinstance(result, float) and result.is_integer():
                return str(int(result))
            else:
                return f"{result:.10g}"
        return str(result)
    
    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get calculation history"""
        return self.history[-limit:] if limit else self.history
    
    def clear_history(self):
        """Clear calculation history"""
        self.history = []
    
    def store_memory(self, key: str, value: float):
        """Store value in memory"""
        self.memory[key] = value
    
    def recall_memory(self, key: str) -> float:
        """Recall value from memory"""
        return self.memory.get(key, 0)
    
    def get_memory_keys(self) -> List[str]:
        """Get all memory keys"""
        return list(self.memory.keys())
    
    def clear_memory(self):
        """Clear all memory"""
        self.memory = {}


class ScientificCalculator(BasicCalculator):
    """Extended calculator with scientific functions"""
    
    def __init__(self):
        super().__init__()
        self.extended_functions = {
            'deg_to_rad': lambda x: math.radians(x),
            'rad_to_deg': lambda x: math.degrees(x),
            'sec': lambda x: 1 / math.cos(x),
            'csc': lambda x: 1 / math.sin(x),
            'cot': lambda x: 1 / math.tan(x),
            'asinh': math.asinh,
            'acosh': math.acosh,
            'atanh': math.atanh,
            'log2': math.log2,
            'log1p': math.log1p,
            'expm1': math.expm1,
            'erf': math.erf,
            'erfc': math.erfc,
            'gamma': math.gamma,
            'lgamma': math.lgamma,
        }
    
    def calculate(self, expression: str) -> Dict[str, Any]:
        """Extended calculation with scientific functions"""
        try:
            # Replace constants
            for const_name, const_value in self.constants.items():
                expression = expression.replace(const_name, str(const_value))
            
            # Safe evaluation with extended functions
            allowed_names = {
                "__builtins__": {},
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, "sqrt": math.sqrt,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "asin": math.asin, "acos": math.acos, "atan": math.atan,
                "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
                "log": math.log, "log10": math.log10, "exp": math.exp,
                "floor": math.floor, "ceil": math.ceil, "factorial": math.factorial,
                "pi": math.pi, "e": math.e,
                **self.extended_functions
            }
            
            result = eval(expression, allowed_names)
            
            # Add to history
            self.history.append({
                'expression': expression,
                'result': result,
                'timestamp': __import__('datetime').datetime.now().isoformat()
            })
            
            return {
                'result': result,
                'status': 'success',
                'expression': expression,
                'formatted_result': self._format_result(result)
            }
            
        except Exception as e:
            return {
                'result': None,
                'status': 'error',
                'error': str(e),
                'expression': expression
            }
    
    def solve_equation(self, equation: str, variable: str = 'x') -> Dict[str, Any]:
        """
        Solve simple equations
        
        Args:
            equation: Equation as string (e.g., "2*x + 3 = 7")
            variable: Variable to solve for
            
        Returns:
            Dictionary with solution and status
        """
        try:
            import sympy as sp
            
            # Parse equation
            if '=' in equation:
                left, right = equation.split('=')
                expr = sp.sympify(f"({left}) - ({right})")
            else:
                expr = sp.sympify(equation)
            
            # Solve for variable
            var = sp.Symbol(variable)
            solutions = sp.solve(expr, var)
            
            return {
                'solutions': [float(sol.evalf()) for sol in solutions],
                'status': 'success',
                'equation': equation,
                'variable': variable
            }
            
        except Exception as e:
            return {
                'solutions': [],
                'status': 'error',
                'error': str(e),
                'equation': equation,
                'variable': variable
            }


def create_calculator() -> ScientificCalculator:
    """Factory function to create calculator instance"""
    return ScientificCalculator()
