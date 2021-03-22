import logging
import os
from datetime import datetime, timedelta

import dateutil.parser
import requests
from celery.decorators import periodic_task
from celery.task.schedules import crontab

from sample_app.models import VideoDetails


@periodic_task(
    run_every=timedelta(seconds=int(os.environ.get("BACKGROUND_JOB_FREQUENCY", 10))),
    name="fetch_task",
    ignore_result=True,
)
def fetch_latest_videos():
    status = "FAILED"
    while status != "PASSED":
        key_values = os.environ["API_KEY"].split(".")
        for key in key_values:
            last_time = datetime.now() - timedelta(
                seconds=int(os.environ.get("BACKGROUND_JOB_FREQUENCY", 10))
            )
            last_time_iso_format = last_time.strftime("%Y-%m-%dT%H:%M:%S%Z") + "Z"
            time_now_iso_format = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%Z") + "Z"
            params = {
                "key": key,
                "q": "flying",
                "part": "snippet",
                "publishedAfter": last_time_iso_format,
                "publishedBefore": time_now_iso_format,
            }
            response = requests.get(
                "https://www.googleapis.com/youtube/v3/search", params=params
            )

            if response.status_code == 200:
                response = response.json()
                item_list = []
                for item in response["items"]:
                    try:
                        VideoDetails.objects.get(videoId=item["id"]["videoId"])
                    except VideoDetails.DoesNotExist:

                        item_list.append(
                            VideoDetails(
                                title=item["snippet"]["title"],
                                description=item["snippet"]["description"],
                                publishedAt=dateutil.parser.parse(
                                    item["snippet"]["publishedAt"]
                                ),
                                videoId=item["id"]["videoId"],
                            )
                        )

                VideoDetails.objects.bulk_create(item_list)
                status = "PASSED"
                break

            else:
                logging.exception("Cron Job Failed")
        break
