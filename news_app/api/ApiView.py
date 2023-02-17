from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView as BaseAPIView
from rest_framework_swagger import renderers

from .helpers.SwaggerAPICodec import SwaggerAPICodec


class ApiView(BaseAPIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer,
    ]

    def get(self, request):
        codec = SwaggerAPICodec()
        bytestr = open('api/swagger.yaml', 'rb').read()
        schema = codec.decode(bytestr)
        return Response(schema)
