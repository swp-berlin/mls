from django.utils.http import parse_header_parameters

from rest_framework import serializers
from rest_framework.exceptions import UnsupportedMediaType
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from mls.utils.embedding import embed, embed_query
from mls.utils.extract import get_extractor
from mls.utils.timed import timed

from .router import router

__all__ = [
    'ExtractView',
    'EmbeddingView',
    'QueryEmbeddingView',
]


def get_media_type(content_type: str):
    media_type, params = parse_header_parameters(content_type)

    return media_type


@router.register('extract', basename='extract')
class ExtractView(APIView):
    parser_classes = [FileUploadParser]

    @staticmethod
    def extract(request: Request):
        media_type = get_media_type(request.content_type)
        extractor = get_extractor(media_type)

        if extractor is None:
            raise UnsupportedMediaType(media_type)

        obj = request.data.get('file')

        return extractor(obj)

    def post(self, request: Request):
        text = self.extract(request)

        return Response(text, content_type='text/plain')

    def put(self, request: Request, filename: str):
        assert filename, 'No filename present.'

        return self.post(request)


@router.register('embedding', basename='embedding')
class EmbeddingView(ExtractView):

    @timed
    def post(self, request: Request):
        text = self.extract(request)

        if embedding := embed(text):
            return Response(embedding)

        return Response(status=HTTP_204_NO_CONTENT)


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(allow_blank=False)


@router.register('query-embed', basename='query-embed')
class QueryEmbeddingView(GenericAPIView):
    serializer_class = QuerySerializer

    @timed
    def get(self, request):
        serializer: QuerySerializer = self.get_serializer(data=request.query_params)

        serializer.is_valid(raise_exception=True)

        embedding = embed_query(**serializer.validated_data)

        return Response(embedding)
