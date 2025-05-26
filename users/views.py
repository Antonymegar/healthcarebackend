from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User
from .serializers import RegisterSerializer,PublicPatientRegisterSerializer, UserSerializer

class PublicRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PublicPatientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Patient registered successfully"}, status=201)
        return Response(serializer.errors, status=400)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=201)
        return Response(serializer.errors, status=400)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    profile_data = {
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    if user.role == 'patient' and hasattr(user, 'patient'):
        profile_data['patient_id'] = user.patient.id

    elif user.role == 'doctor' and hasattr(user, 'doctor'):
        profile_data['doctor_id'] = user.doctor.id

    return Response(profile_data)
