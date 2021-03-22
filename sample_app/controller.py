import json

from django.core import serializers
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods

from sample_app.handler import get_videos


@method_decorator(
    [require_http_methods(["GET"])],
    name="dispatch",
)
class ListingAPI(View):
    def get(self, request):
        query_params = request.GET.dict()

        search_text = query_params.get("q")
        limit = query_params.get("limit")
        offset = query_params.get("offset")
        if isinstance(offset, int):
            offset = int(offset)
        result = get_videos(search_text=search_text, limit=limit, offset=offset)
        if result:
            data = serializers.serialize("json", list(result))
        else:
            data = []
        next_route = str(reverse("sample_app:fetch_video_details"))
        if isinstance(offset, int):
            next_route += "&offset=" + str(offset + 1)
        else:
            next_route += "&offset={new_offset}".format(new_offset=1)
        return JsonResponse(
            {
                "data": [item["fields"] for item in json.loads(data)] if data else [],
                "next": next_route,
            }
        )
