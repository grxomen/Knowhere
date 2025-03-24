
import discord
from discord.ext import commands
import json
import os
import asyncio

class Decrypt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shared_file = "data/shared.json"
        self.decrypted_file = "data/decrypted.json"

    @commands.command(name="decrypt")
    @commands.cooldown(1, 30.0, commands.BucketType.user)
    async def decrypt(self, ctx):
        if not os.path.exists(self.shared_file):
            await ctx.send("🛑 No active decryption sequence found.")
            return

        with open(self.shared_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data.get("active_mission"):
            await ctx.send("🧊 No mission available. Await further signals.")
            return

        mission = data["active_mission"]
        image_url = mission.get("image_url")
        question = mission.get("question")
        answer = mission.get("answer").lower()

        embed = discord.Embed(title="🧠 DECRYPTION REQUIRED", description=question)
        if image_url:
            embed.set_image(url=image_url)

        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for("message", timeout=30.0, check=check)
        except:
            await ctx.send("⏳ Timed out. Try again.")
            return

        if msg.content.strip().lower() == answer:
            await ctx.send("✅ Access granted.")
            self.mark_decrypted(ctx.author.id)
        else:
            await ctx.send(f"❌ Incorrect. The correct answer was: **{answer}**")

    def mark_decrypted(self, user_id):
        if os.path.exists(self.decrypted_file):
            with open(self.decrypted_file, "r", encoding="utf-8") as f:
                decrypted = json.load(f)
        else:
            decrypted = {}

        decrypted[str(user_id)] = True
        with open(self.decrypted_file, "w", encoding="utf-8") as f:
            json.dump(decrypted, f, indent=4)

def setup(bot):
    bot.add_cog(Decrypt(bot))
