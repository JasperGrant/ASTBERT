# Python file containing graph generation functions
# 2024-03-25

from comex.codeviews.AST.AST_driver import ASTDriver
import os

# Function populates folder_name with AST json, dot, and png files for method_name
def generate_graph_for_method(method_name, method_body, folder_name):
    # If file exists
    if os.path.exists(f"{folder_name}/{method_name}_AST_output.json"):
        return
    ASTDriver(
        src_language="java",
        src_code=method_body,
        output_file=f"{folder_name}/{method_name}_AST_output.json",
    )