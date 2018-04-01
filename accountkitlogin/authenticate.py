from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

class authentication:

	# Create an authentication method
	# This is called by the standard Django login procedure
	def authenticate(self, request, username, email=None):
		try:
			user = get_user_model().objects.get(username=username)
		except ObjectDoesNotExist:
			columns = {}
			columns['username'] = username
			if email:
				columns['email'] = email
			user = get_user_model().objects.create_user(**columns)
			user.set_unusable_password()
			user.save()
		return user

	# Required for your backend to work properly - unchanged in most scenarios
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None