# django-accountkit
**Using Facebook accountkit with Django https://developers.facebook.com/products/account-creation**

[![PyPI version](https://badge.fury.io/py/django-accountkit.svg)](https://badge.fury.io/py/django-accountkit) [![Join the community on Spectrum](https://withspectrum.github.io/badge/badge.svg)](https://spectrum.chat/django-accountkit)


## Overview

This package enables the use of Facebook Accountkit with Django authentication

If you want to know more about Facebook Accountkit, check out the following resources
- https://auth0.com/blog/facebook-account-kit-passwordless-authentication/
- https://developers.facebook.com/docs/accountkit

## Requirements

-  Python (>= 2.7 and <= 3.7)
-  Django (>=1.11)


## Installation

Installation is easy using ``pip``

	pip install django-accountkit

Then to add Django Accountkit to your project add the app ``accountkitlogin`` to your ``INSTALLED_APPS``.

Now add the following settings in your settings.py file


	APP_ID = <Accountkit App ID>
	ACCOUNT_KIT_APP_SECRET = <Accountkit App Secret>
	ACCOUNT_KIT_VERSION = "v1.0"
	ACCOUNT_KIT_SUCCESS_REDIRECT = <The URL for the page where user will land after authenticating> (Please Use absolute path only)
	#Example ACCOUNT_KIT_SUCCESS_REDIRECT = "http://localhost:8000/success"
	
Then add the following in your settings.py file

	AUTHENTICATION_BACKENDS = (
		'accountkitlogin.authenticate.GetOrCreateUser',
	)

## Using Accountkitlogin

### View

To use Accountkit to authenticate your users import ``from accountkitlogin.views import login_status``

Then in your view use ``login_status``
	
	@csrf_exempt
	def success_page(request):
		context = login_status(request)

Note that csrf exempt is required because Facebook Accountkit will redirect the user to your success page url and this might throw a cross origin error

The ```login_status``` function accepts the request as parameter and returns a dictionary with

- Key 'authenticated' True or False
- Key 'message' A message related to whether the user is authenticated or not
- Key 'user' Returns a user instance when 'authenticated' is True

Add the view to your urls.py file for the success_page url which you defined in ``ACCOUNT_KIT_SUCCESS_REDIRECT`` setting

### Template Tags

Add ``{% load accountkit %}`` at the starting of your template and add the following template tags to your file where you want to display the login buttons

1) Add ``(% accountkitjs %}`` inside your ``<head></head>`` tag
2) Add ``{% accountkitform %}`` inside your ``<body></body>`` tag
3) Add ``{% smslogin %}`` and/or ``{% emaillogin %}`` anywhere in you body section where you want to display your login buttons. Both these tags accept two parameters className and text where you can add your custom css classes and the text to display on the button. Example ``{% emaillogin "button" "Use the email" %}``

## Notes

### Contribute

Please contribute to this repositiory :)

### Author

- Follow the author on [Linkedin](https://www.linkedin.com/in/shahzebq)

### This is project is inspired by

- The flask implementation of accountkit at https://github.com/everping/accountkit
