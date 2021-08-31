import pdb
from config import *
from gui import Root
from datetime import datetime, timedelta
log = startlog()
log.info(str(datetime.now())+" "+"Starting GUI")
root = Root('icon.png')
root.title("HideMy.name Keygen")
root.setupGUI()
root.setNewKey("Generating...","Time will be displayed when\n generation will be completed",False)
root.flip()


log.debug("Importing libs")
import sqlite3
import utils
from random import randint
from json import loads
from os.path import isfile

def stop_error(logerror="Error", brief="Error", error_text="Error"):
	root.reg_btn.configure(command=exit)
	log.critical(logerror)
	root.setNewKey(brief,error_text,False)
	while True:
		root.flip()

if not isfile(client_ids_file):
	stop_error(
		"No client configuration file found",
		"No client config",
		f"No client configuration file found: \n{client_ids_file}"
		)
else:
	log.info(str(datetime.now())+" "+"Using client configuration")

try: 
	with open(client_ids_file,"rb") as f: json_data = f.read()
except: stop_error("Error while opening configuration file file","File error","Enable to open configuration file")
try: client_configuration = loads(json_data)
except: stop_error("Error while parsing json file","File error","Enable to read configuration file")

API_ID = client_configuration.get("API_ID", False)
API_HASH = client_configuration.get("API_HASH",False)
if not API_HASH:
	stop_error("API_HASH was not found", "configuration error", "No client app hash was provided")
if not API_ID:
	stop_error("API_ID was not found", "configuration error", "No client app ID was provided")


async def get_messages(client):
	log.info(str(datetime.now())+" "+"Getting messages")
	global data_list
	data_list = []

	#getting raw message text
	async for message in client.iter_messages(HOST):
		if message.text.startswith(STARTS_WITH):
			raw_message_text = message.text
			message_date = datetime.timestamp(message.date)
			break
	else:
		stop_error("last message is outdated","Server Error","Keys are not available\nOn the server now")

	#get keys from message
	keys_list = await utils.parse_keys(raw_message_text)
	now_time = datetime.timestamp(datetime.now())
	for key in keys_list:
		data_list.append((key, False, message_date, message.id, int(now_time)))
	root.generating = False



async def check(client):
	await client.connect()
	try:
		await client.sign_in()
	except:
		stop_error("Session is not up","Session error","Session is not associated\nwith any accounts")



def update_keys():
	try:
		with sqlite3.connect(SESSION_NAME+".session") as db:
			cur = db.cursor()
			cur.execute(""" SELECT * FROM sessions """)
			sess = cur.fetchall()
		if not len(sess):
			stop_error("Session file is not connected to any account","Connect account","Connect telergam account\nin order to get updates")
	except sqlite3.OperationalError:
		stop_error("Session file is not connected to any account","Connect error","Connection to account failed\nConnect account again")
	except:
		stop_error("Error while checking session file","Error","Restart or reinstall the program")


	from telethon import TelegramClient
	client = TelegramClient(SESSION_NAME, API_ID, API_HASH, timeout=5)
	client.loop.run_until_complete(check(client))
	try:
		with client:
			client.loop.run_until_complete(get_messages(client))
	except:
		stop_error("error while using client","Server/client error","Enable to get keys list\n form the server")


def regenerate():
	root.setNewKey("Generating...","Time will be displayed when\n generation will be completed",False)
	root.flip()
	root.generating = True
	log.info(str(datetime.now())+" "+"Regenerating a key")
	random_id = randint(0,len(keys_list)-1)
	random_key = keys_list[random_id]
	difference = datetime.now() - datetime.fromtimestamp(msgdate_list[random_id])
	expiration_time = timedelta(days=1)
	try:
		with sqlite3.connect(DB_NAME) as db:
			cur = db.cursor()
			cur.execute(f"""UPDATE keys SET shown = 1 where key_int = {random_key}""")
	except:
		log.error("Enable to setup connection to db")
	get_keyslist_from_db()
	root.setNewKey(random_key, utils.strfdelta(expiration_time - difference))
	root.generating = False


def get_keyslist_from_db():
	log.info(str(datetime.now())+" "+"Getting keylist")
	global keys_list
	global msgdate_list
	keys_list = []
	msgdate_list = []
	with sqlite3.connect(DB_NAME) as db:
		cur = db.cursor()
		expiration_date = datetime.timestamp(datetime.now() - timedelta(days=msg_lasts))
		update_expiration_date = datetime.timestamp(datetime.now() - timedelta(hours=update_interval))
		log.debug("connected to db")
		try:
			cur.execute(f""" SELECT * FROM keys WHERE datestamp > {expiration_date} AND last_update > {update_expiration_date} AND shown = 0""")
			for datapart in cur:
				keys_list.append(datapart[1])
				msgdate_list.append(datapart[3])
			if keys_list == []:
				log.info(str(datetime.now())+" "+"keys in db are outdated")
				raise(sqlite3.OperationalError)
		except sqlite3.OperationalError:
			log.info(str(datetime.now())+" "+"updating keys")
			update_keys()
			cur.execute(""" CREATE TABLE IF NOT EXISTS keys (id INTEGER PRIMARY KEY, key_int INTEGER NOT NULL, shown BOOL NOT NULL, datestamp INTEGER NOT NULL, message_id INTEGER NOT NULL, last_update INTEGER NOT NULL) """)
			cur.executemany(f""" INSERT INTO keys(key_int, shown, datestamp, message_id, last_update) VALUES(?,?,?,?,?) """, data_list)
			cur.execute(f""" SELECT * FROM keys WHERE datestamp > {expiration_date} AND last_update > {update_expiration_date} AND shown = 0""")
			for datapart in cur:
				keys_list.append(datapart[1])
				msgdate_list.append(datapart[3])
			if keys_list == []:
				stop_error("last message is outdated","Server Error","Keys are not available\nOn the server now")
		else:
			log.debug("keys are fine")




get_keyslist_from_db()

root.reg_btn.configure(command=regenerate)


regenerate()
while True:
	root.flip()
