import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!!')


@bot.event
async def on_ready():
    print("Ticket Bot Aktif")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!!.help"))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    guild = message.guild
    category = discord.utils.get(guild.categories, name='Ticket')
    channel = discord.utils.get(guild.channels, name='📞》ticket')
    if str(message.channel) == str(channel):
        await message.channel.purge(limit=1)
        if discord.utils.get(category.channels, name=message.author.name.lower()):
            await discord.utils.get(category.channels, name=message.author.name.lower()).send(
                f"{message.author.mention} zaten aktif bir kanalın var!"
            )
        else:
            roles = discord.utils.get(guild.roles, name='Ticket')
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                message.author: discord.PermissionOverwrite(read_messages=True),
                roles: discord.PermissionOverwrite(read_messages=True)
            }
            channel = await guild.create_text_channel(message.author.name.lower(), overwrites=overwrites,
                                                      category=category)
            embed = discord.Embed(
                title="🎟️Ticket🎟️",
                colour=discord.Color.blue()
            )
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.add_field(name=f"Merhaba {message.author.name}",
                            value="Ekibimiz en kısa sürede sizinle ilgilenecektir", inline=False)
            embed.add_field(name="Ticket atılma sebebi:", value=f"```{message.content}```", inline=False)
            embed.add_field(name="Ticketı kapatmak için ", value="!!kapat", inline=False)

            await channel.send(embed=embed)
            await channel.send(roles.mention)
    await bot.process_commands(message)


@bot.command()
async def kapat(ctx):
    channel = ctx.message.channel
    guild = ctx.message.guild
    category = discord.utils.get(guild.categories, name='Ticket')
    control = discord.utils.get(category.channels, name=str(channel))
    if str(channel) == str(control):
        await ctx.channel.delete()


@bot.command()
async def ayarla(ctx):
    guild = ctx.message.guild
    await guild.create_category(name='Ticket')
    await guild.create_text_channel("📞》ticket")
    await guild.create_role(name="Ticket")


bot.run("TOKEN HERE")
