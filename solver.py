import requests
from urllib.parse import unquote
from passlib.hash import des_crypt
import sys
from string import ascii_letters

CHARMAP=ascii_letters+"0123456789!'+%&/()=?{[]}!_"
INDEX_MAP = ["guest:"+(i*"a")+":" for i in range(8,0,-1)]
FLAG = ""

def get_cookies(u_len):
	burp0_url = "http://10.10.27.68:80/" # REPLACE HERE WITH YOUR MACHINE IP
	r = requests.get(burp0_url,headers={"User-Agent":"a"*u_len},allow_redirects=False)
	cookie_text = unquote(r.headers["Set-Cookie"].split(";")[0].split("=")[1])
	cookie = [cookie_text[i:i+13] for i in range(0,len(cookie_text),13)]
	return cookie

def fuzz(start_index,item_pos,salt):
	global FLAG
	for c in CHARMAP:
		FLAG_PART = FLAG if start_index==8 else FLAG[(start_index-16)+(item_pos[0]+1):]
		if des_crypt.hash(INDEX_MAP[item_pos[0]][start_index:start_index+8]+FLAG_PART+c,salt=salt) == cookie_list[item_pos[0]][item_pos[1]]:
			FLAG+=c
			if(c == "}"):
				print("here is your flag: ",FLAG)
				sys.exit(0)
			return c
	print("nope!",item_pos)
	return None

cookie_list=[get_cookies(i) for i in range(8,0,-1)]
salts = [x[0][:2] for x in cookie_list]

if des_crypt.hash("guest:aa",salt=salts[0]) == cookie_list[0][0]:
	print("verified!")
else:
	print("not verified!")
	sys.exit(0)


i=1
while 1:
	for j in range(8):
		fuzz(i*8,(j,i),salts[j])
	print("partial flag: ",FLAG)
	i+=1

print(FLAG)
