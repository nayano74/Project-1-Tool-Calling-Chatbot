from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel

class ToolResult(BaseModel):
    success: bool
    result: Any
    error: Optional[str] = None

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name for OpenAI function calling"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for OpenAI"""
        pass
    
    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """JSON schema for tool parameters"""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with given parameters"""
        pass
    
    def to_openai_function(self) -> Dict[str, Any]:
        """Convert tool to OpenAI function format"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }