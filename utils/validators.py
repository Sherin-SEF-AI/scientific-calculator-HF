"""
Input Validation Utilities
Handles validation of mathematical expressions, data inputs, and user parameters
"""

import re
import math
from typing import Union, List, Dict, Any, Optional
import numpy as np


class InputValidator:
    """Comprehensive input validation for calculator operations"""
    
    def __init__(self):
        # Allowed mathematical functions and operations
        self.allowed_functions = {
            'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
            'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh',
            'log', 'log10', 'log2', 'ln', 'exp', 'sqrt',
            'abs', 'floor', 'ceil', 'round', 'factorial',
            'gamma', 'lgamma', 'erf', 'erfc',
            'min', 'max', 'sum', 'pow'
        }
        
        # Mathematical constants
        self.constants = {'pi', 'e', 'phi', 'c', 'h', 'k'}
        
        # Pattern for valid mathematical expressions
        self.expression_pattern = re.compile(
            r'^[0-9+\-*/().\s' + 
            ''.join(self.allowed_functions) + 
            ''.join(self.constants) + 
            r']+$'
        )
    
    def validate_expression(self, expression: str) -> Dict[str, Any]:
        """Validate mathematical expression"""
        try:
            # Basic checks
            if not expression or not expression.strip():
                return {
                    'valid': False,
                    'error': 'Expression cannot be empty'
                }
            
            # Check for balanced parentheses
            if not self._check_balanced_parentheses(expression):
                return {
                    'valid': False,
                    'error': 'Unbalanced parentheses'
                }
            
            # Check for valid characters and functions
            if not self._check_valid_characters(expression):
                return {
                    'valid': False,
                    'error': 'Invalid characters or functions in expression'
                }
            
            # Check for division by zero patterns
            if self._check_division_by_zero(expression):
                return {
                    'valid': False,
                    'error': 'Potential division by zero detected'
                }
            
            return {
                'valid': True,
                'expression': expression.strip()
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Validation error: {str(e)}'
            }
    
    def _check_balanced_parentheses(self, expression: str) -> bool:
        """Check if parentheses are balanced"""
        count = 0
        for char in expression:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
                if count < 0:
                    return False
        return count == 0
    
    def _check_valid_characters(self, expression: str) -> bool:
        """Check for valid characters and function names"""
        # Remove spaces and check pattern
        clean_expr = expression.replace(' ', '')
        
        # Check for invalid characters
        invalid_chars = re.findall(r'[^0-9+\-*/().a-zA-Z]', clean_expr)
        if invalid_chars:
            return False
        
        # Check function names
        function_names = re.findall(r'[a-zA-Z]+', clean_expr)
        for func in function_names:
            if func.lower() not in self.allowed_functions and func.lower() not in self.constants:
                return False
        
        return True
    
    def _check_division_by_zero(self, expression: str) -> bool:
        """Check for obvious division by zero patterns"""
        # Look for patterns like "/0", "/0.0", "/0)", etc.
        division_zero_patterns = [
            r'/\s*0\s*[^.]',
            r'/\s*0\s*\)',
            r'/\s*0\s*$',
            r'/\s*0\.0+\s*[^0-9]'
        ]
        
        for pattern in division_zero_patterns:
            if re.search(pattern, expression):
                return True
        
        return False
    
    def validate_matrix_data(self, data: Union[List[List], str]) -> Dict[str, Any]:
        """Validate matrix data"""
        try:
            if isinstance(data, str):
                import json
                data = json.loads(data)
            
            if not isinstance(data, list):
                return {
                    'valid': False,
                    'error': 'Matrix data must be a list of lists'
                }
            
            if not data:
                return {
                    'valid': False,
                    'error': 'Matrix cannot be empty'
                }
            
            # Check if all rows are lists
            for i, row in enumerate(data):
                if not isinstance(row, list):
                    return {
                        'valid': False,
                        'error': f'Row {i} must be a list'
                    }
            
            # Check dimensions consistency
            num_cols = len(data[0])
            for i, row in enumerate(data):
                if len(row) != num_cols:
                    return {
                        'valid': False,
                        'error': f'Inconsistent row lengths. Row {i} has {len(row)} columns, expected {num_cols}'
                    }
            
            # Check if all elements are numeric
            for i, row in enumerate(data):
                for j, element in enumerate(row):
                    try:
                        float(element)
                    except (ValueError, TypeError):
                        return {
                            'valid': False,
                            'error': f'Non-numeric element at row {i}, column {j}: {element}'
                        }
            
            return {
                'valid': True,
                'shape': (len(data), num_cols),
                'data': data
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Matrix validation error: {str(e)}'
            }
    
    def validate_numeric_data(self, data: Union[List, str], 
                            min_length: int = 1,
                            max_length: int = None) -> Dict[str, Any]:
        """Validate numeric data array"""
        try:
            if isinstance(data, str):
                import json
                data = json.loads(data)
            
            if not isinstance(data, list):
                return {
                    'valid': False,
                    'error': 'Data must be a list'
                }
            
            if len(data) < min_length:
                return {
                    'valid': False,
                    'error': f'Data must have at least {min_length} elements'
                }
            
            if max_length and len(data) > max_length:
                return {
                    'valid': False,
                    'error': f'Data must have at most {max_length} elements'
                }
            
            # Check if all elements are numeric
            numeric_data = []
            for i, element in enumerate(data):
                try:
                    numeric_data.append(float(element))
                except (ValueError, TypeError):
                    return {
                        'valid': False,
                        'error': f'Non-numeric element at index {i}: {element}'
                    }
            
            return {
                'valid': True,
                'data': numeric_data,
                'length': len(numeric_data)
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Data validation error: {str(e)}'
            }
    
    def validate_parameter_range(self, value: Union[int, float], 
                               min_val: float = None,
                               max_val: float = None,
                               param_name: str = "parameter") -> Dict[str, Any]:
        """Validate parameter is within specified range"""
        try:
            numeric_value = float(value)
            
            if min_val is not None and numeric_value < min_val:
                return {
                    'valid': False,
                    'error': f'{param_name} must be >= {min_val}'
                }
            
            if max_val is not None and numeric_value > max_val:
                return {
                    'valid': False,
                    'error': f'{param_name} must be <= {max_val}'
                }
            
            return {
                'valid': True,
                'value': numeric_value
            }
            
        except (ValueError, TypeError):
            return {
                'valid': False,
                'error': f'{param_name} must be numeric'
            }
    
    def validate_file_upload(self, filename: str, 
                           allowed_extensions: List[str] = None,
                           max_size_mb: float = 10) -> Dict[str, Any]:
        """Validate uploaded file"""
        try:
            if not filename:
                return {
                    'valid': False,
                    'error': 'No filename provided'
                }
            
            # Check file extension
            if allowed_extensions:
                file_ext = filename.lower().split('.')[-1]
                if file_ext not in [ext.lower() for ext in allowed_extensions]:
                    return {
                        'valid': False,
                        'error': f'File type not allowed. Allowed types: {", ".join(allowed_extensions)}'
                    }
            
            return {
                'valid': True,
                'filename': filename,
                'extension': filename.split('.')[-1].lower()
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'File validation error: {str(e)}'
            }
    
    def sanitize_input(self, input_string: str, max_length: int = 1000) -> str:
        """Sanitize user input"""
        try:
            # Remove potentially dangerous characters
            sanitized = re.sub(r'[^\w\s+\-*/().,;:!?@#$%&]', '', input_string)
            
            # Limit length
            if len(sanitized) > max_length:
                sanitized = sanitized[:max_length]
            
            return sanitized.strip()
            
        except Exception:
            return ""
    
    def validate_equation(self, equation: str) -> Dict[str, Any]:
        """Validate equation for solving"""
        try:
            if not equation or not equation.strip():
                return {
                    'valid': False,
                    'error': 'Equation cannot be empty'
                }
            
            # Check for equals sign
            if '=' not in equation:
                return {
                    'valid': False,
                    'error': 'Equation must contain an equals sign (=)'
                }
            
            # Split by equals sign
            parts = equation.split('=')
            if len(parts) != 2:
                return {
                    'valid': False,
                    'error': 'Equation must have exactly one equals sign'
                }
            
            left_side = parts[0].strip()
            right_side = parts[1].strip()
            
            # Validate both sides
            left_valid = self.validate_expression(left_side)
            right_valid = self.validate_expression(right_side)
            
            if not left_valid['valid']:
                return {
                    'valid': False,
                    'error': f"Invalid left side: {left_valid['error']}"
                }
            
            if not right_valid['valid']:
                return {
                    'valid': False,
                    'error': f"Invalid right side: {right_valid['error']}"
                }
            
            return {
                'valid': True,
                'equation': equation.strip(),
                'left_side': left_side,
                'right_side': right_side
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Equation validation error: {str(e)}'
            }


def create_validator() -> InputValidator:
    """Factory function to create input validator instance"""
    return InputValidator()
