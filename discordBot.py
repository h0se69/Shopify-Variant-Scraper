from discord import *
from discord.ext import commands
from ShopifyScraper import validateURL_JSON, getVariants, createEmbed, failedEmbed

# Sets bot command prefix for commands
client = commands.Bot(command_prefix="$", help_command=None)

@client.event
async def on_ready():
        print(f'Bot is online {client.user}')

@client.command(name='var')
async def getVars(ctx, userUrl):

    if('?' in userUrl): #Trims excess characters from URL
        userUrl = userUrl[0: str(userUrl).index('?')]
    response = validateURL_JSON(userUrl) #Makes sure userURL is a valid shopify site
    
    if(response == True):
        data_list, vars_list = getVariants(userUrl)
        if(len(data_list) == 0):
            embed = failedEmbed()
            await ctx.send(embed=embed)
        else:
            embed = createEmbed(data_list, vars_list, userUrl)
            await ctx.send(embed=embed)
    else:
        embed = failedEmbed()
        await ctx.send(embed=embed)

client.run('') #Place Discord Bot Token here to activate