from prometheus_client import generate_latest
from django.http import HttpResponse


def metrics_view(request):
    return HttpResponse(
        generate_latest(),
        content_type="text/plain",
    )


# from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
# def metrics_view(request):
#     return HttpResponse(
#         generate_latest(),
#         content_type=CONTENT_TYPE_LATEST,
#     )
