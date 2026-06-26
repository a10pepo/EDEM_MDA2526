from datetime import datetime
from typing import List

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.models.ticket import Ticket, TicketItem
from src.services.ticket_service import (
    delete_ticket,
    get_ticket,
    list_tickets,
    register_ticket,
    update_ticket_status,
    _generate_ticket_id,
)
from src.services.product_service import get_product

ticket_app = typer.Typer(help="Manage purchase tickets (sales)")
console = Console()

STATUS_COLORS = {"pending": "yellow", "completed": "green", "returned": "red"}


@ticket_app.command("list")
def cmd_list():
    """List all purchase tickets."""
    tickets = list_tickets()
    if not tickets:
        console.print("[yellow]No tickets registered.[/yellow]")
        return

    table = Table(title="Purchase Tickets", show_lines=True)
    table.add_column("Ticket ID", style="cyan bold")
    table.add_column("Date/Time")
    table.add_column("Cashier")
    table.add_column("Customer")
    table.add_column("Items", justify="right")
    table.add_column("Total (€)", justify="right", style="green")
    table.add_column("Discount (€)", justify="right")
    table.add_column("Discount %", justify="right")
    table.add_column("Payment")
    table.add_column("Status")

    for t in sorted(tickets, key=lambda x: x.date_time, reverse=True):
        color = STATUS_COLORS.get(t.status, "white")
        pct = t.discount_percentage()
        pct_color = "red" if pct > 20 else "white"
        table.add_row(
            t.ticket_id,
            t.date_time,
            t.cashier_id,
            t.customer_id or "—",
            str(len(t.items)),
            f"{t.total_amount():.2f}",
            f"{t.discount_total():.2f}",
            f"[{pct_color}]{pct:.1f}%[/{pct_color}]",
            t.payment_method,
            f"[{color}]{t.status}[/{color}]",
        )

    console.print(table)


@ticket_app.command("register")
def cmd_register(
    cashier: str = typer.Option(..., prompt="Cashier ID"),
    payment: str = typer.Option("card", prompt="Payment method (cash/card/online)"),
    customer: str = typer.Option("", prompt="Customer ID (leave blank if none)"),
):
    """Register a new purchase ticket interactively."""
    items: List[TicketItem] = []

    console.print("\n[bold cyan]Add items to the ticket[/bold cyan] (leave SKU blank to finish)\n")

    while True:
        sku = typer.prompt("  SKU (or Enter to finish)", default="").strip()
        if not sku:
            break

        product = get_product(sku)
        if not product:
            console.print(f"  [yellow]Product '{sku}' not found — skipping.[/yellow]")
            continue

        quantity = typer.prompt(f"  Quantity for {product.name}", default=1, type=int)
        default_price = product.price
        unit_price = typer.prompt(f"  Unit price (€)", default=default_price, type=float)
        discount = typer.prompt("  Discount on this line (€)", default=0.0, type=float)

        items.append(TicketItem(sku=sku, quantity=quantity, unit_price=unit_price, discount=discount))
        subtotal = (unit_price * quantity) - discount
        console.print(f"  [green]Added: {product.name} × {quantity} = €{subtotal:.2f}[/green]\n")

    if not items:
        console.print("[yellow]No items added. Ticket not created.[/yellow]")
        raise typer.Exit(0)

    ticket_id = _generate_ticket_id()
    ticket = Ticket(
        ticket_id=ticket_id,
        cashier_id=cashier,
        date_time=datetime.now().isoformat(timespec="seconds"),
        payment_method=payment,
        status="completed",
        items=items,
        customer_id=customer or None,
    )

    console.print(
        f"\n[bold]Summary:[/bold] {len(items)} items — "
        f"Total €{ticket.total_amount():.2f} — "
        f"Discount €{ticket.discount_total():.2f} ({ticket.discount_percentage():.1f}%)"
    )
    confirm = typer.confirm("Save ticket?")
    if confirm and register_ticket(ticket):
        console.print(f"[green]Ticket [bold]{ticket_id}[/bold] saved.[/green]")
    else:
        console.print("[yellow]Ticket discarded.[/yellow]")


@ticket_app.command("get")
def cmd_get(ticket_id: str = typer.Argument(..., help="Ticket ID")):
    """Show details of a ticket."""
    t = get_ticket(ticket_id)
    if not t:
        console.print(f"[red]Ticket '{ticket_id}' not found.[/red]")
        raise typer.Exit(1)

    color = STATUS_COLORS.get(t.status, "white")
    header = (
        f"[bold]Ticket:[/bold]   {t.ticket_id}\n"
        f"[bold]Date:[/bold]     {t.date_time}\n"
        f"[bold]Cashier:[/bold]  {t.cashier_id}\n"
        f"[bold]Customer:[/bold] {t.customer_id or '—'}\n"
        f"[bold]Payment:[/bold]  {t.payment_method}\n"
        f"[bold]Status:[/bold]   [{color}]{t.status}[/{color}]"
    )
    console.print(Panel(header, title="Ticket Info", border_style="blue"))

    item_table = Table(show_lines=True)
    item_table.add_column("SKU", style="cyan")
    item_table.add_column("Qty", justify="right")
    item_table.add_column("Unit Price (€)", justify="right")
    item_table.add_column("Discount (€)", justify="right")
    item_table.add_column("Subtotal (€)", justify="right", style="green")

    for i in t.items:
        item_table.add_row(i.sku, str(i.quantity), f"{i.unit_price:.2f}", f"{i.discount:.2f}", f"{i.subtotal():.2f}")

    console.print(item_table)
    pct_color = "red" if t.discount_percentage() > 20 else "green"
    console.print(
        f"\n[bold]Total:[/bold] €{t.total_amount():.2f}  |  "
        f"[bold]Discount:[/bold] €{t.discount_total():.2f} "
        f"([{pct_color}]{t.discount_percentage():.1f}%[/{pct_color}])"
    )


@ticket_app.command("status")
def cmd_status(
    ticket_id: str = typer.Argument(..., help="Ticket ID"),
    new_status: str = typer.Argument(..., help="New status: pending / completed / returned"),
):
    """Update the status of a ticket."""
    if not get_ticket(ticket_id):
        console.print(f"[red]Ticket '{ticket_id}' not found.[/red]")
        raise typer.Exit(1)
    if update_ticket_status(ticket_id, new_status):
        color = STATUS_COLORS.get(new_status, "white")
        console.print(f"[green]Ticket {ticket_id} → [{color}]{new_status}[/{color}][/green]")
    else:
        console.print(f"[red]Invalid status '{new_status}'. Use: pending / completed / returned.[/red]")
        raise typer.Exit(1)


@ticket_app.command("delete")
def cmd_delete(ticket_id: str = typer.Argument(..., help="Ticket ID")):
    """Delete a ticket."""
    if not get_ticket(ticket_id):
        console.print(f"[red]Ticket '{ticket_id}' not found.[/red]")
        raise typer.Exit(1)
    if typer.confirm(f"Delete ticket '{ticket_id}'?") and delete_ticket(ticket_id):
        console.print(f"[green]Ticket {ticket_id} deleted.[/green]")
