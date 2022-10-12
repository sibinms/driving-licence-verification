import base64
import os

import requests
from datetime import datetime
from django.conf import settings
import json


def check_for_valid_file_format(driving_licence, user_profile):
    valid_file_formats = settings.ID_ANALYZER_VALID_FILE_FORMATS
    result = {
        "driving_licence": {
            "is_valid": False
        },
        "user_profile": {
            "is_valid": False
        }
    }
    _, driving_licence_extension = os.path.splitext(driving_licence.name)
    _, user_profile_extension = os.path.splitext(user_profile.name)

    if driving_licence_extension not in valid_file_formats:
        result['driving_licence']['is_valid'] = True

    if user_profile_extension not in valid_file_formats:
        result['user_profile']['is_valid'] = True

    return result


def get_encoded_document_image(document):
    with document.file.open('rb') as image_file:
        encoded_document_image = base64.b64encode(image_file.read())
    return encoded_document_image


def create_payload_for_id_analyser(file_base64, face_base64):
    payload = settings.ID_ANALYSER_CONFIG
    payload['apikey'] = settings.ID_ANALYZER_API_KEY
    payload['file_base64'] = file_base64
    payload['face_base64'] = face_base64
    return payload


def send_document_verification_request(payload):
    response = requests.post(
        settings.ID_ANALYZER_API_URL,
        data=payload
    )
    return response


def convert_string_date_to_date_object(string_date):
    try:
        date_format = settings.ID_ANALYSER_DATE_FORMAT
        date_object = datetime.strptime(string_date, date_format).date()
        return date_object
    except Exception:
        return None


def check_documents_are_valid(is_verified, is_identical, authenticity_score):
    if not is_verified:
        return False

    if not is_identical:
        return False

    basic_authenticity_score = settings.ID_ANALYSER_AUTHENTICITY_SCORE
    if authenticity_score < basic_authenticity_score:
        return False

    return True


def format_and_save_api_response(response, driving_licence_obj):
    try:
        response.raise_for_status()
        result = response.json()

        verification = result.get('verification', {})
        is_verified = verification.get('passed', False)
        face = result.get('face', {})
        is_identical = face.get('isIdentical', False)
        authentication = result.get('authentication', {})
        authenticity_score = authentication.get('score', 0)

        # check the validity of the document and face
        is_valid = check_documents_are_valid(
            is_verified,
            is_identical,
            authenticity_score
        )
        driving_licence_obj.is_valid = is_valid
        driving_licence_obj.authenticity_score = authenticity_score

        document_details = result.get('result', {})
        license_id = document_details.get('documentNumber', "")
        driving_licence_obj.license_id = license_id

        # address
        address = document_details.get('address1', "NA")
        if address:
            driving_licence_obj.address = address

        string_date_of_birth = document_details.get('dob', None)
        if string_date_of_birth:
            date_of_birth = convert_string_date_to_date_object(
                string_date_of_birth
            )
            driving_licence_obj.date_of_birth = date_of_birth

        string_expiry_date = document_details.get('expiry', None)
        if string_expiry_date:
            expiry_date = convert_string_date_to_date_object(
                string_expiry_date
            )
            driving_licence_obj.expiry_date = expiry_date

        string_issued_date = document_details.get('issued', None)
        if string_issued_date:
            issued_date = convert_string_date_to_date_object(
                string_issued_date
            )
            driving_licence_obj.issued_date = issued_date

        issued_country = document_details.get('issuerOrg_full', "NA")
        issued_region = document_details.get('issuerOrg_region_full', "NA")
        if issued_country and issued_region:
            driving_licence_obj.issued_by = f'{issued_country}-{issued_region}'

        driving_licence_obj.other_details = json.dumps(result)
        driving_licence_obj.task_scheduled = False
        driving_licence_obj.save()
    except Exception as inst:
        error_details = {
            "error_message": str(inst)
        }
        driving_licence_obj.other_details = json.dumps(error_details)
        driving_licence_obj.save()
