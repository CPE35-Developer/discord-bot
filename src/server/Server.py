import discord
from discord_slash import SlashContext
from discord.utils import get
from discord import  Embed
from pandas import DataFrame
from bs4 import BeautifulSoup
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from pandas import DataFrame
import boto3, os, json
from dotenv import load_dotenv


colors = {'fail':0xb01111,
          'pass': 0x37e407}

load_dotenv()
AWS_ACCCESSKEY = os.getenv('AWS_ACCCESSKEY')
AWS_SECRETKEY = os.getenv('AWS_SECRETKEY')
AWS_REGION = os.getenv('AWS_REGION')
session = boto3.Session(aws_access_key_id=AWS_ACCCESSKEY,
                        aws_secret_access_key=AWS_SECRETKEY, 
                        region_name=AWS_REGION)
ses = session.client('ses')
dynamodb = session.resource("dynamodb")

cpe35_server_user = dynamodb.Table("cpe35_server_user")



SERVICE_ACCOUNT_FILE = 'gcp_client.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SPREADSHEET_ID = '1etE_2Yewic0efF0Gf_3rsuSW58H0OM6Y72KnXK9gycA'
RANGE_NAME = 'Form Responses 1!A1:H'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)


def scan_cpe35_sheet():
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    verify_sheet = DataFrame.from_dict(result['values'])[1:]
    verify_sheet.columns = ['timestamp', 'email', 'id',
                            'nam', 'sur', 'nick', 'discord_usr', 'discord_img_url']
    return verify_sheet


def request_nisit(id: str):

    params = (('stdid', id), ('h', '0'),)
    soup = BeautifulSoup(requests.get('http://nisit-ku.ku.ac.th/WebForm_Index_Report.aspx',
                         params=params, verify=False).content, "html.parser")

    return soup

def request_pirun(id:str):
    
    soup = BeautifulSoup(requests.get(f'https://pirun.ku.ac.th/~b6110503371/api.php/CPE35DiscordBot/user/b{id}', verify=True).content)
    
    return soup

def get_pirun_data(id: str):
    return json.loads(request_pirun(id).text)

def get_nisit_data(id: str):

    k = ['id', 'nam-sur', 'faculty', 'department', 'status', 'campus']
    v = [i[-1].strip() for i in [d.getText().split(":")
                                 for d in request_nisit(id).find('table').find_all('p')[:6]]]

    nisit_data = dict(zip(k, v))
    nisit_data['nam'], nisit_data['sur'] = map(
        str, nisit_data['nam-sur'].replace('นาย', '').replace('นางสาว', '').split())

    return nisit_data

async def get_discorduser_cpe35_form(ctx:SlashContext,verify_msg:discord.Message):
    cpe35_form = scan_cpe35_sheet()
    
    if str(ctx.author) not in cpe35_form.discord_usr.values:
        await verify_msg.edit("Verification failed! Discord username or tag is not the same as in the form.")
        await ctx.author.send(f"Your discord username or tag is not the same as in the form.\nPlease recheck what you have submitted in the form is **valid**.")
        return
    
    return cpe35_form[cpe35_form.discord_usr==str(ctx.author)].to_dict("records")[0]


# def is_verified_email(email:str):
#     return email in ses.list_verified_email_addresses()['VerifiedEmailAddresses']



# def while_not_verified(email:str, timeout:int):
#     timeout = time.time() + timeout
#     while not is_verified_email(email):
#         if time.time() > timeout:
#             return False
#     return True
    
# async def verify_ku_email(ctx: SlashContext, email:str):

#     if ctx.guild_id not in [847172394316464178, 440532168389689345]:
#         await ctx.send(f"This server does not support verification command.", delete_after=10)
#         return
        
#     if email == '':
#         email = get_pirun_data(email.split('@')[0])['google_email']

#     if not is_verified_email(email):
        
#         ses.verify_email_identity(EmailAddress = email)
#         await ctx.author.send("Verification E-mail sent!\nPlease check your KU E-mail")
        
#         if while_not_verified(email, 5*60):
#             await ctx.author.send("Your E-mail is verified!")
#             return True
#         else:    
#             await ctx.author.send("E-mail verification timed out (5 mins)")
#             return False
        
#     else:
#         await ctx.author.send("Your E-mail is verified!")
#         return True

def verify_embed(ctx,color=0xfffff,email_emb:str='-',id_emb:str='-',nam_emb:str='-',sur_emb:str='-',role_emb:str=None,show_email=True):
    embed=discord.Embed(title="CPE35 Server Identity Verification", color=color)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name="E-mail", value=email_emb, inline=True)
    embed.add_field(name="ID", value=id_emb, inline=True)
    embed.add_field(name="Name", value=nam_emb, inline=True)
    embed.add_field(name="Surname", value=sur_emb, inline=True)
    
    if role_emb is not None:
        embed.add_field(name="Role", value=role_emb)
    return embed 


async def ku_verify(ctx: SlashContext):
    

    if ctx.guild_id not in [847172394316464178, 440532168389689345]:
        await ctx.send(f"This server does not support verification command.", delete_after=10)
        return

    verify_msg = await ctx.send(embed=verify_embed(ctx))
        
    form_data = await get_discorduser_cpe35_form(ctx,verify_msg)

    email = form_data['email']
    
    if email != get_pirun_data(form_data['id'])['google_email']:
        await verify_msg.edit(embed=verify_embed(ctx,color=colors['fail'],email_emb="Failed"))
        return
    else:
        await verify_msg.edit(embed=verify_embed(ctx,email_emb="Passed"))
    
    nisit_data = get_nisit_data(form_data["id"])

    if nisit_data is None:
        await verify_msg.edit(embed=verify_embed(color=colors['fail'],email_emb='Passed',id_emb='Failed'))
        await ctx.author.send(f"{form_data['id']} is not found in the KU Database.\nPlease recheck what you have submitted in the form is **valid**.")
        return
    
    for key in ["id","nam","sur"]:
        if form_data[key].strip() != nisit_data[key].strip():
            await ctx.send("Verification failed!")
            await ctx.author.send(f"{form_data[key].strip()} is not found in the Server's forms.\nPlease recheck what you have submitted in the form is **valid**.")
            
            if key == "id":
                await verify_msg.edit(embed=verify_embed(ctx,color=colors['fail'],email_emb='Passed',id_emb='Failed'))
            elif key == "nam":
                await verify_msg.edit(embed=verify_embed(ctx,color=colors['fail'],email_emb='Passed',id_emb='Passed',nam_emb='Failed'))
            elif key == "sur":
                await verify_msg.edit(embed=verify_embed(ctx,color=colors['fail'],email_emb='Passed',id_emb='Passed',nam_emb='Passed', sur_emb='Failed'))

            return
        else:
            if key == "id":
                await verify_msg.edit(embed=verify_embed(ctx,email_emb='Passed',id_emb='Passed'))
            elif key == "nam":
                await verify_msg.edit(embed=verify_embed(ctx,email_emb='Passed',id_emb='Passed',nam_emb='Passed'))
            elif key == "sur":
                await verify_msg.edit(embed=verify_embed(ctx,email_emb='Passed',id_emb='Passed',nam_emb='Passed', sur_emb='Passed'))

        
    if nisit_data['department'] == "วิศวกรรมคอมพิวเตอร์" and nisit_data['campus'] == "วิทยาเขตบางเขน":
        gen = int(nisit_data["id"][:2]) - 64 + 35
        if gen < 31 or gen > 35:
            rolename = f"CPEs"
        else:
            rolename = f"CPE{str(gen)}"
    else:
        rolename = "PEASANT"
        
    await verify_msg.edit(embed=verify_embed(ctx,color=colors['pass'],email_emb='Passed',id_emb='Passed',nam_emb='Passed',sur_emb='Passed',role_emb=rolename))
    if "Verified" not in [y.name for y in ctx.author.roles]:
        await ctx.author.add_roles(get(ctx.guild.roles, name=rolename))
        await ctx.author.add_roles(get(ctx.guild.roles, name="Verified"))
        await ctx.author.send(f"You have been assigned as {rolename}")
        cpe35_server_user.put_item(Item = {'id':ctx.author_id,'verified_name':str(ctx.author)})
        
    
    
def ku_info(ctx: SlashContext, user:discord.Member=None):
    if user is None:
        user = ctx.author
        
    try :
        verified_name = { int(d['id']):d['verified_name'] for d in cpe35_server_user.scan()['Items']}[user.id]
    except KeyError :
        em=discord.Embed(title=f"About {str(user)}",description="Unable to fetch user info from KU database.", color=user.color)
        em.set_thumbnail(url=user.avatar_url)
        
        return em


    
    cpe35_form = scan_cpe35_sheet()
    
    form_data = cpe35_form[cpe35_form.discord_usr == verified_name].to_dict('records')[0]
    pirun_data = get_pirun_data(form_data['id'])
    nisit_data = get_nisit_data(form_data['id'])
    
    engname, engsurname = get_pirun_data(form_data['id'])['engname'].split()
    engsurname = engsurname[0] + engsurname[1:].lower()
    
    em=discord.Embed(title=f"About {str(user)}", color=user.color)
    em.set_thumbnail(url=user.avatar_url)
    em.add_field(name="ชื่อ นามสกุล", value= " ".join(pirun_data['thainame'].split()[1:]), inline=False)
    em.add_field(name="Family name", value=" ".join([engname,engsurname]), inline=False)
    em.add_field(name="Nickname", value=form_data['nick'], inline=True)
    em.add_field(name="Gender", value="Male" if pirun_data['gender'] == "M" else "Female", inline=True)
    em.add_field(name="\u200b", value="\u200b", inline=True)
    em.add_field(name="Faculty", value=nisit_data['faculty'], inline=True)
    em.add_field(name="Department", value=nisit_data['department'], inline=True)
    
    return em
    