from json import loads as jloads
from aiohttp import ClientSession
from bot import Var, bot, ffQueue
from bot.core.text_utils import TextEditor
from bot.core.reporter import rep

# Initialize a variable to store the last message ID
last_message_id = None

async def upcoming_animes():
    global last_message_id  # Use the global variable to keep track of the last message ID
    if Var.SEND_SCHEDULE:
        try:
            async with ClientSession() as ses:
                res = await ses.get("https://subsplease.org/api/?f=schedule&h=true&tz=Asia/Kolkata")
                aniContent = jloads(await res.text())["schedule"]
            
            text = "<b>📆 Today's Anime Releases Schedule</b>\n\n"
            for i in aniContent:
                aname = TextEditor(i["title"])
                await aname.load_anilist()
                text += f''' <a href="https://subsplease.org/shows/{i['page']}">{aname.adata.get('title', {}).get('english') or i['title']}</a>\n    • <b>Time</b> : {i["time"]} hrs\n\n'''
            
            sch_list = text + "<b>⏰ Current TimeZone :</b> <code>IST (UTC +5:30)</code>"
            
            # Delete the previous message if it exists
            if last_message_id:
                try:
                    await bot.delete_message(Var.MAIN_CHANNEL, last_message_id)
                except Exception as delete_error:
                    print(f"Failed to delete the previous message: {delete_error}")

            # Send the new message and store its ID
            TD_SCHR = await bot.send_message(Var.MAIN_CHANNEL, sch_list)
            last_message_id = TD_SCHR.message_id  # Store the ID of the newly sent message
            
        except Exception as e:
            # Handle the exception (e.g., log it)
            print(f"An error occurred: {e}")
