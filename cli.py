import typer
import requests
from rich import print
import os

app = typer.Typer()

API_URL = "http://127.0.0.1:5000/summarize"

@app.command()
def summarize(file_path: str = typer.Argument(..., help="Path to the code file")):
    """Upload a code file to the web-based summarizer API."""
    try:
        file_path = os.path.abspath(os.path.expanduser(file_path))  # Expand and normalize path
        print(f"[bold blue]📂 File Path:[/bold blue] {file_path}")

        with open(file_path, "r") as f:
            code = f.read()

        if not code.strip():
            print("[red]⚠️ Error: The file is empty![/red]")
            return

        print("[bold blue]🔄 Sending code to summarizer API...[/bold blue]")

        response = requests.post(API_URL, json={"code": code})
        
        print(f"🔍 API Response Status: {response.status_code}")

        if response.status_code == 200:
            summary = response.json().get("summary", "No summary available.")
            print(f"\n[bold yellow]📝 Summary:[/bold yellow] {summary}\n")
        else:
            print(f"[red]❌ Error: {response.status_code} - {response.text}[/red]")

    except FileNotFoundError:
        print(f"[red]❌ Error: File not found at {file_path}![/red]")

if __name__ == "__main__":
    app()
