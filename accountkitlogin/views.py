# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json, requests
from django.conf import settings
from django.core.signing import TimestampSigner, BadSignature
from django.contrib.auth import authenticate, login 


api_version = getattr(settings, 'ACCOUNT_KIT_VERSION')
accountkit_secret = getattr(settings, 'ACCOUNT_KIT_APP_SECRET')
accountkit_app_id = getattr(settings, 'APP_ID')

def login_status(request):

	code = request.GET.get('code') if request.GET.get('code', None) else request.POST.get('code', None)
	state = request.GET.get('state') if request.GET.get('state', None) else request.POST.get('state', None)
	status = request.GET.get('status') if request.GET.get('status', None) else request.POST.get('status', None)
	context = {}

	if request.user.is_authenticated:
		context['authenticated'] = True
		context['message'] = "User with username %s is already logged in" % request.user.username
		context['user'] = request.user
		return context

	if status != "PARTIALLY_AUTHENTICATED":
		context['authenticated'] = False
		context['message'] = "Accountkit could not authenticate the user"
		context['user'] = None
		return context

	try:
		signer = TimestampSigner()
		csrf = signer.unsign(state)
	except BadSignature:
		context['authenticated'] = False
		context['message'] = "Invalid request"
		context['user'] = None
		return context

	#Exchange authorization code for access token
	token_url = 'https://graph.accountkit.com/%s/access_token' % api_version
	params = {'grant_type': 'authorization_code', 'code': code,
				'access_token': 'AA|%s|%s' % (accountkit_app_id, accountkit_secret)
			}

	res = requests.get(token_url, params=params)
	token_response = res.json()

	if 'error' in token_response:
		context['authenticated'] = False
		context['message'] = "This authorization code has been used."
		context['user'] = None
		return context

	user_id = token_response.get('id')
	user_access_token = token_response.get('access_token')
	refresh_interval = token_response.get('token_refresh_interval_sec')

	#Get Account Kit information
	identity_url = 'https://graph.accountkit.com/%s/me' % api_version
	identity_params = {'access_token': user_access_token}

	res = requests.get(identity_url, params=identity_params)
	identity_response = res.json()

	if 'error' in identity_response:
		context['authenticated'] = False
		context['message'] = identity_response['error']['message']
		context['user'] = None
		return context
	elif identity_response['application']['id'] != accountkit_app_id:
		context['authenticated'] = False
		context['message'] = "The application id returned does not match the one in your settings"
		context['user'] = None
		return context

	user = None
	username = None
	if 'email' in identity_response:
		username = identity_response['email']['address']
		user = authenticate(request, username=username, email=username)
	elif 'phone' in identity_response:
		username = identity_response['phone']['number']
		user = authenticate(request, username=username)
	
	if not user:
		context['authenticated'] = False
		context['message'] = "Please check if the user with username %s is active" % username
		context['user'] = None
		return context
	
	login(request, user)
	context['authenticated'] = True
	context['message'] = "User with username %s logged in" % username
	context['user'] = user
	return context