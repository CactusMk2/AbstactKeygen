async def parse_keys(string):

	keys_list = []
	form_string = string.replace(" ","")
	splits = form_string.split("\n")

	for part in splits:
		if len(part) == 14:
			keys_list.append(part)
	return(keys_list)
	

def strfdelta(tdelta):
	if tdelta.days:
		if tdelta.days == 1:
			outp_days = f"{tdelta.days} day, "
		else:
			outp_days = f"{tdelta.days} days, "
	else: outp_days = ""

	hours, rem = divmod(tdelta.seconds, 3600)
	minutes, seconds = divmod(rem, 60)

	if minutes:
		if minutes == 1:
			outp_minutes = f"{minutes} minute"
		else:
			outp_minutes = f"{minutes} minutes"
	else: outp_minutes = "0 minutes"

	if hours:
		if hours == 1:
			outp_hours = f"{hours} hour and {outp_minutes}"
		else:
			outp_hours = f"{hours} hours and {outp_minutes}"
	elif minutes and tdelta.days:
		outp_hours = f"{outp_minutes}"
	elif minutes:
		outp_hours = "1 minute"
	elif tdelta.days:
		outp_hours = ""
	else:
		outp_hours = ""
	

	if not tdelta.days and not hours and not minutes:
		output = "0 seconds"
	elif tdelta.days and not hours and not minutes:
		outp_days = outp_days.replace(",","")
		output = f"{outp_days}"
	else:
		output = f"{outp_days}{outp_hours}"

	return output+" left"
		