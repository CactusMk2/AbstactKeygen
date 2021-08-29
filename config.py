def startlog():
	import logging
	logging.basicConfig(level=logging.INFO, filename="log.txt")
	log = logging.getLogger("mainlog")
	return log


# client settings
STARTS_WITH = "**РАЗБИРАЕМ"
HOST = "https://t.me/hidemykeys"
SESSION_NAME = "data"
DB_NAME = "keys.db"
client_ids_file = "client.json"

# time settings
msg_lasts = 1
update_interval = 8

# gui
XPOS = 0
YPOS = 0
SIZEW = 400
SIZEH = 250
ALPHA = 0.95

