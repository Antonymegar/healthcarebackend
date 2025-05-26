# users/validators.py
from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.models import AccessToken
from users.models import User
from core.models import Patient, Doctor

class CustomOAuth2Validator(OAuth2Validator):
    def save_bearer_token(self, token, request, *args, **kwargs):
        super().save_bearer_token(token, request, *args, **kwargs)

        user = request.user
        if user:
            token['user'] = {
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }

            # Include extra info for patients/doctors if needed
            if user.role == 'patient':
                patient = getattr(user, 'patient', None)
                if patient:
                    token['user']['identification_number'] = patient.identification_number
                    token['user']['insurance_id'] = patient.insurance_id
                    token['user']['address'] = patient.address
                    token['user']['phone'] = patient.phone
            elif user.role == 'doctor':
                doctor = getattr(user, 'doctor', None)
                if doctor:
                    token['user']['specialization'] = doctor.specialization
