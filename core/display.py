"""
Display Module - Sherlock-style Terminal Output
Beautiful CLI output with colors and formatting
"""

from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich import print as rprint


console = Console()


class Display:
    """Terminal display with Sherlock-style formatting"""

    @staticmethod
    def show_banner():
        """Show FaceTrace ASCII banner"""
        rprint("[bold cyan]  ███████╗ █████╗  ██████╗███████╗████████╗██████╗  █████╗  ██████╗███████╗[/bold cyan]")
        rprint("[bold cyan]  ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝[/bold cyan]")
        rprint("[bold cyan]  █████╗  ███████║██║     █████╗     ██║   ██████╔╝███████║██║     █████╗  [/bold cyan]")
        rprint("[bold cyan]  ██╔══╝  ██╔══██║██║     ██╔══╝     ██║   ██╔══██╗██╔══██║██║     ██╔══╝  [/bold cyan]")
        rprint("[bold cyan]  ██║     ██║  ██║╚██████╗███████╗   ██║   ██║  ██║██║  ██║╚██████╗███████╗[/bold cyan]")
        rprint("[bold cyan]  ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝[/bold cyan]")
        rprint("[dim]           Reverse Face Search - Find anyone, anywhere[/dim]\n")

    @staticmethod
    def info(msg: str):
        """Show info message (blue)"""
        rprint(f"[bold blue][*][/bold blue] {msg}")

    @staticmethod
    def success(msg: str):
        """Show success message (green)"""
        rprint(f"[bold green][+][/bold green] {msg}")

    @staticmethod
    def warning(msg: str):
        """Show warning message (yellow)"""
        rprint(f"[bold yellow][!][/bold yellow] {msg}")

    @staticmethod
    def error(msg: str):
        """Show error message (red)"""
        rprint(f"[bold red][-][/bold red] {msg}")

    @staticmethod
    def searching(msg: str):
        """Show searching message"""
        rprint(f"[bold yellow][>][/bold yellow] {msg}")

    @staticmethod
    def show_results(results: List[Dict]):
        """
        Display search results in Sherlock style

        Args:
            results: List of match dictionaries with platform, score, url, username
        """
        if not results:
            Display.error("No matches found")
            return

        # Show summary
        Display.success(f"Found {len(results)} match(es)!\n")

        # Show top 20 results in Sherlock style
        rprint("[bold underline]Results:[/bold underline]\n")

        for idx, match in enumerate(results[:20], 1):
            platform = match['platform'].ljust(12)
            score = f"{match['score']}%".ljust(5)
            url = match['url']
            username = match.get('username', '')

            # Color based on score
            if match['score'] >= 90:
                color = "green"
            elif match['score'] >= 80:
                color = "yellow"
            else:
                color = "blue"

            # Format username
            username_str = f"@{username}" if username else ""
            username_display = f" {username_str}".ljust(20) if username_str else ""

            rprint(f"[{color}][+][/{color}] {platform} | {score} |{username_display} {url}")

        # Show count if more than 20
        if len(results) > 20:
            remaining = len(results) - 20
            rprint(f"\n[dim]... and {remaining} more match(es)[/dim]")

        # Show stats
        rprint(f"\n[bold]Statistics:[/bold]")
        rprint(f"  Total matches: {len(results)}")
        if results:
            rprint(f"  Avg. similarity: {sum(r['score'] for r in results) / len(results):.1f}%")
            rprint(f"  Top score: {max(r['score'] for r in results)}%")

        # Platform breakdown
        platforms = {}
        for r in results:
            platforms[r['platform']] = platforms.get(r['platform'], 0) + 1

        rprint(f"\n[bold]Platforms:[/bold]")
        for platform, count in sorted(platforms.items(), key=lambda x: x[1], reverse=True)[:5]:
            rprint(f"  {platform}: {count}")

    @staticmethod
    def show_results_table(results: List[Dict]):
        """
        Alternative: Display results in a table format

        Args:
            results: List of match dictionaries
        """
        if not results:
            Display.error("No matches found")
            return

        table = Table(title=f"FaceTrace Results - {len(results)} matches found")

        table.add_column("Platform", style="cyan", no_wrap=True)
        table.add_column("Score", style="magenta", justify="right")
        table.add_column("Username", style="green")
        table.add_column("URL", style="blue")

        for match in results[:20]:
            table.add_row(
                match['platform'],
                f"{match['score']}%",
                match.get('username', ''),
                match['url'][:60] + "..." if len(match['url']) > 60 else match['url']
            )

        console.print(table)

        if len(results) > 20:
            rprint(f"\n[dim]... and {len(results) - 20} more results[/dim]")
