from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth import login as login_user, logout as logout_user
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth.hashers import check_password
from .liker_helper import get_fb_name, get_profile_id, get_post_id, check_follow_and_get_id, react_post, follow_id, get
from string import ascii_letters, digits
from .models import Site_Info, Account, Contact
from datetime import datetime
import pytz
from email.utils import formataddr
from email.message import EmailMessage
import smtplib
from django.contrib import messages
from random import choices, choice
from threading import Thread

react_dict={'like':0, 'love':1, 'care':2, 'haha':3, 'wow':4, 'sad':5, 'angry':6}

def send_password_change_email(receiverName, receiverEmail, link):
	s=smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
	s.starttls()
	s.login('tz-liker-notifier@outlook.com', 'tzliker@1')
	senderName='TZ Liker'
	sender = "tz-liker-notifier@outlook.com"
	receiver = receiverEmail
	msg = EmailMessage()
	msg['From'] = formataddr((senderName, sender))
	msg['Reply-To'] = formataddr((senderName, sender))
	msg['To'] = formataddr((receiverName, receiver))
	msg['Subject'] = 'Password Changing Instruction'
	msg.set_content(f'''<p>Hi {receiverName},</p>
	<p>We received a request to reset the password on your TZ Liker account.</p>
	<p>If you made this request, <strong>please click the Change Password link below</strong> to proceed.</p>
	<p><a href="{link}" target="_blank">Change Password</a></p>
	<p>If the link doesn't work then copy this link below and paste it in your browser</p>
	<p>{link}</p>
	<p>If you did not make this request, please ignore this email.</p>
	<p>Thank you,</p>
	<p>- The TZ Liker Team</p>''', subtype='html')
	s.send_message(msg)
	s.quit()

def send_contact_email(userName, userEmail, userSubject, userMessage):
	s=smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
	s.starttls()
	s.login('tz-liker-notifier@outlook.com', 'tzliker@1')
	senderName=f'{userName} - TZ Liker'
	sender = "tz-liker-notifier@outlook.com"
	receiverName='S M Shahriar Zarir'
	receiver = 'shahriarzariradvance@gmail.com'
	msg = EmailMessage()
	msg['From'] = formataddr((senderName, sender))
	msg['Reply-To'] = formataddr((userName, userEmail))
	msg['To'] = formataddr((receiverName, receiver))
	msg['Subject'] = userSubject
	msg.set_content(userMessage, subtype='html')
	s.send_message(msg)
	s.quit()

class Email_Validator():
	def __init__(self, email:str):
		self.email=email
		self.resp1=get('https://nobounce.herokuapp.com/isdelivrable/'+email)
		self.resp2=get('https://nobounce.herokuapp.com/istemp/'+email)
		self.temp_mail=self.resp2.json()
		self.valid_mail=True if self.resp1.json()['Delivrable']=='True' else False
	@property
	def is_valid(self):
		return self.valid_mail
	@property
	def is_temp(self):
		return self.temp_mail

def thread_react_post(amount, post_id, react, likable_accounts):
	success=0
	for i in range(int(amount)):
		acc=likable_accounts[i]
		var=react_post(post_id, acc.cookie, react)
		if var:
			success+=1
			acc.used_ids+=f'{post_id},'
			acc.save()
	info=Site_Info.objects.all().first()
	info.likes+=success
	info.save()

def thread_follow_id(amount, fb_id, likable_accounts):
	success=0
	for i in range(int(amount)):
		acc=likable_accounts[i]
		var=follow_id(fb_id, acc.cookie)
		if var:
			success+=1
			acc.used_ids+=f'{fb_id},'
			acc.save()
	info=Site_Info.objects.all().first()
	info.follows+=success
	info.save()

def convert_min_sec(seconds):
	minutes="%02d" % (seconds // 60)
	seconds="%02d" % (seconds % 60)
	return minutes, seconds

def filter_objects(text:str, objects):
	removed_objects=[]
	unique_objects=[]
	for obj in objects:
		used_ids=obj.used_ids
		if not text in used_ids:
			unique_objects.append(obj)
		else:
			removed_objects.append(obj)

	return unique_objects, removed_objects

def encrypt_password(password:str):
	hashed=PBKDF2PasswordHasher().encode(password, ''.join(choices(ascii_letters+str(digits), k=22)), 320000)
	return hashed

def get_unique_token(length=150):
	finished=False
	while not finished:
		token=''.join(choices(ascii_letters, k=length))
		objects=Account.objects.filter(token=token).first()
		if not objects:
			finished=True
	return token

def home(request):
	info=Site_Info.objects.filter(id=0).first()
	if not info:
		info=Site_Info(id=0, likes=0, follows=0, users=len(Account.objects.all()))
		info.save()
		info=Site_Info.objects.filter(id=0).first()
	likes=info.likes
	follows=info.follows
	users=info.users
	active_users=len(Account.objects.filter(has_cookie=True))

	return render(request, 'index.html', context={'likes':likes, 'follows':follows, 'users':users, 'active_users':active_users})

def login(request):
	if not request.user.is_anonymous:
		messages.warning(request, 'You are already logged in!')
		return redirect('/')
	if request.POST:
		username=request.POST.get('username')
		password=request.POST.get('password')
		remember=True if request.POST.get('remember') else False
		if not username:
			messages.warning(request, 'Username can not be empty!')
		elif ' ' in username:
			messages.warning(request, 'Username can not have a space!')
		elif not password:
			messages.warning(request, 'Password can not be empty!')
		elif len(username)<4:
			messages.warning(request, 'Username should have at least 4 characters!')
		elif len(password)<6:
			messages.warning(request, 'Password should have at least 6 characters!')
		else:
			if '@' in username:
				user=Account.objects.filter(email=username).first()
			else:
				user=Account.objects.filter(username=username).first()
			if not user:
				messages.warning(request, 'User could not found')
			else:
				if not check_password(password, user.password):
					messages.warning(request, 'Wrong Password! Please try again.')
				else:
					login_user(request, user)
					request.session.user=user
					if remember:
						request.session.set_expiry(0)
					messages.success(request, 'Successfully logged in!')
					return redirect('/dashboard')

	return render(request, 'login.html')

def register(request):
	if not request.user.is_anonymous:
		messages.warning(request, 'You are already logged in!')
		return redirect('/')
	if request.POST:
		username=request.POST.get('username')
		email=request.POST.get('email')
		password=request.POST.get('password')
		confirm_password=request.POST.get('confirmpassword')
		email_check=Account.objects.filter(email=email).first()
		username_check=Account.objects.filter(username=username).first()
		validator=Email_Validator(email)
		if not username:
			messages.warning(request, 'Username can not be empty!')
		elif not email:
			messages.warning(request, 'Email can not be empty!')
		elif not password:
			messages.warning(request, 'Password can not be empty!')
		elif not confirm_password:
			messages.warning(request, 'Confirm password can not be empty!')
		elif len(username)<4:
			messages.warning(request, 'Username should have at least 4 characters!')
		elif len(password)<6:
			messages.warning(request, 'Password should have at least 6 characters!')
		elif password!=confirm_password:
			messages.warning(request, 'Password should match with Confirm Password!')
		elif email_check:
			messages.warning(request, 'User with that email is already exists!')
		elif username_check:
			messages.warning(request, 'User with that username is already exists!')
		elif not validator.is_valid:
			messages.warning(request, 'Sorry, we could not verify your email. Looks like this email does not exists!')
		elif validator.is_temp:
			messages.warning(request, 'Sorry, temp mails are not allowed to register here!')
		else:
			info=Site_Info.objects.filter(id=0).first()
			info.users+=1
			info.save()
			# token=get_unique_token()
			# link=request.scheme+'://'+request.get_host()+'/verify?token='+token
			user=Account.objects.create_user(username=username, email=email, password=password)
			# user.token=token
			user.is_verified=True
			user.save()
			# messages.success(request, 'Please check your email and verify it!')
			# messages.info(request, f'Your email verification link is: <a class="alert-link" href="{link}">here</a>')
			messages.success(request, 'Your account has been created successfully! You can login now.')
			return redirect('/login')

	return render(request, 'register.html')

def verify_email(request):
	if not request.user.is_anonymous:
		messages.warning(request, 'You are already logged in!')
		return redirect('/')
	token=request.GET.get('token')
	if not token:
		messages.error(request, 'Error: The token is invalid or has been used once!')
		return redirect('/')
	user=Account.objects.filter(token=token).first()
	if not user:
		messages.error(request, 'Error: The token is invalid or has been used once!')
		return redirect('/')
	if user.is_verified:
		messages.error(request, 'Error: User has been already verified!')
		return redirect('/')
	user.token=None
	user.is_verified=True
	user.save()
	messages.success(request, 'Your email has been successfully verified! Now you can login.')
	return redirect('/login')

def about(request):
	return render(request, 'about.html')

def contact(request):
	if request.POST:
		fullname=request.POST.get('fullname')
		email=request.POST.get('email')
		subject=request.POST.get('subject')
		message=request.POST.get('message')
		if not fullname:
			messages.warning(request, 'Name can not be empty!')
		elif not email:
			messages.warning(request, 'Email can not be empty!')
		elif not subject:
			messages.warning(request, 'Subject can not be empty!')
		elif not message:
			messages.warning(request, 'Message can not be empty!')
		else:
			contact=Contact(name=fullname, email=email, subject=subject, message=message)
			contact.save()
			messages.success(request, 'Your request has been submitted! Admin will be in touch shortly!')
			send_contact_email(fullname, email, subject, message)
	return render(request, 'contact.html')

def tutorial(request):
	return render(request, 'tutorial.html')

def dashboard(request):
	if request.user.is_anonymous:
		messages.warning(request, 'Please login first!')
		return redirect('/login')
	return render(request, 'dashboard.html')

def auto_like(request):
	if request.user.is_anonymous:
		messages.warning(request, 'Please login first!')
		return redirect('/login')
	if not request.user.has_cookie:
		messages.warning(request, 'Please set your facebook cookie first!')
		messages.info(request, '<a class="alert-link" href="/tutorial#getcookie">Click here</a> if you don\'t know how to get facebook cookie.')
		return redirect(settings)
	post_id=request.GET.get('id')
	if post_id:
		acc=choice(Account.objects.filter(has_cookie=True).exclude(username=request.user.username))
		valid=get_post_id('https://mbasic.facebook.com/'+post_id, acc.cookie)
		if not valid:
			messages.error(request, 'Please make sure that url is valid, the post is public and it can receive public likes. <a class="alert-link" href="/tutorial#makepublicpost">Learn More.</a>')
			return redirect('/dashboard/auto-like/')
		available_accounts=Account.objects.filter(has_cookie=True).exclude(username=request.user.username)
		likable_accounts=[]
		for acc in available_accounts:
			if not post_id in acc.used_ids:
				likable_accounts.append(acc)
		liked_accounts=[]
		for acc in Account.objects.all().exclude(username=request.user.username):
			if post_id in acc.used_ids:
				liked_accounts.append(acc)
		minimum=0
		if len(likable_accounts)>100:
			maximum=100
		else:
			maximum=len(likable_accounts)

		last_submit=request.user.last_submit
		timenow=datetime.now(tz=pytz.UTC)
		cooldown=(timenow - last_submit).total_seconds()<600
		time_remaining=int(600-(timenow - last_submit).total_seconds())
		if time_remaining<0:
			time_remaining=0
		minutes, seconds=convert_min_sec(time_remaining)
		if request.POST:
			amount=request.POST.get('amount')
			react=request.POST.get('react')
			if cooldown:
				messages.warning(request, 'You can not submit during cooldown process.')
			elif int(amount)>maximum:
				messages.warning(request, 'Maximum reaction amount is 100!')
			elif maximum==0:
				messages.warning(request, 'Sorry, out of stock! All available accounts has been used to like this post.')
			elif react not in react_dict:
				messages.warning(request, 'Invalid reaction type!')
			else:
				if not request.user.is_superuser:
					request.user.last_submit=timenow
					request.user.save()
				t=Thread(target=lambda: thread_react_post(amount, post_id, react, likable_accounts))
				t.setDaemon(True)
				t.start()
				messages.success(request, 'Your request has been submitted. You will receive reactions in a few minutes.')
				return redirect(f'/dashboard/auto-like/?id={post_id}')

		messages.info(request, 'The Likes amount depend on how many users registered on this site. So share this site to everyone and help to add more users here. Remember, the more user registers here, the more reactions you get.\n<b>Note:</b> Users must have set their facebook cookies.')

		return render(request, 'auto_like_submit.html', context={'min':minimum, 'max':maximum, 'minutes':minutes, 'seconds':seconds, 'cooldown':cooldown, 'time_remaining':time_remaining, 'available_accounts':len(available_accounts), 'likable_accounts':len(likable_accounts), 'liked_accounts':len(liked_accounts)})
	else:
		if request.POST:
			url=request.POST.get('fb_post_url')
			acc=choice(Account.objects.filter(has_cookie=True).exclude(username=request.user.username))
			cookie=acc.cookie
			post_id=get_post_id(url, cookie)
			if not post_id:
				messages.error(request, 'Please make sure that url is valid, the post is public and it can receive public likes. <a class="alert-link" href="/tutorial#makepublicpost">Learn More.</a>')
			else:
				return redirect('/dashboard/auto-like/?id='+post_id)

		return render(request, 'auto_like_form.html')

def auto_follow(request):
	if request.user.is_anonymous:
		messages.warning(request, 'Please login first!')
		return redirect('/login')
	if not request.user.has_cookie:
		messages.warning(request, 'Please set your facebook cookie first!')
		messages.info(request, '<a class="alert-link" href="/tutorial#getcookie">Click here</a> if you don\'t know how to get facebook cookie.')
		return redirect(settings)
	fb_id=request.GET.get('id')
	if fb_id:
		acc=choice(Account.objects.filter(has_cookie=True).exclude(username=request.user.username))
		valid=check_follow_and_get_id('https://mbasic.facebook.com/'+fb_id, acc.cookie)
		if not valid:
			messages.error(request, 'Please make sure that url is valid and profile can receive followers. <a class="alert-link" href="/tutorial#makepublicpost">Learn More.</a>')
			return redirect('/dashboard/auto-follow/')
		available_accounts=Account.objects.filter(has_cookie=True).exclude(username=request.user.username)
		followable_accounts=[]
		for acc in available_accounts:
			if not fb_id in acc.used_ids:
				followable_accounts.append(acc)
		followed_accounts=[]
		for acc in Account.objects.all().exclude(username=request.user.username):
			if fb_id in acc.used_ids:
				followed_accounts.append(acc)
		minimum=0
		if len(followable_accounts)>100:
			maximum=100
		else:
			maximum=len(followable_accounts)

		last_submit=request.user.last_submit
		timenow=datetime.now(tz=pytz.UTC)
		cooldown=(timenow - last_submit).total_seconds()<600
		time_remaining=int(600-(timenow - last_submit).total_seconds())
		if time_remaining<0:
			time_remaining=0
		minutes, seconds=convert_min_sec(time_remaining)
		if request.POST:
			amount=request.POST.get('amount')
			if cooldown:
				messages.warning(request, 'You can not submit during cooldown process.')
			elif int(amount)>maximum:
				messages.warning(request, 'Maximum reaction amount is 100!')
			elif maximum==0:
				messages.warning(request, 'Sorry, out of stock! All available accounts has been used to like this post.')
			else:
				if not request.user.is_superuser:
					request.user.last_submit=timenow
					request.user.save()
				t=Thread(target=lambda: thread_follow_id(amount, fb_id, followable_accounts))
				t.setDaemon(True)
				t.start()
				messages.success(request, 'Your request has been submitted. You will receive followers in a few minutes.')
				return redirect(f'/dashboard/auto-follow/?id={fb_id}')

		messages.info(request, 'The Followers amount depend on how many users registered on this site. So share this site to everyone and help to add more users here. Remember, the more user registers here, the more reactions you will get.\n<b>Note:</b> Users must have set their facebook cookies.')
		messages.info(request, 'If you are not receiving likes then you must forget to make your account public. <a class="alert-link" href="/tutorial#makepublicaccount">Click here</a> to make your account public.')

		return render(request, 'auto_follow_submit.html', context={'min':minimum, 'max':maximum, 'minutes':minutes, 'seconds':seconds, 'cooldown':cooldown, 'time_remaining':time_remaining, 'available_accounts':len(available_accounts), 'likable_accounts':len(followable_accounts), 'liked_accounts':len(followed_accounts)})
	else:
		if request.POST:
			url=request.POST.get('fb_id_url')
			acc=choice(Account.objects.filter(has_cookie=True).exclude(username=request.user.username))
			cookie=acc.cookie
			fb_id=check_follow_and_get_id(url, cookie)
			if not fb_id:
				messages.error(request, 'Please make sure that url is valid and profile can receive followers. <a class="alert-link" href="/tutorial#makepublicpost">Learn More.</a>')
			else:
				return redirect('/dashboard/auto-follow/?id='+fb_id)

		return render(request, 'auto_follow_form.html')

def settings(request):
	if request.user.is_anonymous:
		messages.warning(request, 'Please login first!')
		return redirect('/login')
	if request.POST:
		cookie=request.POST.get('cookie')
		if not cookie:
			messages.warning(request, 'Cookie can not be empty!')
		elif cookie==request.user.cookie:
			messages.warning(request, 'Cookie is same as old one!')
		else:
			fullname=get_fb_name(cookie)
			if not fullname:
				messages.warning(request, 'Invalid Cookie! Looks like cookie has been expired.')
			else:
				profile_id=get_profile_id('https://mbasic.facebook.com/me', cookie)
				if not profile_id:
					messages.warning(request, 'Sorry, we could not fetch your profile id.')
				find_user=Account.objects.filter(profile_id=profile_id).exclude(username=request.user.username).first()
				if find_user:
					messages.warning(request, 'This facebook account has been used by someone!')
				else:
					request.user.full_name=fullname
					request.user.cookie=cookie
					request.user.profile_id=profile_id
					request.user.has_cookie=True
					request.user.save()
					messages.success(request, 'Settings successfully updated!')

	return render(request, 'settings.html')

def reset_password(request):
	if not request.user.is_anonymous:
		messages.warning(request, 'Please logout first!')
		return redirect('/')

	if request.POST:
		email=request.POST.get('email')
		if not email:
			messages.warning(request, 'Please enter a valid email!')
		elif '@' not in email:
			messages.warning(request, 'Please enter a valid email!')
		else:
			user=Account.objects.filter(email=email).first()
			if not user:
				messages.warning(request, 'This email is not registered!')
			elif not user.is_verified:
				messages.warning(request, 'Please verify your email first!')
			else:
				token=get_unique_token()
				link=request.scheme+'://'+request.get_host()+'/change-password?token='+token
				user.token=token
				user.save()
				messages.success(request, 'Email has been sent! Please check your inbox. Don\'t forget to check your spam folder!')
				send_password_change_email(user.username, user.email, link)

	return render(request, 'reset_password.html')

def change_password(request):
	if not request.user.is_anonymous:
		messages.warning(request, 'Please logout first!')
		return redirect('/')

	token=request.GET.get('token')
	if not token:
		messages.error(request, 'Empty token!')
		return redirect('/')
	else:
		user=Account.objects.filter(token=token).first()
		if not user:
			messages.error(request, 'Invalid token!')
			return redirect('/')

	if request.POST:
		password=request.POST.get('password')
		confirm_password=request.POST.get('confirmpassword')
		if not password:
			messages.warning(request, 'Password can not be empty!')
		elif not confirm_password:
			messages.warning(request, 'Confirm password can not be empty!')
		elif len(password)<6:
			messages.warning(request, 'Password should have at least 6 characters!')
		elif password!=confirm_password:
			messages.warning(request, 'Password should match with Confirm Password!')
		elif check_password(password, user.password):
			messages.warning(request, 'Your new password is same as old password!')
		else:
			password=encrypt_password(password)
			user.password=password
			user.token=None
			user.save()
			messages.success(request, 'Password successfully changed!')
			return redirect('/login')

	return render(request, 'change_password.html')

def logout(request):
	if request.user.is_anonymous:
		messages.warning(request, 'You are already logged out!')
		return redirect('/')
	logout_user(request)
	messages.success(request, 'Successfully logged out!')
	return redirect('/')

def delete(request):
	if request.user.is_anonymous:
		messages.warning(request, 'You are logged out!')
		return redirect('/')
	if request.POST:
		request.user.delete()
		info=Site_Info.objects.filter(id=0).first()
		info.users-=1
		info.save()
		messages.warning(request, 'Your account has been deleted. You are now logged out!')
		return redirect('/')
	else:
		return redirect('/')

def switch_theme(request):
	try:
		theme=request.COOKIES['theme']
	except:
		theme='dark'
	if not theme in ['light', 'dark']:
		theme='dark'
	response=HttpResponseRedirect(request.GET.get('next','/'))
	if theme=='light':
		response.set_cookie('theme','dark')
	else:
		response.set_cookie('theme','light')
	return response

def google_verify(request):
	return HttpResponse('google-site-verification: googled3920a951d8fb79c.html')
