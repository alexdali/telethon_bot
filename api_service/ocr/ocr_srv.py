import os
import requests
import json
from dotenv import load_dotenv
from service import log_srv

load_dotenv()

logger = log_srv.get_logger(__name__)
OCR_API_KEY = os.getenv('OCR_API_KEY')

# url_api = 'https://api.ocr.space/parse/image'
url_api = 'http://api.ocr.space/parse/image'


def ocr_space_file(filename, language='eng', isTable=False, ocrengine=1):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :param ocrengine: OCR API offers two different
                    OCR engine: 1 or 2.
                    Defaults to 1.
    :return: Result in JSON format.
    """
    logger.info('ocr_space_file args: language={}, isTable={}'.format(
        language, isTable))

    payload = {
        'apikey': OCR_API_KEY,
        'language': language,
        'isTable': isTable,
        'scale': True,
        'OCREngine': ocrengine,
    }

    try:
        logger.info('file {!s} exist: {!s}'.format(
            filename, os.path.isfile(filename)))
    except OSError:
        logger.warning(OSError)

    res=None

    try:
        with open(filename, 'rb') as f:
            r = requests.post(url_api, files={filename: f}, data=payload)
            logger.info(f'response.status_code: {r.status_code}')
            r.raise_for_status()
    except requests.exceptions.HTTPError as res_HTTPError:
        logger.warning(f'res_HTTPError: {str(res_HTTPError)}')
    except requests.exceptions.ConnectionError as res_ConnectionError:
        logger.warning(f'res_ConnectionError: {str(res_ConnectionError)}')
    finally:
        logger.info('try return response ocr api')
        res = r.content.decode()

    return res


def ocr_space_url(url, overlay=False,  language='eng', isTable=False,
                  ocrengine=1):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :param ocrengine: OCR API offers two different
                    OCR engine: 1 or 2.
                    Defaults to 1.
    :return: Result in JSON format.
    """

    payload = {
        'url': url,
        'apikey': OCR_API_KEY,
        'language': language,
        'isTable': isTable,
        'scale': True,
        'OCREngine': ocrengine,
    }

    r = requests.post(url_api, data=payload)
    logger.info('try return response ocr api')
    return r.content.decode()


def ocr_response_data(response_json):
    """
    check value response of ocr service
    """

    logger.info(f'input response ocr: {str(response_json)}')

    response_data = json.loads(response_json)
    # logger.info('proccesing response_data[OCRExitCode]: ' + str(response_data))
    logger.info(f'proccesing response_data: {response_data}')
    # logger.info('proccesing response_data[OCRExitCode]: ' + str(response_data['OCRExitCode']))
    logger.info(f"proccesing response_data[OCRExitCode]: {response_data['OCRExitCode']}")

    if response_data['OCRExitCode'] == 1:

        data_ocr = {
            'ocr_code': 'Parsed Successfully',
            'ocr_exit_code': response_data['OCRExitCode'],
            'fileparse_exit_code': response_data['ParsedResults'][0]['FileParseExitCode'],
            'is_errored_onprocessing': response_data['IsErroredOnProcessing'],
            'processing_time': response_data['ProcessingTimeInMilliseconds'],
            'error_message': response_data['ParsedResults'][0]['ErrorMessage'],
            'error_details': response_data['ParsedResults'][0]['ErrorDetails'],
            'parsed_text': response_data['ParsedResults'][0]['ParsedText'],
        }

        # if data_ocr['ocr_exit_code'] == 2:
        #     data_ocr['ocr_code'] = 'Parsed Partially (Only few pages out of all the pages parsed successfully)'
        # if data_ocr['ocr_exit_code'] == 3:
        #     data_ocr['ocr_code'] = 'Image / All the PDF pages failed parsing (This happens mainly because the OCR engine fails to parse an image)'
        # if data_ocr['ocr_exit_code'] >= 4:
        #     data_ocr['ocr_code'] = 'Error occurred when attempting to parse'
        # if data_ocr['error_message'] == 'limit reached':
        if ('limit reached' in data_ocr['error_message']) or ('limit reached' in data_ocr['error_details']):
            data_ocr['ocr_code'] = 'limit calls/DAY reached'
    else:
        data_ocr = {
            'ocr_code': 'Error occurred when attempting to parse',
            'ocr_exit_code': response_data['OCRExitCode'],
            'is_errored_onprocessing': response_data['IsErroredOnProcessing'],
            'processing_time': response_data['ProcessingTimeInMilliseconds'],
            'error_message': response_data['ErrorMessage'],
            'parsed_text': '',
        }

    logger.info(f"proccesing data response ocr - ocr_code: {str(data_ocr['ocr_code'])}")
    return data_ocr


if __name__ == "__main__":
    # print(ocr_space_file(filename='E:/temp/ru1.png', language='rus'))
    test = ocr_response_data(ocr_space_url(
        url='http://dl.a9t9.com/ocrbenchmark/eng.png'))

    for key, value in test.items():
        print('key: {}, value: {}'.format(key, value))
