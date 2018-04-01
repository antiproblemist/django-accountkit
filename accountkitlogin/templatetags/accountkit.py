from django.template import Library
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.conf import settings
from django.contrib import messages
from django.core.signing import Signer


register = Library()

api_version = getattr(settings, 'ACCOUNT_KIT_VERSION')
accountkit_secret = getattr(settings, 'ACCOUNT_KIT_APP_SECRET')
accountkit_app_id = getattr(settings, 'APP_ID')
accountkit_redirect = getattr(settings, 'ACCOUNT_KIT_SUCCESS_REDIRECT')

@register.simple_tag()
def accountkitjs():
	signer = Signer()
	state = signer.sign(accountkit_app_id)
	html = "<script src='https://sdk.accountkit.com/en_US/sdk.js'></script><script>AccountKit_OnInteractive=function(){AccountKit.init({appId:'%s',state:'%s',version:'%s',redirect:'%s',fbAppEventsEnabled:!0})};function loginCallback(response){if(response.status==='PARTIALLY_AUTHENTICATED'){var code=response.code;var csrf=response.state;document.getElementById('code').value=code;document.getElementById('csrf').value=csrf;document.getElementById('login_success').submit()} else if(response.status==='NOT_AUTHENTICATED'){document.getElementById('message').innerText='Not Authenticated'} else if(response.status==='BAD_PARAMS'){document.getElementById('message').innerText='Bad Params'}}function smsLogin(){AccountKit.login('PHONE',{countryCode:'+1',phoneNumber:''},loginCallback)} function emailLogin(){AccountKit.login('EMAIL',{emailAddress:''},loginCallback)}" % (accountkit_app_id, state, api_version, accountkit_redirect)
	return mark_safe(html)