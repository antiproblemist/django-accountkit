# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json, requests
from django.conf import settings
from django.core.signing import Signer, BadSignature
from django.core.exceptions import PermissionDenied


api_version = getattr(settings, 'ACCOUNT_KIT_VERSION')
accountkit_secret = getattr(settings, 'ACCOUNT_KIT_APP_SECRET')
accountkit_app_id = getattr(settings, 'APP_ID')

@csrf_exempt
def success(request):
	signer = Signer()
	code = request.GET.get('code') if request.GET.get('code', None) else request.POST.get('code', None)
	state = request.GET.get('state') if request.GET.get('state', None) else request.POST.get('state', None)
	print state
	try:
		state = signer.unsign(state)
	except BadSignature:
		raise PermissionDenied

	print state
	#Exchange authorization code for access token
	token_url = 'https://graph.accountkit.com/%s/access_token' % api_version
	params = {'grant_type': 'authorization_code',
				'code': code,
				'access_token': 'AA|%s|%s' % (accountkit_app_id, accountkit_secret)
			}

	res = requests.get(token_url, params=params)
	token_response = res.json()
	
	user_id = token_response.get('id')
	user_access_token = token_response.get('access_token')
	refresh_interval = token_response.get('token_refresh_interval_sec')

	#Get Account Kit information
	identity_url = 'https://graph.accountkit.com/%s/me' % api_version
	identity_params = {'access_token': user_access_token}

	res = requests.get(identity_url, params=identity_params)
	identity_response = res.json()
	email = identity_response['email']['address']
	

def login_view(request):
	context = {}

	context['api_version'] = api_version
	context['accountkit_secret'] = accountkit_secret
	context['accountkit_app_id'] = accountkit_app_id
	return render(request, 'index.html', context)
