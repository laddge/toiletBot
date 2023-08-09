import os
import glob
import subprocess
from dotenv import load_dotenv
import discord
from discord import Option


def main():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path)

    TOKEN = os.getenv("DISCORD_TOKEN")

    bot = discord.Bot()

    @bot.event
    async def on_ready():
        print(f"ready as {bot.user}")

    @bot.slash_command(description="make ascii art")
    async def toilet(
        ctx: discord.ApplicationContext,
        text: Option(str, required=True),
        font: Option(str, required=False),
    ):
        await ctx.defer()
        if font:
            cmd = ["toilet", "-f", font, text]
        else:
            cmd = ["toilet", text]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.stderr:
            await ctx.respond(f"```\n{res.stderr}\n```")
        else:
            await ctx.respond(f"```\n​{res.stdout}\n```")

    @bot.slash_command(description="font list")
    async def fontlist(
        ctx: discord.ApplicationContext,
    ):
        await ctx.defer()
        filelist = glob.glob("/usr/share/figlet/*.flf") + glob.glob(
            "/usr/share/figlet/*.tlf"
        )
        filelist = [os.path.splitext(os.path.basename(path))[0] for path in filelist]
        res = "\n".join(sorted(filelist))
        await ctx.respond(f"```\n{res}\n```")

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
