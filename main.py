import discord
import os
from discord.ext import commands
from datetime import timedelta
from dotenv import load_dotenv # type: ignore

permissoes = discord.Intents.default() # permissões do bot
permissoes.message_content = True
bot = commands.Bot(command_prefix='!', intents = permissoes)



@bot.command()
# Para o voto normal, o código é o descrito abaixo
async def enquete(ctx): # type: ignore
    # Inicio perguntando qual será a opção escolhida
    question = "Qual será a match?"
    options = [
        "Match 1",
        "Match 2",
        "Match 3",
        "Match 4",
        "Match 5",
        "Rebola"
    ]

    # Cria o objeto Poll
    my_poll = discord.Poll(
        question=discord.PollMedia(text=question),
        duration=timedelta(hours=1)
    )

    for option_text in options:
        my_poll.add_answer(text=option_text)

    # Envia a enquete usando o argumento 'poll'
    await ctx.send(poll=my_poll) # type: ignore

@bot.event
async def on_ready():
    print("Estou pronto!")


load_dotenv() # Carrega as variáveis do arquivo .env
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN) # type: ignore