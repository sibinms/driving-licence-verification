from django.urls import path

from driving_licence.views import (
    UploadDocumentsForVerification,
)

app_name = 'driving_licence'

urlpatterns = [
    path('driving-licence/upload-documents/', UploadDocumentsForVerification.as_view(),
         name='upload-verification-documents'),
]
