import asyncio
from pyrogram import Client  # type: ignore
from pyrogram.types import Message
from exported_acc_data.handling import get_all_chats
from config import API_ID, API_HASH, MY_ID, ADMIN_ID
from custom_logger import (
    logger,
    log_exception,
)

my_id, admin_id = MY_ID, ADMIN_ID
api_id = API_ID
api_hash = API_HASH
app: Client = Client("linaff", api_id, api_hash)

chat_ids = get_all_chats()
status = None

@app.on_message()
async def msg_handler(client, message: Message):
    """Watching the messages and invoking functions when a specific command is sent by a specific account"""
    if not message.chat.id in admin_id:
        return
    else:
        global status
        
        # Handle a new ad
        if status == "new_ad":
            status = None
            try:
                # Send received ad to saved messages and save it id in a txt
                logger.info("Received a new ad")                
                forwarded_msg =await app.forward_messages(
                    chat_id=my_id,
                    from_chat_id=message.chat.id,
                    message_ids=message.id,
                )                
                with open("ad_msg_id.txt", "w") as ad_saver:
                    ad_saver.write(str(forwarded_msg.id))  # type: ignore
                await app.send_message(my_id, "New ad message received")

                await asyncio.sleep(2)
                await app.send_message(message.chat.id, "Your ad was successfully saved")
                logger.debug("The ad was updated")
            except Exception as e:
                log_txt = log_exception(e)
                logger.warning(log_txt)
                await app.send_message(message.chat.id, "An error occured while saving. The ad wasn't saved")
                
        elif message.text == "newad":
            await asyncio.sleep(1)
            await app.send_message(chat_id=message.chat.id, text="Please send a new ad")              
            status = "new_ad"
        
        elif message.text == "sendads":
            logger.info("Sending ads to chats...")
            try:
                await send_ads()
                logger.debug("Ad was sent successfully")
                await asyncio.sleep(2)
                await app.send_message(message.chat.id, "The ad was sent successfully")                
            except Exception as exc:
                log_txt =log_exception(exc)                
                logger.warning(log_txt)
                await asyncio.sleep(2)
                await app.send_message(message.chat.id, "An error occurred while sending ads")


async def send_ads():
    with open("ad_msg_id.txt", "r") as ad_file:
        ad_id = int(ad_file.read().strip())
    ad_msg = await app.get_messages(my_id, ad_id)
    for chatid in chat_ids:        
        await app.forward_messages(chat_id=chatid, from_chat_id=my_id, message_ids=ad_msg.id) # type: ignore
        await asyncio.sleep(1)


def run_bot():
    logger.info("Bot started successfully")
    app.run()


if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        log_txt = log_exception(e)
        logger.critical(log_txt)
    finally:
        logger.info("Bot shutdown complete")
