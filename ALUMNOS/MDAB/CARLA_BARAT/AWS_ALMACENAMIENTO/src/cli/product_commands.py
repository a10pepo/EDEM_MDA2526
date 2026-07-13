from datetime import date

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.models.product import Product
from src.services.product_service import (
    delete_product,
    get_product,
    list_products,
    register_product,
    update_stock,
)

product_app = typer.Typer(help="Manage products in inventory")
console = Console()


@product_app.command("list")
def cmd_list():
    """List all products in inventory."""
    products = list_products()
    if not products:
        console.print("[yellow]No products registered.[/yellow]")
        return

    table = Table(title="Product Inventory", show_lines=True)
    table.add_column("SKU", style="cyan bold")
    table.add_column("Name")
    table.add_column("Category")
    table.add_column("Size")
    table.add_column("Color")
    table.add_column("Price (€)", justify="right", style="green")
    table.add_column("Stock", justify="right")
    table.add_column("Threshold", justify="right")
    table.add_column("Supplier")

    for p in sorted(products, key=lambda x: x.sku):
        stock_style = "red bold" if p.is_below_threshold() else "white"
        table.add_row(
            p.sku,
            p.name,
            p.category,
            p.size,
            p.color,
            f"{p.price:.2f}",
            f"[{stock_style}]{p.stock_quantity}[/{stock_style}]",
            str(p.restock_threshold),
            p.supplier_id,
        )

    console.print(table)


@product_app.command("register")
def cmd_register(
    sku: str = typer.Option(..., prompt="SKU"),
    name: str = typer.Option(..., prompt="Product name"),
    category: str = typer.Option(..., prompt="Category (shirt/pants/shoes/etc.)"),
    size: str = typer.Option(..., prompt="Size"),
    color: str = typer.Option(..., prompt="Color"),
    price: float = typer.Option(..., prompt="Price (€)"),
    stock: int = typer.Option(..., prompt="Initial stock quantity"),
    threshold: int = typer.Option(..., prompt="Restock threshold (alert when stock <= this)"),
    last_restock: str = typer.Option(..., prompt="Last restock date (YYYY-MM-DD)"),
    supplier: str = typer.Option(..., prompt="Supplier ID"),
):
    """Register a product in inventory."""
    try:
        date.fromisoformat(last_restock)
    except ValueError:
        console.print("[red]Invalid date format. Use YYYY-MM-DD.[/red]")
        raise typer.Exit(1)

    product = Product(
        sku=sku,
        name=name,
        category=category,
        size=size,
        color=color,
        price=price,
        stock_quantity=stock,
        restock_threshold=threshold,
        last_restock_date=last_restock,
        supplier_id=supplier,
    )
    if register_product(product):
        console.print(f"[green]Product [bold]{sku}[/bold] registered successfully.[/green]")
    else:
        console.print(f"[red]Failed to register product {sku}.[/red]")
        raise typer.Exit(1)


@product_app.command("get")
def cmd_get(sku: str = typer.Argument(..., help="Product SKU")):
    """Show details of a product."""
    p = get_product(sku)
    if not p:
        console.print(f"[red]Product '{sku}' not found.[/red]")
        raise typer.Exit(1)

    stock_color = "red" if p.is_below_threshold() else "green"
    content = (
        f"[bold]SKU:[/bold]          {p.sku}\n"
        f"[bold]Name:[/bold]         {p.name}\n"
        f"[bold]Category:[/bold]     {p.category}\n"
        f"[bold]Size:[/bold]         {p.size}\n"
        f"[bold]Color:[/bold]        {p.color}\n"
        f"[bold]Price:[/bold]        €{p.price:.2f}\n"
        f"[bold]Stock:[/bold]        [{stock_color}]{p.stock_quantity}[/{stock_color}] units\n"
        f"[bold]Threshold:[/bold]    {p.restock_threshold} units\n"
        f"[bold]Last Restock:[/bold] {p.last_restock_date} ({p.days_since_restock()} days ago)\n"
        f"[bold]Supplier:[/bold]     {p.supplier_id}"
    )
    console.print(Panel(content, title=f"Product: {sku}", border_style="blue"))


@product_app.command("stock")
def cmd_stock(sku: str = typer.Argument(..., help="Product SKU")):
    """Check stock level of a product."""
    p = get_product(sku)
    if not p:
        console.print(f"[red]Product '{sku}' not found.[/red]")
        raise typer.Exit(1)

    if p.stock_quantity == 0:
        console.print(f"[red bold]OUT OF STOCK — {p.name} ({sku}) has 0 units.[/red bold]")
    elif p.is_below_threshold():
        console.print(
            f"[yellow]LOW STOCK — {p.name} ({sku}): {p.stock_quantity} units "
            f"(threshold: {p.restock_threshold})[/yellow]"
        )
    else:
        console.print(
            f"[green]{p.name} ({sku}): {p.stock_quantity} units in stock "
            f"(threshold: {p.restock_threshold})[/green]"
        )


@product_app.command("update-stock")
def cmd_update_stock(
    sku: str = typer.Argument(..., help="Product SKU"),
    quantity: int = typer.Argument(..., help="New stock quantity"),
):
    """Update the stock quantity of a product."""
    if not get_product(sku):
        console.print(f"[red]Product '{sku}' not found.[/red]")
        raise typer.Exit(1)
    if update_stock(sku, quantity):
        console.print(f"[green]Stock updated: {sku} → {quantity} units.[/green]")
    else:
        console.print("[red]Failed to update stock.[/red]")
        raise typer.Exit(1)


@product_app.command("delete")
def cmd_delete(sku: str = typer.Argument(..., help="Product SKU")):
    """Delete a product from inventory."""
    if not get_product(sku):
        console.print(f"[red]Product '{sku}' not found.[/red]")
        raise typer.Exit(1)
    confirm = typer.confirm(f"Delete product '{sku}'?")
    if confirm and delete_product(sku):
        console.print(f"[green]Product {sku} deleted.[/green]")
