import asyncio
import sys
import time
import discord
import json
import requests
from database import SubmissionManager
from twitch import TwitchUrl
from cli import CommandBuilder
from utils import get_secret
from discord.ext import commands

API_ENDPOINT = "https://discordapp.com/api/v6"

SECRETS = get_secret()
SECRETS = json.loads(SECRETS)

CLIENT_ID = SECRETS["CLIENT_ID"]
CLIENT_SECRET = SECRETS["CLIENT_SECRET"]

def spinning_cursor():
    while True:
        for cursor in "|/-\\":
            yield cursor


def show_cursor(seconds):
    seconds = seconds * 0.1
    spinner = spinning_cursor()
    for _ in range(50):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b")


def get_token():
    data = {"grant_type": "client_credentials", "scope": "identify connections"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(
        "%s/oauth2/token" % API_ENDPOINT,
        data=data,
        headers=headers,
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    r.raise_for_status()
    return r.json()


# class DiscordClient(discord.Client):
#     db_client = SubmissionManager()
#
#     async def on_ready(self):
#         print("Logged on as {0}!".format(self.user))
#
#     async def on_message(self, message):
#         if message.content:
#             channel = message.channel
#             await channel.send("Send me your vote  👍/👎")
#
#             try:
#                 print(self.db_client.get_submissions_by_user("earlswood"))
#                 reaction, user = await self.wait_for(
#                     "reaction_add", timeout=60.00
#                 )
#             except asyncio.TimeoutError:
#                 await channel.send("👍")
#             else:
#                 await channel.send("👎")

def thumb(th):
    if th is "👍":
        return True
    return False


class DiscordBot:

    bot = commands.Bot(command_prefix='!')
    sb = SubmissionManager()
    token = "YOURTOKEN"
    @bot.command()
    async def by_user(ctx, user_id: str):
        response = SubmissionManager.get_submissions_by_user(user_id)
        tmp = list()
        prettify = list()
        for user in response:
            tmp.append(f"Submitted at {user['created_at']} | {user['url']}")
        prettify.append(f"Found {len(response)} submissions.\n")
        prettify += tmp
        await ctx.send("\n".join(prettify))

    @bot.command()
    async def by_id(ctx, uri: str):
        response = SubmissionManager.get_submission_by_uri(uri)
        prettify = list()
        prettify.append(f"Submitted at {uri['created_at']} | {uri['url']}")
        await ctx.send("\n".join(prettify))

    @bot.command()
    async def all(ctx):
        response = SubmissionManager.list_submissions()
        prettify = list()
        for s in response:
            prettify.append(f"{s.__dict__}")
        joined = "\n".join(prettify)
        await ctx.send(f'{joined}')

    @bot.command()
    async def create_submission(ctx, twitch_url: str):
        url = TwitchUrl(twitch_url)
        parsed = url.parse_url()
        response = SubmissionManager.create_submission(
            url=parsed["url"],
            uri=parsed["uri"],
            twitch_user=parsed["twitch_user"]
        )
        if response is None:
            await ctx.send("Successfully added clip")

    @bot.command()
    async def cast_vote(ctx, uri: str, thumb_vote: str):
        vote = thumb(thumb_vote)
        response = SubmissionManager.cast_vote(uri=uri, voter_id="rizse", vote=vote)
        await ctx.send(response)

    @bot.command()
    async def show_cursor(ctx):
        await ctx.send(show_cursor(100))

    @bot.command()
    async def ping(ctx):
        await ctx.send('pong')

    def run(self):
        self.bot.run(self.token)

if __name__ == "__main__":
    db = SubmissionManager()
    if not db.exists():
        db.create_table()
    # url = TwitchUrl(
    #     "https://www.twitch.tv/earlswood/clip/PatientDullBadgerPeoplesChamp"
    # )
    # url2 = TwitchUrl(
    #     "https://www.twitch.tv/earlswood/clip/PirateEntertainingStorkResidentSleeper"
    # )
    # parsed = url.parse_url()
    # parsed1 = url2.parse_url()
    # db.create_submission(
    #     url=parsed["url"], uri=parsed["uri"], twitch_user=parsed["twitch_user"]
    # )
    # db.create_submission(
    #     url=parsed1["url"], uri=parsed1["uri"], twitch_user=parsed1["twitch_user"]
    # )
    # db.get_submissions_by_user("earlswood")

    cb = CommandBuilder()
    commands = cb.retrieve_file()
    print(cb.yaml_to_json(commands)["commands"])
    bot = DiscordBot()
    bot.run()
    # client = DiscordClient()
    # client.run("NjgwODcyMjg3MDI5MDM1MDcw.XlGeQw.yDPOmVmU1k7bTDLzuONgHkqw2k0")
