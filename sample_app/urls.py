from django.urls import path

from sample_app.controller import ListingAPI

urlpatterns = [path("list", ListingAPI.as_view(), name="fetch_video_details")]
