import requests
import time
import json
import base64

class WabotApiClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.refresh_token = None
        self.token_expiration = None
        self.api_base_url = 'https://api.wabot.shop/v1'

    # Authenticate and obtain access token
    def authenticate(self):
        url = f'{self.api_base_url}/authenticate'

        headers = {
            'clientId': self.client_id,
            'clientSecret': self.client_secret,
        }

        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('token')
            self.refresh_token = data.get('refreshToken')
            self.token_expiration = self.get_token_expiration(self.access_token)
        else:
            raise Exception(f'Authentication failed: {response.text}')

    # Refresh access token
    def refresh_token_method(self):
        url = f'{self.api_base_url}/refreshToken'

        headers = {
            'clientId': self.client_id,
            'clientSecret': self.client_secret,
            'Content-Type': 'application/json',
        }

        body = {
            'refreshToken': self.refresh_token,
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('token')
            self.refresh_token = data.get('refreshToken')
            self.token_expiration = self.get_token_expiration(self.access_token)
        else:
            raise Exception(f'Token refresh failed: {response.text}')

    # Get templates
    def get_templates(self):
        self.ensure_authenticated()

        url = f'{self.api_base_url}/get-templates'

        headers = {
            'Authorization': self.access_token,
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data.get('data')
        else:
            raise Exception(f'Failed to get templates: {response.text}')

    # Send message
    def send_message(self, to, template_id, params=None):
        self.ensure_authenticated()

        url = f'{self.api_base_url}/send-message'

        headers = {
            'Authorization': self.access_token,
            'Content-Type': 'application/json',
        }

        body = {
            'to': to,
            'templateId': template_id,
            'params': params or [],
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Failed to send message: {response.text}')

    # Logout
    def logout(self):
        url = f'{self.api_base_url}/logout/{self.refresh_token}'

        headers = {
            'clientId': self.client_id,
            'clientSecret': self.client_secret,
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            self.access_token = None
            self.refresh_token = None
            self.token_expiration = None
        else:
            raise Exception(f'Logout failed: {response.text}')

    # Utility methods

    def ensure_authenticated(self):
        if not self.access_token or self.is_token_expired():
            if self.refresh_token:
                self.refresh_token_method()
            else:
                self.authenticate()

        if not self.access_token:
            raise Exception('Unable to authenticate.')

    def is_token_expired(self):
        return self.token_expiration and time.time() >= self.token_expiration

    def get_token_expiration(self, token):
        try:
            token_parts = token.split('.')
            if len(token_parts) != 3:
                return None

            payload = token_parts[1]
            payload += '=' * (-len(payload) % 4)  # Padding for base64
            decoded_payload = base64.urlsafe_b64decode(payload)
            data = json.loads(decoded_payload)
            return data.get('exp')
        except Exception:
            return None
