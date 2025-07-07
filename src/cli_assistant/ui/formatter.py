from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from typing import Dict, Any

console = Console()

class UIFormatter:
    @staticmethod
    def format_user_message(message: str) -> None:
        """Format user input message"""
        panel = Panel(
            message,
            title="[bold blue]You[/bold blue]",
            border_style="blue",
            padding=(0, 1)
        )
        console.print(panel)
    
    @staticmethod
    def format_assistant_message(message: str) -> None:
        """Format assistant response"""
        panel = Panel(
            Markdown(message),
            title="[bold green]Assistant[/bold green]", 
            border_style="green",
            padding=(0, 1)
        )
        console.print(panel)
    
    @staticmethod
    def format_tool_call(tool_name: str, arguments: Dict[str, Any]) -> None:
        """Format tool call display"""
        table = Table(title=f"🔧 Calling tool: {tool_name}")
        table.add_column("Parameter", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in arguments.items():
            table.add_row(key, str(value))
        
        console.print(table)
    
    @staticmethod
    def format_error(error: str) -> None:
        """Format error message"""
        console.print(f"[bold red]Error:[/bold red] {error}")
    
    @staticmethod
    def format_welcome() -> None:
        """Format welcome message"""
        welcome_text = """[bold blue]🤖 CLI Assistant[/bold blue]

Connected to OpenAI with tool support!
Available commands:
- Type your message to chat
- '/help' for available tools
- '/quit' to exit
        """
        
        panel = Panel(
            welcome_text,
            title="[bold green]Welcome[/bold green]",
            border_style="green",
            padding=(1, 2)
        )
        console.print(panel)