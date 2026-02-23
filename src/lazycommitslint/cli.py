import typer
from .git_analyze import analyze_staged

# from suggester import generate_message  # Add later

app = typer.Typer()


@app.command()
def lint():
    """Analyze staged changes and suggest commit message."""
    changes = analyze_staged()
    typer.echo("Staged changes:")
    for cat, files in changes.items():
        typer.echo(f"  {cat}: {', '.join(files)}")
    # TODO: REPLACE MESSAGE GENERATING WITH LLM (LLAMA)
    msg = "[CHANGED FILE/DIR: src/lazycommitslint/git_analyze.py] Made git analyzer and mapper work"
    typer.echo(f"\nSuggested message:\n{msg}")


if __name__ == "__main__":
    app()
