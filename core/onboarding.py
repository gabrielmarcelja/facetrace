"""
FaceTrace CLI - Onboarding Wizard
First-time user experience with step-by-step guidance
"""

import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from core.display import Display
from core.config import load_config, save_config, CONFIG_FILE
from core.auth import register_user, login_user

console = Console()


def is_first_time() -> bool:
    """
    Check if this is user's first time running FaceTrace

    Returns:
        True if first time, False otherwise
    """
    # Check if config file exists
    if not CONFIG_FILE.exists():
        return True

    # Check if onboarding was completed
    config = load_config()
    return not config.get('onboarding_completed', False)


def mark_onboarding_complete():
    """Mark onboarding as completed in config"""
    config = load_config()
    config['onboarding_completed'] = True
    save_config(config)


def show_welcome():
    """Show welcome screen"""
    console.clear()

    welcome_text = """[bold cyan]Welcome to FaceTrace![/bold cyan]

[dim]The most powerful reverse face search tool[/dim]

FaceTrace helps you find where a face appears online across
50+ platforms including Instagram, Facebook, Twitter, OnlyFans,
TikTok, LinkedIn, and many more.

[bold]Let's get you started in 3 easy steps...[/bold]"""

    console.print(Panel(welcome_text, border_style="cyan", padding=(1, 2)))
    console.print()

    # Wait a moment for user to read
    time.sleep(1.5)


def show_features():
    """Show key features"""
    features = """[bold]✨ What you can do with FaceTrace:[/bold]

  [cyan]🚀 Lightning Fast[/cyan] - Get results in seconds
  [cyan]🎯 High Accuracy[/cyan] - Advanced facial recognition
  [cyan]🌐 Multi-Platform[/cyan] - Search across 50+ platforms
  [cyan]🎨 Beautiful CLI[/cyan] - Colorful, intuitive interface
  [cyan]🔒 Secure[/cyan] - Encrypted API communication
  [cyan]💪 Plug-and-Play[/cyan] - No complex setup required

[bold]🎁 You'll start with 3 free searches to try it out![/bold]"""

    console.print(Panel(features, border_style="green", padding=(1, 2)))
    console.print()

    time.sleep(1.5)


def show_tips():
    """Show usage tips"""
    tips = """[bold yellow]💡 Pro Tips for Best Results:[/bold yellow]

  [green]✓[/green] Use clear, front-facing photos
  [green]✓[/green] Higher resolution = better accuracy
  [green]✓[/green] Avoid blurry or dark images
  [green]✓[/green] One face per image works best
  [green]✓[/green] Group photos work too (we'll find all faces)

[bold]Average search takes 15-30 seconds[/bold]"""

    console.print(Panel(tips, border_style="yellow", padding=(1, 2)))
    console.print()


def run_wizard():
    """
    Run the complete onboarding wizard

    Returns:
        True if completed successfully, False if cancelled
    """
    try:
        # Step 1: Welcome
        show_welcome()

        if not Confirm.ask("[bold cyan]Ready to continue?[/bold cyan]", default=True):
            console.print("\n[yellow]You can run FaceTrace anytime to start![/yellow]")
            return False

        console.print()

        # Step 2: Features
        show_features()

        # Step 3: Tips
        show_tips()

        # Step 4: Account setup
        console.print("[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]")
        console.print()
        console.print("[bold]Step 1 of 2: Account Setup[/bold]")
        console.print()

        # Ask if they have an account
        has_account = Confirm.ask("[cyan]Do you already have a FaceTrace account?[/cyan]", default=False)
        console.print()

        if has_account:
            # Login flow
            Display.info("Great! Let's log you in...")
            console.print()
            time.sleep(0.5)

            success = login_user()

            if not success:
                console.print()
                console.print("[yellow]No worries! You can login later with:[/yellow]")
                console.print("[dim]  python3 facetrace.py login[/dim]")
                return False
        else:
            # Registration flow
            Display.info("Perfect! Let's create your account...")
            console.print()
            time.sleep(0.5)

            success = register_user()

            if not success:
                console.print()
                console.print("[yellow]No worries! You can register later with:[/yellow]")
                console.print("[dim]  python3 facetrace.py register[/dim]")
                return False

        console.print()

        # Step 5: Quick start guide
        console.print("[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]")
        console.print()
        console.print("[bold green]✓ You're all set![/bold green]")
        console.print()

        quick_start = """[bold]🚀 Quick Start - Common Commands:[/bold]

[cyan]Search by image:[/cyan]
  python3 facetrace.py photo.jpg
  python3 facetrace.py https://example.com/photo.jpg

[cyan]Check your balance:[/cyan]
  python3 facetrace.py --balance

[cyan]Add more credits:[/cyan]
  python3 facetrace.py --add-credits 100

[cyan]Advanced search:[/cyan]
  python3 facetrace.py photo.jpg --min-score 85 --open

[cyan]Help:[/cyan]
  python3 facetrace.py -h

[bold yellow]Ready to find someone?[/bold yellow]
Try your first search now!"""

        console.print(Panel(quick_start, border_style="green", padding=(1, 2)))
        console.print()

        # Mark as complete
        mark_onboarding_complete()

        return True

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Onboarding cancelled. You can run FaceTrace anytime![/yellow]")
        return False
    except Exception as e:
        console.print(f"\n[red]Error during onboarding: {str(e)}[/red]")
        return False


def show_quick_start():
    """
    Show quick start guide for returning users who skipped onboarding
    """
    console.print()
    Display.info("👋 Welcome back! Here are the most common commands:")
    console.print()
    console.print("  [cyan]python3 facetrace.py photo.jpg[/cyan]          Search by image")
    console.print("  [cyan]python3 facetrace.py --balance[/cyan]          Check credits")
    console.print("  [cyan]python3 facetrace.py --add-credits 100[/cyan]  Buy credits")
    console.print("  [cyan]python3 facetrace.py -h[/cyan]                 Full help")
    console.print()
