from rest_framework import status
from rest_framework.response import Response

class ResponseFormatterMixin:
    """
    Global response formatting mixin for all API views
    """

    def finalize_response(self, request, response, *args, **kwargs):
        formatted_response = self._format_response_data(response)
        return super().finalize_response(request, formatted_response, *args, **kwargs)

    def _format_response_data(self, response):
        if isinstance(response, Response) and not response.exception:
            if isinstance(response.data, dict) and "message" in response.data and "data" in response.data:
                return response

            response.data = {
                "message": self._get_default_message(response),
                "data": response.data if response.data is not None else {}
            }
        return response

    def _get_default_message(self, response):
        status_code = response.status_code
        messages = {
            status.HTTP_200_OK: "Success",
            status.HTTP_201_CREATED: "Resource created successfully",
            status.HTTP_204_NO_CONTENT: "Resource deleted successfully",
            status.HTTP_400_BAD_REQUEST: "Validation error",
            status.HTTP_401_UNAUTHORIZED: "Authentication required",
            status.HTTP_403_FORBIDDEN: "Permission denied",
            status.HTTP_404_NOT_FOUND: "Resource not found",
        }
        return messages.get(status_code, "Operation completed successfully")

    def format_response(self, data=None, message=None, status=status.HTTP_200_OK):
        """
        Format the response data with a consistent structure.
        """
        return Response(
            {
                "message": message or self._get_default_message(Response(status=status)),
                "data": data if data is not None else {}
            },
            status=status
        )
