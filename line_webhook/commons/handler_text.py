from commons.dialogflowcx_answer import detect_intent_text
from commons.vertex_agent_search import vertex_search_fund
from commons.flex_message_builder import build_fund_flex_message
from commons.call_crewai_api import crewai_analyze_news
from linebot.v3.messaging import (
    ReplyMessageRequest,
    TextMessage
)


def handle_text_by_keyword(event, line_bot_api):
    text = event.message.text
    if text.startswith("#กองทุน") or text.startswith("#fund"):
        search_query = text[len("#กองทุน") :].strip()
        search_query = text[len("#fund") :].strip()
        response_dict = vertex_search_fund(search_query)
        build_fund_flex_message(
            line_bot_api=line_bot_api,
            event=event,
            response_dict=response_dict,
            search_query=search_query,
        )
    elif text == "#analyse_ข่าวการเงิน":
        crewai_analyze_news(event.source.user_id)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token, messages=[TextMessage(text="กำลังวิเคราะห์ข่าวการเงิน ซึ่งอาจใช้เวลาสักครู่ ฉันจะแจ้งเมื่อเสร็จสิ้น คุณสามารถสอบถามเรื่องอื่นได้เลย")]
            )
        ) 
    else:
        from datetime import datetime
        currentDateAndTime = datetime.now()
        currentTime = currentDateAndTime.strftime("%Y%m%d%H")
        session_id = f"{event.source.user_id}_line_{currentTime}"
        print("session_ID", session_id)
        detect_intent_text(
            text=text,
            session_id=session_id,
            line_bot_api=line_bot_api,
            reply_token=event.reply_token,
        )
