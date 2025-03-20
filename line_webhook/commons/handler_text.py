from commons.dialogflowcx_answer import detect_intent_text
from commons.vertex_agent_search import vertex_search_fund
from commons.flex_message_builder import build_fund_flex_message


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
    else:
        detect_intent_text(
            text=text,
            session_id=event.source.user_id,
            line_bot_api=line_bot_api,
            reply_token=event.reply_token,
        )
