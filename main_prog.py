import discord
import os
import openai
from discord.ext import commands

openai.api_key = 'pk-YukvrbGbWQszkmRTcKDDmQoCvcnTrAjPyUVmwzLsLJnsLQfK'
openai.api_base = 'https://api.pawan.krd/v1'
TOKEN = 'MTEwMzA2MDM1MDkzODY2MDk0NQ.G5xUET.s0jvzCsgHjLcRX6EyMM14QZMPEvWarc0-3LM2U'
request = "what does it mean to you to help people?"


def function_gpt(textes):
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt="Human: "f'{textes}' "\nAI:",
        temperature=0.7,
        max_tokens=750,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["Human: ", "AI: "]
    )
    return response


# Create a Discord client
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')

@client.command()
async def ping(ctx):
    # Ignore messages sent by the bot itself
    if ctx.author == client.user:
        return
    
    user_message = ctx.message.content[6:]  # Extract the user's message (removing '!ping ')
    
    # Generate a response using GPT-3
    response = function_gpt(user_message)
    
    # Send the response back to the channel
    await ctx.send(response.choices[0].text.strip())

client.run(TOKEN)
