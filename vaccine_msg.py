from datetime import datetime
import requests
import schedule
import time

cowin_base_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
dt = now.strftime("%d-%m-%Y")
del_dis = [140,141,142,143,144,145,146,147,148,149,150]
d_name = {140:"New Delhi",141:"Central Delhi",142:"West Delhi",143:"North West Delhi",
144:"South East Delhi",145:"East Delhi",146:"North Delhi",147:"North East Delhi",148:"Shahdara",149:"South Delhi",150:"South West Delhi"}
telegram_api_url = "https://api.telegram.org/bot1711785782:AAG-GWUn8nMABSfX3KfegGiDQZUMeMkKy9k/sendMessage?chat_id=@grpid&text="
grp_id = "vaccine_slot_notifier_delhi"

#message = "vaccine Slots\n"

def fetch_cowin_data(dist_id):
	cowin_final_url = cowin_base_url+"?district_id={}&date={}".format(dist_id,dt)
	response = requests.get(cowin_final_url)
	send_data(response,dist_id)
	


def fetch_dist_data(d_id):
	for id in d_id:
		fetch_cowin_data(id)
	#msg_telegram(message)


def send_data(response,id):
	res = response.json()
	message1 = ""#\nDISTRICT: {}, Dose 1\n~~~~~~~~~~~~~~\n\n".format(d_name[id])
	message2 = ""#\nDISTRICT: {}, Dose 2\n~~~~~~~~~~~~~~\n\n".format(d_name[id])
	a = 0
	b = 0
	for center in res["centers"]:
		x = 0
		y = 0
		z = 0 
		for session in center["sessions"]:
			if z<=2:
				if session["available_capacity_dose1"] > 0 and session["min_age_limit"]==18:
					if a == 0:
						message1 = message1+"\nDISTRICT: {}, Dose 1\n~~~~~~~~~~~~~~\n\n".format(d_name[id])
						a = a+1
					if x == 0:
						message1 = message1+"Pincode: {}\nCenter name: {}, Fee: {} \n".format(center["pincode"],center["name"],center["fee_type"])
						x = x+1
					message1 = message1+"Dose 1:\nSlots: {} \nDate: {} \nVaccine: {} \nAge limit: {} \n-------------\n".format(session["available_capacity_dose1"],session["date"],session["vaccine"],session["min_age_limit"])
				if session["available_capacity_dose2"] > 0 and session["min_age_limit"]==18:
					if b ==0:
						message2 = message2+"\nDISTRICT: {}, Dose 2\n~~~~~~~~~~~~~~\n\n".format(d_name[id])
						b = b+1
					if y == 0:
						message2 = message2+"Pincode: {}\nCenter name: {}, Fee: {} \n".format(center["pincode"],center["name"],center["fee_type"])
						y = y+1
					message2 = message2+"Dose 2:\nSlots: {} \nDate: {} \nVaccine name: {} \nAge limit: {} \n-------------\n".format(session["available_capacity_dose2"],session["date"],session["vaccine"],session["min_age_limit"])
				z = z+1
		if session["available_capacity_dose1"] > 0 and session["min_age_limit"]==18:
			message1 = message1+"-------------\n"
		if session["available_capacity_dose2"] > 0 and session["min_age_limit"]==18:	
			message2 = message2+"-------------\n"
	#print(message1)
	msg_telegram(message1)
	#print(message2)
	msg_telegram(message2)


def msg_telegram(msg):
	telegram_final_url = telegram_api_url.replace("grpid",grp_id)
	telegram_final_url = telegram_final_url+msg
	resp = requests.get(telegram_final_url)
	print(resp)
	print("\n")




if __name__ == '__main__':
	schedule.every(300).seconds.do(lambda: (fetch_dist_data(del_dis)))
	while True:
		schedule.run_pending()
		time.sleep(1)

	
