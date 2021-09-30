import os
from telethon import TelegramClient, events
from dotenv import load_dotenv, find_dotenv

from menu.controls import settings_buttons_inline, language_buttons_inline, \
    menu_button_inline
from menu.description import settings_msg, set_lang
from menu.settings import get_default_settings
from service import log_srv
from service.file_srv import is_file_valid, str_to_file, check_dir
# from api_service import ocr
from api_service.ocr.ocr_srv import ocr_space_file, ocr_response_data

logger = log_srv.get_logger(__name__)
load_dotenv(find_dotenv())

debug = True

# init default menu message
srv_settings = get_default_settings()
logger.info(f'default srv_settings: {str(srv_settings)}')
# init default menu language buttons
list_lang_btn_inline = language_buttons_inline()

BOT_TOKEN = os.getenv('BOT_TOKEN')
APP_API_ID = os.getenv('APP_API_ID')
APP_API_HASH = os.getenv('APP_API_HASH')
OCR_API_KEY = os.getenv('OCR_API_KEY')

bot = TelegramClient('bot', APP_API_ID, APP_API_HASH).start(bot_token=BOT_TOKEN)
# ocr_api = ocr.API(api_key=OCR_API_KEY)


@bot.on(events.NewMessage(pattern='/start|/settings'))
async def start(event):
    """Send a message when the command /start is issued"""
    try:
        await event.respond(
            settings_msg(srv_settings), buttons=settings_buttons_inline())

        if debug: logger.info('event.respond on /start')
    except Exception as inst_exception:
        logger.warning(inst_exception)


@bot.on(events.NewMessage)
async def rec_file(event):
    """receive file from user
       allowed only mime_type: application/pdf, image/png, image/jpeg,
       image/gif, image/bmp, image/tiff.
        The maximum length for a message is 35,000 bytes or 4,096 characters
    """
    # allowed_file_types = [
    # 'application/pdf', 'image/png', 'image/jpeg',
    # 'image/gif', 'image/bmp', 'image/tiff'
    # ]

    if debug: logger.info('event.NewMessage')
    # print(f"NewMessage event: {event}")
    if debug: logger.info(f"event.NewMessage event: {event}")

    event_msg = event.message

    # if event_msg.photo:
    #     if debug: logger.info(f'event_msg.photo: {event_msg.photo}')
    #     if event_msg.file:
    #         user_file = event_msg.file
    #         if debug: logger.info(f'event_msg.file: {event_msg.file}')
    #         if debug: logger.info(f'file.mime_type: {user_file.mime_type}')
    #         if debug: logger.info(f'file.name: {user_file.name}')
    #         if debug: logger.info(f'file.size: {str(user_file.size)}')
    #         # size in bytes of this file.

    if event_msg.document or event_msg.photo:
        if event_msg.document and debug:
            logger.info(f'document.mime_type: {event_msg.document.mime_type}')
        if event_msg.photo and debug:
            logger.info(f'event_msg.photo: {event_msg.photo}')

        if not is_file_valid(event_msg):
            await event.reply(
                f"Sorry, this file type cannot be processed"
                f"Only these types of files can be processed: "
                f"PDF, PNG, JPG(JPEG), BMP, TIF(TIFF), GIF."
                f"Other limits:"
                f"File size limit - 1 MB. PDF page limit - 3"
                f"Limit requests to API service - 500 calls/DAY."
            )

        else:
            await event.reply('Wait please. We process your data ....')

            if event_msg.file:
                user_file = event_msg.file
                if debug: logger.info(f'file.mime_type: {user_file.mime_type}')
                if debug: logger.info(f'file.name: {user_file.name}')
                if debug: logger.info(f'file.size: {str(user_file.size)}')

                check_dir('tmp')

                file_name = user_file.name if user_file.name else \
                    'user_file_name'
                user_file = await event_msg.download_media(
                    file='tmp/' + file_name)
                if debug: logger.info(f'File saved to: {str(user_file)}')

                # processing the file by service ocr api
                resp_ocr = ocr_space_file(
                    user_file,
                    language=srv_settings['lang']['code'],
                    isTable=srv_settings['isTable']['code']
                )
                if not resp_ocr:
                    await event.reply(
                        f"Oops! Something went wrong, try again")
                else:
                    data_ocr = ocr_response_data(resp_ocr)
                    if debug: logger.info(f"result ocr - ocr_code: {str(data_ocr['ocr_code'])}")

                    try:
                        os.remove(user_file)
                        if debug: logger.info(f'File remove {str(user_file)}')
                    except Exception as os_remove_exception:
                        logger.warning(os_remove_exception)

                    if data_ocr['ocr_exit_code'] not in [1, 4]:
                        if debug: logger.info(f"error result ocr code: {data_ocr['ocr_code']}")
                        await event.reply(
                            f"Oops! Something went wrong:\n"
                            f"{data_ocr['ocr_code']}"
                        )
                    else:
                        pars_text = data_ocr['parsed_text']
                        if debug: logger.info(
                            f'Length of parsed text {len(pars_text)} items'
                        )
                        if srv_settings['result']['code'] == 'file':

                            str_to_file(pars_text)
                            if debug: logger.info('reply by text file')

                            await event.respond(
                                file='tmp/ocr_text.txt',
                                message=(
                                    f"**{data_ocr['ocr_code']}**\n"
                                    f'**Parsing result in this file**'
                                )
                            )
                            os.remove('tmp/ocr_text.txt')
                        elif srv_settings['result']['code'] == 'message':
                            if debug: logger.info('reply by message with parsed text')
                            await event.reply(
                                f"**{data_ocr['ocr_code']}**\n"
                                f'**Parsed text:**\n'
                                f'\n'
                                f'{pars_text}'
                            )


@bot.on(events.CallbackQuery)
async def handle_callback_query(event: events.CallbackQuery.Event):

    logger.info(f'event.stringify: {str(event)}')
    # msg_id = event.original_update.msg_id
    # user_id = event.original_update.user_id
    cb_data = event.original_update.data
    logger.info(f'event cb_data: {str(cb_data)}')

    if 'check_limits' in str(cb_data):
        # logger.info('query cb cb_data: ' + str(cb_data))
        limits_msg = settings_msg(srv_settings, limits=True)
        # logger.info('query cb limits_msg: ' + limits_msg)
        await event.edit(limits_msg, buttons=menu_button_inline())
    if 'back_main_menu' in str(cb_data):
        msg = settings_msg(srv_settings)
        # logger.info('query cb msg: ' + msg)
        await event.edit(msg, buttons=settings_buttons_inline())
    elif 'set_lang' in str(cb_data):

        update_msg = settings_msg(srv_settings, lang=True)
        # logger.info('query cb update_msg: ' + update_msg)
        await event.edit(update_msg, buttons=list_lang_btn_inline)

    elif 'langcode_' in str(cb_data):

        lang_code = str(cb_data)[-4:-1]
        logger.info(f'query cb lang_code: {lang_code}')

        srv_settings['lang']['code'] = lang_code
        srv_settings['lang']['desc'] = set_lang[lang_code]

        logger.info(f'query cb settings: {str(srv_settings)}')
        update_msg = settings_msg(srv_settings,  lang=True)
        # logger.info('query cb update_msg: ' + update_msg)
        await event.edit(update_msg, buttons=list_lang_btn_inline)

    elif 'table' in str(cb_data):
        srv_settings['isTable']['code'] = True
        srv_settings['isTable']['desc'] = 'table'
        srv_settings['update'] = True
        update_msg = settings_msg(srv_settings)
        # logger.info('query cb update_msg: ' + update_msg)
        await event.edit(
            update_msg,
            buttons=settings_buttons_inline(format_txt='plain')
        )

    elif 'plain' in str(cb_data):
        srv_settings['isTable']['code'] = False
        srv_settings['isTable']['desc'] = 'plain'
        srv_settings['update'] = True
        update_msg = settings_msg(srv_settings)
        # logger.info('query cb update_msg: ' + update_msg)
        await event.edit(
            update_msg,
            buttons=settings_buttons_inline(format_txt='table')
        )

    elif 'file' in str(cb_data):
        srv_settings['result']['code'] = 'file'
        srv_settings['result']['desc'] = 'file'
        srv_settings['update'] = True
        update_msg = settings_msg(srv_settings)
        # logger.info('query cb update_msg: ' + update_msg)
        await event.edit(
            update_msg,
            buttons=settings_buttons_inline(result='message')
        )

    elif 'message' in str(cb_data):
        srv_settings['result']['code'] = 'message'
        srv_settings['result']['desc'] = 'message'
        srv_settings['update'] = True
        update_msg = settings_msg(srv_settings)
        # logger.info('query cb update_msg: ' + update_msg)
        await event.edit(
            update_msg,
            buttons=settings_buttons_inline(result='file')
        )
    logger.info(f'query cb settings after: {str(srv_settings)}')


@bot.on(events.Raw)
async def handler(update):
    # Print all incoming updates
    # logger.info('update.stringify: ' + update.stringify())
    pass


def main():
    """Start the bot."""
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
