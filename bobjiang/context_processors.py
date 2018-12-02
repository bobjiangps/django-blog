

def device(request):
    '''from mobile browser or pc browser'''
    user_agent = request.META['HTTP_USER_AGENT'].lower()
    mobile_re = ['iphone','android','mobile']

    if any([user_agent.find(name) + 1 for name in mobile_re]):
        return {'device_type':'mobile'}
    else:
        return {'device_type':'pc'}
