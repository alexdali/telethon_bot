<h3 align="center">OCR Bot for Telegram</h3>

<div align="center">

![Language](https://img.shields.io/badge/Python-3.7-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
[![wakatime](https://wakatime.com/badge/github/alexdali/py_ocr_bot.svg)](https://wakatime.com/badge/github/alexdali/py_ocr_bot)
</div>


---

<p align="center"> 🤖 Telegram bot that recognizes text in images and PDF files
    <br>
   <b>Use it live here: https://t.me/text_from_image_bot</b>
</p>

## 📝 Table of Contents
+ [About](#about)
+ [Demo / Working](#demo)
+ [How it works](#working)
+ [Usage](#usage)
+ [Roadmap](#roadmap)
+ [Built Using](#built_using)
+ [Authors](#authors)
+ [License](#license)
+ [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>
A simple and convenient telegram bot that extracts text from images or PDFs after the user uploads these files to the bot. The result of processing files by the text recognition service can be obtained in one of the following ways: message or text file.

## 🎥 Demo / Working <a name = "demo"></a>

ocr in pdf files | ocr in image files
:-: | :-:
<video src='https://user-images.githubusercontent.com/7926403/135529546-12eee5bb-6bbd-41d7-b78a-1ed829f6abe1.mp4' width=180/> | <video src='https://user-images.githubusercontent.com/7926403/135530178-6d61cbad-1a04-419f-9083-1762f3846c0c.mp4' width=180/>


[//]: # "https://user-images.githubusercontent.com/7926403/135529546-12eee5bb-6bbd-41d7-b78a-1ed829f6abe1.mp4"

[//]: # "https://user-images.githubusercontent.com/7926403/135530178-6d61cbad-1a04-419f-9083-1762f3846c0c.mp4"



## 💭 How it works <a name = "working"></a>

The bot uses the Telegram API to communicate with the user and send messages to them. After the user starts the bot by entering the "/start " command, it is ready to accept the file for processing.

The user is provided with default text recognition settings: the text language is English, the content format is plain text, and the recognition result is displayed as a message. You can change these settings using the inline menu buttons. Since the bot uses a free text recognition service, there are restrictions that can be found by clicking on the button: "Limits".

As soon as the bot receives a valid file from the user, it uses the OCR API https://ocr.space/ to get the result of the text recognition service in JSON format. This information is then converted into a message that is sent to the user using the Telegram API.

Current limitations of the free OCR API service:
- supported file formats: PDF, PNG, JPG( JPEG), BMP, TIF (TIFF), GIF
- Maximum file size-1 MB, maximum number of pages in a PDF file-3
- the limit on the number of requests to the API service is 500 requests / day.

The bot uses the Telethon python library to interact with the Telegram API.

The entire bot is written in Python 3.7

## 🎈 Usage <a name = "usage"></a>

To use the bot, type:
```
/start
```
You can change the text recognition settings: text language (24 languages are supported), content format - plain text or table, recognition result - message or text file. You can change these settings using the inline menu buttons.
You can change these settings during use by calling the command: 
```
/settings
```

Please note: The bot could be slow sometimes as it depends on OCR.space's API requests.

## ⛏️ Roadmap <a name = "roadmap"></a>
1. Add the ability to process files by URL
2. ~~Add warning when exceeding the page limit in pdf file~~ DONE
3. Add the ability to process text over 4096 characters
4. Anti-flood protection
5. Refactoring

## ⛏️ Built Using <a name = "built_using"></a>
+ [Telethon](https://github.com/LonamiWebs/Telethon) - Telethon is an asyncio Python 3 MTProto library to interact with Telegram's API as a user or through a bot account (bot API alternative).
+ [ocr.space](https://ocr.space/) - Free Online OCR - Convert images and PDF to text
+ Logging - Logging library for debugging

## ✍️ Authors <a name = "authors"></a>
+ Alexey Tasbauov

## 📗 License <a name = "license"></a>
This project is licensed under the MIT License - see the LICENSE file for more details.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>
+ Thank you to Telethon for providing the python wrapper!
