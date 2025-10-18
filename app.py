"""
Scientific Calculator Pro - Main Application
Advanced mathematical computations, statistical analysis, and data visualization
"""

import gradio as gr
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import io
import base64
from typing import Union, List, Dict, Any, Optional

# Import our custom modules
from modules.calculator import create_calculator
from modules.matrix import create_matrix_calculator
from modules.statistics import create_statistical_analyzer
from modules.visualization import create_visualizer
from modules.data_handler import create_data_handler
from modules.advanced_features import create_advanced_calculator, create_ml_tools, create_financial_calculator
from utils.validators import create_validator
from utils.formatters import create_formatter
from utils.helpers import create_helper

# Initialize components
calculator = create_calculator()
matrix_calc = create_matrix_calculator()
stats_analyzer = create_statistical_analyzer()
visualizer = create_visualizer()
data_handler = create_data_handler()
advanced_calc = create_advanced_calculator()
ml_tools = create_ml_tools()
financial_calc = create_financial_calculator()
validator = create_validator()
formatter = create_formatter()
helper = create_helper()

# Corporate theme colors
THEME_COLORS = {
    'primary': '#1E40AF',    # Navy Blue
    'secondary': '#6B7280',  # Gray
    'accent': '#F59E0B',     # Orange
    'background': '#F9FAFB', # Light Gray
    'text': '#374151'        # Dark Gray
}

# Custom CSS for corporate theme
CUSTOM_CSS = """
.gradio-container {
    background-color: #F9FAFB !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

.main-header {
    background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%) !important;
    color: white !important;
    padding: 20px !important;
    border-radius: 10px !important;
    margin-bottom: 20px !important;
    text-align: center !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
}

.calc-button {
    background-color: #1E40AF !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.calc-button:hover {
    background-color: #1D4ED8 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 8px rgba(30, 64, 175, 0.3) !important;
}

.result-display {
    background-color: white !important;
    border: 2px solid #E5E7EB !important;
    border-radius: 10px !important;
    padding: 20px !important;
    font-family: 'Courier New', monospace !important;
    font-size: 16px !important;
    min-height: 100px !important;
}

.card {
    background-color: white !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 10px !important;
    padding: 20px !important;
    margin: 10px 0 !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
}

.section-header {
    color: #1E40AF !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    margin-bottom: 15px !important;
    border-bottom: 2px solid #F59E0B !important;
    padding-bottom: 5px !important;
}
"""


def calculate_expression(expression: str) -> str:
    """Handle basic calculator operations"""
    try:
        # Validate input
        validation = validator.validate_expression(expression)
        if not validation['valid']:
            return f"❌ {validation['error']}"
        
        # Calculate result
        result = calculator.calculate(expression)
        
        if result['status'] == 'success':
            return f"✅ {result['formatted_result']}"
        else:
            return f"❌ {result['error']}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def solve_equation(equation: str, variable: str = 'x') -> str:
    """Solve mathematical equations"""
    try:
        # Validate equation
        validation = validator.validate_equation(equation)
        if not validation['valid']:
            return f"❌ {validation['error']}"
        
        # Solve equation
        result = calculator.solve_equation(equation, variable)
        
        if result['status'] == 'success':
            solutions = result['solutions']
            if len(solutions) == 1:
                return f"✅ Solution: {variable} = {formatter.format_number(solutions[0])}"
            elif len(solutions) > 1:
                sol_str = ", ".join([formatter.format_number(sol) for sol in solutions])
                return f"✅ Solutions: {variable} = {sol_str}"
            else:
                return "ℹ️ No solutions found"
        else:
            return f"❌ {result['error']}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def matrix_operation(operation: str, matrix1_str: str, matrix2_str: str = "", scalar: float = 1.0) -> str:
    """Handle matrix operations"""
    try:
        # Parse matrices
        matrix1 = json.loads(matrix1_str) if matrix1_str else [[1, 2], [3, 4]]
        matrix2 = json.loads(matrix2_str) if matrix2_str else [[1, 0], [0, 1]]
        
        # Validate matrices
        validation1 = validator.validate_matrix_data(matrix1)
        validation2 = validator.validate_matrix_data(matrix2) if matrix2_str else {'valid': True}
        
        if not validation1['valid']:
            return f"❌ Matrix 1: {validation1['error']}"
        if not validation2['valid']:
            return f"❌ Matrix 2: {validation2['error']}"
        
        # Perform operation
        if operation == "Addition":
            result = matrix_calc.add_matrices(matrix1, matrix2)
        elif operation == "Multiplication":
            result = matrix_calc.multiply_matrices(matrix1, matrix2)
        elif operation == "Scalar Multiply":
            result = matrix_calc.scalar_multiply(matrix1, scalar)
        elif operation == "Transpose":
            result = matrix_calc.transpose(matrix1)
        elif operation == "Determinant":
            result = matrix_calc.determinant(matrix1)
        elif operation == "Inverse":
            result = matrix_calc.inverse(matrix1)
        elif operation == "Eigenvalues":
            result = matrix_calc.eigenvalues(matrix1)
        elif operation == "Rank":
            result = matrix_calc.rank(matrix1)
        elif operation == "Trace":
            result = matrix_calc.trace(matrix1)
        else:
            return "❌ Unknown operation"
        
        if result['status'] == 'success':
            if operation in ["Determinant", "Rank", "Trace"]:
                return f"✅ Result: {formatter.format_number(result['result'])}"
            elif operation == "Eigenvalues":
                eigenvals = [formatter.format_number(val) for val in result['eigenvalues']]
                return f"✅ Eigenvalues: {', '.join(eigenvals)}"
            else:
                formatted_matrix = formatter.format_matrix(result['result'])
                return f"✅ Result:\n{formatted_matrix}"
        else:
            return f"❌ {result['error']}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def statistical_analysis(analysis_type: str, data_str: str, confidence_level: float = 0.95) -> str:
    """Handle statistical analysis"""
    try:
        # Parse data
        data = json.loads(data_str) if data_str else helper.generate_random_data('normal', 100)
        
        # Validate data
        validation = validator.validate_numeric_data(data)
        if not validation['valid']:
            return f"❌ {validation['error']}"
        
        # Perform analysis
        if analysis_type == "Descriptive Statistics":
            result = stats_analyzer.descriptive_stats(data)
            if result['status'] == 'success':
                return f"✅ {formatter.format_statistics(result)}"
            else:
                return f"❌ {result['error']}"
        
        elif analysis_type == "T-Test (One Sample)":
            result = stats_analyzer.t_test(data)
            if result['status'] == 'success':
                return f"✅ {formatter.format_hypothesis_test(result)}"
            else:
                return f"❌ {result['error']}"
        
        elif analysis_type == "Confidence Interval":
            result = stats_analyzer.confidence_interval(data, confidence_level)
            if result['status'] == 'success':
                ci_lower = formatter.format_number(result['confidence_interval'][0])
                ci_upper = formatter.format_number(result['confidence_interval'][1])
                mean = formatter.format_number(result['mean'])
                return f"✅ Mean: {mean}\nConfidence Interval ({confidence_level*100}%): [{ci_lower}, {ci_upper}]"
            else:
                return f"❌ {result['error']}"
        
        else:
            return "❌ Unknown analysis type"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def correlation_analysis(x_data_str: str, y_data_str: str) -> str:
    """Perform correlation analysis"""
    try:
        # Parse data
        x_data = json.loads(x_data_str)
        y_data = json.loads(y_data_str)
        
        # Validate data
        x_validation = validator.validate_numeric_data(x_data)
        y_validation = validator.validate_numeric_data(y_data)
        
        if not x_validation['valid']:
            return f"❌ X data: {x_validation['error']}"
        if not y_validation['valid']:
            return f"❌ Y data: {y_validation['error']}"
        
        # Perform correlation analysis
        result = stats_analyzer.correlation_analysis(x_data, y_data)
        
        if result['status'] == 'success':
            return f"✅ {formatter.format_correlation_results(result)}"
        else:
            return f"❌ {result['error']}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def linear_regression(x_data_str: str, y_data_str: str) -> str:
    """Perform linear regression"""
    try:
        # Parse data
        x_data = json.loads(x_data_str)
        y_data = json.loads(y_data_str)
        
        # Validate data
        x_validation = validator.validate_numeric_data(x_data)
        y_validation = validator.validate_numeric_data(y_data)
        
        if not x_validation['valid']:
            return f"❌ X data: {x_validation['error']}"
        if not y_validation['valid']:
            return f"❌ Y data: {y_validation['error']}"
        
        # Perform regression
        result = stats_analyzer.linear_regression(x_data, y_data)
        
        if result['status'] == 'success':
            return f"✅ {formatter.format_regression_results(result)}"
        else:
            return f"❌ {result['error']}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def create_visualization(plot_type: str, x_data_str: str, y_data_str: str, plot_title: str, x_label: str, y_label: str) -> go.Figure:
    """Create data visualizations"""
    try:
        # Parse data
        x_data = json.loads(x_data_str) if x_data_str else helper.generate_random_data('normal', 50)
        
        if plot_type in ["Line Plot", "Scatter Plot", "Regression Plot"]:
            y_data = json.loads(y_data_str) if y_data_str else helper.generate_random_data('normal', 50)
        
        # Create plots
        if plot_type == "Line Plot":
            return visualizer.line_plot(x_data, y_data, 
                                      plot_title or 'Line Plot',
                                      x_label or 'X',
                                      y_label or 'Y')
        
        elif plot_type == "Scatter Plot":
            return visualizer.scatter_plot(x_data, y_data,
                                         plot_title or 'Scatter Plot',
                                         x_label or 'X',
                                         y_label or 'Y')
        
        elif plot_type == "Histogram":
            return visualizer.histogram(x_data,
                                      plot_title or 'Histogram',
                                      30,  # bins
                                      x_label or 'Value',
                                      y_label or 'Frequency')
        
        elif plot_type == "Box Plot":
            return visualizer.box_plot(x_data,
                                     plot_title or 'Box Plot',
                                     y_label or 'Value')
        
        elif plot_type == "Regression Plot":
            # Perform regression first
            reg_result = stats_analyzer.linear_regression(x_data, y_data)
            if reg_result['status'] == 'success':
                return visualizer.regression_plot(x_data, y_data,
                                                reg_result['slope'],
                                                reg_result['intercept'],
                                                plot_title or 'Regression Plot')
            else:
                # Fallback to scatter plot
                return visualizer.scatter_plot(x_data, y_data, "Scatter Plot")
        
        else:
            # Default to histogram
            return visualizer.histogram(x_data, "Histogram")
            
    except Exception as e:
        # Return error plot
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error creating plot: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color="red", size=16)
        )
        return fig


def function_plotter(function_expr: str, x_min: float = -10, x_max: float = 10) -> go.Figure:
    """Plot mathematical functions"""
    try:
        return visualizer.function_plot(function_expr, (x_min, x_max), title=f"y = {function_expr}")
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error plotting function: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color="red", size=16)
        )
        return fig


def load_csv_data(csv_content: str) -> str:
    """Load and process CSV data"""
    try:
        result = data_handler.load_csv_from_string(csv_content)
        
        if result['status'] == 'success':
            info = f"✅ Dataset loaded successfully!\n\n"
            info += f"Shape: {result['shape'][0]} rows × {result['shape'][1]} columns\n"
            info += f"Columns: {', '.join(result['columns'])}\n\n"
            info += "Preview:\n"
            
            # Format preview data
            preview_df = pd.DataFrame(result['preview'])
            info += preview_df.to_string(index=False)
            
            return info
        else:
            return f"❌ {result['error']}"
            
    except Exception as e:
        return f"❌ Error loading CSV: {str(e)}"


def generate_sample_data(data_type: str, n_samples: int = 100, **params) -> str:
    """Generate sample datasets"""
    try:
        result = data_handler.generate_sample_data(data_type, n_samples=n_samples, **params)
        
        if result['status'] == 'success':
            info = f"✅ Generated {data_type} dataset!\n\n"
            info += f"Shape: {result['shape'][0]} rows × {result['shape'][1]} columns\n"
            info += f"Columns: {', '.join(result['columns'])}\n\n"
            info += "Preview:\n"
            
            # Format preview data
            preview_df = pd.DataFrame(result['preview'])
            info += preview_df.to_string(index=False)
            
            return info
        else:
            return f"❌ {result['error']}"
            
    except Exception as e:
        return f"❌ Error generating data: {str(e)}"


# Advanced Features Functions
def numerical_integration(function_expr: str, lower: float, upper: float, method: str) -> str:
    """Perform numerical integration"""
    try:
        result = advanced_calc.numerical_integration(function_expr, lower, upper, method)
        
        if result['status'] == 'success':
            formatted_result = formatter.format_number(result['result'])
            info = f"✅ Integration Result:\n"
            info += f"Function: {function_expr}\n"
            info += f"Interval: [{lower}, {upper}]\n"
            info += f"Method: {result['method']}\n"
            info += f"Result: {formatted_result}\n"
            
            if 'error_estimate' in result:
                error = formatter.format_number(result['error_estimate'])
                info += f"Error Estimate: {error}\n"
            
            return info
        else:
            return f"❌ {result['error']}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def numerical_optimization(function_expr: str, method: str, lower_bound: float, upper_bound: float) -> str:
    """Perform numerical optimization"""
    try:
        bounds = (lower_bound, upper_bound) if lower_bound != upper_bound else None
        result = advanced_calc.optimization(function_expr, method, bounds)
        
        if result['status'] == 'success':
            info = f"✅ Optimization Result:\n"
            info += f"Function: {function_expr}\n"
            info += f"Method: {result['method']}\n"
            info += f"Optimal Point: {formatter.format_number(result['optimal_point'])}\n"
            info += f"Optimal Value: {formatter.format_number(result['optimal_value'])}\n"
            info += f"Success: {result['success']}\n"
            
            return info
        else:
            return f"❌ {result['error']}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def polynomial_regression_advanced(x_data_str: str, y_data_str: str, degree: int) -> str:
    """Perform advanced polynomial regression"""
    try:
        x_data = json.loads(x_data_str)
        y_data = json.loads(y_data_str)
        
        result = ml_tools.polynomial_regression(x_data, y_data, degree)
        
        if result['status'] == 'success':
            info = f"✅ Polynomial Regression (Degree {degree}):\n"
            info += f"R² Score: {formatter.format_number(result['r2_score'], 4)}\n"
            info += f"RMSE: {formatter.format_number(result['rmse'])}\n"
            info += f"Coefficients: {[formatter.format_number(coef) for coef in result['coefficients']]}\n"
            info += f"Intercept: {formatter.format_number(result['intercept'])}\n"
            
            return info
        else:
            return f"❌ {result['error']}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def kmeans_clustering(data_str: str, n_clusters: int) -> str:
    """Perform K-means clustering"""
    try:
        data = json.loads(data_str)
        result = ml_tools.kmeans_clustering(data, n_clusters)
        
        if result['status'] == 'success':
            info = f"✅ K-means Clustering:\n"
            info += f"Number of Clusters: {result['n_clusters']}\n"
            info += f"Inertia: {formatter.format_number(result['inertia'])}\n"
            info += f"Cluster Centers:\n"
            
            for i, center in enumerate(result['centers']):
                formatted_center = [formatter.format_number(coord) for coord in center]
                info += f"  Cluster {i+1}: {formatted_center}\n"
            
            return info
        else:
            return f"❌ {result['error']}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def financial_calculations(calc_type: str, principal: float, rate: float, time: float, compounding: int = 1) -> str:
    """Perform financial calculations"""
    try:
        if calc_type == "Compound Interest":
            result = financial_calc.compound_interest(principal, rate, time, compounding)
        elif calc_type == "Present Value":
            result = financial_calc.present_value(principal, rate, time)
        elif calc_type == "Loan Payment":
            result = financial_calc.loan_payment(principal, rate, int(time))
        else:
            return "❌ Unknown calculation type"
        
        if result['status'] == 'success':
            info = f"✅ {calc_type} Result:\n"
            for key, value in result.items():
                if key != 'status' and key != 'calc_type':
                    if isinstance(value, float):
                        info += f"{key.replace('_', ' ').title()}: {formatter.format_number(value)}\n"
                    else:
                        info += f"{key.replace('_', ' ').title()}: {value}\n"
            
            return info
        else:
            return f"❌ {result['error']}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def monte_carlo_simulation(n_simulations: int, distribution: str, mean: float, std: float) -> str:
    """Perform Monte Carlo simulation"""
    try:
        params = {'mean': mean, 'std': std}
        result = advanced_calc.monte_carlo_simulation(n_simulations, distribution, **params)
        
        if result['status'] == 'success':
            info = f"✅ Monte Carlo Simulation:\n"
            info += f"Distribution: {result['distribution']}\n"
            info += f"Simulations: {result['n_simulations']}\n"
            info += f"Mean: {formatter.format_number(result['mean'])}\n"
            info += f"Std Dev: {formatter.format_number(result['std'])}\n"
            info += f"Min: {formatter.format_number(result['min'])}\n"
            info += f"Max: {formatter.format_number(result['max'])}\n"
            
            return info
        else:
            return f"❌ {result['error']}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Create Gradio interface
def create_interface():
    """Create the main Gradio interface"""
    
    with gr.Blocks(css=CUSTOM_CSS, title="Scientific Calculator Pro") as app:
        
        # Header
        gr.HTML(f"""
        <div class="main-header">
            <h1>🧮 Scientific Calculator Pro</h1>
            <p>Advanced Mathematical Computations • Statistical Analysis • Data Visualization</p>
        </div>
        """)
        
        # Main tabs
        with gr.Tabs():
            
            # Basic Calculator Tab
            with gr.Tab("🧮 Calculator"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.HTML('<div class="section-header">Basic Calculator</div>')
                        
                        calc_input = gr.Textbox(
                            label="Enter Expression",
                            placeholder="e.g., 2 + 3 * sin(π/4)",
                            lines=2
                        )
                        
                        calc_result = gr.Textbox(
                            label="Result",
                            lines=3,
                            interactive=False,
                            elem_classes=["result-display"]
                        )
                        
                        calc_btn = gr.Button("Calculate", elem_classes=["calc-button"])
                        
                        # Equation Solver
                        gr.HTML('<div class="section-header">Equation Solver</div>')
                        
                        equation_input = gr.Textbox(
                            label="Enter Equation",
                            placeholder="e.g., 2*x + 3 = 7",
                            lines=2
                        )
                        
                        variable_input = gr.Textbox(
                            label="Variable",
                            value="x",
                            lines=1
                        )
                        
                        equation_result = gr.Textbox(
                            label="Solution",
                            lines=2,
                            interactive=False,
                            elem_classes=["result-display"]
                        )
                        
                        equation_btn = gr.Button("Solve", elem_classes=["calc-button"])
                    
                    with gr.Column(scale=1):
                        gr.HTML('<div class="section-header">Constants & Functions</div>')
                        
                        constants_info = gr.Markdown("""
                        **Mathematical Constants:**
                        - π (pi) ≈ 3.14159
                        - e ≈ 2.71828
                        - φ (phi) ≈ 1.61803
                        
                        **Available Functions:**
                        - Trigonometric: sin, cos, tan, asin, acos, atan
                        - Hyperbolic: sinh, cosh, tanh, asinh, acosh, atanh
                        - Logarithmic: log, log10, ln, exp
                        - Other: sqrt, abs, factorial, gamma
                        
                        **Examples:**
                        - sin(π/2)
                        - log(10)
                        - sqrt(16) + 2^3
                        - factorial(5)
                        """)
                
                # Event handlers
                calc_btn.click(
                    calculate_expression,
                    inputs=[calc_input],
                    outputs=[calc_result]
                )
                
                equation_btn.click(
                    solve_equation,
                    inputs=[equation_input, variable_input],
                    outputs=[equation_result]
                )
            
            # Matrix Operations Tab
            with gr.Tab("🔢 Matrix Operations"):
                with gr.Row():
                    with gr.Column():
                        gr.HTML('<div class="section-header">Matrix Calculator</div>')
                        
                        matrix_operation_type = gr.Dropdown(
                            choices=[
                                "Addition", "Multiplication", "Scalar Multiply",
                                "Transpose", "Determinant", "Inverse",
                                "Eigenvalues", "Rank", "Trace"
                            ],
                            label="Operation",
                            value="Addition"
                        )
                        
                        matrix1_input = gr.Textbox(
                            label="Matrix 1 (JSON format)",
                            placeholder='[[1, 2], [3, 4]]',
                            lines=4
                        )
                        
                        matrix2_input = gr.Textbox(
                            label="Matrix 2 (JSON format)",
                            placeholder='[[1, 0], [0, 1]]',
                            lines=4
                        )
                        
                        scalar_input = gr.Number(
                            label="Scalar",
                            value=2.0
                        )
                        
                        matrix_result = gr.Textbox(
                            label="Result",
                            lines=8,
                            interactive=False,
                            elem_classes=["result-display"]
                        )
                        
                        matrix_btn = gr.Button("Calculate", elem_classes=["calc-button"])
                    
                    with gr.Column():
                        gr.HTML('<div class="section-header">Matrix Examples</div>')
                        
                        matrix_examples = gr.Markdown("""
                        **Example Matrices:**
                        
                        2×2 Identity:
                        ```
                        [[1, 0], [0, 1]]
                        ```
                        
                        2×2 Matrix:
                        ```
                        [[1, 2], [3, 4]]
                        ```
                        
                        3×3 Matrix:
                        ```
                        [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
                        ```
                        
                        **Operations:**
                        - **Addition**: Same dimensions required
                        - **Multiplication**: Cols of Matrix 1 = Rows of Matrix 2
                        - **Determinant**: Square matrices only
                        - **Inverse**: Square matrices with non-zero determinant
                        """)
                
                matrix_btn.click(
                    matrix_operation,
                    inputs=[matrix_operation_type, matrix1_input, matrix2_input, scalar_input],
                    outputs=[matrix_result]
                )
            
            # Statistics Tab
            with gr.Tab("📊 Statistics"):
                with gr.Row():
                    with gr.Column():
                        gr.HTML('<div class="section-header">Statistical Analysis</div>')
                        
                        stats_type = gr.Dropdown(
                            choices=[
                                "Descriptive Statistics",
                                "T-Test (One Sample)",
                                "Confidence Interval"
                            ],
                            label="Analysis Type",
                            value="Descriptive Statistics"
                        )
                        
                        stats_data_input = gr.Textbox(
                            label="Data (JSON array)",
                            placeholder='[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]',
                            lines=4
                        )
                        
                        confidence_level = gr.Slider(
                            minimum=0.8,
                            maximum=0.99,
                            value=0.95,
                            step=0.01,
                            label="Confidence Level"
                        )
                        
                        stats_result = gr.Textbox(
                            label="Analysis Result",
                            lines=10,
                            interactive=False,
                            elem_classes=["result-display"]
                        )
                        
                        stats_btn = gr.Button("Analyze", elem_classes=["calc-button"])
                        
                        # Correlation Analysis
                        gr.HTML('<div class="section-header">Correlation Analysis</div>')
                        
                        x_data_input = gr.Textbox(
                            label="X Data (JSON array)",
                            placeholder='[1, 2, 3, 4, 5]',
                            lines=2
                        )
                        
                        y_data_input = gr.Textbox(
                            label="Y Data (JSON array)",
                            placeholder='[2, 4, 6, 8, 10]',
                            lines=2
                        )
                        
                        correlation_result = gr.Textbox(
                            label="Correlation Result",
                            lines=5,
                            interactive=False,
                            elem_classes=["result-display"]
                        )
                        
                        correlation_btn = gr.Button("Calculate Correlation", elem_classes=["calc-button"])
                    
                    with gr.Column():
                        gr.HTML('<div class="section-header">Sample Data Generator</div>')
                        
                        sample_type = gr.Dropdown(
                            choices=["normal", "uniform", "exponential", "poisson", "binomial"],
                            label="Distribution Type",
                            value="normal"
                        )
                        
                        sample_size = gr.Number(
                            label="Sample Size",
                            value=100,
                            precision=0
                        )
                        
                        sample_params = gr.Textbox(
                            label="Parameters (JSON)",
                            placeholder='{"mean": 0, "std": 1}',
                            lines=2
                        )
                        
                        sample_data_output = gr.Textbox(
                            label="Generated Data",
                            lines=6,
                            interactive=False
                        )
                        
                        generate_sample_btn = gr.Button("Generate Sample", elem_classes=["calc-button"])
                
                # Event handlers
                stats_btn.click(
                    statistical_analysis,
                    inputs=[stats_type, stats_data_input, confidence_level],
                    outputs=[stats_result]
                )
                
                correlation_btn.click(
                    correlation_analysis,
                    inputs=[x_data_input, y_data_input],
                    outputs=[correlation_result]
                )
                
                generate_sample_btn.click(
                    lambda t, s, p: generate_sample_data(t, s, **json.loads(p) if p else {}),
                    inputs=[sample_type, sample_size, sample_params],
                    outputs=[sample_data_output]
                )
            
            # Visualization Tab
            with gr.Tab("📈 Visualization"):
                with gr.Row():
                    with gr.Column():
                        gr.HTML('<div class="section-header">Data Visualization</div>')
                        
                        plot_type = gr.Dropdown(
                            choices=["Line Plot", "Scatter Plot", "Histogram", "Box Plot", "Regression Plot"],
                            label="Plot Type",
                            value="Line Plot"
                        )
                        
                        viz_x_data = gr.Textbox(
                            label="X Data (JSON array)",
                            placeholder='[1, 2, 3, 4, 5]',
                            lines=2
                        )
                        
                        viz_y_data = gr.Textbox(
                            label="Y Data (JSON array)",
                            placeholder='[2, 4, 6, 8, 10]',
                            lines=2
                        )
                        
                        plot_title = gr.Textbox(
                            label="Plot Title",
                            value="",
                            lines=1
                        )
                        
                        x_label = gr.Textbox(
                            label="X Label",
                            value="X",
                            lines=1
                        )
                        
                        y_label = gr.Textbox(
                            label="Y Label",
                            value="Y",
                            lines=1
                        )
                        
                        plot_output = gr.Plot(label="Plot")
                        
                        create_plot_btn = gr.Button("Create Plot", elem_classes=["calc-button"])
                        
                        # Function Plotter
                        gr.HTML('<div class="section-header">Function Plotter</div>')
                        
                        function_expr = gr.Textbox(
                            label="Function Expression",
                            placeholder="sin(x)",
                            lines=1
                        )
                        
                        x_min = gr.Number(
                            label="X Min",
                            value=-10
                        )
                        
                        x_max = gr.Number(
                            label="X Max",
                            value=10
                        )
                        
                        function_plot_output = gr.Plot(label="Function Plot")
                        
                        plot_function_btn = gr.Button("Plot Function", elem_classes=["calc-button"])
                    
                    with gr.Column():
                        gr.HTML('<div class="section-header">Visualization Examples</div>')
                        
                        viz_examples = gr.Markdown("""
                        **Sample Data Examples:**
                        
                        Linear data:
                        ```
                        X: [1, 2, 3, 4, 5]
                        Y: [2, 4, 6, 8, 10]
                        ```
                        
                        Random normal data:
                        ```
                        X: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                        Y: [2.1, 3.9, 6.2, 7.8, 10.1, 11.9, 14.2, 15.8, 18.1, 19.9]
                        ```
                        
                        **Function Examples:**
                        - sin(x)
                        - cos(x)
                        - x^2 + 2*x + 1
                        - exp(x)
                        - log(x)
                        - sqrt(x)
                        
                        **Features:**
                        - Interactive zoom and pan
                        - Hover tooltips
                        - Download plots
                        - Customizable styling
                        """)
                
                # Event handlers
                create_plot_btn.click(
                    create_visualization,
                    inputs=[plot_type, viz_x_data, viz_y_data, plot_title, x_label, y_label],
                    outputs=[plot_output]
                )
                
                plot_function_btn.click(
                    function_plotter,
                    inputs=[function_expr, x_min, x_max],
                    outputs=[function_plot_output]
                )
            
            # Advanced Mathematics Tab
            with gr.Tab("🔬 Advanced Math"):
                with gr.Row():
                    with gr.Column():
                        gr.HTML('<div class="section-header">Numerical Integration</div>')
                        
                        int_function = gr.Textbox(
                            label="Function Expression",
                            placeholder="x**2 + 2*x + 1",
                            lines=1
                        )
                        
                        int_lower = gr.Number(label="Lower Bound", value=0)
                        int_upper = gr.Number(label="Upper Bound", value=1)
                        int_method = gr.Dropdown(
                            choices=["quad", "trapezoid", "simpson"],
                            label="Method",
                            value="quad"
                        )
                        
                        int_result = gr.Textbox(
                            label="Integration Result",
                            lines=6,
                            interactive=False
                        )
                        
                        int_btn = gr.Button("Integrate", elem_classes=["calc-button"])
                        
                        gr.HTML('<div class="section-header">Numerical Optimization</div>')
                        
                        opt_function = gr.Textbox(
                            label="Function to Optimize",
                            placeholder="x**2 - 4*x + 3",
                            lines=1
                        )
                        
                        opt_method = gr.Dropdown(
                            choices=["minimize", "maximize"],
                            label="Optimization Type",
                            value="minimize"
                        )
                        
                        opt_lower = gr.Number(label="Lower Bound", value=-10)
                        opt_upper = gr.Number(label="Upper Bound", value=10)
                        
                        opt_result = gr.Textbox(
                            label="Optimization Result",
                            lines=6,
                            interactive=False
                        )
                        
                        opt_btn = gr.Button("Optimize", elem_classes=["calc-button"])
                    
                    with gr.Column():
                        gr.HTML('<div class="section-header">Advanced Features</div>')
                        
                        advanced_info = gr.Markdown("""
                        **Numerical Integration:**
                        - **Quad**: Adaptive quadrature (most accurate)
                        - **Trapezoid**: Trapezoidal rule
                        - **Simpson**: Simpson's rule
                        
                        **Optimization:**
                        - Find minimum or maximum of functions
                        - Supports bounded optimization
                        - Uses scipy optimization algorithms
                        
                        **Function Examples:**
                        - Polynomial: `x**2 + 2*x + 1`
                        - Trigonometric: `sin(x) + cos(x)`
                        - Exponential: `exp(-x**2)`
                        - Logarithmic: `log(x + 1)`
                        
                        **Applications:**
                        - Area under curves
                        - Finding extrema
                        - Engineering calculations
                        - Physics simulations
                        """)
                
                # Event handlers
                int_btn.click(
                    numerical_integration,
                    inputs=[int_function, int_lower, int_upper, int_method],
                    outputs=[int_result]
                )
                
                opt_btn.click(
                    numerical_optimization,
                    inputs=[opt_function, opt_method, opt_lower, opt_upper],
                    outputs=[opt_result]
                )
            
            # Machine Learning Tab
            with gr.Tab("🤖 Machine Learning"):
                with gr.Row():
                    with gr.Column():
                        gr.HTML('<div class="section-header">Advanced Regression</div>')
                        
                        poly_x_data = gr.Textbox(
                            label="X Data (JSON array)",
                            placeholder='[1, 2, 3, 4, 5]',
                            lines=2
                        )
                        
                        poly_y_data = gr.Textbox(
                            label="Y Data (JSON array)",
                            placeholder='[2, 8, 18, 32, 50]',
                            lines=2
                        )
                        
                        poly_degree = gr.Number(
                            label="Polynomial Degree",
                            value=2,
                            precision=0,
                            minimum=1,
                            maximum=10
                        )
                        
                        poly_result = gr.Textbox(
                            label="Polynomial Regression Result",
                            lines=8,
                            interactive=False
                        )
                        
                        poly_btn = gr.Button("Fit Polynomial", elem_classes=["calc-button"])
                        
                        gr.HTML('<div class="section-header">K-means Clustering</div>')
                        
                        cluster_data = gr.Textbox(
                            label="Data (JSON array of arrays)",
                            placeholder='[[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]]',
                            lines=3
                        )
                        
                        n_clusters = gr.Number(
                            label="Number of Clusters",
                            value=3,
                            precision=0,
                            minimum=2,
                            maximum=10
                        )
                        
                        cluster_result = gr.Textbox(
                            label="Clustering Result",
                            lines=8,
                            interactive=False
                        )
                        
                        cluster_btn = gr.Button("Cluster Data", elem_classes=["calc-button"])
                    
                    with gr.Column():
                        gr.HTML('<div class="section-header">Machine Learning Tools</div>')
                        
                        ml_info = gr.Markdown("""
                        **Polynomial Regression:**
                        - Fit polynomials of any degree
                        - R² score and RMSE metrics
                        - Coefficients and intercept
                        - Perfect for non-linear relationships
                        
                        **K-means Clustering:**
                        - Unsupervised learning algorithm
                        - Find natural groupings in data
                        - Cluster centers and inertia
                        - Data visualization support
                        
                        **Applications:**
                        - Predictive modeling
                        - Data classification
                        - Pattern recognition
                        - Business analytics
                        
                        **Data Format:**
                        - X/Y data as JSON arrays
                        - Clustering data as array of coordinate pairs
                        - Automatic validation and error handling
                        """)
                
                # Event handlers
                poly_btn.click(
                    polynomial_regression_advanced,
                    inputs=[poly_x_data, poly_y_data, poly_degree],
                    outputs=[poly_result]
                )
                
                cluster_btn.click(
                    kmeans_clustering,
                    inputs=[cluster_data, n_clusters],
                    outputs=[cluster_result]
                )
            
            # Financial Calculator Tab
            with gr.Tab("💰 Financial"):
                with gr.Row():
                    with gr.Column():
                        gr.HTML('<div class="section-header">Financial Calculations</div>')
                        
                        fin_calc_type = gr.Dropdown(
                            choices=["Compound Interest", "Present Value", "Loan Payment"],
                            label="Calculation Type",
                            value="Compound Interest"
                        )
                        
                        principal = gr.Number(
                            label="Principal Amount",
                            value=1000
                        )
                        
                        rate = gr.Number(
                            label="Interest Rate (decimal)",
                            value=0.05
                        )
                        
                        time_period = gr.Number(
                            label="Time Period",
                            value=5
                        )
                        
                        compounding_freq = gr.Number(
                            label="Compounding Frequency (per year)",
                            value=12,
                            precision=0
                        )
                        
                        fin_result = gr.Textbox(
                            label="Financial Calculation Result",
                            lines=8,
                            interactive=False
                        )
                        
                        fin_btn = gr.Button("Calculate", elem_classes=["calc-button"])
                        
                        gr.HTML('<div class="section-header">Monte Carlo Simulation</div>')
                        
                        mc_simulations = gr.Number(
                            label="Number of Simulations",
                            value=10000,
                            precision=0
                        )
                        
                        mc_distribution = gr.Dropdown(
                            choices=["normal", "uniform", "exponential"],
                            label="Distribution",
                            value="normal"
                        )
                        
                        mc_mean = gr.Number(label="Mean", value=0)
                        mc_std = gr.Number(label="Standard Deviation", value=1)
                        
                        mc_result = gr.Textbox(
                            label="Monte Carlo Result",
                            lines=6,
                            interactive=False
                        )
                        
                        mc_btn = gr.Button("Run Simulation", elem_classes=["calc-button"])
                    
                    with gr.Column():
                        gr.HTML('<div class="section-header">Financial Tools</div>')
                        
                        fin_info = gr.Markdown("""
                        **Financial Calculations:**
                        - **Compound Interest**: Calculate future value with compounding
                        - **Present Value**: Find current value of future amount
                        - **Loan Payment**: Calculate monthly loan payments
                        
                        **Monte Carlo Simulation:**
                        - Risk analysis and modeling
                        - Portfolio optimization
                        - Project valuation
                        - Statistical modeling
                        
                        **Usage Examples:**
                        - Investment planning
                        - Retirement calculations
                        - Loan analysis
                        - Risk assessment
                        
                        **Rate Format:**
                        - Use decimal format (0.05 = 5%)
                        - Annual rates for most calculations
                        - Monthly rates for loan payments
                        """)
                
                # Event handlers
                fin_btn.click(
                    financial_calculations,
                    inputs=[fin_calc_type, principal, rate, time_period, compounding_freq],
                    outputs=[fin_result]
                )
                
                mc_btn.click(
                    monte_carlo_simulation,
                    inputs=[mc_simulations, mc_distribution, mc_mean, mc_std],
                    outputs=[mc_result]
                )
            
            # Data Management Tab
            with gr.Tab("💾 Data Management"):
                with gr.Row():
                    with gr.Column():
                        gr.HTML('<div class="section-header">Load Data</div>')
                        
                        csv_input = gr.Textbox(
                            label="CSV Data",
                            placeholder="col1,col2,col3\n1,2,3\n4,5,6",
                            lines=6
                        )
                        
                        csv_result = gr.Textbox(
                            label="Load Result",
                            lines=8,
                            interactive=False
                        )
                        
                        load_csv_btn = gr.Button("Load CSV", elem_classes=["calc-button"])
                        
                        gr.HTML('<div class="section-header">Generate Sample Data</div>')
                        
                        data_type = gr.Dropdown(
                            choices=["normal", "linear_regression", "categorical", "time_series"],
                            label="Data Type",
                            value="normal"
                        )
                        
                        data_size = gr.Number(
                            label="Sample Size",
                            value=100,
                            precision=0
                        )
                        
                        sample_result = gr.Textbox(
                            label="Generated Data",
                            lines=8,
                            interactive=False
                        )
                        
                        generate_data_btn = gr.Button("Generate Data", elem_classes=["calc-button"])
                    
                    with gr.Column():
                        gr.HTML('<div class="section-header">Data Management</div>')
                        
                        data_info = gr.Markdown("""
                        **Supported Formats:**
                        - CSV files with headers
                        - JSON arrays
                        - Manual data entry
                        
                        **Data Types:**
                        - **Normal**: Gaussian distribution
                        - **Linear Regression**: Linear relationship with noise
                        - **Categorical**: Categorical and numeric variables
                        - **Time Series**: Date and value columns
                        
                        **Features:**
                        - Data validation
                        - Statistical summaries
                        - Export capabilities
                        - Data preview
                        
                        **CSV Format Example:**
                        ```
                        name,age,salary
                        Alice,25,50000
                        Bob,30,60000
                        Carol,35,70000
                        ```
                        """)
                
                # Event handlers
                load_csv_btn.click(
                    load_csv_data,
                    inputs=[csv_input],
                    outputs=[csv_result]
                )
                
                generate_data_btn.click(
                    lambda dt, ds: generate_sample_data(dt, ds),
                    inputs=[data_type, data_size],
                    outputs=[sample_result]
                )
    
    return app


# Create and launch the application
if __name__ == "__main__":
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )


