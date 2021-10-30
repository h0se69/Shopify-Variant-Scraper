import requests as r
import json, discord

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

def validateURL_JSON(userUrl):
    response = r.get(f'{userUrl}.json',headers=header)
    if(response.status_code == 200 and ('application/json' in response.headers.get('content-type'))):
        return True
    else:
        return False

def getVariants(userUrl):
    data_list  = []
    vars_list  = []
    response = r.get(f'{userUrl}.json',headers=header)
    jsonData = json.loads(response.text)

    try:
        product_Image = jsonData['product']['image']['src']
    except:
        product_Image = 'https://www.macmillandictionary.com/external/slideshow/thumb/White_thumb.png'
    try:
        product_Name = jsonData['product']['title']
    except:
        product_Name = userUrl

    for data in jsonData['product']['variants']:
        try:
            product_Price = str(data['price'])
        except:
            product_Price = '0'
        try:
            product_Variant = str(data['id'])
            product_Title_o1 = str(data['option1'])
            product_Title_o2 = str(data['option2'])
            if('-' in product_Title_o1 or 'None' in product_Title_o1):
                product_Title_o1 = ''
                product_Title = f'{product_Title_o2}'
            elif('-' in product_Title_o2 or 'None' in product_Title_o2):
                product_Title_o2 = ''
                product_Title = f'{product_Title_o1}'
            else:
                product_Title = f'{product_Title_o1}/{product_Title_o2}'

            vars_list.append(product_Variant + ' ')
            data_list.append(product_Title + ' - ' + product_Variant)
        except Exception as e:
            print('Error getting variants: (' + str(e) + ')')
            continue
    data_list.append(product_Name)
    data_list.append(product_Image)
    data_list.append(product_Price)

    return data_list, vars_list

def createEmbed(data_list, vars_list, userUrl):
    size_vars = '\n'.join(data_list[0:-3])
    product_Title = '\n'.join(data_list[-3:-2])
    product_Image = '\n'.join(data_list[-2:-1])
    product_Price = '\n'.join(data_list[-1:len(data_list)])
    vars_only = '\n'.join(vars_list)

    embed = discord.Embed(title=product_Title,url=userUrl ,description=("**Retail: ${}** \n**Product Link: {}**".format(product_Price,userUrl)))
    embed.set_thumbnail(url=product_Image)
    embed.add_field(name="Size-Variants", value= f"```{size_vars}```")    
    embed.add_field(name="Variants", value= f"```{vars_only}```")
    return embed

def failedEmbed():
    embed = discord.Embed(title="Unable to generate Variants!", description=f'Please try again...')
    return embed