import discord
import os
import json
from dotenv import load_dotenv
from discord.ext import commands
from datetime import timedelta

permissoes = discord.Intents.default() # permissões do bot
permissoes.message_content = True
bot = commands.Bot(command_prefix='!', intents = permissoes)

MIN = 5
MAX = 9

opcoes_match_final = {}


# Comando de Instruções
@bot.command()
async def helpme(ctx):
    await ctx.send(f"Caso queira que a enquete tenha {MIN} opções (padrão), basta digitar o comando '!enquete' sem o número no comando.")
    await ctx.send(f"Caso queira que a enquete tenha mais que {MIN} opções, digite o comando '!enquete' + o número de opções no comando. Ex: '!enquete 7'.")
    await ctx.send(f"Importante ressaltar: É necessário que a enquete tenha entre {MIN} e {MAX} opções. Caso seja escolhida alguma outra opção, haverá uma mensagem de erro.")

# Função para pegar o nome do usuário Discord e cadastrá-lo no JSON
@bot.command()
async def linkar(ctx, nickname):
    try:
        with open('links.json', 'r') as f:
            links = json.load(f)
    except FileNotFoundError:
        links = {} 
    
    # Adicionando o id do usuário com seu nickname ao dicionário

    id_usuario = str(ctx.author.id)
    links[id_usuario] = nickname
    
    with open('links.json', 'w') as f:
        json.dump(links, f, indent=4)
    
    # Envio da confirmação para o usuário
    await ctx.send(f"Seu nick {nickname} foi vinculado com sucesso.")


MATCH_EN = 'Match'
MATCH_PT = 'Partida'
SCORE_EN = 'Score'
SCORE_PT = 'Pontuação'

@bot.command()
async def rebola(ctx, *, opcoes):

    partidas_da_rodada = {} # Dicionário onde serão armazenadas as matches para validação
    n_match = 1
    options = []
    question = "Qual será a match?"

    divisor_partidas = MATCH_EN
    divisor_pontuacao = SCORE_EN

    if MATCH_PT in opcoes:
        divisor_partidas = MATCH_PT
        divisor_pontuacao = SCORE_PT

    blocos_opcoes = opcoes.split(divisor_partidas)
    for bloco in blocos_opcoes[1:]:
        linhas = bloco.split('\n')
        time_dir = []
        time_esq = []
        for linha in linhas: 

            if ('x' in linha) and (divisor_pontuacao not in linha): # Seleciono as linhas que tem "x" e excluo a linha de "Score"
                match = linha.split('x') # Dividindo as linhas com o "x" de separador

                # Jogador lado Esquerdo
                jogador_esq_format = match[0] # Texto do lado esquerdo do X -> 'Top:    Vinicim (8) '
                jogador_esq_format_2 = jogador_esq_format.split(":") # Divido em 2 strings separadas por : -> ['Top','    Vinicim (8) ']
                jogador_est_format_3 = jogador_esq_format_2[1].split("(") # '    Vinicim (8) ' -> ['    Vinicim ', '8) ']
                nome_esq_final = jogador_est_format_3[0].strip() # '    Vinicim ' -> 'Vinicim'
                time_esq.append(nome_esq_final)

                # Jogador lado Direito
                jogador_dir_format = match[1] # ' (8) Pedro Ruim'
                jogador_dir_final = jogador_dir_format.split(") ") # ' (8) Pedro Ruim' -> [' (8', 'Pedro Ruim']
                nome_dir_final = jogador_dir_final[1] # [' (8', 'Pedro Ruim'] -> 'Pedro Ruim'
                time_dir.append(nome_dir_final)

            else:
                continue # Caso não atenda ambas as condições, o código segue em frente.
        
        chave_partida = f"Match {n_match}"
        partidas_da_rodada[chave_partida] = { # O nome do Dicionário é partidas_da_rodada com a match como chave, onde dentro há duas listas: time esquerdo e direito
            'esquerdo': time_esq,
            'direito': time_dir
        }

        n_match += 1 # Incremento de cada nova match processada
        options.append(chave_partida)
        

        
    with open('partidas.json', 'w') as f:
        json.dump(partidas_da_rodada, f, indent=4)

    options.append("Rebola")

    my_poll = discord.Poll(
        question=discord.PollMedia(text=question),
        duration=timedelta(hours=1)
        )

    # Criando as opções para votação
    for option in options:
            my_poll.add_answer(text=option)

        # Envia a enquete usando o argumento 'poll'

    await ctx.send(poll=my_poll)

    print(f'FINAL DA FORMATAÇÃO: {options}')
    print('-------------------------------------------')




# # Para o voto normal, o código é o descrito abaixo
# @bot.command()
# async def rebola(ctx, num=MIN):
#     # Inicio perguntando qual será a opção escolhida
#     question = "Qual será a match?"
#     options = []

#     if num < MIN or num > MAX:
#         await ctx.send(f"Você pode escolher entre {MIN} e {MAX} opções. Digite o comando novamente.")
#     else:
#         for n in range(1, num+1):
#             options.append(f"Match {n}")
#         options.append("Rebola")

#         my_poll = discord.Poll(
#         question=discord.PollMedia(text=question),
#         duration=timedelta(hours=1)
#         )

#         for option_text in options:
#             my_poll.add_answer(text=option_text)

#         # Envia a enquete usando o argumento 'poll'
#         await ctx.send(poll=my_poll)   
        

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


