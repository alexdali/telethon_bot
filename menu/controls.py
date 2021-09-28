from telethon import Button
from service import log_srv

logger = log_srv.get_logger(__name__)


set_lang = {
    'rus': 'Russian',
    'eng': 'English',
    'ara': 'Arabic',
    'bul': 'Bulgarian',
    'chs': 'China(sm)',
    'cht': 'China(tr)',
    'hrv': 'Croatian',
    'cze': 'Czech',
    'dan': 'Danish',
    'dut': 'Dutch',
    'fin': 'Finnish',
    'fre': 'French',
    'ger': 'German',
    'gre': 'Greek',
    'hun': 'Hungarian',
    'kor': 'Korean',
    'ita': 'Italian',
    'jpn': 'Japanese',
    'pol': 'Polish',
    'por': 'Portuguese',
    'slv': 'Slovenian',
    'spa': 'Spanish',
    'swe': 'Swedish',
    'tur': 'Turkish',
}

"""
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None, back_menu_button=False):
    'Build menu'
    logger.info('build menu')

    back_menu_button = [Button.text('Back to main menu', single_use=True, resize=True)]

    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    if back_menu_button:
        menu.append(back_menu_button)
    return menu
"""

#
# def settings_msg(data_set=None, default=True, lang=False, limits=False):
#     """
#     generate a message about settings
#     """
#     update_flag = data_set['update']
#
#     logger.info('settings_msg arg: default={}, lang={}, limits={} update_flag={}'.format(
#         default, lang, limits, update_flag))
#
#     def_str = 'Choose preferred language and content format in file for better text recognition.\nDefault '
#     lang_str = 'Choose preferred language.\nDefault '
#     update_str = 'Your '
#     update_lang_str = 'Choose preferred language.\nYour '
#
#     settings_str = 'settings: language - {}, content format - {} text, processing result - as {}.'.format(
#         data_set['lang']['desc'], data_set['isTable']['desc'], data_set['result']['desc'])
#
#     limits_str = 'Only the following types of files can be processed: PDF, PNG, JPG(JPEG), BMP, TIF(TIFF), GIF.\nOther limits:\nFile size limit - 1 MB. PDF page limit - 3\nLimit requests to API service - 500 calls/day.'
#
#     # if default:
#     if not lang and not update_flag and not limits:
#         msg = def_str + settings_str
#         logger.info('settings_msg by not update_flag: {}'.format(msg))
#
#     if lang and not update_flag and not limits:
#         msg = lang_str + settings_str
#         logger.info('settings_msg by lang and not update_flag: {}'.format(msg))
#
#     if lang and update_flag and not limits:
#         msg = update_lang_str + settings_str
#         logger.info('settings_msg by lang: {}'.format(msg))
#
#     if not lang and update_flag and not limits:
#         msg = update_str + settings_str
#         logger.info('settings_msg by ELSE: {}'.format(msg))
#     if limits:
#         msg = limits_str
#         logger.info('settings_msg by limits: {}'.format(msg))
#
#     return msg


def settings_buttons_inline(format_txt='table', result='file'):
    """
    generate key buttons about settings
    """

    format_btn_text = 'Is content format a {} text?'.format(format_txt)
    result_btn_text = 'Processing result as a {}?'.format(result)

    buttons_inline = [
        [Button.inline('Choose language', data='set_lang')],
        [Button.inline(format_btn_text, data=format_txt)],
        [Button.inline(result_btn_text, data=result)],
        [Button.inline("Check out the service's limits", data='check_limits')],
    ]

    return buttons_inline


def language_buttons_inline():
    """
    docstring
    """
    list_buttons_inline = []

    for key, value in set_lang.items():
        btn = Button.inline(value, data='langcode_' + key)
        # logger.info('btn: ' + str(btn))
        list_buttons_inline.append(btn)

    col_btn = 4
    rows_buttons = [list_buttons_inline[i:i + col_btn]
                    for i in range(0, len(list_buttons_inline), col_btn)]

    footer_button = Button.inline('Back to main menu', data='back_main_menu')

    rows_buttons.append([footer_button])
    # logger.info('buttons_inline: ' + str(rows_buttons))

    return rows_buttons


def menu_button_inline():
    """
    generate key button about main menu
    """

    footer_button = Button.inline('Main menu', data='back_main_menu')

    logger.info('footer_button: {!s}'.format(footer_button))

    return [footer_button]
