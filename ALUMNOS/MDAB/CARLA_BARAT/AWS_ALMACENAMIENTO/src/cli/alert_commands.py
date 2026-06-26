import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.services.alert_service import get_all_alerts

alert_app = typer.Typer(help="Show system alerts")
console = Console()


@alert_app.command("check")
def cmd_check():
    """Run all alert checks and display results."""
    alerts = get_all_alerts()
    total = sum(len(v) for v in alerts.values())

    if total == 0:
        console.print(Panel("[green bold]All systems OK — no alerts triggered.[/green bold]", border_style="green"))
        return

    console.print(Panel(f"[red bold]{total} alert(s) detected[/red bold]", border_style="red"))

    if alerts["low_stock"]:
        table = Table(title="LOW STOCK Alerts", show_lines=True, border_style="red")
        table.add_column("SKU", style="cyan")
        table.add_column("Name")
        table.add_column("Stock", justify="right", style="red bold")
        table.add_column("Threshold", justify="right")
        for a in alerts["low_stock"]:
            table.add_row(a["sku"], a["name"], str(a["stock"]), str(a["threshold"]))
        console.print(table)

    if alerts["high_discount"]:
        table = Table(title="HIGH DISCOUNT Alerts (>20%)", show_lines=True, border_style="yellow")
        table.add_column("Ticket ID", style="cyan")
        table.add_column("Discount %", justify="right", style="red bold")
        table.add_column("Discount (€)", justify="right")
        table.add_column("Total (€)", justify="right")
        for a in alerts["high_discount"]:
            table.add_row(
                a["ticket_id"],
                f"{a['discount_pct']:.1f}%",
                f"{a['discount_total']:.2f}",
                f"{a['total_amount']:.2f}",
            )
        console.print(table)

    if alerts["return_rate"]:
        for a in alerts["return_rate"]:
            console.print(
                Panel(
                    f"[red bold]{a['returned']} of {a['total']} tickets returned ({a['rate_pct']}%)[/red bold]\n"
                    f"Threshold: 10% — action required.",
                    title="HIGH RETURN RATE Alert",
                    border_style="red",
                )
            )
