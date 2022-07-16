# -*- coding: utf-8 -*-
import tkinter as tk
from PIL import Image, ImageTk
import telethon
import asyncio
import json
import python_socks
import helpers as hp
import models
import time
from typing import Optional
from telethon import TelegramClient
from telethon import events

sessions = []

proxy = models.get_proxy()
get_sessions = hp.get_sessions()

class AsyncTk(tk.Tk):
	def __init__(self):
		super().__init__()
		self.protocol("WM_DELETE_WINDOW", self.on_close)

	def on_close(self):
		self.done = True

	async def updater(self):
		self.done = False
		while not self.done:
			self.update()
			await asyncio.sleep(0.05)

	def mainloop(self):
		asyncio.get_event_loop().run_until_complete(self.updater())

async def parse_sessions(request):
	for i in range(len(get_sessions)):
		with open(f'./ss/{get_sessions[i]}.json', 'r', encoding='utf-8') as file:
			get_data = json.load(file)
			TelegClient = TelegramClient(
				session=f'./ss/{get_sessions[i]}.session', 
				api_id=get_data['app_id'],
				api_hash=get_data['app_hash'],
				system_version=get_data['sdk'],
				app_version=get_data['app_version'],
				device_model=get_data['device'],
				lang_code=get_data['lang_pack'], 
				proxy=proxy,
				connection_retries=3,
				request_retries=3,
				retry_delay=1,
				system_lang_code=get_data['system_lang_pack'],
				auto_reconnect=True,
				timeout=30
			)
			sessions.append(TelegClient)
	await account_connect(client=sessions[0], request=request)

async def account_connect(client, request):
	try:
		await client.connect()
	except:
		pass
	await client.send_message('https://t.me/sber_rudalle_xl_bot', '/start')
	await client.send_message('https://t.me/sber_rudalle_xl_bot', f'{request}')
	@client.on(events.NewMessage(pattern=f'Изображение сгенерировано моделью ruDALL-E от Сбера по запросу "{request}"'))
	async def handler(event):
		download_photo = await event.download_media(file="photos/output")
		pil_image = Image.open(download_photo)
		image = ImageTk.PhotoImage(pil_image)
		name_label.config(image=image, text='')
		name_label.image = image
		button['state'] = 'normal'

def load_image():
	button['state'] = 'disabled'
	name_label['text'] = 'Генерирую...'
	asyncio.ensure_future(parse_sessions(request=request.get()))

root = AsyncTk()
root.title("Генератор картинок")

request = tk.StringVar()
 
name_label = tk.Label(text="Введите запрос")
name_label.pack()
 
name_entry = tk.Entry(textvariable=request)
name_entry.pack()

button = tk.Button(text="Сгенерировать", command=load_image)
button.pack()

root.mainloop()