"""
FaceTrace CLI - Authentication Commands
Handles user registration, login, and logout
"""

import sys
import getpass
from .api_client import FaceTraceAPI, FaceTraceAPIError
from .config import set_api_key, clear_config, get_email, is_authenticated
from .display import Display


def register_user(silent_mode=False):
    """
    Interactive user registration

    Prompts for email and password, creates account

    Args:
        silent_mode: If True, doesn't show banner (for use in onboarding)

    Returns:
        bool: True if registration successful, False otherwise
    """
    if not silent_mode:
        Display.show_banner()

    Display.info("Create your FaceTrace account")
    print()

    try:
        # Get email
        while True:
            email = input("Email: ").strip()

            if not email:
                Display.error("Email is required")
                continue

            if '@' not in email or '.' not in email:
                Display.error("Please enter a valid email address")
                continue

            break

        # Get password
        while True:
            password = getpass.getpass("Password (min 8 characters): ")

            if len(password) < 8:
                Display.error("Password must be at least 8 characters")
                continue

            password_confirm = getpass.getpass("Confirm password: ")

            if password != password_confirm:
                Display.error("Passwords do not match")
                continue

            break

        # Create account
        Display.info("Creating account...")

        api = FaceTraceAPI()

        try:
            result = api.register(email, password)

            Display.success("Account created successfully!")
            print()

            # Show message from backend (handles both verified and unverified cases)
            backend_message = result.get('message', '')

            if result.get('email_verified', False):
                # Email auto-verified (SMTP not configured)
                Display.info("✓ You can now login with your credentials")
            else:
                # Email verification required
                Display.info("✓ Verification email sent")
                print()
                Display.warning("IMPORTANT: Check your email and click the verification link")
                Display.info("After verification, run: facetrace login")

            return True

        except FaceTraceAPIError as e:
            Display.error(f"Registration failed: {str(e)}")
            return False

    except KeyboardInterrupt:
        print()
        Display.warning("\nRegistration cancelled")
        return False


def login_user(silent_mode=False):
    """
    Interactive user login

    Prompts for email and password, saves API key

    Args:
        silent_mode: If True, doesn't show banner (for use in onboarding)

    Returns:
        bool: True if login successful, False otherwise
    """
    if not silent_mode:
        Display.show_banner()

    Display.info("Login to your FaceTrace account")
    print()

    # Loop until successful login or user cancels (Ctrl+C)
    while True:
        try:
            # Get credentials
            email = input("Email: ").strip()

            if not email:
                Display.error("Email is required")
                print()
                continue

            password = getpass.getpass("Password: ")

            if not password:
                Display.error("Password is required")
                print()
                continue

            # Login
            Display.info("Logging in...")

            api = FaceTraceAPI()

            try:
                result = api.login(email, password)

                # Save API key
                api_key = result.get('api_key')
                balance = result.get('balance', 0)

                if not api_key:
                    Display.error("Login failed: No API key received")
                    print()
                    continue

                set_api_key(api_key, email)

                Display.success("Logged in successfully!")
                print()
                Display.info(f"✓ Email: {email}")
                Display.info(f"✓ Credits: {balance} searches available")
                print()

                if not silent_mode:
                    Display.info("You can now use: facetrace <image> to search")

                if balance == 0:
                    print()
                    Display.warning("You have no credits remaining")
                    Display.info("To add credits, run: facetrace --add-credits <amount>")

                return True

            except FaceTraceAPIError as e:
                Display.error(f"Login failed: {str(e)}")

                if "verify your email" in str(e).lower():
                    Display.info("Please check your email for the verification link")

                print()
                Display.warning("Please try again or press Ctrl+C to cancel")
                print()
                continue

        except KeyboardInterrupt:
            print()
            Display.warning("\nLogin cancelled")
            return False


def logout_user():
    """
    Logout user (clear config)
    """
    if not is_authenticated():
        Display.warning("You are not logged in")
        sys.exit(0)

    email = get_email()

    clear_config()

    Display.success(f"Logged out successfully")

    if email:
        Display.info(f"Account: {email}")


def check_authentication():
    """
    Check if user is authenticated, exit if not

    Raises:
        SystemExit: If user is not authenticated
    """
    if not is_authenticated():
        Display.error("You are not logged in")
        Display.info("To login, run: facetrace login")
        Display.info("To create account, run: facetrace register")
        sys.exit(1)
