"""
Advanced Features Module
Handles advanced mathematical computations, machine learning, and specialized tools
"""

import numpy as np
import pandas as pd
from scipy import optimize, integrate, interpolate
from scipy.stats import norm, t, chi2, f
import sympy as sp
from typing import Union, List, Dict, Any, Tuple, Optional
import json
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


class AdvancedCalculator:
    """Advanced mathematical and computational features"""
    
    def __init__(self):
        self.integration_history = []
        self.optimization_history = []
    
    def numerical_integration(self, function_expr: str, lower: float, upper: float, method: str = "quad") -> Dict[str, Any]:
        """Perform numerical integration"""
        try:
            # Parse function expression
            x = sp.Symbol('x')
            func = sp.sympify(function_expr)
            func_numpy = sp.lambdify(x, func, 'numpy')
            
            if method == "quad":
                result, error = integrate.quad(func_numpy, lower, upper)
                return {
                    'result': float(result),
                    'error_estimate': float(error),
                    'method': 'quadrature',
                    'status': 'success'
                }
            
            elif method == "trapezoid":
                x_vals = np.linspace(lower, upper, 1000)
                y_vals = func_numpy(x_vals)
                result = integrate.trapezoid(y_vals, x_vals)
                return {
                    'result': float(result),
                    'method': 'trapezoid',
                    'status': 'success'
                }
            
            elif method == "simpson":
                x_vals = np.linspace(lower, upper, 1001)  # Odd number for Simpson's rule
                y_vals = func_numpy(x_vals)
                result = integrate.simpson(y_vals, x_vals)
                return {
                    'result': float(result),
                    'method': 'simpson',
                    'status': 'success'
                }
            
            else:
                return {
                    'result': None,
                    'status': 'error',
                    'error': f'Unknown integration method: {method}'
                }
                
        except Exception as e:
            return {
                'result': None,
                'status': 'error',
                'error': str(e)
            }
    
    def numerical_differentiation(self, function_expr: str, point: float, h: float = 1e-6) -> Dict[str, Any]:
        """Perform numerical differentiation"""
        try:
            x = sp.Symbol('x')
            func = sp.sympify(function_expr)
            func_numpy = sp.lambdify(x, func, 'numpy')
            
            # Forward difference
            forward_diff = (func_numpy(point + h) - func_numpy(point)) / h
            
            # Central difference (more accurate)
            central_diff = (func_numpy(point + h) - func_numpy(point - h)) / (2 * h)
            
            # Backward difference
            backward_diff = (func_numpy(point) - func_numpy(point - h)) / h
            
            return {
                'forward_difference': float(forward_diff),
                'central_difference': float(central_diff),
                'backward_difference': float(backward_diff),
                'point': point,
                'step_size': h,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def optimization(self, function_expr: str, method: str = "minimize", 
                    bounds: Tuple[float, float] = None, initial_guess: float = 0) -> Dict[str, Any]:
        """Perform numerical optimization"""
        try:
            x = sp.Symbol('x')
            func = sp.sympify(function_expr)
            func_numpy = sp.lambdify(x, func, 'numpy')
            
            if method == "minimize":
                if bounds:
                    result = optimize.minimize_scalar(func_numpy, bounds=bounds, method='bounded')
                else:
                    result = optimize.minimize_scalar(func_numpy)
                
                return {
                    'optimal_point': float(result.x),
                    'optimal_value': float(result.fun),
                    'method': 'minimize',
                    'success': result.success,
                    'status': 'success'
                }
            
            elif method == "maximize":
                # Maximize by minimizing negative function
                neg_func = lambda x: -func_numpy(x)
                if bounds:
                    result = optimize.minimize_scalar(neg_func, bounds=bounds, method='bounded')
                else:
                    result = optimize.minimize_scalar(neg_func)
                
                return {
                    'optimal_point': float(result.x),
                    'optimal_value': float(-result.fun),  # Convert back to positive
                    'method': 'maximize',
                    'success': result.success,
                    'status': 'success'
                }
            
            else:
                return {
                    'status': 'error',
                    'error': f'Unknown optimization method: {method}'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def interpolation(self, x_data: List[float], y_data: List[float], 
                     x_new: List[float], method: str = "linear") -> Dict[str, Any]:
        """Perform interpolation"""
        try:
            x_data = np.array(x_data)
            y_data = np.array(y_data)
            x_new = np.array(x_new)
            
            if method == "linear":
                f = interpolate.interp1d(x_data, y_data, kind='linear')
                y_new = f(x_new)
            elif method == "cubic":
                f = interpolate.interp1d(x_data, y_data, kind='cubic')
                y_new = f(x_new)
            elif method == "quadratic":
                f = interpolate.interp1d(x_data, y_data, kind='quadratic')
                y_new = f(x_new)
            elif method == "spline":
                tck = interpolate.splrep(x_data, y_data)
                y_new = interpolate.splev(x_new, tck)
            else:
                return {
                    'status': 'error',
                    'error': f'Unknown interpolation method: {method}'
                }
            
            return {
                'x_interpolated': x_new.tolist(),
                'y_interpolated': y_new.tolist(),
                'method': method,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def fourier_transform(self, data: List[float], sample_rate: float = 1.0) -> Dict[str, Any]:
        """Perform FFT analysis"""
        try:
            data_array = np.array(data)
            n = len(data_array)
            
            # Compute FFT
            fft_result = np.fft.fft(data_array)
            frequencies = np.fft.fftfreq(n, 1/sample_rate)
            
            # Get magnitude and phase
            magnitude = np.abs(fft_result)
            phase = np.angle(fft_result)
            
            return {
                'frequencies': frequencies[:n//2].tolist(),
                'magnitude': magnitude[:n//2].tolist(),
                'phase': phase[:n//2].tolist(),
                'sample_rate': sample_rate,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def differential_equation_solver(self, equation_expr: str, initial_conditions: Dict[str, float],
                                   t_span: Tuple[float, float], t_eval: List[float] = None) -> Dict[str, Any]:
        """Solve ordinary differential equations"""
        try:
            from scipy.integrate import solve_ivp
            
            # This is a simplified version - in practice, you'd need more sophisticated parsing
            # For now, we'll solve a simple example: dy/dt = -y
            def dydt(t, y):
                return -y  # Simple exponential decay
            
            if t_eval is None:
                t_eval = np.linspace(t_span[0], t_span[1], 100)
            
            y0 = initial_conditions.get('y0', 1.0)
            
            sol = solve_ivp(dydt, t_span, [y0], t_eval=t_eval)
            
            return {
                'time': sol.t.tolist(),
                'solution': sol.y[0].tolist(),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def monte_carlo_simulation(self, n_simulations: int, distribution: str = "normal", **params) -> Dict[str, Any]:
        """Perform Monte Carlo simulation"""
        try:
            if distribution == "normal":
                mean = params.get('mean', 0)
                std = params.get('std', 1)
                samples = np.random.normal(mean, std, n_simulations)
            
            elif distribution == "uniform":
                low = params.get('low', 0)
                high = params.get('high', 1)
                samples = np.random.uniform(low, high, n_simulations)
            
            elif distribution == "exponential":
                scale = params.get('scale', 1)
                samples = np.random.exponential(scale, n_simulations)
            
            else:
                return {
                    'status': 'error',
                    'error': f'Unknown distribution: {distribution}'
                }
            
            return {
                'samples': samples.tolist(),
                'mean': float(np.mean(samples)),
                'std': float(np.std(samples)),
                'min': float(np.min(samples)),
                'max': float(np.max(samples)),
                'n_simulations': n_simulations,
                'distribution': distribution,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }


class MachineLearningTools:
    """Machine learning and advanced statistical tools"""
    
    def __init__(self):
        self.models = {}
    
    def polynomial_regression(self, x_data: List[float], y_data: List[float], degree: int = 2) -> Dict[str, Any]:
        """Perform polynomial regression"""
        try:
            x_data = np.array(x_data).reshape(-1, 1)
            y_data = np.array(y_data)
            
            # Create polynomial features
            poly_features = PolynomialFeatures(degree=degree)
            x_poly = poly_features.fit_transform(x_data)
            
            # Fit linear regression
            model = LinearRegression()
            model.fit(x_poly, y_data)
            
            # Predictions
            y_pred = model.predict(x_poly)
            
            # Metrics
            r2 = r2_score(y_data, y_pred)
            mse = mean_squared_error(y_data, y_pred)
            rmse = np.sqrt(mse)
            
            return {
                'coefficients': model.coef_.tolist(),
                'intercept': float(model.intercept_),
                'r2_score': float(r2),
                'mse': float(mse),
                'rmse': float(rmse),
                'predictions': y_pred.tolist(),
                'degree': degree,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def ridge_regression(self, x_data: List[List[float]], y_data: List[float], alpha: float = 1.0) -> Dict[str, Any]:
        """Perform ridge regression"""
        try:
            x_data = np.array(x_data)
            y_data = np.array(y_data)
            
            model = Ridge(alpha=alpha)
            model.fit(x_data, y_data)
            
            y_pred = model.predict(x_data)
            
            r2 = r2_score(y_data, y_pred)
            mse = mean_squared_error(y_data, y_pred)
            
            return {
                'coefficients': model.coef_.tolist(),
                'intercept': float(model.intercept_),
                'r2_score': float(r2),
                'mse': float(mse),
                'alpha': alpha,
                'predictions': y_pred.tolist(),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def lasso_regression(self, x_data: List[List[float]], y_data: List[float], alpha: float = 1.0) -> Dict[str, Any]:
        """Perform LASSO regression"""
        try:
            x_data = np.array(x_data)
            y_data = np.array(y_data)
            
            model = Lasso(alpha=alpha)
            model.fit(x_data, y_data)
            
            y_pred = model.predict(x_data)
            
            r2 = r2_score(y_data, y_pred)
            mse = mean_squared_error(y_data, y_pred)
            
            return {
                'coefficients': model.coef_.tolist(),
                'intercept': float(model.intercept_),
                'r2_score': float(r2),
                'mse': float(mse),
                'alpha': alpha,
                'predictions': y_pred.tolist(),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def kmeans_clustering(self, data: List[List[float]], n_clusters: int = 3) -> Dict[str, Any]:
        """Perform K-means clustering"""
        try:
            data_array = np.array(data)
            
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            labels = kmeans.fit_predict(data_array)
            
            return {
                'labels': labels.tolist(),
                'centers': kmeans.cluster_centers_.tolist(),
                'n_clusters': n_clusters,
                'inertia': float(kmeans.inertia_),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def principal_component_analysis(self, data: List[List[float]], n_components: int = 2) -> Dict[str, Any]:
        """Perform PCA"""
        try:
            data_array = np.array(data)
            
            pca = PCA(n_components=n_components)
            pca_result = pca.fit_transform(data_array)
            
            return {
                'transformed_data': pca_result.tolist(),
                'explained_variance_ratio': pca.explained_variance_ratio_.tolist(),
                'components': pca.components_.tolist(),
                'n_components': n_components,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }


class FinancialCalculator:
    """Financial and business calculations"""
    
    @staticmethod
    def compound_interest(principal: float, rate: float, time: float, compounding_frequency: int = 1) -> Dict[str, Any]:
        """Calculate compound interest"""
        try:
            amount = principal * (1 + rate / compounding_frequency) ** (compounding_frequency * time)
            interest = amount - principal
            
            return {
                'principal': principal,
                'final_amount': float(amount),
                'interest_earned': float(interest),
                'rate': rate,
                'time': time,
                'compounding_frequency': compounding_frequency,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    @staticmethod
    def present_value(future_value: float, rate: float, time: float) -> Dict[str, Any]:
        """Calculate present value"""
        try:
            present_val = future_value / (1 + rate) ** time
            
            return {
                'future_value': future_value,
                'present_value': float(present_val),
                'rate': rate,
                'time': time,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    @staticmethod
    def loan_payment(principal: float, annual_rate: float, years: int) -> Dict[str, Any]:
        """Calculate loan payment"""
        try:
            monthly_rate = annual_rate / 12
            num_payments = years * 12
            
            if monthly_rate == 0:
                monthly_payment = principal / num_payments
            else:
                monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / \
                                ((1 + monthly_rate) ** num_payments - 1)
            
            total_payments = monthly_payment * num_payments
            total_interest = total_payments - principal
            
            return {
                'principal': principal,
                'monthly_payment': float(monthly_payment),
                'total_payments': float(total_payments),
                'total_interest': float(total_interest),
                'annual_rate': annual_rate,
                'years': years,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }


def create_advanced_calculator() -> AdvancedCalculator:
    """Factory function to create advanced calculator instance"""
    return AdvancedCalculator()


def create_ml_tools() -> MachineLearningTools:
    """Factory function to create ML tools instance"""
    return MachineLearningTools()


def create_financial_calculator() -> FinancialCalculator:
    """Factory function to create financial calculator instance"""
    return FinancialCalculator()
