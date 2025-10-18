"""
Data Visualization Module
Handles plotting, charting, and interactive visualizations using Plotly and Matplotlib
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Union, List, Dict, Any, Optional, Tuple
import json
import io
import base64


class DataVisualizer:
    """Comprehensive data visualization tools"""
    
    def __init__(self):
        self.theme_colors = {
            'primary': '#1E40AF',    # Navy Blue
            'secondary': '#6B7280',  # Gray
            'accent': '#F59E0B',     # Orange
            'background': '#F9FAFB', # Light Gray
            'text': '#374151'        # Dark Gray
        }
    
    def _prepare_data(self, data: Union[List, str, np.ndarray, pd.DataFrame]) -> np.ndarray:
        """Prepare data for visualization"""
        if isinstance(data, str):
            data = json.loads(data)
        elif isinstance(data, pd.DataFrame):
            return data
        return np.array(data, dtype=float)
    
    def line_plot(self, x: Union[List, str, np.ndarray], 
                  y: Union[List, str, np.ndarray],
                  title: str = "Line Plot",
                  x_label: str = "X",
                  y_label: str = "Y") -> go.Figure:
        """Create interactive line plot"""
        try:
            x_data = self._prepare_data(x)
            y_data = self._prepare_data(y)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                mode='lines+markers',
                line=dict(color=self.theme_colors['primary'], width=2),
                marker=dict(color=self.theme_colors['accent'], size=6),
                name='Data'
            ))
            
            fig.update_layout(
                title=dict(text=title, x=0.5, font=dict(color=self.theme_colors['text'])),
                xaxis_title=x_label,
                yaxis_title=y_label,
                plot_bgcolor='white',
                paper_bgcolor=self.theme_colors['background'],
                font=dict(color=self.theme_colors['text']),
                margin=dict(l=50, r=50, t=60, b=50)
            )
            
            return fig
            
        except Exception as e:
            # Return error figure
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error creating line plot: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(color="red", size=16)
            )
            return fig
    
    def scatter_plot(self, x: Union[List, str, np.ndarray], 
                     y: Union[List, str, np.ndarray],
                     title: str = "Scatter Plot",
                     x_label: str = "X",
                     y_label: str = "Y",
                     color: Union[List, str, np.ndarray] = None) -> go.Figure:
        """Create interactive scatter plot"""
        try:
            x_data = self._prepare_data(x)
            y_data = self._prepare_data(y)
            
            fig = go.Figure()
            
            if color is not None:
                color_data = self._prepare_data(color)
                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=y_data,
                    mode='markers',
                    marker=dict(
                        color=color_data,
                        colorscale='Viridis',
                        size=8,
                        showscale=True,
                        colorbar=dict(title="Color Scale")
                    ),
                    name='Data'
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=y_data,
                    mode='markers',
                    marker=dict(
                        color=self.theme_colors['accent'],
                        size=8
                    ),
                    name='Data'
                ))
            
            fig.update_layout(
                title=dict(text=title, x=0.5, font=dict(color=self.theme_colors['text'])),
                xaxis_title=x_label,
                yaxis_title=y_label,
                plot_bgcolor='white',
                paper_bgcolor=self.theme_colors['background'],
                font=dict(color=self.theme_colors['text']),
                margin=dict(l=50, r=50, t=60, b=50)
            )
            
            return fig
            
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error creating scatter plot: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(color="red", size=16)
            )
            return fig
    
    def bar_chart(self, categories: Union[List, str], 
                  values: Union[List, str, np.ndarray],
                  title: str = "Bar Chart",
                  x_label: str = "Categories",
                  y_label: str = "Values") -> go.Figure:
        """Create interactive bar chart"""
        try:
            if isinstance(categories, str):
                categories = json.loads(categories)
            values_data = self._prepare_data(values)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=categories,
                y=values_data,
                marker_color=self.theme_colors['primary'],
                marker_line=dict(color=self.theme_colors['secondary'], width=1)
            ))
            
            fig.update_layout(
                title=dict(text=title, x=0.5, font=dict(color=self.theme_colors['text'])),
                xaxis_title=x_label,
                yaxis_title=y_label,
                plot_bgcolor='white',
                paper_bgcolor=self.theme_colors['background'],
                font=dict(color=self.theme_colors['text']),
                margin=dict(l=50, r=50, t=60, b=50)
            )
            
            return fig
            
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error creating bar chart: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(color="red", size=16)
            )
            return fig
    
    def histogram(self, data: Union[List, str, np.ndarray],
                  title: str = "Histogram",
                  bins: int = 30,
                  x_label: str = "Value",
                  y_label: str = "Frequency") -> go.Figure:
        """Create interactive histogram"""
        try:
            data_array = self._prepare_data(data)
            
            fig = go.Figure()
            
            fig.add_trace(go.Histogram(
                x=data_array,
                nbinsx=bins,
                marker_color=self.theme_colors['primary'],
                marker_line=dict(color=self.theme_colors['secondary'], width=1),
                opacity=0.7
            ))
            
            fig.update_layout(
                title=dict(text=title, x=0.5, font=dict(color=self.theme_colors['text'])),
                xaxis_title=x_label,
                yaxis_title=y_label,
                plot_bgcolor='white',
                paper_bgcolor=self.theme_colors['background'],
                font=dict(color=self.theme_colors['text']),
                margin=dict(l=50, r=50, t=60, b=50)
            )
            
            return fig
            
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error creating histogram: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(color="red", size=16)
            )
            return fig
    
    def pie_chart(self, labels: Union[List, str], 
                  values: Union[List, str, np.ndarray],
                  title: str = "Pie Chart") -> go.Figure:
        """Create interactive pie chart"""
        try:
            if isinstance(labels, str):
                labels = json.loads(labels)
            values_data = self._prepare_data(values)
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values_data,
                marker_colors=[self.theme_colors['primary'], 
                              self.theme_colors['accent'], 
                              self.theme_colors['secondary']]
            )])
            
            fig.update_layout(
                title=dict(text=title, x=0.5, font=dict(color=self.theme_colors['text'])),
                paper_bgcolor=self.theme_colors['background'],
                font=dict(color=self.theme_colors['text']),
                margin=dict(l=50, r=50, t=60, b=50)
            )
            
            return fig
            
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error creating pie chart: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(color="red", size=16)
            )
            return fig
    
    def box_plot(self, data: Union[List, str, np.ndarray],
                 title: str = "Box Plot",
                 y_label: str = "Value") -> go.Figure:
        """Create interactive box plot"""
        try:
            data_array = self._prepare_data(data)
            
            fig = go.Figure()
            
            fig.add_trace(go.Box(
                y=data_array,
                marker_color=self.theme_colors['primary'],
                boxmean='sd'  # Show mean and standard deviation
            ))
            
            fig.update_layout(
                title=dict(text=title, x=0.5, font=dict(color=self.theme_colors['text'])),
                yaxis_title=y_label,
                plot_bgcolor='white',
                paper_bgcolor=self.theme_colors['background'],
                font=dict(color=self.theme_colors['text']),
                margin=dict(l=50, r=50, t=60, b=50)
            )
            
            return fig
            
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error creating box plot: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(color="red", size=16)
            )
            return fig
    
    def heatmap(self, data: Union[List[List], str],
                title: str = "Heatmap",
                x_labels: List[str] = None,
                y_labels: List[str] = None) -> go.Figure:
        """Create interactive heatmap"""
        try:
            if isinstance(data, str):
                data = json.loads(data)
            data_array = np.array(data, dtype=float)
            
            fig = go.Figure(data=go.Heatmap(
                z=data_array,
                x=x_labels if x_labels else list(range(data_array.shape[1])),
                y=y_labels if y_labels else list(range(data_array.shape[0])),
                colorscale='Viridis',
                showscale=True
            ))
            
            fig.update_layout(
                title=dict(text=title, x=0.5, font=dict(color=self.theme_colors['text'])),
                plot_bgcolor='white',
                paper_bgcolor=self.theme_colors['background'],
                font=dict(color=self.theme_colors['text']),
                margin=dict(l=50, r=50, t=60, b=50)
            )
            
            return fig
            
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error creating heatmap: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(color="red", size=16)
            )
            return fig
    
    def surface_plot_3d(self, x: Union[List, str, np.ndarray],
                       y: Union[List, str, np.ndarray],
                       z: Union[List[List], str],
                       title: str = "3D Surface Plot") -> go.Figure:
        """Create 3D surface plot"""
        try:
            x_data = self._prepare_data(x)
            y_data = self._prepare_data(y)
            
            if isinstance(z, str):
                z = json.loads(z)
            z_data = np.array(z, dtype=float)
            
            fig = go.Figure(data=[go.Surface(
                x=x_data,
                y=y_data,
                z=z_data,
                colorscale='Viridis'
            )])
            
            fig.update_layout(
                title=dict(text=title, x=0.5, font=dict(color=self.theme_colors['text'])),
                scene=dict(
                    xaxis_title="X",
                    yaxis_title="Y",
                    zaxis_title="Z",
                    bgcolor='white'
                ),
                paper_bgcolor=self.theme_colors['background'],
                font=dict(color=self.theme_colors['text']),
                margin=dict(l=50, r=50, t=60, b=50)
            )
            
            return fig
            
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error creating 3D surface plot: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(color="red", size=16)
            )
            return fig
    
    def regression_plot(self, x: Union[List, str, np.ndarray],
                       y: Union[List, str, np.ndarray],
                       slope: float = None,
                       intercept: float = None,
                       title: str = "Regression Plot") -> go.Figure:
        """Create regression plot with trend line"""
        try:
            x_data = self._prepare_data(x)
            y_data = self._prepare_data(y)
            
            fig = go.Figure()
            
            # Add scatter points
            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                mode='markers',
                marker=dict(color=self.theme_colors['primary'], size=8),
                name='Data Points'
            ))
            
            # Add regression line if coefficients provided
            if slope is not None and intercept is not None:
                x_line = np.linspace(min(x_data), max(x_data), 100)
                y_line = slope * x_line + intercept
                
                fig.add_trace(go.Scatter(
                    x=x_line,
                    y=y_line,
                    mode='lines',
                    line=dict(color=self.theme_colors['accent'], width=3),
                    name='Regression Line'
                ))
            
            fig.update_layout(
                title=dict(text=title, x=0.5, font=dict(color=self.theme_colors['text'])),
                xaxis_title="X",
                yaxis_title="Y",
                plot_bgcolor='white',
                paper_bgcolor=self.theme_colors['background'],
                font=dict(color=self.theme_colors['text']),
                margin=dict(l=50, r=50, t=60, b=50)
            )
            
            return fig
            
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error creating regression plot: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(color="red", size=16)
            )
            return fig
    
    def function_plot(self, function_expr: str,
                     x_range: Tuple[float, float] = (-10, 10),
                     num_points: int = 1000,
                     title: str = "Function Plot") -> go.Figure:
        """Plot mathematical function"""
        try:
            import sympy as sp
            
            # Parse function expression
            x = sp.Symbol('x')
            func = sp.sympify(function_expr)
            
            # Convert to numpy function
            func_numpy = sp.lambdify(x, func, 'numpy')
            
            # Generate x values
            x_values = np.linspace(x_range[0], x_range[1], num_points)
            
            # Calculate y values
            y_values = func_numpy(x_values)
            
            # Handle complex results
            if np.iscomplexobj(y_values):
                y_values = np.real(y_values)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=x_values,
                y=y_values,
                mode='lines',
                line=dict(color=self.theme_colors['primary'], width=2),
                name=f'y = {function_expr}'
            ))
            
            fig.update_layout(
                title=dict(text=title, x=0.5, font=dict(color=self.theme_colors['text'])),
                xaxis_title="x",
                yaxis_title="y",
                plot_bgcolor='white',
                paper_bgcolor=self.theme_colors['background'],
                font=dict(color=self.theme_colors['text']),
                margin=dict(l=50, r=50, t=60, b=50)
            )
            
            return fig
            
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error plotting function: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(color="red", size=16)
            )
            return fig
    
    def export_plot(self, fig: go.Figure, format: str = "png") -> str:
        """Export plot as base64 encoded string"""
        try:
            if format == "png":
                img_bytes = fig.to_image(format="png", width=800, height=600)
            elif format == "svg":
                img_bytes = fig.to_image(format="svg", width=800, height=600)
            else:
                raise ValueError("Unsupported format. Use 'png' or 'svg'")
            
            return base64.b64encode(img_bytes).decode()
            
        except Exception as e:
            return f"Error exporting plot: {str(e)}"


def create_visualizer() -> DataVisualizer:
    """Factory function to create data visualizer instance"""
    return DataVisualizer()


