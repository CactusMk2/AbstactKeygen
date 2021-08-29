from json import loads, dump
from config import client_ids_file, SESSION_NAME, HOST
import os
import sqlite3


def error(text, clerror=True):
	if clerror:
		try:
			client.disconnect()
			os.remove(SESSION_NAME+".session")
		except:
			print("ENABLE TO REMOVE SESSION FILE, REMOVE IT MANUALY")
		print("Connection error", text)
	else:
		print(text)
	input("Hit enter to exit.")
	exit()


if not os.path.isfile(client_ids_file):
	error("NO CLIENT CONFIGURATION FILE FOUND")
try:
	with open(client_ids_file,"rb") as f: json_data = f.read()
	client_configuration = loads(json_data)
except:
	error("ERROR WHILE READING CLIENT CONFIGURATION FILE")



if not (API_ID := client_configuration.get("API_ID", False)):
	try:
		API_ID = int(input("API_ID was not found\nEnter your telergam app id: "))
	except:
		error("Invalid type of id")
	client_configuration["API_ID"] = API_ID
	with open(client_ids_file, "w") as f:
			dump(client_configuration, f)

if not (API_HASH := client_configuration.get("API_HASH",False)):
	API_HASH = input("API_HASH was not found\nEnter your telergam app hash: ")

	client_configuration["API_HASH"] = API_HASH
	with open(client_ids_file, "w") as f:
			dump(client_configuration, f)

if not (phone := client_configuration.get("phone",False)):
	phone = input("please enter your phone number: ")



try:
	from telethon import TelegramClient
	from telethon.errors.rpcerrorlist import FloodWaitError
	client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
	client.start(phone)
	if not client.is_connected():
		raise(OSError())


except FloodWaitError:
	error("FLOOD CONTROL, WAIT A WHILE AND THEN TRY AGAIN")
except:
	error("ERROR WHILE TRING TO CONNECT")
else:
	error("Script is completed", clerror=False)

error("If you see this message that means something went wrong.", clerror=False)
