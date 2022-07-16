from Home.models import Site_Info

def global_context(request):
	host=request.scheme+'://'+request.get_host()
	try:
		theme=request.COOKIES['theme']
	except:
		theme='dark'
	if not theme in ['light', 'dark']:
		theme='dark'
	return {'host':host, 'theme':theme}
	