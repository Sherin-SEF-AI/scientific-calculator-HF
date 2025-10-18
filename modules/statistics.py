"""
Statistical Analysis Module
Handles descriptive statistics, hypothesis testing, regression analysis, and probability distributions
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Union, List, Dict, Any, Tuple, Optional
import json


class StatisticalAnalyzer:
    """Comprehensive statistical analysis tools"""
    
    def __init__(self):
        self.history = []
    
    def _prepare_data(self, data: Union[List, str, np.ndarray]) -> np.ndarray:
        """Prepare data for analysis"""
        if isinstance(data, str):
            data = json.loads(data)
        return np.array(data, dtype=float)
    
    def descriptive_stats(self, data: Union[List, str, np.ndarray]) -> Dict[str, Any]:
        """Calculate descriptive statistics"""
        try:
            data_array = self._prepare_data(data)
            
            stats_dict = {
                'count': len(data_array),
                'mean': float(np.mean(data_array)),
                'median': float(np.median(data_array)),
                'mode': float(stats.mode(data_array, keepdims=True)[0][0]),
                'std': float(np.std(data_array, ddof=1)),
                'var': float(np.var(data_array, ddof=1)),
                'min': float(np.min(data_array)),
                'max': float(np.max(data_array)),
                'range': float(np.max(data_array) - np.min(data_array)),
                'q1': float(np.percentile(data_array, 25)),
                'q3': float(np.percentile(data_array, 75)),
                'iqr': float(np.percentile(data_array, 75) - np.percentile(data_array, 25)),
                'skewness': float(stats.skew(data_array)),
                'kurtosis': float(stats.kurtosis(data_array)),
                'status': 'success'
            }
            
            return stats_dict
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def correlation_analysis(self, x: Union[List, str, np.ndarray], 
                           y: Union[List, str, np.ndarray]) -> Dict[str, Any]:
        """Calculate correlation coefficients"""
        try:
            x_array = self._prepare_data(x)
            y_array = self._prepare_data(y)
            
            if len(x_array) != len(y_array):
                raise ValueError("Arrays must have the same length")
            
            pearson_corr, pearson_p = stats.pearsonr(x_array, y_array)
            spearman_corr, spearman_p = stats.spearmanr(x_array, y_array)
            
            return {
                'pearson_correlation': float(pearson_corr),
                'pearson_p_value': float(pearson_p),
                'spearman_correlation': float(spearman_corr),
                'spearman_p_value': float(spearman_p),
                'sample_size': len(x_array),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def t_test(self, data1: Union[List, str, np.ndarray], 
               data2: Union[List, str, np.ndarray] = None,
               test_type: str = 'independent') -> Dict[str, Any]:
        """Perform t-test"""
        try:
            data1_array = self._prepare_data(data1)
            
            if data2 is not None:
                data2_array = self._prepare_data(data2)
                
                if test_type == 'independent':
                    t_stat, p_value = stats.ttest_ind(data1_array, data2_array)
                elif test_type == 'paired':
                    if len(data1_array) != len(data2_array):
                        raise ValueError("Paired t-test requires equal length arrays")
                    t_stat, p_value = stats.ttest_rel(data1_array, data2_array)
                else:
                    raise ValueError("test_type must be 'independent' or 'paired'")
                
                return {
                    'test_type': f'{test_type}_t_test',
                    't_statistic': float(t_stat),
                    'p_value': float(p_value),
                    'sample1_size': len(data1_array),
                    'sample2_size': len(data2_array),
                    'significant': p_value < 0.05,
                    'status': 'success'
                }
            else:
                # One-sample t-test
                t_stat, p_value = stats.ttest_1samp(data1_array, 0)
                
                return {
                    'test_type': 'one_sample_t_test',
                    't_statistic': float(t_stat),
                    'p_value': float(p_value),
                    'sample_size': len(data1_array),
                    'significant': p_value < 0.05,
                    'status': 'success'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def chi_square_test(self, observed: Union[List[List], str], 
                       expected: Union[List[List], str] = None) -> Dict[str, Any]:
        """Perform chi-square test"""
        try:
            if isinstance(observed, str):
                observed = json.loads(observed)
            observed_array = np.array(observed)
            
            if expected is not None:
                if isinstance(expected, str):
                    expected = json.loads(expected)
                expected_array = np.array(expected)
                chi2, p_value, dof, expected_freq = stats.chi2_contingency(observed_array)
            else:
                chi2, p_value, dof, expected_freq = stats.chi2_contingency(observed_array)
            
            return {
                'test_type': 'chi_square_test',
                'chi2_statistic': float(chi2),
                'p_value': float(p_value),
                'degrees_of_freedom': int(dof),
                'expected_frequencies': expected_freq.tolist(),
                'significant': p_value < 0.05,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def anova_test(self, *groups: Union[List, str, np.ndarray]) -> Dict[str, Any]:
        """Perform one-way ANOVA"""
        try:
            prepared_groups = [self._prepare_data(group) for group in groups]
            
            f_stat, p_value = stats.f_oneway(*prepared_groups)
            
            group_means = [np.mean(group) for group in prepared_groups]
            group_stds = [np.std(group, ddof=1) for group in prepared_groups]
            group_sizes = [len(group) for group in prepared_groups]
            
            return {
                'test_type': 'one_way_anova',
                'f_statistic': float(f_stat),
                'p_value': float(p_value),
                'num_groups': len(groups),
                'group_means': group_means,
                'group_stds': group_stds,
                'group_sizes': group_sizes,
                'significant': p_value < 0.05,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def linear_regression(self, x: Union[List, str, np.ndarray], 
                         y: Union[List, str, np.ndarray]) -> Dict[str, Any]:
        """Perform linear regression"""
        try:
            x_array = self._prepare_data(x)
            y_array = self._prepare_data(y)
            
            if len(x_array) != len(y_array):
                raise ValueError("Arrays must have the same length")
            
            # Calculate regression coefficients
            slope, intercept, r_value, p_value, std_err = stats.linregress(x_array, y_array)
            
            # Calculate R-squared
            r_squared = r_value ** 2
            
            # Calculate residuals
            y_pred = slope * x_array + intercept
            residuals = y_array - y_pred
            
            # Calculate standard error of estimate
            mse = np.mean(residuals ** 2)
            rmse = np.sqrt(mse)
            
            return {
                'slope': float(slope),
                'intercept': float(intercept),
                'r_squared': float(r_squared),
                'correlation': float(r_value),
                'p_value': float(p_value),
                'std_error': float(std_err),
                'rmse': float(rmse),
                'sample_size': len(x_array),
                'predictions': y_pred.tolist(),
                'residuals': residuals.tolist(),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def polynomial_regression(self, x: Union[List, str, np.ndarray], 
                            y: Union[List, str, np.ndarray], 
                            degree: int = 2) -> Dict[str, Any]:
        """Perform polynomial regression"""
        try:
            x_array = self._prepare_data(x)
            y_array = self._prepare_data(y)
            
            if len(x_array) != len(y_array):
                raise ValueError("Arrays must have the same length")
            
            # Fit polynomial
            coeffs = np.polyfit(x_array, y_array, degree)
            poly_func = np.poly1d(coeffs)
            
            # Calculate predictions
            y_pred = poly_func(x_array)
            
            # Calculate R-squared
            ss_res = np.sum((y_array - y_pred) ** 2)
            ss_tot = np.sum((y_array - np.mean(y_array)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            
            # Calculate RMSE
            rmse = np.sqrt(np.mean((y_array - y_pred) ** 2))
            
            return {
                'degree': degree,
                'coefficients': coeffs.tolist(),
                'r_squared': float(r_squared),
                'rmse': float(rmse),
                'predictions': y_pred.tolist(),
                'sample_size': len(x_array),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def probability_distribution(self, distribution: str, **params) -> Dict[str, Any]:
        """Generate probability distribution"""
        try:
            if distribution == 'normal':
                if 'loc' not in params or 'scale' not in params:
                    raise ValueError("Normal distribution requires 'loc' and 'scale' parameters")
                dist = stats.norm(loc=params['loc'], scale=params['scale'])
                
            elif distribution == 'uniform':
                if 'loc' not in params or 'scale' not in params:
                    raise ValueError("Uniform distribution requires 'loc' and 'scale' parameters")
                dist = stats.uniform(loc=params['loc'], scale=params['scale'])
                
            elif distribution == 'exponential':
                if 'scale' not in params:
                    raise ValueError("Exponential distribution requires 'scale' parameter")
                dist = stats.expon(scale=params['scale'])
                
            elif distribution == 'binomial':
                if 'n' not in params or 'p' not in params:
                    raise ValueError("Binomial distribution requires 'n' and 'p' parameters")
                dist = stats.binom(n=params['n'], p=params['p'])
                
            elif distribution == 'poisson':
                if 'mu' not in params:
                    raise ValueError("Poisson distribution requires 'mu' parameter")
                dist = stats.poisson(mu=params['mu'])
                
            else:
                raise ValueError(f"Unknown distribution: {distribution}")
            
            # Generate sample data
            sample_size = params.get('size', 1000)
            samples = dist.rvs(size=sample_size)
            
            # Calculate distribution statistics
            mean = dist.mean()
            var = dist.var()
            std = dist.std()
            
            return {
                'distribution': distribution,
                'parameters': params,
                'samples': samples.tolist(),
                'mean': float(mean),
                'variance': float(var),
                'std_deviation': float(std),
                'sample_size': sample_size,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def confidence_interval(self, data: Union[List, str, np.ndarray], 
                          confidence: float = 0.95) -> Dict[str, Any]:
        """Calculate confidence interval for mean"""
        try:
            data_array = self._prepare_data(data)
            
            mean = np.mean(data_array)
            std_err = stats.sem(data_array)
            
            # Calculate confidence interval
            alpha = 1 - confidence
            h = std_err * stats.t.ppf(1 - alpha/2, len(data_array) - 1)
            
            ci_lower = mean - h
            ci_upper = mean + h
            
            return {
                'mean': float(mean),
                'confidence_level': confidence,
                'confidence_interval': [float(ci_lower), float(ci_upper)],
                'margin_of_error': float(h),
                'sample_size': len(data_array),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }


def create_statistical_analyzer() -> StatisticalAnalyzer:
    """Factory function to create statistical analyzer instance"""
    return StatisticalAnalyzer()


