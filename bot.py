import json
import info
import discord
from discord.ext import commands
import asyncio

# 1261280540503822341 <-- my account

victims = [172340872367702016]

class TrumpBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.discord_tweet())

    async def on_ready(self):

        print("lets go!")
        await self.change_presence(activity=discord.Game(name="Trump 2020"))




    async def discord_tweet(self):
        await self.wait_until_ready()

        while not self.is_closed():

            with open("tweet.json","r") as f:
                database  = json.load(f)
            
            if database["new_tweet"] == True:
                for id in victims:
                    await self.get_user(id).send(database["tweet"])
                    database["new_tweet"] = False
            with open("tweet.json","w") as f:
                    json.dump(database,f)

            await asyncio.sleep(60)


client = TrumpBot()

client.run(info.bot_token)