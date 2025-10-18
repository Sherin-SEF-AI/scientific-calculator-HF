"""
Output Formatting Utilities
Handles formatting of mathematical results, data display, and export formats
"""

import math
import numpy as np
from typing import Union, List, Dict, Any, Optional
import json
from decimal import Decimal, ROUND_HALF_UP


class OutputFormatter:
    """Comprehensive output formatting for calculator results"""
    
    def __init__(self):
        self.precision = 10  # Default precision for decimal places
        self.scientific_threshold = 1e10  # Threshold for scientific notation
        self.small_threshold = 1e-10  # Threshold for small numbers
    
    def format_number(self, number: Union[int, float, complex], 
                     precision: int = None,
                     use_scientific: bool = None) -> str:
        """Format a number for display"""
        try:
            if precision is None:
                precision = self.precision
            
            # Handle complex numbers
            if isinstance(number, complex):
                real_part = self.format_number(number.real, precision, use_scientific)
                imag_part = self.format_number(number.imag, precision, use_scientific)
                if number.imag >= 0:
                    return f"{real_part} + {imag_part}i"
                else:
                    return f"{real_part} - {abs(number.imag):.{precision}g}i"
            
            # Handle infinity and NaN
            if math.isinf(number):
                return "∞" if number > 0 else "-∞"
            
            if math.isnan(number):
                return "NaN"
            
            # Determine if scientific notation should be used
            if use_scientific is None:
                use_scientific = (abs(number) >= self.scientific_threshold or 
                                (abs(number) < self.small_threshold and number != 0))
            
            if use_scientific:
                return f"{number:.{precision}e}"
            
            # Handle integers
            if isinstance(number, int) or (isinstance(number, float) and number.is_integer()):
                return str(int(number))
            
            # Format decimal number
            formatted = f"{number:.{precision}g}"
            
            # Remove trailing zeros and unnecessary decimal point
            if '.' in formatted:
                formatted = formatted.rstrip('0').rstrip('.')
            
            return formatted
            
        except Exception as e:
            return str(number)
    
    def format_matrix(self, matrix: Union[List[List], np.ndarray], 
                     precision: int = None,
                     max_cols: int = 10,
                     max_rows: int = 10) -> str:
        """Format matrix for display"""
        try:
            if isinstance(matrix, np.ndarray):
                matrix = matrix.tolist()
            
            if precision is None:
                precision = self.precision
            
            # Handle empty matrix
            if not matrix or not matrix[0]:
                return "[]"
            
            rows, cols = len(matrix), len(matrix[0])
            
            # Truncate if too large
            display_rows = min(rows, max_rows)
            display_cols = min(cols, max_cols)
            
            formatted_rows = []
            for i in range(display_rows):
                row_str = "["
                for j in range(display_cols):
                    formatted_num = self.format_number(matrix[i][j], precision)
                    row_str += f"{formatted_num:>12}"
                    if j < display_cols - 1:
                        row_str += ", "
                
                # Add ellipsis if truncated
                if display_cols < cols:
                    row_str += ", ..."
                
                row_str += "]"
                formatted_rows.append(row_str)
            
            # Add ellipsis for rows if truncated
            if display_rows < rows:
                formatted_rows.append("...")
            
            return "[" + ",\n ".join(formatted_rows) + "]"
            
        except Exception as e:
            return f"Error formatting matrix: {str(e)}"
    
    def format_statistics(self, stats_dict: Dict[str, Any]) -> str:
        """Format statistical results"""
        try:
            formatted = []
            
            # Basic statistics
            if 'count' in stats_dict:
                formatted.append(f"Count: {int(stats_dict['count'])}")
            
            if 'mean' in stats_dict:
                formatted.append(f"Mean: {self.format_number(stats_dict['mean'])}")
            
            if 'median' in stats_dict:
                formatted.append(f"Median: {self.format_number(stats_dict['median'])}")
            
            if 'std' in stats_dict:
                formatted.append(f"Standard Deviation: {self.format_number(stats_dict['std'])}")
            
            if 'min' in stats_dict:
                formatted.append(f"Minimum: {self.format_number(stats_dict['min'])}")
            
            if 'max' in stats_dict:
                formatted.append(f"Maximum: {self.format_number(stats_dict['max'])}")
            
            # Percentiles
            if 'q1' in stats_dict:
                formatted.append(f"Q1 (25th percentile): {self.format_number(stats_dict['q1'])}")
            
            if 'q3' in stats_dict:
                formatted.append(f"Q3 (75th percentile): {self.format_number(stats_dict['q3'])}")
            
            # Skewness and kurtosis
            if 'skewness' in stats_dict:
                formatted.append(f"Skewness: {self.format_number(stats_dict['skewness'])}")
            
            if 'kurtosis' in stats_dict:
                formatted.append(f"Kurtosis: {self.format_number(stats_dict['kurtosis'])}")
            
            return "\n".join(formatted)
            
        except Exception as e:
            return f"Error formatting statistics: {str(e)}"
    
    def format_correlation_results(self, results: Dict[str, Any]) -> str:
        """Format correlation analysis results"""
        try:
            formatted = []
            
            if 'pearson_correlation' in results:
                pearson_r = results['pearson_correlation']
                pearson_p = results['pearson_p_value']
                formatted.append(f"Pearson Correlation: {self.format_number(pearson_r)}")
                formatted.append(f"Pearson p-value: {self.format_number(pearson_p, 6)}")
                
                # Interpret correlation strength
                abs_r = abs(pearson_r)
                if abs_r >= 0.8:
                    strength = "very strong"
                elif abs_r >= 0.6:
                    strength = "strong"
                elif abs_r >= 0.4:
                    strength = "moderate"
                elif abs_r >= 0.2:
                    strength = "weak"
                else:
                    strength = "very weak"
                
                direction = "positive" if pearson_r > 0 else "negative"
                formatted.append(f"Interpretation: {strength} {direction} correlation")
            
            if 'spearman_correlation' in results:
                spearman_r = results['spearman_correlation']
                spearman_p = results['spearman_p_value']
                formatted.append(f"Spearman Correlation: {self.format_number(spearman_r)}")
                formatted.append(f"Spearman p-value: {self.format_number(spearman_p, 6)}")
            
            if 'sample_size' in results:
                formatted.append(f"Sample Size: {int(results['sample_size'])}")
            
            return "\n".join(formatted)
            
        except Exception as e:
            return f"Error formatting correlation results: {str(e)}"
    
    def format_hypothesis_test(self, results: Dict[str, Any]) -> str:
        """Format hypothesis test results"""
        try:
            formatted = []
            
            if 'test_type' in results:
                formatted.append(f"Test Type: {results['test_type'].replace('_', ' ').title()}")
            
            if 't_statistic' in results:
                formatted.append(f"t-statistic: {self.format_number(results['t_statistic'])}")
            
            if 'f_statistic' in results:
                formatted.append(f"F-statistic: {self.format_number(results['f_statistic'])}")
            
            if 'chi2_statistic' in results:
                formatted.append(f"Chi-square statistic: {self.format_number(results['chi2_statistic'])}")
            
            if 'p_value' in results:
                p_val = results['p_value']
                formatted.append(f"p-value: {self.format_number(p_val, 6)}")
                
                # Interpret significance
                alpha = 0.05
                if p_val < alpha:
                    formatted.append(f"Result: Statistically significant (p < {alpha})")
                else:
                    formatted.append(f"Result: Not statistically significant (p ≥ {alpha})")
            
            if 'degrees_of_freedom' in results:
                formatted.append(f"Degrees of Freedom: {int(results['degrees_of_freedom'])}")
            
            if 'sample_size' in results:
                formatted.append(f"Sample Size: {int(results['sample_size'])}")
            
            if 'sample1_size' in results and 'sample2_size' in results:
                formatted.append(f"Sample 1 Size: {int(results['sample1_size'])}")
                formatted.append(f"Sample 2 Size: {int(results['sample2_size'])}")
            
            return "\n".join(formatted)
            
        except Exception as e:
            return f"Error formatting hypothesis test results: {str(e)}"
    
    def format_regression_results(self, results: Dict[str, Any]) -> str:
        """Format regression analysis results"""
        try:
            formatted = []
            
            if 'slope' in results:
                formatted.append(f"Slope: {self.format_number(results['slope'])}")
            
            if 'intercept' in results:
                formatted.append(f"Intercept: {self.format_number(results['intercept'])}")
            
            if 'r_squared' in results:
                r_sq = results['r_squared']
                formatted.append(f"R-squared: {self.format_number(r_sq, 4)}")
                
                # Interpret R-squared
                if r_sq >= 0.9:
                    fit = "excellent"
                elif r_sq >= 0.8:
                    fit = "good"
                elif r_sq >= 0.6:
                    fit = "moderate"
                elif r_sq >= 0.4:
                    fit = "poor"
                else:
                    fit = "very poor"
                
                formatted.append(f"Model Fit: {fit}")
            
            if 'correlation' in results:
                formatted.append(f"Correlation: {self.format_number(results['correlation'])}")
            
            if 'p_value' in results:
                formatted.append(f"p-value: {self.format_number(results['p_value'], 6)}")
            
            if 'rmse' in results:
                formatted.append(f"Root Mean Square Error: {self.format_number(results['rmse'])}")
            
            if 'sample_size' in results:
                formatted.append(f"Sample Size: {int(results['sample_size'])}")
            
            # Add regression equation
            if 'slope' in results and 'intercept' in results:
                slope = self.format_number(results['slope'])
                intercept = self.format_number(results['intercept'])
                formatted.append(f"Regression Equation: y = {slope}x + {intercept}")
            
            return "\n".join(formatted)
            
        except Exception as e:
            return f"Error formatting regression results: {str(e)}"
    
    def format_json(self, data: Any, indent: int = 2) -> str:
        """Format data as JSON string"""
        try:
            # Handle numpy arrays and other non-serializable types
            def convert_numpy(obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.complexfloating):
                    return str(obj)
                return obj
            
            # Convert numpy types
            converted_data = self._recursive_convert(data, convert_numpy)
            
            return json.dumps(converted_data, indent=indent, ensure_ascii=False)
            
        except Exception as e:
            return f"Error formatting JSON: {str(e)}"
    
    def _recursive_convert(self, obj, convert_func):
        """Recursively convert objects using convert_func"""
        if isinstance(obj, dict):
            return {key: self._recursive_convert(value, convert_func) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._recursive_convert(item, convert_func) for item in obj]
        else:
            return convert_func(obj)
    
    def format_table(self, data: List[Dict[str, Any]], 
                    headers: List[str] = None,
                    max_width: int = 80) -> str:
        """Format data as a table"""
        try:
            if not data:
                return "No data to display"
            
            # Use provided headers or extract from data
            if headers is None:
                headers = list(data[0].keys())
            
            # Calculate column widths
            col_widths = []
            for header in headers:
                col_widths.append(len(str(header)))
            
            for row in data:
                for i, header in enumerate(headers):
                    value = str(row.get(header, ''))
                    col_widths[i] = max(col_widths[i], len(value))
            
            # Limit column widths
            total_width = sum(col_widths) + len(headers) * 3 - 1
            if total_width > max_width:
                scale_factor = max_width / total_width
                col_widths = [int(w * scale_factor) for w in col_widths]
            
            # Format table
            formatted_lines = []
            
            # Header
            header_line = " | ".join(f"{header:<{col_widths[i]}}" for i, header in enumerate(headers))
            formatted_lines.append(header_line)
            formatted_lines.append("-" * len(header_line))
            
            # Data rows
            for row in data:
                row_line = " | ".join(
                    f"{str(row.get(headers[i], '')):<{col_widths[i]}}" 
                    for i in range(len(headers))
                )
                formatted_lines.append(row_line)
            
            return "\n".join(formatted_lines)
            
        except Exception as e:
            return f"Error formatting table: {str(e)}"
    
    def format_error(self, error: str, context: str = None) -> str:
        """Format error message with context"""
        try:
            formatted = f"Error: {error}"
            
            if context:
                formatted += f"\nContext: {context}"
            
            return formatted
            
        except Exception:
            return f"Error: {error}"


def create_formatter() -> OutputFormatter:
    """Factory function to create output formatter instance"""
    return OutputFormatter()


