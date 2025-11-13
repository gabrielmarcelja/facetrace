"""
FaceTrace CLI - Authentication Commands
Handles user registration, login, and logout
"""

import sys
import getpass
from .api_client import FaceTraceAPI, FaceTraceAPIError
from .config import set_api_key, clear_config, get_email, is_authenticated
from .display import Display


def register_user():
    """
    Interactive user registration

    Prompts for email and password, creates account
    """
    Display.show_banner()

    Display.info("Create your FaceTrace account")
    print()

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
        Display.info(f"✓ You have {result.get('free_searches', 3)} free searches")
        Display.info("✓ Verification email sent")
        print()
        Display.warning("IMPORTANT: Check your email and click the verification link")
        Display.info("After verification, run: facetrace login")

    except FaceTraceAPIError as e:
        Display.error(f"Registration failed: {str(e)}")
        sys.exit(1)


def login_user():
    """
    Interactive user login

    Prompts for email and password, saves API key
    """
    Display.show_banner()

    Display.info("Login to your FaceTrace account")
    print()

    # Get credentials
    email = input("Email: ").strip()

    if not email:
        Display.error("Email is required")
        sys.exit(1)

    password = getpass.getpass("Password: ")

    if not password:
        Display.error("Password is required")
        sys.exit(1)

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
            sys.exit(1)

        set_api_key(api_key, email)

        Display.success("Logged in successfully!")
        print()
        Display.info(f"✓ Email: {email}")
        Display.info(f"✓ Credits: {balance} searches available")
        print()
        Display.info("You can now use: facetrace <image> to search")

        if balance == 0:
            print()
            Display.warning("You have no credits remaining")
            Display.info("To add credits, run: facetrace --add-credits <amount>")

    except FaceTraceAPIError as e:
        Display.error(f"Login failed: {str(e)}")

        if "verify your email" in str(e).lower():
            print()
            Display.info("Please check your email for the verification link")

        sys.exit(1)


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
