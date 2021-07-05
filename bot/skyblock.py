import requests
from discord.ext import commands
from util.secret_config import key
from util.skill import *
from util.uuid import uuid


class skyblock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="rates", aliases=["r"])
    async def rates(self, ctx, ign, profile=None):
        mcuuid = uuid(ign)
        if profile is None:
            request = requests.get(f"https://api.slothpixel.me/api/skyblock/profile/{mcuuid}?key={key}")
        else:
            request = requests.get(f"https://api.slothpixel.me/api/skyblock/profile/{mcuuid}/{profile}?key={key}")
        r = request.json()

# fortune from farming level
        total_xp = r["members"][mcuuid]["skills"]["farming"]["xp"]
        try:
            cap = r["members"][mcuuid]["jacob2"]["perks"]["farming_level_cap"] + 50
        except KeyError:
            cap = 50

        farming_level = lvcheck(total_xp, cap)

# fortune from anita bonus
        try:
            anita = r["members"][mcuuid]["jacob2"]["perks"]["double_drops"]
        except KeyError:
            anita = 0

# fortune from elephant
        try:
            pet_name = r["members"][mcuuid]["active_pet"]["name"]
            pet_rarity = r["members"][mcuuid]["active_pet"]["rarity"]
        except KeyError:
            pet_name = ""
            pet_rarity = ""

        if pet_name == "Elephant" and pet_rarity == "LEGENDARY":
            pet_level = r["members"][mcuuid]["active_pet"]["level"]
        else:
            pet_level = 0
        
#fortune from wart hoe
        hoe_ff = 0

        try:
            hoe = r["members"][mcuuid]["inventory"][0]["attributes"]["id"]
        except KeyError:
            await ctx.reply("You must place your hoe in your first hotbar slot!")

        if hoe == "THEORETICAL_HOE_WARTS_1":
            hoe_ff += 10
        elif hoe == "THEORETICAL_HOE_WARTS_2":
            hoe_ff += 25
        elif hoe == "THEORETICAL_HOE_WARTS_3":
            hoe_ff += 50
        
        try:
            reforge = r["members"][mcuuid]["inventory"][0]["attributes"]["modifier"]
        except KeyError:
            reforge = ""
        try:
            rarity = r["members"][mcuuid]["inventory"][0]["rarity"]
        except KeyError:
            rarity = ""

        if reforge == "blessed":
            if rarity == "mythic":
                hoe_ff += 20
            elif rarity == "legendary":
                hoe_ff += 16
            elif rarity == "epic":
                hoe_ff += 13
            elif rarity == "rare":
                hoe_ff += 9
            elif rarity == "uncommon":
                hoe_ff += 7
            elif rarity == "common":
                hoe_ff += 5
            
        try:
            harvesting = r["members"][mcuuid]["inventory"][0]["attributes"]["enchantments"]["harvesting"]
        except KeyError:
            harvesting = 0
        for i in range(harvesting):
            hoe_ff += 12.5
        
        try:
            turbo_warts = r["members"][mcuuid]["inventory"][0]["attributes"]["enchantments"]["turbo_warts"]
        except KeyError:
            turbo_warts = 0
        for i in range(turbo_warts):
            hoe_ff += 5

        try:
            cultivating = r["members"][mcuuid]["inventory"][0]["attributes"]["enchantments"]["cultivating"]
        except KeyError:
            cultivating = 0
        for i in range(cultivating):
            hoe_ff += 1

        ff = (farming_level * 4) + (anita * 2) + (pet_level * 1.8) + hoe_ff

        wart_coins = 3 * (2 * (1 + ff/100))


        await ctx.reply(f"Total farming fortune: {ff}\n\
Fortune from farming skill: {farming_level * 4}\n\
Fortune from Anita bonus: {anita * 2}\n\
Fortune from elephant: {pet_level * 1.8}\n\
Fortune from wart hoe: {hoe_ff}\n\
You should be getting {wart_coins} coins from one block of warts!")


def setup(bot: commands.Bot):
    bot.add_cog(skyblock(bot))