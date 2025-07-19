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
        for _ in range(50):
            await self.message_channel.send('Lạy ông đi qua, lạy bà đi lại, thương tình cho con xin ít coin để sống qua ngày ạ! thành tâm xin coin')
            print('Message sent!')
            await asyncio.sleep(2)
        await self.close()
        await asyncio.sleep(2)
        await self.start(user_token)


client = MyClient()
client.run(user_token)