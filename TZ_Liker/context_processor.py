from django.conf import settings

def global_context(request):
	# if settings.DEBUG:
	# 	prot='http'
	# else:
	# 	prot='https'
	# host=prot+'://'+request.get_host()
	host="/"
	try:
		theme=request.COOKIES['theme']
	except:
		theme='dark'
	if not theme in ['light', 'dark']:
		theme='dark'
	return {'host':host, 'theme':theme}

