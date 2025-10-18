"""
Matrix Operations Module
Handles matrix calculations, linear algebra operations, and related computations
"""

import numpy as np
from typing import Union, List, Dict, Any, Tuple
import json


class MatrixCalculator:
    """Advanced matrix operations and linear algebra"""
    
    def __init__(self):
        self.history = []
    
    def create_matrix(self, data: Union[List[List], str], shape: Tuple[int, int] = None) -> np.ndarray:
        """
        Create matrix from data
        
        Args:
            data: Matrix data as list of lists or JSON string
            shape: Optional shape override
            
        Returns:
            NumPy array representing the matrix
        """
        try:
            if isinstance(data, str):
                data = json.loads(data)
            
            matrix = np.array(data, dtype=float)
            
            if shape and matrix.shape != shape:
                raise ValueError(f"Matrix shape {matrix.shape} doesn't match expected {shape}")
            
            return matrix
            
        except Exception as e:
            raise ValueError(f"Invalid matrix data: {e}")
    
    def add_matrices(self, matrix1: Union[List[List], str], matrix2: Union[List[List], str]) -> Dict[str, Any]:
        """Add two matrices"""
        try:
            A = self.create_matrix(matrix1)
            B = self.create_matrix(matrix2)
            
            if A.shape != B.shape:
                raise ValueError("Matrices must have the same dimensions")
            
            result = A + B
            
            return {
                'result': result.tolist(),
                'status': 'success',
                'operation': 'addition',
                'shape': result.shape
            }
            
        except Exception as e:
            return {
                'result': None,
                'status': 'error',
                'error': str(e),
                'operation': 'addition'
            }
    
    def multiply_matrices(self, matrix1: Union[List[List], str], matrix2: Union[List[List], str]) -> Dict[str, Any]:
        """Multiply two matrices"""
        try:
            A = self.create_matrix(matrix1)
            B = self.create_matrix(matrix2)
            
            if A.shape[1] != B.shape[0]:
                raise ValueError("Number of columns in first matrix must equal number of rows in second matrix")
            
            result = np.dot(A, B)
            
            return {
                'result': result.tolist(),
                'status': 'success',
                'operation': 'multiplication',
                'shape': result.shape
            }
            
        except Exception as e:
            return {
                'result': None,
                'status': 'error',
                'error': str(e),
                'operation': 'multiplication'
            }
    
    def scalar_multiply(self, matrix: Union[List[List], str], scalar: float) -> Dict[str, Any]:
        """Multiply matrix by scalar"""
        try:
            A = self.create_matrix(matrix)
            result = A * scalar
            
            return {
                'result': result.tolist(),
                'status': 'success',
                'operation': 'scalar_multiplication',
                'scalar': scalar,
                'shape': result.shape
            }
            
        except Exception as e:
            return {
                'result': None,
                'status': 'error',
                'error': str(e),
                'operation': 'scalar_multiplication'
            }
    
    def transpose(self, matrix: Union[List[List], str]) -> Dict[str, Any]:
        """Transpose matrix"""
        try:
            A = self.create_matrix(matrix)
            result = A.T
            
            return {
                'result': result.tolist(),
                'status': 'success',
                'operation': 'transpose',
                'original_shape': A.shape,
                'new_shape': result.shape
            }
            
        except Exception as e:
            return {
                'result': None,
                'status': 'error',
                'error': str(e),
                'operation': 'transpose'
            }
    
    def determinant(self, matrix: Union[List[List], str]) -> Dict[str, Any]:
        """Calculate matrix determinant"""
        try:
            A = self.create_matrix(matrix)
            
            if A.shape[0] != A.shape[1]:
                raise ValueError("Matrix must be square to calculate determinant")
            
            det = np.linalg.det(A)
            
            return {
                'result': float(det),
                'status': 'success',
                'operation': 'determinant',
                'shape': A.shape
            }
            
        except Exception as e:
            return {
                'result': None,
                'status': 'error',
                'error': str(e),
                'operation': 'determinant'
            }
    
    def inverse(self, matrix: Union[List[List], str]) -> Dict[str, Any]:
        """Calculate matrix inverse"""
        try:
            A = self.create_matrix(matrix)
            
            if A.shape[0] != A.shape[1]:
                raise ValueError("Matrix must be square to calculate inverse")
            
            det = np.linalg.det(A)
            if abs(det) < 1e-10:
                raise ValueError("Matrix is singular (determinant ≈ 0)")
            
            result = np.linalg.inv(A)
            
            return {
                'result': result.tolist(),
                'status': 'success',
                'operation': 'inverse',
                'determinant': float(det),
                'shape': result.shape
            }
            
        except Exception as e:
            return {
                'result': None,
                'status': 'error',
                'error': str(e),
                'operation': 'inverse'
            }
    
    def eigenvalues(self, matrix: Union[List[List], str]) -> Dict[str, Any]:
        """Calculate eigenvalues and eigenvectors"""
        try:
            A = self.create_matrix(matrix)
            
            if A.shape[0] != A.shape[1]:
                raise ValueError("Matrix must be square to calculate eigenvalues")
            
            eigenvalues, eigenvectors = np.linalg.eig(A)
            
            return {
                'eigenvalues': eigenvalues.tolist(),
                'eigenvectors': eigenvectors.tolist(),
                'status': 'success',
                'operation': 'eigenvalues',
                'shape': A.shape
            }
            
        except Exception as e:
            return {
                'eigenvalues': None,
                'eigenvectors': None,
                'status': 'error',
                'error': str(e),
                'operation': 'eigenvalues'
            }
    
    def rank(self, matrix: Union[List[List], str]) -> Dict[str, Any]:
        """Calculate matrix rank"""
        try:
            A = self.create_matrix(matrix)
            rank = np.linalg.matrix_rank(A)
            
            return {
                'result': int(rank),
                'status': 'success',
                'operation': 'rank',
                'shape': A.shape
            }
            
        except Exception as e:
            return {
                'result': None,
                'status': 'error',
                'error': str(e),
                'operation': 'rank'
            }
    
    def trace(self, matrix: Union[List[List], str]) -> Dict[str, Any]:
        """Calculate matrix trace"""
        try:
            A = self.create_matrix(matrix)
            
            if A.shape[0] != A.shape[1]:
                raise ValueError("Matrix must be square to calculate trace")
            
            trace = np.trace(A)
            
            return {
                'result': float(trace),
                'status': 'success',
                'operation': 'trace',
                'shape': A.shape
            }
            
        except Exception as e:
            return {
                'result': None,
                'status': 'error',
                'error': str(e),
                'operation': 'trace'
            }
    
    def solve_linear_system(self, A: Union[List[List], str], b: Union[List, str]) -> Dict[str, Any]:
        """Solve linear system Ax = b"""
        try:
            matrix_A = self.create_matrix(A)
            vector_b = np.array(b if isinstance(b, list) else json.loads(b))
            
            if matrix_A.shape[0] != len(vector_b):
                raise ValueError("Matrix A rows must equal vector b length")
            
            if matrix_A.shape[0] != matrix_A.shape[1]:
                # Use least squares for non-square systems
                solution = np.linalg.lstsq(matrix_A, vector_b, rcond=None)[0]
                method = 'least_squares'
            else:
                solution = np.linalg.solve(matrix_A, vector_b)
                method = 'direct'
            
            return {
                'solution': solution.tolist(),
                'status': 'success',
                'operation': 'solve_linear_system',
                'method': method,
                'shape': matrix_A.shape
            }
            
        except Exception as e:
            return {
                'solution': None,
                'status': 'error',
                'error': str(e),
                'operation': 'solve_linear_system'
            }
    
    def create_identity(self, size: int) -> List[List[float]]:
        """Create identity matrix of given size"""
        return np.eye(size).tolist()
    
    def create_zeros(self, shape: Tuple[int, int]) -> List[List[float]]:
        """Create zero matrix of given shape"""
        return np.zeros(shape).tolist()
    
    def create_ones(self, shape: Tuple[int, int]) -> List[List[float]]:
        """Create matrix of ones of given shape"""
        return np.ones(shape).tolist()


def create_matrix_calculator() -> MatrixCalculator:
    """Factory function to create matrix calculator instance"""
    return MatrixCalculator()
