from rest_framework import serializers
from users.models import User 
from core.models import Patient, Doctor

# 🔹 Public serializer: Only registers patients
class PublicPatientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.role = 'patient'
        user.save()

        Patient.objects.create(
            user=user,
            identification_number='TEMP',
            insurance_id='TEMP'
        )
        return user


# 🔹 Admin serializer: Can assign any role
class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    password = serializers.CharField(write_only=True)
    
    phone = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    identification_number = serializers.CharField(required=False)
    insurance_id = serializers.CharField(required=False)
    specialization = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role','phone', 'address', 'identification_number', 'specialization','insurance_id']

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')

        phone = validated_data.pop('phone', None)
        address = validated_data.pop('address', None)
        identification_number = validated_data.pop('identification_number', None)
        insurance_id = validated_data.pop('insurance_id', None)
        specialization = validated_data.pop('specialization', None)

        user = User(**validated_data)
        user.set_password(password)
        user.role = role
        user.save()

        if role == 'patient':
            Patient.objects.create(
                user=user,
                phone=phone or '',
                address=address or '',
                identification_number=identification_number or '',
                insurance_id=insurance_id or ''
            )
        elif role == 'doctor':
                Doctor.objects.create(
                user=user,
                specialization=specialization or '',
                available_from='09:00',
                available_to='17:00'

            )

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','role']