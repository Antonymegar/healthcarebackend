from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from core.models import Patient, Doctor, Appointment
from .serializers import PatientSerializer, DoctorSerializer, AppointmentSerializer
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.select_related('user').all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('user').all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('doctor', 'patient').all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return self.queryset.filter(patient__user=user)
        elif user.role == 'doctor':
            return self.queryset.filter(doctor__user=user)
        return self.queryset.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'patient' and hasattr(user, 'patient'):
            serializer.save(patient=user.patient)
        else:
            raise PermissionDenied("Only patients can book appointments.")

    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()

        if user.role == 'patient' and instance.patient.user == user:
            if self.request.data.get('status') == 'cancelled':
                serializer.save(status='cancelled')
            else:
                raise PermissionDenied("Patients can only cancel appointments.")
        elif user.role == 'doctor' and instance.doctor.user == user:
            if self.request.data.get('status') == 'completed':
                serializer.save(status='completed')
            else:
                raise PermissionDenied("Doctors can only mark as completed.")
        else:
            raise PermissionDenied("You do not have permission to modify this appointment.")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_list(request):
    doctors = Doctor.objects.select_related('user').all()
    data = [
        {
            "id": doctor.id,
            "name": f"Dr. {doctor.user.first_name} {doctor.user.last_name}",
            "specialization": doctor.specialization
        }
        for doctor in doctors
    ]
    return Response(data)