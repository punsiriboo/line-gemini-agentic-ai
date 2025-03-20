import functions_framework
import logging
from flask import jsonify
from financial_crew_ai_workflow import create_ai_financial_news_workflow
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
    FlexContainer,
    FlexCarousel,
    FlexMessage,
)


@functions_framework.http
def callback(request):
    logger.info("--- Incoming Request Details ---")
    logger.info(f"Method: {request.method}")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"URL: {request.url}")
    logger.info(f"Arguments: {dict(request.args)}")

    try:
        
        text = create_ai_financial_news_workflow()
        json_data = json.loads(text)
        print(json_data)
        news_title = json_data[0]["title"]
        news_summary = json_data[0]["summary"]
        bubble_string = {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://storage.googleapis.com/punsiriboo_public/finance_news_title.png",
                        "size": "full",
                        "aspectRatio": "25:10",
                        "aspectMode": "cover"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": news_title,
                            "weight": "bold",
                            "size": "xl",
                            "wrap": True
                        },
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": news_summary,
                                "wrap": True
                            }
                            ]
                        }
                        ]
                    }
                }

        CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
        configuration = Configuration(
            access_token=CHANNEL_ACCESS_TOKEN,
        )

        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            request_json = request.get_json(silent=True)
            if request_json and isinstance(request_json, dict):
                logger.info("Request body is JSON")
                line_user_id = str(request_json.get("line_user_id", ""))
                line_bot_api.push_message(
                    PushMessageRequest(
                        to=line_user_id, 
                        messages=[TextMessage(text=text)]
                    )
                )
                my_flex_message = FlexMessage(
                    alt_text="hello",
                    contents=FlexCarousel(
                        type="carousel",
                        contents=[
                            FlexContainer.from_dict(bubble_string),
                        ],
                    ),
                )
                line_bot_api.reply_message(
                    PushMessageRequest(
                        to=line_user_id, messages=[my_flex_message]
                    )
                )
                
    except Exception as e:
        error_message = str(e)
        logger.error(error_message)
        return f"Error: {error_message}", 500

    return "OK"
