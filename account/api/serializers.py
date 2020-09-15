from rest_framework import serializers
from account.models import Account

class RegistrationSerializer(serializers.ModelSerializer):

	password_confirmation = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = Account
		fields = ['email', 'username', 'password', 'password_confirmation']
		extra_kwargs = {
			'password': {'write_only': True}
		}
	def save(self):
		account = Account(
			email=self.validated_data['email'],
			username=self.validated_data['username'],
		)
		password = self.validated_data['password']
		password_confirmation = self.validated_data['password_confirmation']
		if password != password_confirmation:
			raise serializers.ValidationError({'password': 'Passwords did not match.'})
		account.set_password(password)
		result = account.save()

		return account

class AccountPropertiesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ['pk', 'email', 'username']

class ChangePasswordSerializer(serializers.Serializer):
	old_password 		 = serializers.CharField(required=True)
	new_password 		 = serializers.CharField(required=True)
	confirm_new_password = serializers.CharField(required=True)