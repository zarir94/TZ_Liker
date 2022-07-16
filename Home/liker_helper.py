import re
from requests import get
from bs4 import BeautifulSoup
from tldextract import extract
from urllib.parse import urlparse
from urllib.parse import parse_qs

def check_follow_and_get_id(profile_url, cookies):
	try:
		resp=get(convert_to_mbasic(profile_url), cookies=convert_to_dict(cookies))
		html=resp.text
		match=re.findall(r'subscribe.php\?id=\d+', html)
		if not match:
			match=re.findall(r'remove\?subject_id=\d+', html)
		if not match:
			return False
		fb_id=match[0].split('=')[1]
		return fb_id
	except: 
		return False

def get_profile_id(profile_url:str, cookies:str):
	try:
		resp=get(convert_to_mbasic(profile_url), cookies=convert_to_dict(cookies))
		html=resp.text
		match=re.findall(r'profile_id=\d+', html)
		if not match:
			match=re.findall(r'owner_id=\d+', html)
		if not match:
			match=re.findall(r'confirm/\?bid=\d+', html)
		if not match:
			match=re.findall(r'subscribe.php\?id=\d+', html)
		if not match:
			match=re.findall(r'subject_id=\d+', html)
		if not match:
			match=re.findall(r'poke_target=\d+', html)
		if not match:
			return False
		fb_id=match[0].split('=')[1]
		return fb_id
	except:
		return False

def get_post_id(post_url, cookie):
	try:
		resp=get(convert_to_mbasic(post_url), cookies=convert_to_dict(cookie))
		html=resp.text
		match=re.findall(r'ft_ent_identifier=\d+', html)
		if not match:
			match=re.findall(r'target_id=\d+', html)
		if not match:
			match=re.findall(r';sid=\d+', html)
		if not match:
			return False
		post_id=match[0].split('=')[1]
		return post_id
	except:
		return False

def convert_to_mbasic(url:str):
	ext=extract(url)
	domain=ext.domain+'.'+ext.suffix
	new_url='https://mbasic.facebook.com'+url[url.find(domain)+len(domain):]
	return new_url

def convert_to_dict(cookie:str) -> dict:
	try:
		fb_cookies=cookie.replace(' ','')
		fb_cookies=fb_cookies.replace('\n','')
		fb_cookies=fb_cookies.split(';')
		if '' in fb_cookies:
			fb_cookies.remove('')
		fb_cookies_dict={}
		for item in fb_cookies:
			name, value=item.split('=')
			fb_cookies_dict[name]=value
		return fb_cookies_dict
	except:
		return False

def get_fb_name(cookie:str):
	resp=get('https://mbasic.facebook.com/me', cookies=convert_to_dict(cookie))
	soap=BeautifulSoup(resp.text, 'html.parser')
	title=soap.find('title').text
	if 'log in' in title.lower():
		return False
	elif 'facebook' in title.lower():
		return False
	return title

def react_post(post_id:str, cookie:str, react_name:str):
	try:
		# React ID's
		react_dict={'like':0, 'love':1, 'care':2, 'haha':3, 'wow':4, 'sad':5, 'angry':6}
		if not react_name in react_dict:
			raise Exception('Invalid react name')
		react_id=react_dict[react_name]
		
		# Converting Cookie string to dict
		fb_cookie=convert_to_dict(cookie)

		# Like on the post
		resp=get('https://mbasic.facebook.com/reactions/picker/?ft_id='+post_id, cookies=fb_cookie)
		soap=BeautifulSoup(resp.text, 'html.parser')
		ul=soap.find('ul')
		a=ul.find_all('a')
		react_link='https://mbasic.facebook.com'+a[react_id].get('href')
		resp=get(react_link, cookies=fb_cookie)
		return True
	except:
		 return False

def follow_id(fb_id:str, cookie:str):
	try:
		resp=get('https://mbasic.facebook.com/'+fb_id, cookies=convert_to_dict(cookie))
		soap=BeautifulSoup(resp.text, 'html.parser')
		follow_a=soap.find('a', string='Follow')
		if not follow_a:
			raise Exception('Cannot follow this id. Something went wrong')
		follow_link='https://mbasic.facebook.com'+follow_a.get('href')
		resp=get(follow_link, cookies=convert_to_dict(cookie))
		return True
	except:
		return False



fb_cookies='c_user=100075924800901; datr=Wx24Yp4zrg7wLRfHP06ZVZ1G; fr=0wwNB0XoxjuHwuroS.AWU9eNMY4KSZyK-LE0J1J2XiIEE.BiuB1b.Lg.AAA.0.0.BiuB2s.AWUgvNF3HKs; presence=C{"t3":[],"utc3":1656233569175,"v":1}; sb=Wx24Yn8uV2LPCQQSel0js97b; wd=1366x615; xs=41:Hp4MRyACawwtYg:2:1656233385:-1:4915; '
# post_id='174801738156290'
# react='sad'

# react_post(post_id=post_id, cookie=fb_cookies, react_name=react)
