# .env
import discord
from discord.ext import commands
import os 
from session import Session
import re


DISCORD_TOKEN = "MTM2NzYwMjI1MTk0MTY3OTI2NA.GJ6blt.xbOJYY41h5tKQY5_64L_SmQD9dHBBMrnKgMHBQ"

bot = commands.Bot(command_prefix="!",case_insensitive=True, intents = discord.Intents.all())

mySessions = []


def checkSessions(member):
    for i in mySessions:
        if i.getUser() == member:
            return i
    return None




    


@bot.event
async def on_ready():
    print("HEY HOWDY MFFFF")
    
@bot.command()
async def hello(ctx):
    await ctx.send("HEYYY GIRLLLLLLL")
    
@bot.command()
async def add(ctx, *arr):
    result = int(arr[0])
    prefix = str(arr[0])
    arr = arr[1:]
    for i in arr:
        result += int(i)
        prefix = prefix + " + " + str(i) 
    output = prefix + " = " + str(result)
    await ctx.send(output)
    
    
@bot.command()
async def investigate(ctx):
    i = checkSessions(ctx.author)
    if i is not None:
        i.close()
        mySessions.remove(i)
    mySession = Session(ctx.author, ctx.channel, "Bot Test.txt")
    mySessions.append(mySession)
    curInvestigation = mySession.investigate()
    if curInvestigation is not None:
        await ctx.send(curInvestigation)
    
    
    
    
    
@bot.command()
async def getSessionInfo(ctx):
    await ctx.send("Fetching session info...")
    i = checkSessions(ctx.author)
    if i is None:
        await ctx.send("No existing session from this user.")
    else:
        await ctx.send("ID: " + str(i.getID()))
        await ctx.send("User: " + str(i.getUser()))
        await ctx.send("Path: " + i.getPath())
        await ctx.send("User Vars: " + str(i.userVars))
        
        
@bot.command()
async def harvest(ctx, *args):
    whitelist = []
    for item in args:
        print(item)
        whitelist.append(item)
    thisChannel = ctx.channel
    await ctx.send("Harvesting data from users: " + str(whitelist))
    file = open(str(thisChannel) + ".txt", "x")
    async for message in thisChannel.history(limit=10000, oldest_first=False):
        if str(message.author) in whitelist:
            file.write("||" + str(message.author) + "||" + re.sub(r'[^\x00-\x7f]',r'', str(message.content)) + "\n")
    file.close()
    await ctx.send("Done.")
    
@bot.command()
async def close(ctx):
    i = checkSessions(ctx.author)
    if i is not None:
        mySessions.remove(i)
        i.close()
        await ctx.send("Done.")
    else:
        await ctx.send("No open sessions from " + str(ctx.author))
        
    
    
            
    
    
        
        
@bot.listen()
async def on_message(message):
    i = checkSessions(message.author)
    if i is None:
        return
    elif i.awaitingInput and message.content.isnumeric():
            print(message.content)
            num = int(message.content)
            if len(i.options) >= num:
                print(i.options)
                i.addPath(i.options[num - 1])
                await message.channel.send("You chose: " + i.options[num - 1])
                i.awaitingInput = False
                investigation = i.investigate()
                if investigation is None:
                    mySessions.remove(i)
                    i.close()
                elif not i.isAwaitingInput():
                    mySessions.remove(i)
                    i.close()
                    await message.channel.send(investigation)
                else:
                    await message.channel.send(investigation)
                    
                    
            return
    
        


bot.run(DISCORD_TOKEN)