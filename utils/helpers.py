"""
Helper Utilities
Common helper functions for the scientific calculator application
"""

import math
import numpy as np
from typing import Union, List, Dict, Any, Optional, Tuple
import json
import base64
import io
from datetime import datetime


class HelperFunctions:
    """Collection of helper functions for calculator operations"""
    
    @staticmethod
    def degrees_to_radians(degrees: float) -> float:
        """Convert degrees to radians"""
        return math.radians(degrees)
    
    @staticmethod
    def radians_to_degrees(radians: float) -> float:
        """Convert radians to degrees"""
        return math.degrees(radians)
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calculate factorial with validation"""
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if n > 170:
            raise ValueError("Factorial too large for computation")
        return math.factorial(n)
    
    @staticmethod
    def combinations(n: int, k: int) -> int:
        """Calculate combinations (n choose k)"""
        if n < 0 or k < 0:
            raise ValueError("Combinations not defined for negative numbers")
        if k > n:
            return 0
        return math.comb(n, k)
    
    @staticmethod
    def permutations(n: int, k: int) -> int:
        """Calculate permutations"""
        if n < 0 or k < 0:
            raise ValueError("Permutations not defined for negative numbers")
        if k > n:
            return 0
        return math.perm(n, k)
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Calculate greatest common divisor"""
        return math.gcd(a, b)
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Calculate least common multiple"""
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // math.gcd(a, b)
    
    @staticmethod
    def prime_factors(n: int) -> List[int]:
        """Find prime factors of a number"""
        if n <= 1:
            return []
        
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        
        if n > 1:
            factors.append(n)
        
        return factors
    
    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if a number is prime"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        
        return True
    
    @staticmethod
    def fibonacci_sequence(n: int) -> List[int]:
        """Generate Fibonacci sequence up to n terms"""
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        
        sequence = [0, 1]
        for i in range(2, n):
            sequence.append(sequence[i-1] + sequence[i-2])
        
        return sequence
    
    @staticmethod
    def unit_conversion(value: float, from_unit: str, to_unit: str) -> float:
        """Convert between different units"""
        # Length conversions (to meters)
        length_conversions = {
            'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'km': 1000.0,
            'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mi': 1609.34
        }
        
        # Weight conversions (to kilograms)
        weight_conversions = {
            'mg': 0.000001, 'g': 0.001, 'kg': 1.0, 'lb': 0.453592, 'oz': 0.0283495
        }
        
        # Temperature conversions
        temp_conversions = {
            'c': 'celsius', 'f': 'fahrenheit', 'k': 'kelvin'
        }
        
        # Handle temperature conversions
        if from_unit.lower() in temp_conversions and to_unit.lower() in temp_conversions:
            return HelperFunctions._convert_temperature(value, from_unit.lower(), to_unit.lower())
        
        # Handle length conversions
        if from_unit.lower() in length_conversions and to_unit.lower() in length_conversions:
            # Convert to meters first, then to target unit
            meters = value * length_conversions[from_unit.lower()]
            return meters / length_conversions[to_unit.lower()]
        
        # Handle weight conversions
        if from_unit.lower() in weight_conversions and to_unit.lower() in weight_conversions:
            # Convert to kilograms first, then to target unit
            kg = value * weight_conversions[from_unit.lower()]
            return kg / weight_conversions[to_unit.lower()]
        
        raise ValueError(f"Unsupported unit conversion: {from_unit} to {to_unit}")
    
    @staticmethod
    def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature between Celsius, Fahrenheit, and Kelvin"""
        # Convert to Celsius first
        if from_unit == 'f':
            celsius = (value - 32) * 5/9
        elif from_unit == 'k':
            celsius = value - 273.15
        else:  # celsius
            celsius = value
        
        # Convert from Celsius to target unit
        if to_unit == 'f':
            return celsius * 9/5 + 32
        elif to_unit == 'k':
            return celsius + 273.15
        else:  # celsius
            return celsius
    
    @staticmethod
    def generate_random_data(distribution: str, size: int, **params) -> List[float]:
        """Generate random data from various distributions"""
        np.random.seed(params.get('seed', None))
        
        if distribution == 'normal':
            mean = params.get('mean', 0)
            std = params.get('std', 1)
            return np.random.normal(mean, std, size).tolist()
        
        elif distribution == 'uniform':
            low = params.get('low', 0)
            high = params.get('high', 1)
            return np.random.uniform(low, high, size).tolist()
        
        elif distribution == 'exponential':
            scale = params.get('scale', 1)
            return np.random.exponential(scale, size).tolist()
        
        elif distribution == 'poisson':
            lam = params.get('lambda', 1)
            return np.random.poisson(lam, size).tolist()
        
        elif distribution == 'binomial':
            n = params.get('n', 10)
            p = params.get('p', 0.5)
            return np.random.binomial(n, p, size).tolist()
        
        else:
            raise ValueError(f"Unknown distribution: {distribution}")
    
    @staticmethod
    def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate Euclidean distance between two points"""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    @staticmethod
    def calculate_area_circle(radius: float) -> float:
        """Calculate area of a circle"""
        return math.pi * radius**2
    
    @staticmethod
    def calculate_area_rectangle(length: float, width: float) -> float:
        """Calculate area of a rectangle"""
        return length * width
    
    @staticmethod
    def calculate_area_triangle(base: float, height: float) -> float:
        """Calculate area of a triangle"""
        return 0.5 * base * height
    
    @staticmethod
    def calculate_volume_sphere(radius: float) -> float:
        """Calculate volume of a sphere"""
        return (4/3) * math.pi * radius**3
    
    @staticmethod
    def calculate_volume_cylinder(radius: float, height: float) -> float:
        """Calculate volume of a cylinder"""
        return math.pi * radius**2 * height
    
    @staticmethod
    def solve_quadratic(a: float, b: float, c: float) -> Tuple[complex, complex]:
        """Solve quadratic equation ax² + bx + c = 0"""
        discriminant = b**2 - 4*a*c
        
        if discriminant >= 0:
            sqrt_disc = math.sqrt(discriminant)
            x1 = (-b + sqrt_disc) / (2*a)
            x2 = (-b - sqrt_disc) / (2*a)
        else:
            sqrt_disc = math.sqrt(-discriminant)
            x1 = complex(-b/(2*a), sqrt_disc/(2*a))
            x2 = complex(-b/(2*a), -sqrt_disc/(2*a))
        
        return x1, x2
    
    @staticmethod
    def parse_expression(expression: str) -> Dict[str, Any]:
        """Parse mathematical expression and extract components"""
        try:
            # Remove whitespace
            clean_expr = expression.replace(' ', '')
            
            # Find variables
            import re
            variables = set(re.findall(r'[a-zA-Z]+', clean_expr))
            
            # Find numbers
            numbers = [float(x) for x in re.findall(r'\d+\.?\d*', clean_expr)]
            
            # Find operators
            operators = re.findall(r'[+\-*/^]', clean_expr)
            
            # Find functions
            functions = re.findall(r'[a-zA-Z]+\s*\(', clean_expr)
            functions = [f.replace('(', '') for f in functions]
            
            return {
                'expression': expression,
                'variables': list(variables),
                'numbers': numbers,
                'operators': operators,
                'functions': functions,
                'length': len(expression)
            }
            
        except Exception as e:
            return {
                'expression': expression,
                'error': str(e)
            }
    
    @staticmethod
    def format_time_duration(seconds: float) -> str:
        """Format duration in seconds to human-readable format"""
        if seconds < 1:
            return f"{seconds*1000:.2f} ms"
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs:.2f}s"
        elif minutes > 0:
            return f"{minutes}m {secs:.2f}s"
        else:
            return f"{secs:.2f}s"
    
    @staticmethod
    def create_data_summary(data: List[float]) -> Dict[str, Any]:
        """Create comprehensive summary of numeric data"""
        try:
            data_array = np.array(data)
            
            return {
                'count': len(data),
                'sum': float(np.sum(data_array)),
                'mean': float(np.mean(data_array)),
                'median': float(np.median(data_array)),
                'std': float(np.std(data_array)),
                'var': float(np.var(data_array)),
                'min': float(np.min(data_array)),
                'max': float(np.max(data_array)),
                'range': float(np.max(data_array) - np.min(data_array)),
                'q1': float(np.percentile(data_array, 25)),
                'q3': float(np.percentile(data_array, 75)),
                'iqr': float(np.percentile(data_array, 75) - np.percentile(data_array, 25))
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def validate_matrix_dimensions(matrix1: List[List], matrix2: List[List]) -> Dict[str, Any]:
        """Validate matrix dimensions for operations"""
        try:
            rows1, cols1 = len(matrix1), len(matrix1[0])
            rows2, cols2 = len(matrix2), len(matrix2[0])
            
            return {
                'matrix1_shape': (rows1, cols1),
                'matrix2_shape': (rows2, cols2),
                'can_add': (rows1 == rows2 and cols1 == cols2),
                'can_multiply': (cols1 == rows2),
                'can_element_wise': (rows1 == rows2 and cols1 == cols2)
            }
            
        except Exception as e:
            return {'error': str(e)}


def create_helper() -> HelperFunctions:
    """Factory function to create helper functions instance"""
    return HelperFunctions()


