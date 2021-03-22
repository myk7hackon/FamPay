from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from sample_app.models import VideoDetails


def get_videos(search_text=None, limit=None, offset=None):
    if search_text:

        video_list = VideoDetails.objects.filter(
            Q(title__icontains=search_text) | Q(description__icontains=search_text)
        ).order_by("publishedAt")

    else:
        video_list = VideoDetails.objects.all().order_by("publishedAt")
    if not limit:
        paginator = Paginator(video_list, 1)
    try:
        if not offset:
            return paginator.page(1) or []
        else:
            return paginator.page(offset) or []

    except PageNotAnInteger:
        return paginator.page(1) or []
    except EmptyPage:
        return paginator.page(paginator.num_pages) or []
