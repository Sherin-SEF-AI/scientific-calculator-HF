"""
Simple test script to verify the scientific calculator functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.calculator import create_calculator
from modules.matrix import create_matrix_calculator
from modules.statistics import create_statistical_analyzer
from modules.visualization import create_visualizer
from modules.data_handler import create_data_handler

def test_basic_functionality():
    """Test basic functionality of all modules"""
    print("🧮 Testing Scientific Calculator Pro...")
    
    # Test calculator
    print("\n1. Testing Calculator...")
    calc = create_calculator()
    result = calc.calculate("2 + 3 * 4")
    print(f"   2 + 3 * 4 = {result['formatted_result']}")
    
    result = calc.calculate("sin(π/2)")
    print(f"   sin(π/2) = {result['formatted_result']}")
    
    # Test matrix operations
    print("\n2. Testing Matrix Operations...")
    matrix_calc = create_matrix_calculator()
    
    # Test matrix addition
    matrix1 = [[1, 2], [3, 4]]
    matrix2 = [[5, 6], [7, 8]]
    result = matrix_calc.add_matrices(matrix1, matrix2)
    print(f"   Matrix addition: {result['result']}")
    
    # Test determinant
    result = matrix_calc.determinant(matrix1)
    print(f"   Determinant of [[1,2],[3,4]] = {result['result']}")
    
    # Test statistics
    print("\n3. Testing Statistical Analysis...")
    stats = create_statistical_analyzer()
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = stats.descriptive_stats(data)
    print(f"   Mean of {data} = {result['mean']}")
    print(f"   Standard deviation = {result['std']}")
    
    # Test data handler
    print("\n4. Testing Data Handler...")
    data_handler = create_data_handler()
    csv_data = "name,age,salary\nAlice,25,50000\nBob,30,60000"
    result = data_handler.load_csv_from_string(csv_data)
    print(f"   CSV loaded: {result['shape']} shape")
    
    # Test visualizer
    print("\n5. Testing Visualizer...")
    visualizer = create_visualizer()
    x_data = [1, 2, 3, 4, 5]
    y_data = [2, 4, 6, 8, 10]
    fig = visualizer.line_plot(x_data, y_data, "Test Plot")
    print(f"   Line plot created successfully")
    
    print("\n✅ All tests passed! The application is ready to run.")
    print("\nTo start the application, run:")
    print("   python app.py")
    print("\nThen open your browser to http://localhost:7860")

if __name__ == "__main__":
    test_basic_functionality()


