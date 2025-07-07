import asyncio
import json
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from .config import Config
from .tools.registry import registry

class LLMClient:
    def __init__(self, config: Config):
        self.client = AsyncOpenAI(api_key=config.openai_api_key)
        self.config = config
        self.conversation_history: List[Dict[str, Any]] = []
    
    async def chat(self, message: str) -> str:
        """Send a message and get a response, handling function calls"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Get available tools
        available_tools = registry.get_openai_functions()
        
        # Call OpenAI
        response = await self.client.chat.completions.create(
            model=self.config.model_name,
            messages=self.conversation_history,
            tools=available_tools if available_tools else None,
            tool_choice="auto" if available_tools else None,
            temperature=self.config.temperature
        )
        
        assistant_message = response.choices[0].message
        
        # Add assistant message to history
        self.conversation_history.append(assistant_message.model_dump())
        
        # Handle function calls
        if assistant_message.tool_calls:
            await self._handle_tool_calls(assistant_message.tool_calls)
            
            # Get final response after function calls
            final_response = await self.client.chat.completions.create(
                model=self.config.model_name,
                messages=self.conversation_history,
                temperature=self.config.temperature
            )
            
            final_message = final_response.choices[0].message
            self.conversation_history.append(final_message.model_dump())
            return final_message.content
        
        return assistant_message.content
    
    async def _handle_tool_calls(self, tool_calls) -> None:
        """Execute tool calls and add results to conversation"""
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            try:
                tool = registry.get_tool(tool_name)
                result = await tool.execute(**arguments)
                
                # Add tool result to conversation
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(result.model_dump())
                })
                
            except Exception as e:
                # Add error to conversation
                self.conversation_history.append({
                    "role": "tool", 
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps({"error": str(e)})
                })