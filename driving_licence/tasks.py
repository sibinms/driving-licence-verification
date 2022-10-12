from celery import shared_task

from driving_licence.models import DrivingLicence
from driving_licence.utils import (
    get_encoded_document_image,
    create_payload_for_id_analyser,
    send_document_verification_request,
    format_and_save_api_response,
)


@shared_task
def verify_driving_license_and_biometric(driving_licence_id):
    driving_licence_obj = DrivingLicence.objects.get(
        id=driving_licence_id
    )
    # encode the images
    base64_licence = get_encoded_document_image(
        driving_licence_obj.driving_licence
    )
    base64_user_profile = get_encoded_document_image(
        driving_licence_obj.profile
    )

    # create payload
    payload = create_payload_for_id_analyser(
        base64_licence,
        base64_user_profile
    )

    # send request to ID Analyser
    response = send_document_verification_request(payload)

    # formatting and saving the response
    format_and_save_api_response(response, driving_licence_obj)
