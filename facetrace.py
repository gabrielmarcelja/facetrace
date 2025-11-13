#!/usr/bin/env python3
"""
FaceTrace - Reverse Face Search CLI Tool
Find where a face appears online

Usage:
    facetrace register                  # Create account
    facetrace login                     # Login to account
    facetrace logout                    # Logout
    facetrace --balance                 # Check credits
    facetrace --add-credits 100         # Buy credits
    facetrace <image> [options]         # Search by image
    facetrace <url> [options]           # Search by URL

Examples:
    facetrace register
    facetrace login
    facetrace photo.jpg
    facetrace https://example.com/photo.jpg
    facetrace image.png --min-score 85 --open
    facetrace --balance
    facetrace --add-credits 100
"""

import sys
import argparse
import webbrowser
import time
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

# Import core modules
from core.display import Display
from core.auth import register_user, login_user, logout_user, check_authentication
from core.api_client import FaceTraceAPI, FaceTraceAPIError
from core.downloader import is_url, download_image, validate_image_size
from core.utils import export_results, open_in_browser
from core.config import get_email
from core.onboarding import is_first_time, run_wizard


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='FaceTrace - Reverse Face Search CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Authentication
  facetrace register                    Create new account
  facetrace login                       Login to account
  facetrace logout                      Logout

  # Search
  facetrace photo.jpg                   Search by file
  facetrace https://example.com/img.jpg Search by URL
  facetrace image.png --min-score 85    With minimum score
  facetrace photo.jpg --open --top 10   Open top 10 in browser

  # Credits
  facetrace --balance                   Check balance
  facetrace --add-credits 100           Purchase 100 searches ($40)
        """
    )

    # Commands (mutually exclusive)
    parser.add_argument(
        'command',
        nargs='?',
        help='Command: register, login, logout, or image path/URL'
    )

    # Credit management
    parser.add_argument(
        '--balance',
        action='store_true',
        help='Check credit balance'
    )

    parser.add_argument(
        '--add-credits',
        type=int,
        metavar='N',
        help='Purchase N credits (minimum 10)'
    )

    # Search options
    parser.add_argument(
        '--min-score',
        type=int,
        default=70,
        metavar='N',
        help='Minimum similarity score (70-100, default: 70)'
    )

    parser.add_argument(
        '--platform',
        type=str,
        default=None,
        metavar='NAME',
        help='Filter by platform (instagram, facebook, twitter, etc.)'
    )

    parser.add_argument(
        '--open',
        action='store_true',
        help='Auto-open top matches in browser'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=None,
        metavar='FILE',
        help='Export results to file (json or csv)'
    )

    parser.add_argument(
        '--top',
        type=int,
        default=5,
        metavar='N',
        help='Number of top matches to open (default: 5, requires --open)'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode with detailed error output'
    )

    return parser.parse_args()


def poll_search_with_progress(api: FaceTraceAPI, search_id: str):
    """
    Poll search status and show real-time progress bar

    Args:
        api: FaceTraceAPI instance
        search_id: Search ID from async search

    Returns:
        Tuple of (results, remaining_credits)
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(complete_style="green", finished_style="bold green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("•"),
        TextColumn("[cyan]{task.fields[found]} found"),
        TimeElapsedColumn(),
        transient=False
    ) as progress:

        task = progress.add_task(
            "Searching across platforms...",
            total=100,
            found=0
        )

        max_attempts = 120  # 2 minutes max
        attempt = 0

        while attempt < max_attempts:
            try:
                status_data = api.get_search_status(search_id)

                status = status_data.get('status')
                current_progress = status_data.get('progress', 0)
                found = status_data.get('found', 0)

                # Update progress bar
                progress.update(task, completed=current_progress, found=found)

                if status == 'complete':
                    # Search complete!
                    progress.update(task, completed=100, description="[bold green]✓ Search complete!")
                    results = status_data.get('results', [])
                    remaining_credits = status_data.get('remaining_credits', 0)
                    return results, remaining_credits

                # Wait before next poll
                time.sleep(2)
                attempt += 1

            except FaceTraceAPIError as e:
                Display.error(f"Progress check failed: {str(e)}")
                raise

        # Timeout
        raise FaceTraceAPIError("Search timed out after 2 minutes")


def handle_balance():
    """Handle --balance command"""
    check_authentication()

    Display.info("Checking balance...")

    api = FaceTraceAPI()

    try:
        result = api.get_balance()

        Display.success("Credit Balance")
        print()
        Display.info(f"✓ Available: {result['balance']} searches")
        Display.info(f"✓ Total used: {result['total_searches']} searches")

        if result['balance'] == 0:
            print()
            Display.warning("You have no credits remaining")
            Display.info("To add credits, run: facetrace --add-credits <amount>")

    except FaceTraceAPIError as e:
        Display.error(f"Failed to get balance: {str(e)}")
        sys.exit(1)


def handle_add_credits(amount: int):
    """Handle --add-credits command"""
    check_authentication()

    if amount < 10:
        Display.error("Minimum purchase is 10 credits")
        sys.exit(1)

    usd_amount = amount * 0.40

    Display.info(f"Creating payment invoice for {amount} searches...")
    Display.info(f"Total: ${usd_amount:.2f} USD")

    api = FaceTraceAPI()

    try:
        result = api.create_invoice(amount)

        invoice_url = result['invoice_url']

        Display.success("Invoice created!")
        print()
        Display.info(f"Credits: {amount} searches")
        Display.info(f"Amount: ${result['usd_amount']} USD")
        Display.info(f"Payment: Cryptocurrency (BTC, ETH, USDT, etc.)")
        print()
        Display.warning("Opening payment page in browser...")
        Display.info("Complete payment to add credits to your account")

        # Open invoice URL in browser
        webbrowser.open(invoice_url)

        print()
        Display.info("After payment, check balance with: facetrace --balance")

    except FaceTraceAPIError as e:
        Display.error(f"Failed to create invoice: {str(e)}")
        sys.exit(1)


def handle_search(image_path_or_url: str, args):
    """Handle search command"""
    check_authentication()

    Display.show_banner()

    # Check if it's a URL or file path
    if is_url(image_path_or_url):
        # URL-based search
        Display.info(f"Downloading image from URL...")

        image_data = download_image(image_path_or_url)

        if not image_data:
            Display.error("Failed to download image from URL")
            sys.exit(1)

        # Validate size
        if not validate_image_size(image_data):
            Display.error("Image too large. Maximum size is 10MB")
            sys.exit(1)

        Display.success("Image downloaded")

        # Start async search
        api = FaceTraceAPI()

        try:
            # Start search
            Display.info("Starting face search...")
            start_result = api.search_face_async(
                image_url=image_path_or_url,
                min_score=args.min_score,
                platform_filter=args.platform
            )

            search_id = start_result.get('search_id')

            # Poll for progress with progress bar
            all_results, remaining_credits = poll_search_with_progress(api, search_id)

        except FaceTraceAPIError as e:
            if "Insufficient credits" in str(e):
                Display.error("No credits remaining")
                Display.info("To add credits, run: facetrace --add-credits <amount>")
            else:
                Display.error(f"Search failed: {str(e)}")
            sys.exit(1)

    else:
        # File-based search
        image_path = Path(image_path_or_url)

        if not image_path.exists():
            Display.error(f"Image not found: {image_path_or_url}")
            sys.exit(1)

        # Validate file extension
        valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif'}
        if image_path.suffix.lower() not in valid_extensions:
            Display.error(f"Unsupported file format: {image_path.suffix}")
            Display.info(f"Supported formats: {', '.join(valid_extensions)}")
            sys.exit(1)

        Display.info(f"Analyzing image: {image_path.name}")

        # Read image file
        with open(image_path, 'rb') as f:
            image_data = f.read()

        # Validate size
        if not validate_image_size(image_data):
            Display.error("Image too large. Maximum size is 10MB")
            sys.exit(1)

        # Start async search
        api = FaceTraceAPI()

        try:
            # Start search
            Display.info("Starting face search...")
            start_result = api.search_face_async(
                image_data=image_data,
                min_score=args.min_score,
                platform_filter=args.platform
            )

            search_id = start_result.get('search_id')

            # Poll for progress with progress bar
            all_results, remaining_credits = poll_search_with_progress(api, search_id)

        except FaceTraceAPIError as e:
            if "Insufficient credits" in str(e):
                Display.error("No credits remaining")
                Display.info("To add credits, run: facetrace --add-credits <amount>")
            else:
                Display.error(f"Search failed: {str(e)}")
            sys.exit(1)

    # Show results
    if not all_results:
        Display.warning(f"No matches found above {args.min_score}% similarity")
        Display.info("Try lowering --min-score or use a different image")
        print()
        Display.info(f"Remaining credits: {remaining_credits} searches")
        sys.exit(0)

    Display.show_results(all_results)

    # Show remaining credits
    print()
    Display.success(f"Remaining credits: {remaining_credits} searches")

    # Export if requested
    if args.output:
        export_results(all_results, args.output)
        Display.success(f"Results exported to: {args.output}")

    # Open top matches in browser if requested
    if args.open and all_results:
        top_matches = all_results[:args.top]
        Display.info(f"Opening top {len(top_matches)} match(es) in browser...")
        open_in_browser(top_matches)


def main():
    """Main entry point"""
    args = parse_args()

    # Run onboarding wizard for first-time users (only if not already authenticated)
    from core.config import is_authenticated
    if is_first_time() and not is_authenticated():
        run_wizard()
        # After wizard, exit gracefully
        sys.exit(0)

    try:
        # Handle authentication commands
        if args.command == 'register':
            register_user()
            sys.exit(0)

        elif args.command == 'login':
            login_user()
            sys.exit(0)

        elif args.command == 'logout':
            logout_user()
            sys.exit(0)

        # Handle credit commands
        if args.balance:
            handle_balance()
            sys.exit(0)

        if args.add_credits:
            handle_add_credits(args.add_credits)
            sys.exit(0)

        # Handle search command
        if args.command:
            # Validate search parameters
            if not 70 <= args.min_score <= 100:
                Display.error("--min-score must be between 70 and 100")
                sys.exit(1)

            if args.top <= 0:
                Display.error("--top must be a positive number")
                sys.exit(1)

            handle_search(args.command, args)
        else:
            # No command provided
            Display.error("No command or image provided")
            Display.info("Usage:")
            Display.info("  facetrace register           Create account")
            Display.info("  facetrace login              Login")
            Display.info("  facetrace <image>            Search")
            Display.info("  facetrace --balance          Check credits")
            Display.info("  facetrace --add-credits N    Buy credits")
            Display.info("")
            Display.info("Run 'facetrace -h' for more help")
            sys.exit(1)

    except KeyboardInterrupt:
        Display.warning("\nInterrupted by user")
        sys.exit(0)

    except Exception as e:
        Display.error(f"An error occurred: {str(e)}")
        if args.debug:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
