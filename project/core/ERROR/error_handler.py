from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status

from core.ERROR.error_cases import *


def custom_exception_handler(exc, context):
    """
        DRF 의 Global Error handler 를 customizing 을 하는 것이며,
        기존의 처리는 그대로 맞기며, 그외의 경우는
        내가 만든 Global Error 을 바탕으로 만들었다.

        주로, Return 할 떄, 코드의 가독성을 위해서 만든 경우가 대부분이다.
    """
    # print("exc", exc)
    # print("type(exc)", type(exc))

    if isinstance(exc, (APIException, Http404, PermissionDenied)):
        response = drf_exception_handler(exc, context)
        # Now add the HTTP status code to the response.
        if response is not None:
            response.data['status_code'] = response.status_code
        return response

    if isinstance(exc, GlobalErrorMessage):
        return Response({
            'response': 'error',
            'message': str(exc)
        })

    if isinstance(exc, GlobalErrorMessage400):
        return Response({
            'response': 'error',
            'message': str(exc)
        }, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, GlobalErrorMessage401):
        return Response({
            'response': 'error',
            'message': str(exc)
        }, status=status.HTTP_401_UNAUTHORIZED)
