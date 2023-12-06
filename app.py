# app.py

import requests
from encryption import generate_key, encrypt_message, decrypt_message

class SecureMessenger:
    def __init__(self):
        self.key = generate_key()
        self.api_url = 'http://localhost:5000'

    def send_message(self, message):
        encrypted_message = encrypt_message(message, self.key)
        response = requests.post(f'{self.api_url}/write_message', json={'message': encrypted_message})
        if response.status_code == 201:
            print("Message sent successfully.")
        else:
            print("Failed to send message.")

    def get_messages(self):
        response = requests.get(f'{self.api_url}/get_messages')
        if response.status_code == 200:
            encrypted_messages = response.json().get('messages', [])
            decrypted_messages = [decrypt_message(msg, self.key) for msg in encrypted_messages]
            return decrypted_messages
        else:
            print("Failed to retrieve messages.")
            return []

if __name__ == '__main__':
    messenger = SecureMessenger()
    
    while True:
        choice = input("1. Send Message\n2. Get Messages\n3. Exit\nChoose an option: ")
        
        if choice == '1':
            message = input("Enter the message: ")
            messenger.send_message(message)
        elif choice == '2':
            messages = messenger.get_messages()
            print("Received Messages:")
            for msg in messages:
                print(f"- {msg}")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
