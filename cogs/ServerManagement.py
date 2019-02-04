import discord
import asyncio
from discord.ext import commands

import json
import codecs
import time
from pathlib import Path

class ServerManagement:
    def __init__(self, bot):
        self.bot = bot


    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["spark"])
    async def kick(self, ctx, *, bruker: discord.Member):
        """Kaster ut en bruker fra serveren"""

        await bruker.kick()
        await ctx.send(f"<@{bruker.id}> ({bruker.name}#{bruker.discriminator}) ble kastet ut av serveren")


    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def ban(self, ctx, *, bruker: discord.Member):
        """Utesteng en bruker fra serveren"""

        #   Utfør
        await bruker.ban()
        await ctx.send(f"<@{bruker.id}> ({bruker.name}#{bruker.discriminator}) ble utestengt fra serveren")


    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    @commands.command(aliases=["purge", "delete", "slett"])
    async def prune(self, ctx, antall: int):
        """Sletter de siste antall meldingene du spesifiser"""

        #   Utfør
        await ctx.message.channel.purge(limit=antall+1)
        statusmsg = await ctx.send(f"Slettet {antall} meldinger!")
        await asyncio.sleep(3)
        await statusmsg.delete()


    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["setloggkanal", "setlogkanal", "settlogkanal", "setlogchannel", "setlogging", "setloggingchannel"])
    async def settloggkanal(self, ctx, *, kanal: discord.TextChannel):
        """Setter en kanal som loggkanal"""
        
        #   Sjekk om fil allerede eksisterer
        serverDataFile = Path(f"./assets/serverdata/{ctx.message.guild.id}.json")
        if serverDataFile.is_file() == False:
            #   Skriv fil med gitt data
            with codecs.open(f"./assets/serverdata/{ctx.message.guild.id}.json", "w") as f:
                json.dump({"name": ctx.message.guild.name, "logChannelId": kanal.id}, f)

        else:
            #   Skriv data til eksisterende fil
            with codecs.open(f"./assets/serverdata/{ctx.message.guild.id}.json", "r+", encoding="utf8") as f:
                serverdata = json.load(f)
                serverdata["logChannelId"] = kanal.id
                f.seek(0)
                f.write(json.dumps(serverdata))                

        await ctx.send(f"Loggkanal satt til {kanal.mention}")


    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["logchannel", "logkanal", "loggingchannel"])
    async def loggkanal(self, ctx):
        """Viser hvilken kanal som er satt som loggkanal på serveren"""
        
        #   Last inn serverdata
        with codecs.open(f"./assets/serverdata/{ctx.message.guild.id}.json", "r", encoding="utf8") as f:
            serverdata = json.load(f)
            logChannelId = serverdata["logChannelId"]

            #   Sjekk om loggkanal eksisterer
            if logChannelId == None:
                await ctx.send("Du har ikke satt en loggkanal enda.")
            else:
                kanal = self.bot.get_channel(logChannelId)
                await ctx.send(f"Loggkanalen for denne serveren er {kanal.mention}")
        

def setup(bot):
    bot.add_cog(ServerManagement(bot))