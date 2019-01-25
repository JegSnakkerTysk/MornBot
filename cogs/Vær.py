import discord
import asyncio
from discord.ext import commands

import codecs
import json
import requests
import datetime

with codecs.open("config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    prefix = config["prefix"]

class Vær:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["weather", "forecast", "værmelding", "yr"])
    async def vær(self, ctx, *, by):
        """Viser været i en valgt by"""

        user = ctx.message.author

        #   Hent API key
        with codecs.open("config.json", "r", encoding="utf8") as f:
            config = json.load(f)
            openweathermapApiKey = config["openweathermapApiKey"]

            #   Sjekk for error
            try:
                dataUrl = f"http://api.openweathermap.org/data/2.5/weather?appid={openweathermapApiKey}&q={by}"
                data = requests.get(dataUrl).json()

                byId = str(data["id"])

            except KeyError:
                await ctx.send(f"Fant ikke værstasjon. Prøv en annen by\nSkriv `{prefix}help vær` for hjelp")
                return

            #   Hent resten av data
            link = f"https://openweathermap.org/city/{byId}"
            byName = data["name"]
            countryCode = data["sys"]["country"].lower()
            weatherFetchDate = str(datetime.datetime.fromtimestamp(int(data["dt"])).strftime("%d.%m.%Y %H:%M"))
            description = data["weather"][0]["description"]
            tempCelcius = round((data["main"]["temp"]) - 273)
            tempFahrenheit = round(1.8 * ((data["main"]["temp"]) - 273) + 32)
            windSpeed = data["wind"]["speed"]
            humidity = data["main"]["humidity"]
            cloudiness = data["clouds"]["all"]
            sunrise = str(datetime.datetime.fromtimestamp(int(data["sys"]["sunrise"])).strftime("%H:%M"))
            sunset = str(datetime.datetime.fromtimestamp(int(data["sys"]["sunset"])).strftime("%H:%M"))

            #   Embed
            embed = discord.Embed(title=f":flag_{countryCode}: {byName}, {countryCode.upper()} | {weatherFetchDate} (Norsk Tid)", color=0x0085ff, url=link, description=description)
            embed.add_field(name="Temperatur", value=f"{tempCelcius} °C\n{tempFahrenheit} °F")
            embed.add_field(name="Vind", value=f"{windSpeed} m/s")
            embed.add_field(name="Luftfuktighet", value=f"{humidity}%")
            embed.add_field(name="Skyer", value=f"{cloudiness}%")
            embed.add_field(name="Soloppgang (Norsk tid)", value=sunrise)
            embed.add_field(name="Solnedgang (Norsk tid)", value=sunset)
            embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.avatar_url)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Vær(bot))