from django.template import Library
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.conf import settings

register = Library()

api_version = getattr(settings, 'ACCOUNT_KIT_VERSION')
accountkit_secret = getattr(settings, 'ACCOUNT_KIT_APP_SECRET')
accountkit_app_id = getattr(settings, 'APP_ID')
accountkit_redirect = getattr(settings, 'ACCOUNT_KIT_SUCCESS_REDIRECT')

@register.simple_tag(takes_context = True)
def accountkitjs(csrf):
    html = "<script src='https://sdk.accountkit.com/en_US/sdk.js'></script><script>AccountKit_OnInteractive = function () {AccountKit.init(	{appId: '%s',state: '%s',version: '%s',redirect: '%s',fbAppEventsEnabled: true});};function smsLogin() {AccountKit.login('PHONE',{countryCode: '+1', phoneNumber: ''},);}function emailLogin() {AccountKit.login('EMAIL',{emailAddress:''},);}</script>" % (accountkit_app_id, csrf, api_version, accountkit_redirect)
    return mark_safe(html)