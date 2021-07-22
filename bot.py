'''
© All rights reserved by Mrvishal2k2

Kangers dont f*ckin kang this !!!
Should have to give credits 😏 else f***off 
This is only for personal use Dont use this for ur bot channel business 😂
Thanks to Mahesh Malekar for his Gplinks Bot !!
'''

# Bitly Bot

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import os

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from pyshorteners import Shortener
from config import *


SHORTLINKBOT = Client('ShortlinkBot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)
                      

@SHORTLINKBOT.on_message(filters.command(['start']))
async def start(_, update):
    await _.send_message(
            BIN_CHANNEL,
            f"**New User Joined:** \n\nUser [{update.from_user.first_name}](tg://user?id={update.from_user.id}) started Bot!!"
        )
    if UPDATES_CHANNEL:
        try:
            user = await _.get_chat_member(UPDATES_CHANNEL, update.chat.id)
            if user.status == "kicked":
               await update.reply_text(" Sorry, You are **B A N N E D**")
               return
        except UserNotParticipant:
            # await update.reply_text(f"Join @{update_channel} To Use Me")
            await update.reply_text(
                text="**Please Join My Update Channel Before Using Me..**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join Updates Channel", url=f"https://t.me/NewBotz")],
                    [ InlineKeyboardButton(text="Refresh", url=f"https://t.me/NewURLShortenBot?start")]
              ])
            )
            return
        else:
            #markup = InlineKeyboardMarkup([[InlineKeyboardButton("My Owner", url=f"https://t.me/{OWNER}"),
                                                #InlineKeyboardMaButton("Share", url="tg://msg?text=Hai%20Friend%2C%0D%0AAm%20Introducing%20a%20Powerful%20%2A%2AURL%20Shortener%20Bot%2A%2A%20for%20Free.%0D%0A%2A%2ABot%20Link%2A%2A%20%3A%20%40NewURLShortenBot")]])
            markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("My Owner", url=f"https://t.me/{OWNER}"),
                        InlineKeyboardButton("Share", url="tg://msg?text=Hai%20Friend%2C%0D%0AAm%20Introducing%20a%20Powerful%20%2A%2AURL%20Shortener%20Bot%2A%2A%20for%20Free.%0D%0A%2A%2ABot%20Link%2A%2A%20%3A%20%40NewURLShortenBot")
                    ]
                ]
            )
            await update.reply(
                f"**Hi {update.chat.first_name}!**\n\n"
                "I'm shortlink bot. Just send me link and get adsless short link",
                reply_markup=markup,
                quote=True)

@SHORTLINKBOT.on_message(filters.regex(r'https?://[^\s]+'))
async def link_handler(_, update):
    url = update.text
    log_msg = None
    log_msg = await update.forward(chat_id=BIN_CHANNEL)
    message_url = await update.reply_text(
        text="`Generating...`",
        disable_web_page_preview=True,
        quote=True
    )
    link = update.matches[0].group(0)
    shortened_url, Err = get_shortlink(link)
    if shortened_url is None:
        message = f"Something went wrong \n{Err}"
        await log_msg.reply_text(f'**User Name:** {update.from_user.mention(style="md")}\n\n**User Id:** `{update.from_user.id}`\n\n**Shortened Link :** Failed\n\nCheck logs for error')
        await update.reply(message, quote=True)
        return
    message = f"Here is your shortlink\n\n`{shortened_url}`"
    #markup = InlineKeyboardMarkup([[InlineKeyboardButton("Link 🔗", url=shortened_url)]])
    # i don't think this bot with get sending message error so no need of exceptions
    await log_msg.reply_text(text=f"**User Name :** [{update.from_user.first_name}](tg://user?id={update.from_user.id})\n\n**User Id :** `{update.from_user.id}`\n\n**Shortened Link :** {shortened_url}", disable_web_page_preview=True, parse_mode="Markdown", quote=True)
    await update.edit_text(text=message, quote=True)
      
def get_shortlink(url):
    shortened_url = None
    Err = None
    try:
       if BITLY_KEY:
           ''' Bittly Shorten'''
           s = Shortener(api_key=BITLY_KEY)
           shortened_url = s.bitly.short(url)
       else:
           ''' Da.gd : I prefer this '''
           s = Shortener()
           shortened_url = s.dagd.short(url)
    except Exception as error:
        Err = f"#ERROR: {error}"
        log.info(Err)
    return shortened_url,Err
        
      
if __name__ == "__main__" :
    log.info(">>Bot-Started<<")
    SHORTLINKBOT.run()
