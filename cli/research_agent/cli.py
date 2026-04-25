import sys
import click
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


@click.group()
@click.option(
    "--api-url",
    default="http://localhost:8000",
    envvar="RESEARCH_AGENT_API_URL",
    help="Backend API URL",
    show_default=True,
)
@click.pass_context
def cli(ctx, api_url):
    """Research Agent CLI — manage your AI tool directory."""
    ctx.ensure_object(dict)
    ctx.obj["api_url"] = api_url.rstrip("/")


@cli.command()
@click.argument("url")
@click.pass_context
def add(ctx, url):
    """Scrape a URL and add it to the directory."""
    try:
        import httpx as _httpx
        from bs4 import BeautifulSoup

        console.print(f"[cyan]Fetching[/cyan] {url}")
        page = _httpx.get(url, follow_redirects=True, timeout=15)
        soup = BeautifulSoup(page.text, "html.parser")

        # Note: bs4 Tag defines __len__, so an empty self-closing tag like
        # <meta> evaluates as falsy. Use `is not None` for presence checks.
        og_title_tag = soup.find("meta", {"property": "og:title"})
        og_title = og_title_tag.get("content") if og_title_tag is not None else None
        h1_tag = soup.find("h1")
        h1_text = h1_tag.get_text(strip=True) if h1_tag is not None else None
        name = og_title or h1_text or url

        desc_meta = soup.find("meta", {"name": "description"})
        desc = desc_meta.get("content", "") if desc_meta is not None else ""
        raw = soup.get_text(separator=" ")[:8000]
    except Exception as e:
        console.print(f"[red]Failed to fetch page:[/red] {e}")
        raise click.Abort()

    api = ctx.obj["api_url"]
    console.print("[cyan]Generating Signal Summary via Claude...[/cyan]")
    try:
        r = httpx.post(
            f"{api}/api/tools",
            json={"name": name, "url": url, "description": desc, "raw_content": raw},
            timeout=60,
        )
        r.raise_for_status()
    except httpx.HTTPStatusError as e:
        console.print(f"[red]API error {e.response.status_code}:[/red] {e.response.text}")
        raise click.Abort()
    except httpx.RequestError as e:
        console.print(f"[red]Connection error:[/red] {e}\nIs the backend running at {api}?")
        raise click.Abort()

    tool = r.json()
    console.print(Panel(
        f"[bold]{tool['name']}[/bold]\n\n"
        f"[dim]{tool.get('signal_summary', '')}[/dim]\n\n"
        f"Price: [cyan]{tool.get('price_tier', '?')}[/cyan]  "
        f"For: [yellow]{tool.get('target_audience', '?')}[/yellow]\n"
        f"Tags: {', '.join(tool.get('use_cases', []))}",
        title="[green]Added to Directory[/green]",
        border_style="green",
    ))


@cli.command("list")
@click.option("--use-case", default=None, help="Filter by use case tag")
@click.option("--price-tier", default=None,
              type=click.Choice(["free", "freemium", "paid", "enterprise"]),
              help="Filter by price tier")
@click.option("--search", default=None, help="Search by name or summary")
@click.pass_context
def list_tools(ctx, use_case, price_tier, search):
    """List tools in the directory."""
    params = {}
    if use_case:   params["use_case"]   = use_case
    if price_tier: params["price_tier"] = price_tier
    if search:     params["search"]     = search

    try:
        r = httpx.get(f"{ctx.obj['api_url']}/api/tools", params=params, timeout=15)
        r.raise_for_status()
    except httpx.RequestError as e:
        console.print(f"[red]Connection error:[/red] {e}")
        raise click.Abort()

    tools = r.json()
    if not tools:
        console.print("[yellow]No tools found.[/yellow]")
        return

    table = Table(title=f"AI Tools Directory ({len(tools)} results)", show_lines=False)
    table.add_column("ID",     style="dim",    width=5)
    table.add_column("Name",   style="bold",   min_width=20)
    table.add_column("Price",  style="cyan",   width=12)
    table.add_column("Clicks", style="green",  width=8)
    table.add_column("Summary", no_wrap=False, min_width=40)

    for t in tools:
        summary = t.get("signal_summary") or ""
        table.add_row(
            str(t["id"]),
            t["name"],
            t.get("price_tier") or "?",
            str(t["click_count"]),
            summary[:100] + ("..." if len(summary) > 100 else ""),
        )
    console.print(table)


@cli.command()
@click.option("--limit", default=10, show_default=True)
@click.pass_context
def trending(ctx, limit):
    """Show the most-clicked tools."""
    try:
        r = httpx.get(
            f"{ctx.obj['api_url']}/api/analytics",
            params={"limit": limit},
            timeout=15,
        )
        r.raise_for_status()
    except httpx.RequestError as e:
        console.print(f"[red]Connection error:[/red] {e}")
        raise click.Abort()

    items = r.json()
    if not items:
        console.print("[yellow]No analytics data yet.[/yellow]")
        return

    console.print("\n[bold cyan]Trending Tools[/bold cyan]\n")
    for i, item in enumerate(items, 1):
        bar = "█" * min(item["click_count"], 40)
        console.print(
            f"  {i:>2}. [bold]{item['tool_name']:<30}[/bold] "
            f"[green]{bar}[/green] [dim]{item['click_count']} clicks[/dim]"
        )


@cli.command()
@click.argument("url")
@click.pass_context
def summary(ctx, url):
    """Show the Signal Summary for a tool by URL (or partial name)."""
    try:
        r = httpx.get(
            f"{ctx.obj['api_url']}/api/tools",
            params={"search": url},
            timeout=15,
        )
        r.raise_for_status()
    except httpx.RequestError as e:
        console.print(f"[red]Connection error:[/red] {e}")
        raise click.Abort()

    tools = r.json()
    if not tools:
        console.print("[yellow]Not in directory. Use `research-agent add <url>` first.[/yellow]")
        return

    t = tools[0]
    console.print(Panel(
        f"[bold]{t['name']}[/bold]\n\n"
        f"{t.get('signal_summary', 'No summary available.')}\n\n"
        f"Price: [cyan]{t.get('price_tier', '?')}[/cyan]  "
        f"Clicks: [green]{t['click_count']}[/green]\n"
        f"Tags: {', '.join(t.get('use_cases', []))}",
        title="Signal Summary",
        border_style="cyan",
    ))


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
