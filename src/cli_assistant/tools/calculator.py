import ast
import operator
from typing import Any, Dict
from .base import BaseTool, ToolResult

class CalculatorTool(BaseTool):
    @property
    def name(self) -> str:
        return "calculate"
    
    @property 
    def description(self) -> str:
        return "Evaluate mathematical expressions safely"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4')"
                }
            },
            "required": ["expression"]
        }
    
    async def execute(self, expression: str) -> ToolResult:
        try:
            # Safe evaluation using AST
            result = self._safe_eval(expression)
            return ToolResult(success=True, result=result)
        except Exception as e:
            return ToolResult(success=False, result=None, error=str(e))
    
    def _safe_eval(self, expression: str) -> float:
        """Safely evaluate mathematical expressions"""
        # Define allowed operations
        allowed_ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
        }
        
        def eval_node(node):
            if isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                return allowed_ops[type(node.op)](left, right)
            elif isinstance(node, ast.UnaryOp):
                operand = eval_node(node.operand)
                return allowed_ops[type(node.op)](operand)
            else:
                raise ValueError(f"Unsupported operation: {type(node)}")
        
        tree = ast.parse(expression, mode='eval')
        return eval_node(tree.body)