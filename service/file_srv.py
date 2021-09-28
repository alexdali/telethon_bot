import os
from .log_srv import get_logger

logger = get_logger(__name__)


def str_to_file(ocr_value):
    """
    open new file,
    write the ocr result to it
    and return it
    """
    logger.info('str_to_file')

    try:
        with open('tmp/ocr_text.txt', 'tw', encoding='utf-8') as f:
            f.write(ocr_value)

        if os.path.isfile('tmp/ocr_text.txt'):
            logger.info('ocr result file exist: tmp/ocr_text.txt')

        return 'tmp/ocr_text.txt'

    except Exception as file_exception:
        logger.warning(file_exception)


def check_dir(path):
    """
    check if directory exists for temporary files
    if not then create a directory
    """
    # cur_dir = os.getcwd()
    # path_dir = os.path.join(cur_dir, path)

    try:
        os.makedirs(path, exist_ok = True)
    except OSError:
        logger.warning(OSError)
        logger.info("Creation of the directory %s failed" % path)
    else:
        logger.info("Successfully created the directory %s " % path)


def is_file_valid(event_msg):
    """
    check the file for service restrictions
    """
    allowed_file_types = ['application/pdf', 'image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/tiff']

    file_type = False
    file_size = False

    user_file = event_msg.file

    logger.info('file.name: ' + user_file.name)
    logger.info('file.size: ' + str(user_file.size)) #size in bytes of this file.

    # logger.info('allowed_file_types index: ' + str(allowed_file_types.index(user_file.mime_type)))

    if user_file.mime_type in allowed_file_types:
        logger.info('user_file.mime_type in allowed_file_types: ' + user_file.mime_type)
        file_type = True

    if user_file.size <= 1048576:
        file_size = True

    logger.info('file_type: {!s} and file_size: {!s}'.format(file_type, file_size))

    if file_type and file_size:
        return True
    # else:
    #     return False