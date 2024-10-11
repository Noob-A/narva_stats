import csv
import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')  # e.g., '+1234567890'
session_name = 'telegram_parser_session'  # Name for the session file

# The target group
target_group = 'Transfer_SPB_Estonia1'  # You can use the username or the invite link

# Search terms
search_terms = ['отчет', '#отчет']

# Output CSV file
output_file = 'parsed_messages.csv'

async def main():
    # Initialize the client
    client = TelegramClient(session_name, api_id, api_hash)

    await client.start(phone=phone_number)

    # Ensure you're authorized
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone_number)
            code = input('Enter the code you received: ')
            await client.sign_in(phone_number, code)
        except SessionPasswordNeededError:
            password = input('Two-Step Verification enabled. Please enter your password: ')
            await client.sign_in(password=password)

    # Get the target group entity
    try:
        entity = await client.get_entity(target_group)
    except Exception as e:
        print(f"Failed to get entity for {target_group}: {e}")
        await client.disconnect()
        return

    # Prepare to collect messages
    messages_collected = []

    # Define a function to check if a message contains any of the search terms
    def contains_search_term(message_text):
        if not message_text:
            return False
        for term in search_terms:
            if term.lower() in message_text.lower():
                return True
        return False

    # Iterate over the messages in the group
    print("Fetching messages. This may take a while depending on the group size...")

    async for message in client.iter_messages(entity, search='отчет', limit=None):
        if contains_search_term(message.text):
            messages_collected.append({
                'id': message.id,
                'date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
                'sender': (await message.get_sender()).username if message.sender else 'N/A',
                'text': message.text.replace('\n', ' ').replace('\r', ' ') if message.text else ''
            })

    # Remove duplicates if any
    unique_messages = {msg['id']: msg for msg in messages_collected}.values()

    # Write to CSV
    print(f"Writing {len(unique_messages)} messages to {output_file}...")
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'date', 'sender', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for msg in unique_messages:
            writer.writerow(msg)

    print("Done!")
    await client.disconnect()

# Run the main function
if __name__ == '__main__':
    asyncio.run(main())
