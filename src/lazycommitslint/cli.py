import typer
from .git_analyze import analyze_all_changes

app = typer.Typer()


def print_section(title: str, categories: dict):
    if not categories:
        return
    typer.echo(f"\n{title}:")
    for cat, files in categories.items():
        if files:
            typer.echo(f"  {cat}: {', '.join(files)}")


@app.command()
def lint():
    changes = analyze_all_changes()

    staged = changes.get("staged", {})
    unstaged = changes.get("unstaged", {})
    untracked = changes.get("untracked", {})

    print_section("Staged", staged)
    print_section("Unstaged", unstaged)
    print_section("Untracked", untracked)

    if not staged:
        typer.echo("\nNo staged changes! Stage something with `git add` first.")
        raise typer.Exit()

    commit_explanation = input("\nWhat did you do/fix/etc in this commit?:\n")

    staged_files = [f for files in staged.values() for f in files]
    cat_str = ", ".join(staged.keys())
    file_str = ", ".join(staged_files)
    msg = f"[{cat_str}: {file_str}] {commit_explanation}"

    typer.echo(f"\nSuggested commit message:\n  {msg}")


def main():
    app()


if __name__ == "__main__":
    main()
