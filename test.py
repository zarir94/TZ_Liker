from email.utils import formataddr
from email.message import EmailMessage
import smtplib

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


send_contact_email('Amera','johnamera8324@gmail.com','I need help', '<b>Hello Sir,</b><p>I can\'t register on your site.</p>')
