import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

load_dotenv()

from src.cli.product_commands import product_app
from src.cli.ticket_commands import ticket_app
from src.cli.customer_commands import customer_app
from src.cli.alert_commands import alert_app
from src.db.dynamodb import create_tables

app = typer.Typer(
    name="zara-mgmt",
    help="Zara Store Management System — Sprint 1 MVP",
    add_completion=False,
    rich_markup_mode="rich",
)

app.add_typer(product_app, name="product")
app.add_typer(ticket_app, name="ticket")
app.add_typer(customer_app, name="customer")
app.add_typer(alert_app, name="alerts")

console = Console()


@app.command("setup")
def cmd_setup():
    """Create DynamoDB tables (run once on first deploy)."""
    console.print("[cyan]Creating DynamoDB tables...[/cyan]")
    created = create_tables()
    if created:
        for name in created:
            console.print(f"  [green]Created:[/green] {name}")
    else:
        console.print("  [yellow]All tables already exist.[/yellow]")
    console.print("[green bold]Setup complete.[/green bold]")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        console.print(
            Panel(
                "[bold cyan]Zara Store Management System[/bold cyan]\n"
                "[white]Sprint 1 — Terminal MVP[/white]\n\n"
                "  [green]python main.py product[/green]   — manage inventory\n"
                "  [green]python main.py ticket[/green]    — manage purchase tickets\n"
                "  [green]python main.py customer[/green]  — manage customers\n"
                "  [green]python main.py alerts check[/green]  — run alert checks\n"
                "  [green]python main.py setup[/green]     — initialise DynamoDB tables\n\n"
                "Run [bold]python main.py --help[/bold] for full command reference.",
                title="Welcome",
                border_style="cyan",
            )
        )


if __name__ == "__main__":
    app()
