from __future__ import unicode_literals
from django.template import Library
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.conf import settings
from django.contrib import messages
from django.core.signing import TimestampSigner


register = Library()

api_version = getattr(settings, 'ACCOUNT_KIT_VERSION')
accountkit_secret = getattr(settings, 'ACCOUNT_KIT_APP_SECRET')
accountkit_app_id = getattr(settings, 'APP_ID')
accountkit_redirect = getattr(settings, 'ACCOUNT_KIT_SUCCESS_REDIRECT')

@register.simple_tag()
def accountkitjs():
	signer = TimestampSigner()
	state = signer.sign(accountkit_app_id)
	html = u"<script src='https://sdk.accountkit.com/en_US/sdk.js'></script><script>AccountKit_OnInteractive=function(){AccountKit.init({appId:'%s',state:'%s',version:'%s',redirect:'%s',fbAppEventsEnabled:!0})};function loginCallback(response){var code=response.code;var state=response.state;var status=response.status;document.getElementById('code').value=code;document.getElementById('state').value=state;document.getElementById('status').value=status;document.getElementById('login').submit();} function smsLogin(){AccountKit.login('PHONE',{countryCode:'+1',phoneNumber:''},loginCallback)} function emailLogin(){AccountKit.login('EMAIL',{emailAddress:''},loginCallback)}></script>" % (accountkit_app_id, state, api_version, accountkit_redirect)
	return mark_safe(html)

@register.simple_tag()
def accountkitform():
	html = u"<form id='login' method='post' action='%s'><input id='state' type='hidden' name='state'/><input id='code' type='hidden' name='code'/><input id='status' type='hidden' name='status'/></form>" % accountkit_redirect
	return format_html(html)

@register.simple_tag()
def smslogin(className="btn btn-outline-primary btn-block", text="Sign-in via SMS"):
	html = u"<button onclick='smsLogin();' class='%s'>%s</button>" % (className, text)
	return format_html(html)

@register.simple_tag()
def emaillogin(className="btn btn-outline-primary btn-block", text="Sign-in via Email"):
	html = u"<button onclick='emailLogin();' class='%s'>%s</button>" % (className, text)
	return format_html(html)