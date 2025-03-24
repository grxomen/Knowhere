
import discord
from discord.ext import commands
import aiosqlite

DB_PATH = "data/knowhere_memory.db"

class Memory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.setup_db())

    async def setup_db(self):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS memory (
                    user_id TEXT PRIMARY KEY,
                    bravery INTEGER DEFAULT 0,
                    obedience INTEGER DEFAULT 0,
                    independence INTEGER DEFAULT 0,
                    title TEXT DEFAULT 'Unclassified'
                )
            """)
            await db.commit()

    @commands.command(name="mindscan")
    @commands.cooldown(1, 15.0, commands.BucketType.user)
    async def mindscan(self, ctx):
        user_id = str(ctx.author.id)
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT * FROM memory WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()

            if not row:
                await db.execute("INSERT INTO memory (user_id) VALUES (?)", (user_id,))
                await db.commit()
                bravery, obedience, independence, title = 0, 0, 0, "Unclassified"
            else:
                _, bravery, obedience, independence, title = row

        embed = discord.Embed(
            title="🧠 Mindscan Report",
            description=f"**User:** {ctx.author.display_name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="🦾 Bravery", value=bravery)
        embed.add_field(name="⚖️ Obedience", value=obedience)
        embed.add_field(name="🚀 Independence", value=independence)
        embed.add_field(name="🪪 Title", value=title)

        await ctx.send(embed=embed)

    @commands.command(name="adjust_trait")
    @commands.has_permissions(administrator=True)
    async def adjust_trait(self, ctx, member: discord.Member, trait: str, amount: int):
        if trait.lower() not in ["bravery", "obedience", "independence"]:
            await ctx.send("❌ Trait must be bravery, obedience, or independence.")
            return

        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(f"""
                INSERT INTO memory (user_id) VALUES (?)
                ON CONFLICT(user_id) DO NOTHING
            """, (str(member.id),))
            await db.execute(f"""
                UPDATE memory SET {trait} = {trait} + ? WHERE user_id = ?
            """, (amount, str(member.id)))
            await db.commit()

        await ctx.send(f"✅ Updated {member.display_name}'s `{trait}` by `{amount}` points.")

def setup(bot):
    bot.add_cog(Memory(bot))
