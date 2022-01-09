import discord
from discord.ext import commands
import random

bot = discord.Bot(debug_guilds=[927905225694666813])
game_data = {}

class OptionsButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    async def check_answer(self, interaction, button, type):
        correct_answer = game_data[interaction.guild.id]["correct_answer"]
        game_data[interaction.guild.id]["total_questions"] += 1
        if int(button.custom_id[4]) == correct_answer:
            for child in self.children:
                if child.custom_id in ['opt_1', 'opt_2', 'opt_3', 'opt_4']:
                    child.disabled = True
                    if int(child.custom_id[4]) == correct_answer:
                        child.style = discord.ButtonStyle.green
                    else:
                        child.style = discord.ButtonStyle.grey
            game_data[interaction.guild.id]["correct"] += 1
            await interaction.response.edit_message(content="Correct Option!",view=self)
        else:
            for child in self.children:
                if child.custom_id in ['opt_1', 'opt_2', 'opt_3', 'opt_4']:
                    child.disabled = True
                    if int(child.custom_id[4]) == correct_answer:
                        child.style = discord.ButtonStyle.green
                    elif child.custom_id[4] == button.custom_id[4]:
                        child.style = discord.ButtonStyle.red
                    else:
                        child.style = discord.ButtonStyle.grey
            await interaction.response.edit_message(content="Wrong Option!",view=self)
        try:
            await interaction.guild.voice_client.stop()
        except:
            pass
        if game_data[interaction.guild.id]["total_questions"] == 5 and game_data[interaction.guild.id]["total_questions"] == game_data[interaction.guild.id]["correct"]:
            game_data[interaction.guild.id]["game_going"] = False
            await interaction.channel.send(content=f"*Game Over!* <@{interaction.user.id}>\nYou answered all the questions correctly! Thats a **HUGE W**")
            await interaction.guild.voice_client.disconnect()
        elif game_data[interaction.guild.id]["total_questions"] == 5:
            game_data[interaction.guild.id]["game_going"] = False
            await interaction.channel.send(content=f"*Game Over!* <@{interaction.user.id}>\nYou got a solid {game_data[interaction.guild.id]['correct']}/5!")
            await interaction.guild.voice_client.disconnect()
        else:
            if type == 1:
                await ask_question_instrunment(interaction)
            elif type == 2:
                await ask_question_voice(interaction)
            elif type == 3:
                pass

    @discord.ui.button(label=f"Option 1", style=discord.ButtonStyle.blurple, custom_id="opt_1")
    async def opt_1_btn(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.check_answer(interaction, button, self.value)
    @discord.ui.button(label=f"Option 2", style=discord.ButtonStyle.blurple, custom_id="opt_2")
    async def opt_2_btn(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.check_answer(interaction, button, self.value)
    @discord.ui.button(label=f"Option 3", style=discord.ButtonStyle.blurple, custom_id="opt_3")
    async def opt_3_btn(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.check_answer(interaction, button, self.value)
    @discord.ui.button(label=f"Option 4", style=discord.ButtonStyle.blurple, custom_id="opt_4")
    async def opt_4_btn(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.check_answer(interaction, button, self.value)

class ChoosePlay(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.choice = None

    async def disable_color(self, interaction, button):
        for child in self.children:
            if child.custom_id in ['instrunment', 'music', 'voice']:
                child.disabled = True
                if child.custom_id == button.custom_id:
                    child.style = discord.ButtonStyle.green
                else:
                    child.style = discord.ButtonStyle.grey
        await interaction.response.edit_message(content=f"{button.custom_id.capitalize()} it is!",view=self)

    @discord.ui.button(label="Instrunment", style=discord.ButtonStyle.blurple, emoji="🎹", custom_id="instrunment")
    async def instrunment(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.disable_color(interaction, button)
        await ask_question_instrunment(interaction)

    @discord.ui.button(label="Voice", style=discord.ButtonStyle.blurple, emoji="🗣️", custom_id="voice")
    async def voice(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.disable_color(interaction, button)
        await ask_question_voice(interaction)
class HowToPlay(discord.ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(label="How To Play", style=discord.ButtonStyle.green, emoji="📒", custom_id="how_to_play")
    async def helpplay(self, button: discord.ui.Button, interaction: discord.Interaction):
        for child in self.children:
            if child.custom_id in ['how_to_play']:
                child.disabled = True
                child.style = discord.ButtonStyle.grey

        embed = discord.Embed(title="How To Play", description="", color=0x00ff00)
        embed.add_field(name="Join a voice channel.", value="You need to be in a voice channel to play the game.\nBe in a voice channel and use `/join` to make the bot join your voice channel.", inline=False)
        embed.add_field(name="Start the game.", value="Use `/play` to start the game.\nYou will be asked for conformation prompt.\nThen you will be greeted with **two** game modes to choose from choose any of them to staty the game.", inline=False)
        embed.add_field(name="Start playing.", value="You will be asked a question and you will have 4 options to choose from.\nYou can only choose one option per question.\nTotal of 5 questions will be asked and will be concluded by saying your points.", inline=False)
        await interaction.response.edit_message(embed=embed,view=self)
class ConfirmPlay(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Play", style=discord.ButtonStyle.blurple, emoji="🕹️", custom_id="play_continue")
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        for child in self.children:
            if child.custom_id in ['play_continue', 'play_cancel']:
                child.disabled = True
                if child.custom_id == 'play_continue':
                    child.style = discord.ButtonStyle.green
                else:
                    child.style = discord.ButtonStyle.grey
        await interaction.response.edit_message(content="Lets Play!",view=self)
        view = ChoosePlay()
        await interaction.channel.send(content="Choose your game type!", view=view)
        game_data[interaction.guild.id] = {"correct": 0, "total_questions": 0, "correct_answer": None, "game_going": True}

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey, custom_id="play_cancel")
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        for child in self.children:
            if child.custom_id in ['play_continue', 'play_cancel']:
                child.disabled = True
                if child.custom_id == 'play_continue':
                    child.style = discord.ButtonStyle.grey
                else:
                    child.style = discord.ButtonStyle.red
        await interaction.response.edit_message(content="Cancelled!",view=self)

@bot.slash_command(description="Joins the bot into the VC.", name="join")
async def join(ctx, *, channel: discord.VoiceChannel = None):
    if channel is None:
        channel = ctx.author.voice.channel
        if channel is None:
            await ctx.respond("Please be in a voice channel or mention a channel!", ephemeral=True)
            return
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
        await ctx.respond("Joined your VC!", ephemeral=True)
        return
    
    await channel.connect()
    await ctx.respond("Joined your VC!", ephemeral=True)

@bot.slash_command(description="Adjust the volume of the player.", name="volume")
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.respond("Not connected to a voice channel.", ephemeral=True)
    if volume < 0 or volume > 100:
        return await ctx.respond("Volume must be between 0 and 100.", ephemeral=True)
    ctx.voice_client.source.volume = volume / 100
    await ctx.respond(f"Changed volume to {volume}%")

@bot.slash_command(description="List outs all the commands.", name="help")
async def help(ctx):
    embed = discord.Embed(title="Help", description="List of all commands", color=0x00ff00)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
    embed.add_field(name="Commands", value="\n".join(f"`{cmd.name}` - {cmd.description}" for cmd in bot.commands))
    view = HowToPlay()
    await ctx.respond(embed=embed, view=view)

@bot.slash_command(description="Play the epic game!", name="play")
async def play(ctx):
    if ctx.voice_client is None:
        return await ctx.respond("Not connected to a voice channel.\nPlease use `/join` to join a voice channel.")
    try:
        if game_data[ctx.guild.id]["game_going"]:
            return await ctx.respond("A game is already going on!\nMultiplayer is not available yet, so please wait for it to end.", ephemeral=True)
    except KeyError:
        pass
    view = ConfirmPlay()
    await ctx.respond("Welcome to **Guess the Music!**\nCan we continue?", view=view)

async def ask_question_instrunment(ctx):
    sounds = ["drums", "guitar", "piano", "violin", "bell", "flute", "saxophone", "whistle", "trumpet", "seashore"];
    choices = ["drums", "guitar", "piano", "violin", "viola", "cello", "flute", "keyboard", "saxophone", "trumpet", "trombone", "tuba", "clarinet", "oboe", "bass", "harp", "sitar", "mandolin", "banjo", "shamisen", "koto", "bongos", "gamelan", "xylophone", "timpani", "tambourine", "marimba", "dulcimer", "bagpipes", "fiddle", "shanai", "sepulcher", "bell", "tinklebell", "agogo", "steel drums", "woodblock", "taiko drum", "melodic tom", "synth drum", "reverse cymbal", "claves", "cowbell", "crash cymbals", "vibraslap", "vibraphone", "maracas", "whistle", "breath noise", "seashore", "bird tweet", "telephone ring", "helicopter", "applause", "gunshot"];
    play_sound = random.choice(sounds)
    choices.remove(play_sound)
    randomlist = random.sample(range(0, len(choices)), 3)
    randomOptions = [choices[i] for i in randomlist]
    randomOptions.append(play_sound)
    random.shuffle(randomOptions)

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"sounds\instrunment\{play_sound}.mp3"))
    ctx.guild.voice_client.play(
        source, after=lambda e: ctx.channel.send(f"Player error: Cannot play audio in VC.") if e else None
    )
    view = OptionsButton()
    view.value = 1
    for child in view.children:
        if child.custom_id in ['opt_1', 'opt_2', 'opt_3', 'opt_4']:
            child.label = randomOptions[int(child.custom_id[4]) - 1].capitalize()
    try:
        game_data[ctx.guild.id]
        game_data[ctx.guild.id]["correct_answer"] = randomOptions.index(play_sound)+1
        game_data[ctx.guild.id]["game_going"] = True
    except:
        game_data[ctx.guild.id] = {"correct": 0, "total_questions": 0, "correct_answer": randomOptions.index(play_sound)+1, "game_going": True}
    
    await ctx.channel.send("What instrument do you hear play?", view=view)

async def ask_question_voice(ctx):
    sounds = ['barack_Obama', 'bill_Gates', 'donald_Trump', 'elon_Musk', 'justin_Bieber', 'kim_Kardashian', 'kylie_Jenner', 'oprah_Winfrey', 'stephen_Hawkins', 'the_Rock']
    choices = ['barack_Obama', 'bill_Gates', 'donald_Trump', 'elon_Musk', 'justin_Bieber', 'kim_Kardashian', 'kylie_Jenner', 'oprah_Winfrey', 'stephen_Hawkins', 'the_Rock', 'Ronaldo', 'Messi', 'Dyana', 'Lil Baby', 'YG', 'Mark Zuckerberg', 'Tim Cook', 'Michel']
    play_sound = random.choice(sounds)
    choices.remove(play_sound)
    randomlist = random.sample(range(0, len(choices)), 3)
    randomOptions = [choices[i] for i in randomlist]
    randomOptions.append(play_sound)
    random.shuffle(randomOptions)

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"sounds/voice/{play_sound}.mp3"))
    ctx.guild.voice_client.play(
        source, after=lambda e: ctx.channel.send(f"Player error: Cannot play audio in VC.") if e else None
    )
    view = OptionsButton()
    view.value = 2
    for child in view.children:
        if child.custom_id in ['opt_1', 'opt_2', 'opt_3', 'opt_4']:
            child.label = randomOptions[int(child.custom_id[4]) - 1].replace("_", " ").capitalize()
    try:
        game_data[ctx.guild.id]
        game_data[ctx.guild.id]["correct_answer"] = randomOptions.index(play_sound)+1
        game_data[ctx.guild.id]["game_going"] = True
    except:
        game_data[ctx.guild.id] = {"correct": 0, "total_questions": 0, "correct_answer": randomOptions.index(play_sound)+1, "game_going": True}

    await ctx.channel.send("Who's voice do you hear play?", view=view)

bot.run("OTI3OTAzNjQ5MjAyNTY5MjE3.YdQ_nQ.3Pg6zxHv0KMLzy_Yjo2rsXGQFG4")