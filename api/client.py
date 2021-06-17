import os
from dotenv import load_dotenv
import discord

load_dotenv(override=True)

client = discord.Client()
vcn_channel = 833004981388443678
is_notification = True


@client.event
async def on_message(message):
    global vcn_channel
    global is_notification
    if message.author == client.user:
        return

    if message.content.split()[0] == '/help':
        await message.channel.send("/vcn_help ： VC通知コマンド一覧を表示 \n")

    if message.content.split()[0] == '/vcn_help':
        await message.channel.send("/vcn_help ： VC通知コマンド一覧を表示 \n" +
                                   "/vcn_stop ： VC通知を停止 \n" +
                                   "/vcn_start ： VC通知を開始 \n" +
                                   "/vcn_change_channel ： VC通知チャンネルを変更 \n")

    if message.content.split()[0] == '/vcn_stop':
        if is_notification == True:
            is_notification = False
        print(is_notification)
        await message.channel.send('VC通知を停止しました')

    if message.content.split()[0] == '/vcn_start':
        if is_notification == False:
            is_notification = True
        print(is_notification)
        await message.channel.send('VC通知を開始しました')

    if message.content.split()[0] == '/vcn_change_channel':
        vcn_channel = message.channel.id
        await message.channel.send(f'VC通知チャンネルを#{message.channel}に変更しました。')


@client.event
async def on_voice_state_update(member, before, after):
    global is_notification
    global vcn_channel
    if vcn_channel == None:
        vcn_channel = client.guilds[0].text_channels[0].id
    alert_channel = client.get_channel(vcn_channel)
    if is_notification == True:
        if before.channel is None:
            embed = discord.Embed(
                title=f"【VC入室通知】", description=f"{member.nick or member.name}が {after.channel.name} に参加しました", color=0xff0000)
            embed.set_thumbnail(url=member.avatar_url)
            await alert_channel.send(embed=embed)
        elif after.channel is None:
            embed = discord.Embed(
                title=f"【VC退出通知】", description=f"{member.nick or member.name}が {before.channel.name} から抜けました", color=0xff0000,)
            embed.set_thumbnail(url=member.avatar_url)
            await alert_channel.send(embed=embed)

client.run(os.environ.get("DISCORD_TOKEN"))
