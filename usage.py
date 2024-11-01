from wabot_api_client import WabotApiClient

def main():
    try:
        client_id = 'YOUR_CLIENT_ID'
        client_secret = 'YOUR_CLIENT_SECRET'

        wabot = WabotApiClient(client_id, client_secret)

        # Authenticate
        wabot.authenticate()

        # Get Templates
        templates = wabot.get_templates()

        for template in templates:
            print(f"Template ID: {template['template_id']}, Name: {template['name']}")

        # Send a message
        to = '+1234567890'
        template_id = '339'  # Replace with your template ID
        template_params = ['John', 'your email address']

        wabot.send_message(to, template_id, template_params)

        print('Message sent successfully.')

        # Logout
        wabot.logout()

    except Exception as e:
        print('Error:', str(e))

if __name__ == '__main__':
    main()
