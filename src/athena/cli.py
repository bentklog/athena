"""
Command-line interface for Athena.
"""

import typer
from rich.console import Console

app = typer.Typer(
    name="athena",
    help="AI knowledge management assistant for Obsidian markdown notes",
    add_completion=False,
)
console = Console()

@app.command()
def init():
    """Initialize Athena with your Obsidian vault."""
    console.print("[bold green]Initializing Athena...[/bold green]")
    # TODO: Implement initialization

@app.command()
def process():
    """Process your notes for cleaning and enhancement."""
    console.print("[bold green]Processing notes...[/bold green]")
    # TODO: Implement note processing

@app.command()
def connect():
    """View connections between your notes."""
    console.print("[bold green]Analyzing connections...[/bold green]")
    # TODO: Implement connection analysis

@app.command()
def recommend():
    """Get recommendations for your notes."""
    console.print("[bold green]Generating recommendations...[/bold green]")
    # TODO: Implement recommendations

def main():
    """Main entry point for the CLI."""
    app() 