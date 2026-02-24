import typer
from .git_analyze import analyze_staged

app = typer.Typer()


@app.command()
def lint():
    """Analyze staged changes and suggest commit message."""
    changes = analyze_staged()
    typer.echo("Staged changes:")
    for cat, files in changes.items():
        typer.echo(f"  {cat}: {', '.join(files)}")
    # TODO: REPLACE MESSAGE GENERATING WITH LLM (LLAMA)

    # ONLY A PLACEHOLDER!!
    msg = f"[{cat}: {', '.join(files)}] Made git analyzer and mapper work"
    typer.echo(f"\nSuggested message:\n{msg}")


def main():
    app()


if __name__ == "__main__":
    main()
