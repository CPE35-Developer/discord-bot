import discord
from discord import embeds
from discord_slash import SlashContext
from discord.utils import get
from discord import Embed
from google.auth.transport import Response
from pandas import DataFrame
from bs4 import BeautifulSoup
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from pandas import DataFrame
import boto3
import json
from src.utils.env import vars

colors = {'fail': 0xb01111,
          'pass': 0x37e407}

session = boto3.Session(aws_access_key_id=vars.AWS_ACCCESSKEY,
                        aws_secret_access_key=vars.AWS_SECRETKEY,
                        region_name=vars.AWS_REGION)
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
    soup = BeautifulSoup(requests.get(vars.NISIT_KU_URL,
                         params=params, verify=False).content, "html.parser")

    return soup


def request_pirun(id: str):

    soup = BeautifulSoup(requests.get(
        f'{vars.PIRUN_URL}{id}', verify=True).content)

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


def is_verified_email(email:str):
    return email in ses.list_verified_email_addresses()['VerifiedEmailAddresses']


def while_not_verified(email:str, timeout:int):
    timeout = time.time() + timeout
    while not is_verified_email(email):
        if time.time() > timeout:
            return False
    return True

async def verify_ku_email(ctx: SlashContext, email:str):

    if ctx.guild_id not in [847172394316464178, 440532168389689345]:
        await ctx.send(f"This server does not support verification command.", delete_after=10)
        return

    if email == '':
        email = get_pirun_data(email.split('@')[0])['google_email']

    if not is_verified_email(email):

        ses.verify_email_identity(EmailAddress = email)
        await ctx.author.send("Verification E-mail sent!\nPlease check your KU E-mail")

        if while_not_verified(email, 5*60):
            await ctx.author.send("Your E-mail is verified!")
            return True
        else:
            await ctx.author.send("E-mail verification timed out (5 mins)")
            return False

    else:
        await ctx.author.send("Your E-mail is verified!")
        return True

def verify_embed(ctx: SlashContext, color=0xfffff, email_emb: str = '-', id_emb: str = '-', nam_emb: str = '-', sur_emb: str = '-', role_emb: str = None):
    embed = discord.Embed(
        title="CPE35 Server Identity Verification", color=color)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name="E-mail", value=email_emb, inline=True)
    embed.add_field(name="ID", value=id_emb, inline=True)
    embed.add_field(name="Name", value=nam_emb, inline=True)
    embed.add_field(name="Surname", value=sur_emb, inline=True)

    if role_emb is not None: embed.add_field(name="Role", value=role_emb)
    return embed


async def ku_verify(ctx: SlashContext):

    if ctx.guild_id not in [847172394316464178, 440532168389689345]:
        await ctx.send(f"This server does not support verification command.", delete_after=10)
        return

    verify_msg = await ctx.send(embed=verify_embed(ctx))

    cpe35_form = scan_cpe35_sheet()
    if str(ctx.author) not in cpe35_form.discord_usr.values:
        await verify_msg.edit(embed=verify_embed(ctx, color=colors['fail']))
        await ctx.author.send(f"Your discord username or tag ({str(ctx.author)}) is not in the form.\nPlease recheck what you have submitted in the form is **valid**. You can edit/submit the form with this link https://forms.gle/uz9AzuDLaHgD4Rix5.")
        return

    form_data = cpe35_form[cpe35_form.discord_usr ==
                           str(ctx.author)].to_dict("records")[0]

    pirun_data = get_pirun_data(form_data['id'])
    email = form_data['email']

    if email != pirun_data['google_email']:
        await verify_msg.edit(embed=verify_embed(ctx, color=colors['fail'], email_emb="Failed"))
        return
    else:
        await verify_msg.edit(embed=verify_embed(ctx, email_emb="Passed"))

    nisit_data = get_nisit_data(form_data["id"])

    if nisit_data is None:
        await verify_msg.edit(embed=verify_embed(ctx, color=colors['fail'], email_emb='Passed', id_emb='Failed'))
        await ctx.author.send(f"{form_data['id']} is not found in the KU Database.\nPlease recheck what you have submitted in the form is **valid**.")
        return

    for key in ["id", "nam", "sur"]:
        if form_data[key].strip() != nisit_data[key].strip():
            await ctx.send("Verification failed!")
            await ctx.author.send(f"{form_data[key].strip()} is not found in the Server's forms.\nPlease recheck what you have submitted in the form is **valid**.")

            if key == "id":
                await verify_msg.edit(embed=verify_embed(ctx, color=colors['fail'], email_emb='Passed', id_emb='Failed'))
            elif key == "nam":
                await verify_msg.edit(embed=verify_embed(ctx, color=colors['fail'], email_emb='Passed', id_emb='Passed', nam_emb='Failed'))
            elif key == "sur":
                await verify_msg.edit(embed=verify_embed(ctx, color=colors['fail'], email_emb='Passed', id_emb='Passed', nam_emb='Passed', sur_emb='Failed'))

            return
        else:
            if key == "id":
                await verify_msg.edit(embed=verify_embed(ctx, email_emb='Passed', id_emb='Passed'))
            elif key == "nam":
                await verify_msg.edit(embed=verify_embed(ctx, email_emb='Passed', id_emb='Passed', nam_emb='Passed'))
            elif key == "sur":
                await verify_msg.edit(embed=verify_embed(ctx, email_emb='Passed', id_emb='Passed', nam_emb='Passed', sur_emb='Passed'))

    if nisit_data['department'] == "วิศวกรรมคอมพิวเตอร์" and nisit_data['campus'] == "วิทยาเขตบางเขน":
        gen = int(nisit_data["id"][:2]) - 64 + 35
        rolename = f"CPE{str(gen)}"
        if rolename not in [y.name for y in ctx.guild.roles]:
            role = await ctx.guild.create_role(name=rolename)
        else:
            role = get(ctx.guild.roles, name=rolename)

    else:
        role = None

    await verify_msg.edit(embed=verify_embed(ctx, color=colors['pass'], email_emb='Passed', id_emb='Passed', nam_emb='Passed', sur_emb='Passed', role_emb=rolename))

    if "Verified" not in [y.name for y in ctx.guild.roles]:
        await ctx.guild.create_role(name="Verified")

    if "Verified" not in [y.name for y in ctx.author.roles]:
        await ctx.author.add_roles(get(ctx.guild.roles, name="Verified"))
        if role is not None:
            await ctx.author.add_roles(role)
            await ctx.author.send(f"You have been assigned as {role.name}")
        cpe35_server_user.put_item(Item={'id': ctx.author_id,
                                         'verified_name': str(ctx.author),
                                         'email_ku': email,
                                         'email_other': pirun_data['other_email'],
                                         'id_ku': pirun_data['idcode'],
                                         'thainame': " ".join(pirun_data['thainame'].split()[1:]),
                                         'engname': (lambda engname: engname[:engname.find(' ')+2] + engname[engname.find(' ')+2:].lower())(pirun_data['engname']),
                                         'nickname': form_data['nick'],
                                         'gender': pirun_data['gender'],
                                         'faculty': nisit_data['faculty'],
                                         'department': nisit_data['department'],
                                         'advisor-id': pirun_data['advisor-id'],
                                         'faculty-id': pirun_data['faculty-id'],
                                         'major-id': pirun_data['major-id'], })


def ku_info(ctx: SlashContext, user: discord.Member = None):
    if user is None:
        user = ctx.author

    response = cpe35_server_user.get_item(Key={"id": user.id})

    if "Item" not in response:
        em = discord.Embed(
            title=f"About {str(user)}", description="Unable to fetch user info from KU database.", color=user.color)
        em.set_thumbnail(url=user.avatar_url)
        return em
    else:
        user_data = response['Item']

        em = discord.Embed(title=f"About {str(user)}", color=user.color)
        em.set_thumbnail(url=user.avatar_url)
        em.add_field(name="ชื่อ นามสกุล",
                     value=user_data['thainame'], inline=False)
        em.add_field(name="Forename Surname",
                     value=user_data['engname'], inline=False)
        em.add_field(name="Nickname", value=user_data['nickname'], inline=True)
        em.add_field(
            name="Gender", value="ชาย" if user_data['gender'] == "M" else "หญิง", inline=True)
        em.add_field(name="\u200b", value="\u200b", inline=True)
        em.add_field(name="Faculty", value=user_data['faculty'], inline=True)
        em.add_field(name="Department",
                     value=user_data['department'], inline=True)

        return em
