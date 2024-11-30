from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class IndexForApi(APIView):
    def get(self, request):
        return Response({"Index for lab 3 API"})
