import asyncio
import discord
import os


user_token = os.getenv('USER_TOKEN')
print(f"Token: {user_token}")
channel_id = int(os.getenv('CHANNEL_ID'))
print(f"Channel ID: {channel_id}")

class MyClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.message_channel = None

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.do_spam()

    async def do_spam(self):
        self.message_channel = self.get_channel(channel_id)
        while True:
            await self.message_channel.send('/dice amount:5000')
            print('Message sent!')
            await asyncio.sleep(10)


client = MyClient()
client.run(user_token)