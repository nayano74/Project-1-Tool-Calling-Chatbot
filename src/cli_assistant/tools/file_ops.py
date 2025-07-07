# src/cli_assistant/tools/file_ops.py
import os
from pathlib import Path
from typing import Any, Dict
from .base import BaseTool, ToolResult

class FileOpsTool(BaseTool):
    @property
    def name(self) -> str:
        return "file_operations"
    
    @property
    def description(self) -> str:
        return "List directory contents or read file information"
    
    @property 
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["list", "info"],
                    "description": "Operation to perform"
                },
                "path": {
                    "type": "string",
                    "description": "File or directory path"
                }
            },
            "required": ["operation", "path"]
        }
    
    async def execute(self, operation: str, path: str) -> ToolResult:
        try:
            path_obj = Path(path)
            
            if operation == "list":
                if path_obj.is_dir():
                    files = [f.name for f in path_obj.iterdir()]
                    return ToolResult(success=True, result=files)
                else:
                    return ToolResult(success=False, error="Path is not a directory")
            
            elif operation == "info":
                if path_obj.exists():
                    stat = path_obj.stat()
                    return ToolResult(success=True, result={
                        "name": path_obj.name,
                        "size": stat.st_size,
                        "is_file": path_obj.is_file(),
                        "is_dir": path_obj.is_dir()
                    })
                else:
                    return ToolResult(success=False, error="Path does not exist")
                    
        except Exception as e:
            return ToolResult(success=False, error=str(e))