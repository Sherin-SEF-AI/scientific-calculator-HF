"""
Data Handler Module
Handles data import/export, file processing, and data manipulation
"""

import pandas as pd
import numpy as np
import json
import csv
import io
from typing import Union, List, Dict, Any, Optional
import base64


class DataHandler:
    """Comprehensive data handling and processing tools"""
    
    def __init__(self):
        self.loaded_datasets = {}
        self.current_dataset = None
    
    def load_csv_from_string(self, csv_string: str, delimiter: str = ',') -> Dict[str, Any]:
        """Load CSV data from string"""
        try:
            # Use StringIO to read CSV from string
            csv_buffer = io.StringIO(csv_string)
            
            # Try to detect if first row contains headers
            sample = csv_buffer.read(1024)
            csv_buffer.seek(0)
            
            # Check if first row looks like headers (non-numeric)
            first_line = sample.split('\n')[0]
            first_row = first_line.split(delimiter)
            
            # Simple heuristic: if most values are non-numeric, treat as headers
            numeric_count = 0
            for value in first_row[:5]:  # Check first 5 columns
                try:
                    float(value.strip())
                    numeric_count += 1
                except ValueError:
                    pass
            
            has_headers = numeric_count < len(first_row) / 2
            
            # Read CSV
            df = pd.read_csv(csv_buffer, delimiter=delimiter, header=0 if has_headers else None)
            
            # Store dataset
            dataset_id = f"dataset_{len(self.loaded_datasets) + 1}"
            self.loaded_datasets[dataset_id] = df
            self.current_dataset = dataset_id
            
            return {
                'status': 'success',
                'dataset_id': dataset_id,
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'data_types': df.dtypes.astype(str).to_dict(),
                'preview': df.head().to_dict('records'),
                'has_headers': has_headers
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def load_csv_from_file(self, file_content: str, filename: str) -> Dict[str, Any]:
        """Load CSV data from uploaded file"""
        try:
            # Decode base64 content if needed
            try:
                file_data = base64.b64decode(file_content).decode('utf-8')
            except:
                file_data = file_content
            
            return self.load_csv_from_string(file_data)
            
        except Exception as e:
            return {
                'status': 'error',
                'error': f"Error loading file {filename}: {str(e)}"
            }
    
    def create_dataset_from_data(self, data: Union[List[Dict], str], 
                                columns: List[str] = None) -> Dict[str, Any]:
        """Create dataset from structured data"""
        try:
            if isinstance(data, str):
                data = json.loads(data)
            
            df = pd.DataFrame(data)
            
            if columns:
                if len(columns) == len(df.columns):
                    df.columns = columns
                else:
                    return {
                        'status': 'error',
                        'error': f"Number of column names ({len(columns)}) doesn't match number of columns ({len(df.columns)})"
                    }
            
            # Store dataset
            dataset_id = f"dataset_{len(self.loaded_datasets) + 1}"
            self.loaded_datasets[dataset_id] = df
            self.current_dataset = dataset_id
            
            return {
                'status': 'success',
                'dataset_id': dataset_id,
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'data_types': df.dtypes.astype(str).to_dict(),
                'preview': df.head().to_dict('records')
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_dataset_info(self, dataset_id: str = None) -> Dict[str, Any]:
        """Get information about a dataset"""
        try:
            if dataset_id is None:
                dataset_id = self.current_dataset
            
            if dataset_id not in self.loaded_datasets:
                return {
                    'status': 'error',
                    'error': f"Dataset {dataset_id} not found"
                }
            
            df = self.loaded_datasets[dataset_id]
            
            # Calculate basic statistics
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
            
            info = {
                'status': 'success',
                'dataset_id': dataset_id,
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'data_types': df.dtypes.astype(str).to_dict(),
                'numeric_columns': numeric_columns,
                'categorical_columns': categorical_columns,
                'missing_values': df.isnull().sum().to_dict(),
                'memory_usage': df.memory_usage(deep=True).sum()
            }
            
            # Add descriptive statistics for numeric columns
            if numeric_columns:
                info['numeric_stats'] = df[numeric_columns].describe().to_dict()
            
            return info
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_column_data(self, column_name: str, dataset_id: str = None) -> Dict[str, Any]:
        """Get data from a specific column"""
        try:
            if dataset_id is None:
                dataset_id = self.current_dataset
            
            if dataset_id not in self.loaded_datasets:
                return {
                    'status': 'error',
                    'error': f"Dataset {dataset_id} not found"
                }
            
            df = self.loaded_datasets[dataset_id]
            
            if column_name not in df.columns:
                return {
                    'status': 'error',
                    'error': f"Column {column_name} not found in dataset"
                }
            
            column_data = df[column_name]
            
            return {
                'status': 'success',
                'column_name': column_name,
                'data_type': str(column_data.dtype),
                'values': column_data.tolist(),
                'unique_values': column_data.nunique(),
                'missing_count': column_data.isnull().sum()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def filter_dataset(self, conditions: Dict[str, Any], dataset_id: str = None) -> Dict[str, Any]:
        """Filter dataset based on conditions"""
        try:
            if dataset_id is None:
                dataset_id = self.current_dataset
            
            if dataset_id not in self.loaded_datasets:
                return {
                    'status': 'error',
                    'error': f"Dataset {dataset_id} not found"
                }
            
            df = self.loaded_datasets[dataset_id]
            filtered_df = df.copy()
            
            # Apply filters
            for column, condition in conditions.items():
                if column not in df.columns:
                    continue
                
                if condition['type'] == 'equals':
                    filtered_df = filtered_df[filtered_df[column] == condition['value']]
                elif condition['type'] == 'greater_than':
                    filtered_df = filtered_df[filtered_df[column] > condition['value']]
                elif condition['type'] == 'less_than':
                    filtered_df = filtered_df[filtered_df[column] < condition['value']]
                elif condition['type'] == 'contains':
                    filtered_df = filtered_df[filtered_df[column].astype(str).str.contains(condition['value'])]
                elif condition['type'] == 'in_range':
                    filtered_df = filtered_df[
                        (filtered_df[column] >= condition['min']) & 
                        (filtered_df[column] <= condition['max'])
                    ]
            
            # Store filtered dataset
            filtered_id = f"filtered_{len(self.loaded_datasets) + 1}"
            self.loaded_datasets[filtered_id] = filtered_df
            
            return {
                'status': 'success',
                'filtered_dataset_id': filtered_id,
                'original_rows': len(df),
                'filtered_rows': len(filtered_df),
                'conditions_applied': conditions,
                'preview': filtered_df.head().to_dict('records')
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def export_dataset(self, dataset_id: str = None, format: str = 'csv') -> Dict[str, Any]:
        """Export dataset in various formats"""
        try:
            if dataset_id is None:
                dataset_id = self.current_dataset
            
            if dataset_id not in self.loaded_datasets:
                return {
                    'status': 'error',
                    'error': f"Dataset {dataset_id} not found"
                }
            
            df = self.loaded_datasets[dataset_id]
            
            if format == 'csv':
                csv_string = df.to_csv(index=False)
                return {
                    'status': 'success',
                    'format': format,
                    'data': csv_string,
                    'size': len(csv_string)
                }
            
            elif format == 'json':
                json_string = df.to_json(orient='records', indent=2)
                return {
                    'status': 'success',
                    'format': format,
                    'data': json_string,
                    'size': len(json_string)
                }
            
            elif format == 'excel':
                # Convert to base64 for Excel
                excel_buffer = io.BytesIO()
                df.to_excel(excel_buffer, index=False)
                excel_data = base64.b64encode(excel_buffer.getvalue()).decode()
                return {
                    'status': 'success',
                    'format': format,
                    'data': excel_data,
                    'size': len(excel_data)
                }
            
            else:
                return {
                    'status': 'error',
                    'error': f"Unsupported format: {format}"
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def generate_sample_data(self, data_type: str, **params) -> Dict[str, Any]:
        """Generate sample datasets for testing"""
        try:
            if data_type == 'normal':
                n_samples = params.get('n_samples', 1000)
                mean = params.get('mean', 0)
                std = params.get('std', 1)
                
                data = np.random.normal(mean, std, n_samples)
                df = pd.DataFrame({'value': data})
                
            elif data_type == 'linear_regression':
                n_samples = params.get('n_samples', 100)
                noise = params.get('noise', 0.1)
                
                x = np.random.uniform(-10, 10, n_samples)
                y = 2 * x + 3 + np.random.normal(0, noise, n_samples)
                df = pd.DataFrame({'x': x, 'y': y})
                
            elif data_type == 'categorical':
                n_samples = params.get('n_samples', 100)
                categories = params.get('categories', ['A', 'B', 'C'])
                
                category_data = np.random.choice(categories, n_samples)
                value_data = np.random.normal(10, 2, n_samples)
                df = pd.DataFrame({
                    'category': category_data,
                    'value': value_data
                })
                
            elif data_type == 'time_series':
                n_samples = params.get('n_samples', 100)
                
                dates = pd.date_range(start='2020-01-01', periods=n_samples, freq='D')
                trend = np.arange(n_samples) * 0.1
                seasonal = 5 * np.sin(2 * np.pi * np.arange(n_samples) / 365.25)
                noise = np.random.normal(0, 1, n_samples)
                values = trend + seasonal + noise
                
                df = pd.DataFrame({
                    'date': dates,
                    'value': values
                })
                
            else:
                return {
                    'status': 'error',
                    'error': f"Unknown data type: {data_type}"
                }
            
            # Store generated dataset
            dataset_id = f"generated_{len(self.loaded_datasets) + 1}"
            self.loaded_datasets[dataset_id] = df
            self.current_dataset = dataset_id
            
            return {
                'status': 'success',
                'dataset_id': dataset_id,
                'data_type': data_type,
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'preview': df.head().to_dict('records')
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def list_datasets(self) -> Dict[str, Any]:
        """List all loaded datasets"""
        try:
            dataset_info = {}
            for dataset_id, df in self.loaded_datasets.items():
                dataset_info[dataset_id] = {
                    'shape': df.shape,
                    'columns': df.columns.tolist(),
                    'data_types': df.dtypes.astype(str).to_dict()
                }
            
            return {
                'status': 'success',
                'datasets': dataset_info,
                'current_dataset': self.current_dataset,
                'total_datasets': len(self.loaded_datasets)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def delete_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """Delete a dataset"""
        try:
            if dataset_id not in self.loaded_datasets:
                return {
                    'status': 'error',
                    'error': f"Dataset {dataset_id} not found"
                }
            
            del self.loaded_datasets[dataset_id]
            
            # Reset current dataset if it was deleted
            if self.current_dataset == dataset_id:
                self.current_dataset = list(self.loaded_datasets.keys())[-1] if self.loaded_datasets else None
            
            return {
                'status': 'success',
                'deleted_dataset': dataset_id,
                'remaining_datasets': len(self.loaded_datasets)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }


def create_data_handler() -> DataHandler:
    """Factory function to create data handler instance"""
    return DataHandler()
