import discord
import asyncio
from discord.ext import commands

import codecs
import json
import requests
from datetime import datetime
import urllib.parse

with codecs.open("config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    prefix = config["prefix"]

class Vær:
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["weather", "forecast", "værmelding", "yr"])
    async def vær(self, ctx, *, by):
        """Viser været i en valgt by"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Hent API key
        with codecs.open("config.json", "r", encoding="utf8") as f:
            config = json.load(f)
            openweathermapApiKey = config["openweathermapApiKey"]

            #   Sjekk for error
            try:
                url = "http://api.openweathermap.org/data/2.5/weather?" + urllib.parse.urlencode({"appid": openweathermapApiKey, "q": by})
                data = requests.get(url).json()

                byId = str(data["id"])

            except KeyError:
                embed = discord.Embed(color=0xFF0000, description=f":x: Noe gikk galt\n\nSkriv `{prefix}help vær` for hjelp")
                await statusmsg.edit(embed=embed)
                return

            #   Hent resten av data
            link = f"https://openweathermap.org/city/{byId}"
            byName = data["name"]
            countryCode = data["sys"]["country"].lower()
            weatherFetchDate = datetime.fromtimestamp(data["dt"]).strftime("%d.%m.%Y %H:%M")
            description = data["weather"][0]["description"]
            tempCelcius = round((data["main"]["temp"]) - 273)
            tempFahrenheit = round(1.8 * ((data["main"]["temp"]) - 273) + 32)
            windSpeed = data["wind"]["speed"]
            humidity = data["main"]["humidity"]
            cloudiness = data["clouds"]["all"]
            sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
            sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")
            nowTime = datetime.now().strftime("%d.%m.%Y %H:%M")

            #   Embed
            embed = discord.Embed(title=f":flag_{countryCode}: {byName}, {countryCode.upper()} | {weatherFetchDate} (Norsk Tid)", color=0x0085ff, url=link, description=description)
            embed.set_author(name="OpenWeatherMap", icon_url="https://pbs.twimg.com/profile_images/720298646630084608/wb7LSoAc_400x400.jpg")
            embed.add_field(name="Temperatur", value=f"{tempCelcius} °C\n{tempFahrenheit} °F")
            embed.add_field(name="Vind", value=f"{windSpeed} m/s")
            embed.add_field(name="Luftfuktighet", value=f"{humidity}%")
            embed.add_field(name="Skyer", value=f"{cloudiness}%")
            embed.add_field(name="Soloppgang (Norsk tid)", value=sunrise)
            embed.add_field(name="Solnedgang (Norsk tid)", value=sunset)
            embed.set_footer(text=f"Tid i Norge nå: {nowTime}")
            await statusmsg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Vær(bot))