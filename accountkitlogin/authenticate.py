from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

class GetOrCreateUser:

	def authenticate(self, request, username, email=None):
		User = get_user_model()
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			columns = {}
			columns['username'] = username
			if email:
				columns['email'] = email
			user = User.objects.create_user(**columns)
			user.set_unusable_password()
			user.save()
		user = user if user.is_active else None
		return user

	# Required for your backend to work properly - unchanged in most scenarios
	def get_user(self, user_id):
		User = get_user_model()
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None