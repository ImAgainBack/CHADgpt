import discord
import os
import openai
from discord.ext import commands

openai.api_key = 'pk-YukvrbGbWQszkmRTcKDDmQoCvcnTrAjPyUVmwzLsLJnsLQfK'
openai.api_base = 'https://api.pawan.krd/v1'
TOKEN = 'MTEwMzA2MDM1MDkzODY2MDk0NQ.G5xUET.s0jvzCsgHjLcRX6EyMM14QZMPEvWarc0-3LM2U'

conversation_history = {}  # Dictionary to store conversation history

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
async def a(ctx):
    # Ignore messages sent by the bot itself
    if ctx.author == client.user:
        return
    
    user_message = ctx.message.content[2:]  # Extract the user's message (removing '!ping ')
    
    #Test if the bot has to make a program or not
    print(user_message)
    yes_no = function_gpt('I will give you a sentence made by a user.If the sentence contains elements that are specific to programming languages then it is likely a demand to make a program in Python or another programming language. In this case, you should respond with "yes." However, if the sentence lacks these programming-specific elements, then it is likely not a program and you should respond with "no."\n' + user_message)
    print(yes_no.choices[0].text.lower())
    # Retrieve the user's conversation history
    history = conversation_history.get(ctx.author.id, [])
    
    # Clear the conversation history if the user types "!ping clear"
    if user_message.lower() == 'clear' or user_message.lower() == ' clear':
        conversation_history.pop(ctx.author.id, None)
        await ctx.send("Conversation history cleared.")
        return
    
    # Generate a response using GPT-3

    
    # Store the current question in the conversation history
    history.append(user_message)
    
    # Store the current question in the conversation history
    history.append(user_message)
    conversation_history[ctx.author.id] = history

    # Send the response back to the channel
    if yes_no.choices[0].text.strip().lower().startswith('yes'):
        response = function_gpt(' \n'.join(str(item) for item in history) +'\nAll the things before this sentence are messages send you before by the user, this is made so you will be able to remember what the user told you and the next sentence is what the user wants you todo.\n' + user_message)
        await ctx.send('```py\n' +response.choices[0].text.strip()+'\n```')
    else:
        response = function_gpt(' \n'.join(str(item) for item in history) +'\nAll the things before this sentence are messages send you before by the user, this is made so you will be able to remember what the user told you and the next sentence is what the user wants you todo.\n' + user_message)
        await ctx.send(response.choices[0].text.strip())
client.run(TOKEN)
