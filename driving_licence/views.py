from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from celery.result import AsyncResult
from django.core.exceptions import ObjectDoesNotExist

from driving_licence.models import DrivingLicence
from driving_licence.serializers import DrivingLicenceSerializer
from driving_licence.tasks import verify_driving_license_and_biometric
from driving_licence.utils import check_for_valid_file_format


class UploadDocumentsForVerification(APIView):
    """
    API for uploading licence and user profile images to check the validity
    and authenticity of the information supplied
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DrivingLicenceSerializer

    def get(self, request, *args, **kwargs):
        task_id = request.GET.get('task_id', None)
        driving_licence_id = request.GET.get('driving_licence_id', None)

        if not (task_id or driving_licence_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        task_result = AsyncResult(task_id)
        task_status = task_result.status
        if task_status == 'SUCCESS':
            try:
                driving_licence_obj = DrivingLicence.objects.get(
                    id=driving_licence_id
                )
                if driving_licence_obj.is_valid:
                    serializer = self.serializer_class(driving_licence_obj)
                    return Response(
                        data={
                            "message": "User documents are valid",
                            "data": serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
                return Response(
                    data={
                        "message": "Uploaded documents are invalid. Please try re-uploading a different document  "
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            except ObjectDoesNotExist:
                return Response(
                    data={
                        "message": "Requested user details not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        else:
            return Response(
                data={
                    "task_status": task_status,
                },
                status=status.HTTP_202_ACCEPTED
            )

    def post(self, request, *args, **kwargs):
        driving_licence = request.FILES.get("driving_licence", None)
        user_profile = request.FILES.get("user_profile", None)
        user_id = request.data.get("user_id", None)

        if not (driving_licence or user_profile or user_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        result = check_for_valid_file_format(driving_licence, user_profile)
        if not result['driving_licence']['is_valid']:
            return Response(
                data={
                    "message": "Driving licence document format is invalid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if not result['user_profile']['is_valid']:
            return Response(
                data={
                    "message": "User profile document format is invalid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
            driving_licence_obj, _ = DrivingLicence.objects.get_or_create(
                user=user
            )
            driving_licence_obj.driving_licence = driving_licence
            driving_licence_obj.profile = user_profile
            driving_licence_obj.save()

            if driving_licence_obj.task_scheduled:
                return Response(
                    data={
                        "message": "Verification is in progress"
                    },
                    status=status.HTTP_200_OK
                )

            task = verify_driving_license_and_biometric.delay(
                driving_licence_obj.id
            )
            driving_licence_obj.task_scheduled = True
            driving_licence_obj.save()
            return Response(
                data={
                    "message": "Document verification started",
                    "task_id": task.id,
                    "driving_licence_id": driving_licence_obj.id
                },
                status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
