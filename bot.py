import json
import info
import discord
import random
from discord.ext import commands
import asyncio

# 1261280540503822341 <-- my account


class TrumpBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.discord_tweet())

    async def on_ready(self):

        print("lets go!")
        await self.change_presence(activity=discord.Game(name="Trump 2020"))
    
    async def on_message(self, message: discord.Message):
        if message.guild is None and not message.author.bot:
            with open("tweet.json","r") as f:
                    database = json.load(f)

            if message.author.id == 172340872367702016 and message.content == "blocked_victims":
                for victim in database["blocked"]:
                    await self.get_user(172340872367702016).send(f"{self.get_user(victim).name}:{id}")

            elif message.author.id == 172340872367702016 and message.content == "toggle_dmfeed":
                if database["dm_feed"]:
                    database["dm_feed"] = False
                    temp = await self.get_user(172340872367702016).send("**DM feed toggled OFF** :red_circle:")
                    await asyncio.sleep(5)
                    await temp.delete()
                else:
                    database["dm_feed"] = True
                    temp = await self.get_user(172340872367702016).send("**DM feed toggled ON** :green_circle:")
                    await asyncio.sleep(5)
                    await temp.delete()

            elif message.author.id == 172340872367702016 and message.content == "list_subs":
                index = 0
                for sub in database["subs"]:
                    user = await self.fetch_user(sub)
                    await self.get_user(172340872367702016).send(f"[{index}] {user.name} : {sub}")
                    index += 1

            elif message.author.id == 172340872367702016 and message.content[:5] == "!send":
                try:
                    await self.get_user(database["subs"][int(message.content[6])]).send(message.content[8:])
                    await message.add_reaction("\U00002705")
                except:
                    await message.add_reaction("\U0000274c")
                    if not id in database["blocked"]:
                            await self.get_user(172340872367702016).send(f"Yo boss, {self.get_user(id)} blocked me. :worried:")
                            database["blocked"].append(id)

            elif message.author.id == 172340872367702016 and message.content == "CLOSE_BOT":
                database["quit"] = True

            else:
                with open("answers.txt", "a+") as answers:
                    answers.write(f"{message.author.name}: {message.content}\n")
                if database["dm_feed"]:
                    await self.get_user(172340872367702016).send(f"```{message.author.name}: {message.content}```")
            
            with open("tweet.json","w") as f:
                    json.dump(database,f)



    async def discord_tweet(self):
        await self.wait_until_ready()

        message_presets = [
        ":sunglasses: **OMG look what ma boi TRUMP just tweeted:**", 
        ":angel: **Oh jeez, our lord and saviour donald j trump has blessed us with another amazing tweet dude:**", 
        ":sunglasses: **DAMN These stupid fucking libtards. You tell' em trump:**", 
        ":tv: **CNN IS FAKE NEWS MAN. Fox News is where its at. and their hero trump is tweeting:**",
        "**Trump knows words alright, her has the best words:**",
        "**Sleepy joe is never gonna win hahah GO TRUMP:**"
        ]

        while not self.is_closed():

            with open("tweet.json","r") as f:
                database  = json.load(f)

            if database["quit"]:
                exit()
            
            if database["new_tweet"] == True:
                for id in database["subs"]:
                    try:
                        if "https://" in database["tweet"]:
                            await self.get_user(id).send(database["tweet"]+"\n#Trump2020")
                        else:
                            await self.get_user(id).send(message_presets[random.randint(0, len(message_presets)-1)]+"\n```"+database["tweet"]+"```\n#Trump2020")
                    except:
                        if not id in database["blocked"]:
                            await self.get_user(172340872367702016).send(f"Yo boss, {self.get_user(id)} blocked me. :worried:")
                            database["blocked"].append(id)
                    database["new_tweet"] = False
            with open("tweet.json","w") as f:
                    json.dump(database,f)

            await asyncio.sleep(60)


client = TrumpBot()

client.run(info.bot_token)