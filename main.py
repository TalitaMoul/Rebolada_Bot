import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import timedelta

permissoes = discord.Intents.default() # permissões do bot
permissoes.message_content = True
bot = commands.Bot(command_prefix='!', intents = permissoes)

MIN = 5
MAX = 9


# Comando de Instruções
@bot.command()
async def helpme(ctx):
    await ctx.send(f"Caso queira que a enquete tenha {MIN} opções (padrão), basta digitar o comando '!enquete' sem o número no comando.")
    await ctx.send(f"Caso queira que a enquete tenha mais que {MIN} opções, digite o comando '!enquete' + o número de opções no comando. Ex: '!enquete 7'.")
    await ctx.send(f"Importante ressaltar: É necessário que a enquete tenha entre {MIN} e {MAX} opções. Caso seja escolhida alguma outra opção, haverá uma mensagem de erro.")

# Para o voto normal, o código é o descrito abaixo
@bot.command()
async def rebola(ctx, num=MIN):
    # Inicio perguntando qual será a opção escolhida
    question = "Qual será a match?"
    options = []

    if num < MIN or num > MAX:
        await ctx.send(f"Você pode escolher entre {MIN} e {MAX} opções. Digite o comando novamente.")
    else:
        for n in range(1, num+1):
            options.append(f"Match {n}")
        options.append("Rebola")

        my_poll = discord.Poll(
        question=discord.PollMedia(text=question),
        duration=timedelta(hours=1)
        )

        for option_text in options:
            my_poll.add_answer(text=option_text)

        # Envia a enquete usando o argumento 'poll'
        await ctx.send(poll=my_poll)
        

@bot.event
async def on_ready():
    print("Estou pronto!")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.BadArgument):
    await ctx.send("O valor informado deve ser um número inteiro (Ex: 7). Digite o comando novamente.")

load_dotenv() # Carrega as variáveis do arquivo .env

TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(TOKEN)


