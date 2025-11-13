"""
FaceTrace CLI - API Client
HTTP client for communicating with api.facetrace.lat backend
"""

import requests
from typing import Dict, List, Optional
from .config import get_api_key, get_api_url


class FaceTraceAPIError(Exception):
    """Custom exception for API errors"""
    pass


class FaceTraceAPI:
    """API client for FaceTrace backend"""

    def __init__(self):
        self.base_url = get_api_url()
        self.api_key = get_api_key()

    def _get_headers(self) -> Dict:
        """
        Get HTTP headers with API key

        Returns:
            Dict of headers
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'

        return headers

    def _handle_response(self, response: requests.Response) -> Dict:
        """
        Handle API response and raise errors if needed

        Args:
            response: requests Response object

        Returns:
            Response JSON data

        Raises:
            FaceTraceAPIError: If API returns error
        """
        try:
            data = response.json()
        except:
            raise FaceTraceAPIError(f"Invalid response from server (HTTP {response.status_code})")

        if response.status_code >= 400:
            error_msg = data.get('error', f'HTTP {response.status_code} error')
            raise FaceTraceAPIError(error_msg)

        return data

    def register(self, email: str, password: str) -> Dict:
        """
        Register new user

        Args:
            email: User email
            password: User password

        Returns:
            Registration response dict

        Raises:
            FaceTraceAPIError: If registration fails
        """
        url = f"{self.base_url}/auth/register.php"

        try:
            response = requests.post(
                url,
                json={'email': email, 'password': password},
                headers=self._get_headers(),
                timeout=30
            )

            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise FaceTraceAPIError(f"Network error: {str(e)}")

    def login(self, email: str, password: str) -> Dict:
        """
        Login user and get API key

        Args:
            email: User email
            password: User password

        Returns:
            Login response dict with api_key

        Raises:
            FaceTraceAPIError: If login fails
        """
        url = f"{self.base_url}/auth/login.php"

        try:
            response = requests.post(
                url,
                json={'email': email, 'password': password},
                headers=self._get_headers(),
                timeout=30
            )

            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise FaceTraceAPIError(f"Network error: {str(e)}")

    def search_face(
        self,
        image_data: bytes = None,
        image_url: str = None,
        min_score: int = 70,
        platform_filter: str = None
    ) -> Dict:
        """
        Search for face matches

        Args:
            image_data: Image file bytes (for file uploads)
            image_url: Image URL (for URL-based searches)
            min_score: Minimum similarity score (70-100)
            platform_filter: Optional platform filter

        Returns:
            Search results dict

        Raises:
            FaceTraceAPIError: If search fails
        """
        if not self.api_key:
            raise FaceTraceAPIError("Not authenticated. Please login first.")

        url = f"{self.base_url}/search/face.php"
        headers = {'Authorization': f'Bearer {self.api_key}'}

        try:
            if image_data:
                # File upload
                files = {'image': ('image.jpg', image_data, 'image/jpeg')}
                data = {
                    'min_score': min_score
                }

                if platform_filter:
                    data['platform_filter'] = platform_filter

                response = requests.post(
                    url,
                    files=files,
                    data=data,
                    headers=headers,
                    timeout=180  # 3 minutes for search
                )
            elif image_url:
                # URL-based search
                data = {
                    'image_url': image_url,
                    'min_score': min_score
                }

                if platform_filter:
                    data['platform_filter'] = platform_filter

                response = requests.post(
                    url,
                    data=data,
                    headers=headers,
                    timeout=180
                )
            else:
                raise FaceTraceAPIError("Either image_data or image_url must be provided")

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise FaceTraceAPIError("Search timeout. Please try again.")
        except requests.exceptions.RequestException as e:
            raise FaceTraceAPIError(f"Network error: {str(e)}")

    def get_balance(self) -> Dict:
        """
        Get user's credit balance

        Returns:
            Balance info dict

        Raises:
            FaceTraceAPIError: If request fails
        """
        if not self.api_key:
            raise FaceTraceAPIError("Not authenticated. Please login first.")

        url = f"{self.base_url}/credits/balance.php"

        try:
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=30
            )

            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise FaceTraceAPIError(f"Network error: {str(e)}")

    def create_invoice(self, credits: int) -> Dict:
        """
        Create payment invoice for credits purchase

        Args:
            credits: Number of credits to purchase

        Returns:
            Invoice data dict with invoice_url

        Raises:
            FaceTraceAPIError: If request fails
        """
        if not self.api_key:
            raise FaceTraceAPIError("Not authenticated. Please login first.")

        url = f"{self.base_url}/credits/add.php"

        try:
            response = requests.post(
                url,
                json={'credits': credits},
                headers=self._get_headers(),
                timeout=30
            )

            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise FaceTraceAPIError(f"Network error: {str(e)}")
