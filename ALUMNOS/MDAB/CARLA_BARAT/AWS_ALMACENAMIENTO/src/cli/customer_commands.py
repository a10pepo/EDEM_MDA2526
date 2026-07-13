from datetime import date

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.models.customer import Customer
from src.services.customer_service import (
    delete_customer,
    get_customer,
    list_customers,
    register_customer,
)
from src.services.ticket_service import list_tickets

customer_app = typer.Typer(help="Manage customers")
console = Console()

MEMBERSHIP_COLORS = {"none": "white", "basic": "blue", "silver": "bright_white", "gold": "yellow"}


@customer_app.command("list")
def cmd_list():
    """List all registered customers."""
    customers = list_customers()
    if not customers:
        console.print("[yellow]No customers registered.[/yellow]")
        return

    table = Table(title="Customers", show_lines=True)
    table.add_column("ID", style="cyan bold")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Phone")
    table.add_column("Date of Birth")
    table.add_column("Membership")

    for c in sorted(customers, key=lambda x: x.name):
        color = MEMBERSHIP_COLORS.get(c.membership_level, "white")
        table.add_row(
            c.customer_id,
            c.name,
            c.email,
            c.phone,
            c.date_of_birth,
            f"[{color}]{c.membership_level}[/{color}]",
        )

    console.print(table)


@customer_app.command("register")
def cmd_register(
    customer_id: str = typer.Option(..., prompt="Customer ID (DNI/passport)"),
    name: str = typer.Option(..., prompt="Full name"),
    email: str = typer.Option(..., prompt="Email"),
    phone: str = typer.Option(..., prompt="Phone"),
    dob: str = typer.Option(..., prompt="Date of birth (YYYY-MM-DD)"),
    membership: str = typer.Option("none", prompt="Membership level (none/basic/silver/gold)"),
):
    """Register a new customer."""
    try:
        date.fromisoformat(dob)
    except ValueError:
        console.print("[red]Invalid date format. Use YYYY-MM-DD.[/red]")
        raise typer.Exit(1)

    valid_levels = {"none", "basic", "silver", "gold"}
    if membership not in valid_levels:
        console.print(f"[red]Invalid membership. Use: {', '.join(valid_levels)}[/red]")
        raise typer.Exit(1)

    customer = Customer(
        customer_id=customer_id,
        name=name,
        email=email,
        phone=phone,
        date_of_birth=dob,
        membership_level=membership,
    )
    if register_customer(customer):
        console.print(f"[green]Customer [bold]{customer_id}[/bold] registered successfully.[/green]")
    else:
        console.print(f"[red]Failed to register customer {customer_id}.[/red]")
        raise typer.Exit(1)


@customer_app.command("get")
def cmd_get(customer_id: str = typer.Argument(..., help="Customer ID")):
    """Show details of a customer and their purchase history."""
    c = get_customer(customer_id)
    if not c:
        console.print(f"[red]Customer '{customer_id}' not found.[/red]")
        raise typer.Exit(1)

    color = MEMBERSHIP_COLORS.get(c.membership_level, "white")
    content = (
        f"[bold]ID:[/bold]         {c.customer_id}\n"
        f"[bold]Name:[/bold]       {c.name}\n"
        f"[bold]Email:[/bold]      {c.email}\n"
        f"[bold]Phone:[/bold]      {c.phone}\n"
        f"[bold]Born:[/bold]       {c.date_of_birth}\n"
        f"[bold]Membership:[/bold] [{color}]{c.membership_level}[/{color}]"
    )
    console.print(Panel(content, title=f"Customer: {customer_id}", border_style="blue"))

    tickets = [t for t in list_tickets() if t.customer_id == customer_id]
    if tickets:
        table = Table(title="Purchase History", show_lines=True)
        table.add_column("Ticket ID", style="cyan")
        table.add_column("Date")
        table.add_column("Items", justify="right")
        table.add_column("Total (€)", justify="right", style="green")
        table.add_column("Status")
        for t in sorted(tickets, key=lambda x: x.date_time, reverse=True):
            sc = {"pending": "yellow", "completed": "green", "returned": "red"}.get(t.status, "white")
            table.add_row(
                t.ticket_id,
                t.date_time,
                str(len(t.items)),
                f"{t.total_amount():.2f}",
                f"[{sc}]{t.status}[/{sc}]",
            )
        total_spent = sum(t.total_amount() for t in tickets if t.status != "returned")
        console.print(table)
        console.print(f"\n[bold]Total spent:[/bold] €{total_spent:.2f} across {len(tickets)} ticket(s).")
    else:
        console.print("\n[yellow]No purchase history for this customer.[/yellow]")


@customer_app.command("tickets")
def cmd_tickets(customer_id: str = typer.Argument(..., help="Customer ID")):
    """Check purchase/return status of a customer's tickets."""
    if not get_customer(customer_id):
        console.print(f"[red]Customer '{customer_id}' not found.[/red]")
        raise typer.Exit(1)

    tickets = [t for t in list_tickets() if t.customer_id == customer_id]
    if not tickets:
        console.print(f"[yellow]No tickets found for customer {customer_id}.[/yellow]")
        return

    returned = [t for t in tickets if t.status == "returned"]
    pending = [t for t in tickets if t.status == "pending"]
    completed = [t for t in tickets if t.status == "completed"]
    console.print(
        f"\nCustomer [bold]{customer_id}[/bold]: "
        f"[green]{len(completed)} completed[/green], "
        f"[yellow]{len(pending)} pending[/yellow], "
        f"[red]{len(returned)} returned[/red]"
    )


@customer_app.command("delete")
def cmd_delete(customer_id: str = typer.Argument(..., help="Customer ID")):
    """Delete a customer."""
    if not get_customer(customer_id):
        console.print(f"[red]Customer '{customer_id}' not found.[/red]")
        raise typer.Exit(1)
    if typer.confirm(f"Delete customer '{customer_id}'?") and delete_customer(customer_id):
        console.print(f"[green]Customer {customer_id} deleted.[/green]")
