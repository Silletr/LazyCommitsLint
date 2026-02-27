import typer
from .git_analyze import analyze_all_changes

app = typer.Typer()


@app.command()
def lint():
    changes = analyze_all_changes()
    typer.echo(f"ALL CHANGES LIST:\n{dict(changes)}")  # Keep your debug

    # Show only staged
    staged_files = changes.get("CHANGED", []) + changes.get("NEW", [])
    typer.echo("Staged changes:")
    for cat, files in changes.items():
        if cat in ["CHANGED", "NEW"]:
            typer.echo(f"  {cat}: {', '.join(files)}")

    if not staged_files:
        typer.echo("No staged changes!")
        raise typer.Exit()

    commit_explanation = input("What you did/fixed/etc in this commit?:\n")

    # Only staged categories/files
    staged_categories = [cat for cat in ["CHANGED", "NEW"] if changes.get(cat)]
    cat_str = ", ".join(staged_categories)
    file_str = ", ".join(staged_files)
    msg = f"[{cat_str}: {file_str}] {commit_explanation}"

    typer.echo(f"\nSuggested message:\n{msg}")


def main():
    app()


if __name__ == "__main__":
    main()
