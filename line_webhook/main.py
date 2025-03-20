import os
import logging
import functions_framework

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    LocationMessageContent,
    StickerMessageContent,
    ImageMessageContent,
    AudioMessageContent,
    PostbackEvent,
    BeaconEvent,
    FollowEvent,
    UnfollowEvent,
    JoinEvent,
    MemberJoinedEvent,
)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage,
    StickerMessage,
    FlexMessage,
    FlexContainer,
    ShowLoadingAnimationRequest,
    MentionSubstitutionObject,
    TextMessageV2,
    UserMentionTarget,
)


from commons.gcs_utils import upload_blob_from_memory
from commons.gemini_image_understanding import gemini_describe_image
from commons.handler_text import handle_text_by_keyword


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]


configuration = Configuration(
    access_token=CHANNEL_ACCESS_TOKEN,
)
handler = WebhookHandler(CHANNEL_SECRET)

# Create a global API client instance
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)
line_bot_blob_api = MessagingApiBlob(api_client)


@functions_framework.http
def callback(request):
    logger.info("--- Incoming Request Details ---")
    logger.info(f"Method: {request.method}")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"URL: {request.url}")
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    line_bot_api.show_loading_animation_with_http_info(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )
    handle_text_by_keyword(event, line_bot_api)


@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    line_bot_api.show_loading_animation_with_http_info(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )

    message_content = line_bot_blob_api.get_message_content(message_id=event.message.id)
    upload_blob_from_memory(
        contents=message_content,
        user_id=event.source.user_id,
        message_id=event.message.id,
        type="image",
    )

    image_description = gemini_describe_image(
        user_id=event.source.user_id,
        message_id=event.message.id,
    )

    print("Image description: " + image_description)


@handler.add(MessageEvent, message=AudioMessageContent)
def handle_audio_message(event):
    line_bot_api.show_loading_animation_with_http_info(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )
    audio_content = line_bot_blob_api.get_message_content(message_id=event.message.id)
    upload_blob_from_memory(
        contents=audio_content,
        user_id=event.source.user_id,
        message_id=event.message.id,
        type="audio",
    )

    print("Audio content uploaded to GCS")


@handler.add(MessageEvent, message=LocationMessageContent)
def handle_location_message(event):
    line_bot_api.show_loading_animation_with_http_info(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )

    latitude = event.message.latitude
    longitude = event.message.longitude
    print("Location message received:  {} {}".format(latitude, longitude))


@handler.add(MessageEvent, message=StickerMessageContent)
def handle_sticker_message(event):
    line_bot_api.show_loading_animation_with_http_info(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                StickerMessage(
                    package_id=event.message.package_id,
                    sticker_id=event.message.sticker_id,
                )
            ],
        )
    )


@handler.add(PostbackEvent)
def handle_postback(event: PostbackEvent):
    print("Got Postback event:" + event.source.user_id)


@handler.add(BeaconEvent)
def handle_beacon(event: BeaconEvent):
    print("Got Beacon event:" + event.source.user_id)


@handler.add(FollowEvent)
def handle_follow(event):
    print("Got Follow event:" + event.source.user_id)
    profile = line_bot_api.get_profile(user_id=event.source.user_id)
    if event.follow.is_unblocked:
        text_message = TextMessage(
            text="สวัสดีค่ะ คุณ "
            + profile.display_name
            + " ยินดีต้อนรับกลับเข้าสู่แชทบอทของ​ Beat Finanical Agent อีกครั้งนะค่ะ\n\nแชทบอท 'น้อง Beat' 👧🏻 จะขอเป็นผู้ช่วยของคุณในการเงินเองค่ะ"
        )

    else:
        text_message = TextMessage(
            text="สวัสดีค่ะ คุณ "
            + profile.display_name
            + " ยินดีต้อนรับสู่​ Beat Finanical Agent! แชทบอท 'น้อง Beat' 👧🏻 \nจะขอเป็นผู้ช่วยการเงินของ"
        )

    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                text_message,
            ],
        )
    )


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print("Got Unfollow event:" + event.source.user_id)
