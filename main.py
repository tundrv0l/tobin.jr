import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import numpy as np
import scipy as sp
from imgutil import *
import math

# Load the token in the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create the client, optimize the intents, declare functions
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='*',intents=intents)
member_list = {}


# Startup Function
@client.event
async def on_startup():
    print('Bot is ready')
    await client.change_presence(activity=discord.Game(name='with linear independence!'))

#---------------------------------UTILITY FUNCTIONS---------------------------------#

# Help Command Override
class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

client.help_command = MyHelpCommand()

# Stores the list of members in the current server into a dictionary
@client.event
async def on_ready():
    for guild in client.guilds:
        for member in guild.members:    
            # Add the member to the dictionary
            member_list[member.name] = member.id
        return member_list


# function to check if a numpy matrix is square
def is_square(matrix):
    return matrix.shape[0] == matrix.shape[1]


#---------------------------------COMMANDS---------------------------------#


#How-To Function
@client.command(description = 'Gives a general overview of how to use the bot')
async def howto(ctx):
    await ctx.send ('''
        This bot is designed to employ a wide variety of linear algebra concepts to help you with your homework. To use a vector command, simply type the command and then the vectors in the form (a,b,c,...n) and (d,e,f,...n) exactly. **Don't leave spaces between the numbers and commas/parenthesis.** To use a matrix command, simply type the command followed by your matrix in the form [a,b;c,d;f,g]. Each semicolon denotes a new row. Therefore, a belongs to M11, c to M21, etc. This is a wip (*vectors are really stupid to parse*), so if you have any suggestions, please let me know!''')


# Rank of a Matrix Function
@client.command(description='Calculates the rank of a matrix.')
async def rank(ctx, message):
    try:
        #Split the message into a matrix
        message = ctx.message.content[6:].replace(' ','')
        # Get the matrix
        matrix = np.matrix(message, dtype=float)
        image_genB(matrix, 'has a rank of: ' + str(np.linalg.matrix_rank(matrix)))
        await ctx.send(file=discord.File('result.png'))
    except SyntaxError:
        await ctx.send("Cannot Compute. Please ensure you entered your matrix in the correct form.")
        
# Determinant of a Matrix Function
@client.command(description='Calculates the determinant of a matrix. Returns whether or not if the matrix is singular/nonsingular.')
async def det(ctx, message):
    try:
        #Split the message into a matrix
        message = ctx.message.content[5:].replace(' ','')
        # Get the matrix
        matrixA = np.matrix(message, dtype=int)
        matrixB = math.trunc(np.linalg.det(matrixA))
        # Check to see if the matrix is singular/nonsingular depending if the determinant is 0 or not
        if np.linalg.matrix_rank(matrixA) == 0:
            await ctx.send("This matrix is singular or invertible")
        else:
            image_genB(matrixA, f"has a determinant of: {matrixB}")
            await ctx.send(file=discord.File('result.png'))
    except SyntaxError:
        await ctx.send("Cannot Compute. Please ensure you entered your matrix in the correct form.")

# Inverse of a Matrix Function
@client.command(description='Calculates the inverse of a matrix. Matrix must be square and be nonsingular.')
async def inverse(ctx, message):
    try:
        #Split the message into a matrix
        message = ctx.message.content[8:].replace(' ','')
        # Get the matrix
        matrix = np.matrix(message, dtype=int)
        if is_square(matrix) == False: # If the matrix is not square, raise an error 
            await ctx.send("Your matrix must be square to have an inverse.")
        elif np.linalg.det(matrix) == 0: # If the matrix is singular, raise an error
            await ctx.send("Your matrix must be nonsingular to have an inverse.")
        else:
            matrixB =  np.linalg.inv(matrix)
            matrixB = np.array_str(matrixB, precision=2)
            image_genA(matrix, "has a inverse of: ", matrixB)
            await ctx.send(file=discord.File('result.png'))
    except SyntaxError:
        await ctx.send("Cannot Compute. Please ensure you entered your matrix in the correct form.")

# Solve a linear matrix equation Function
@client.command(description='Solves a linear matrix equation.')
async def solvelinear(ctx, message):
    try:
        #Split the message into a matrix
        message = ctx.message.content[12:].replace(' ','')
        message = message.split('/')
        # Get the matrix
        matrixA = np.matrix(message[0], dtype=int)
        matrixB = np.matrix(message[1], dtype=int)
        matrixC = np.linalg.solve(matrixA, matrixB)
        if np.linalg.det(matrixA) == 0: # If the matrix is singular, raise an error
            await ctx.send("Your matrixes must be nonsingular to solve the system.")
        else:
            image_genC(matrixA, matrixB, "has a solution of: ", matrixC)
            await ctx.send(file=discord.File('result.png'))
    except SyntaxError:
        await ctx.send("Cannot Compute. Please ensure you entered your matrix in the correct form.")

# Find the nullspace of a matrix Function
@client.command(description='Finds the nullspace of a matrix.')
async def nullspace(ctx, message):
    try:
        #Split the message into a matrix
        message = ctx.message.content[11:].replace(' ','')
        # Get the matrix
        matrixA = np.matrix(message, dtype=int)
        matrixB = np.array_str(sp.linalg.null_space(matrixA), precision=2)
        image_genA(matrixA, "has a nullspace of: ", matrixB)
        await ctx.send(file=discord.File('result.png'))
    except SyntaxError:
        await ctx.send("Cannot Compute. Please ensure you entered your matrix in the correct form.")

# Finds the orthonormal basis of a matrix Function
@client.command(description='Finds the orthonormal basis of a matrix.')
async def orthonormal(ctx, message):
    try:
        #Split the message into a matrix
        message = ctx.message.content[13:].replace(' ','')
        # Get the matrix
        matrixA = np.matrix(message, dtype=int)
        matrixB - sp.linalg.orth(matrixA)
        image_genA(matrixA, "has an orthonormal basis of: ", matrixB)
        await ctx.send(file=discord.File('result.png'))
    except SyntaxError:
        await ctx.send("Cannot Compute. Please ensure you entered your matrix in the correct form.")



client.run(TOKEN)