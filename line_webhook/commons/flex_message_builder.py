import json

from linebot.v3.messaging import (
    ReplyMessageRequest,
    TextMessage,
    FlexContainer,
    FlexMessage,
    FlexCarousel,
)


def build_fund_flex_message(
    line_bot_api, event, response_dict, search_query, additional_explain=None
):
    result_products_list = []
    for idx, result in enumerate(response_dict["results"]):
        fund_data = result["document"]["structData"]
        return1D_color = "#FF5555" if fund_data["return1D"] < 0 else "#00AA00"
        returnYTD_color = "#FF5555" if fund_data["returnYTD"] < 0 else "#00AA00"

        flex_message = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": fund_data["fundCode"],
                        "weight": "bold",
                        "size": "lg",
                        "wrap": True,
                    },
                    {
                        "type": "text",
                        "text": fund_data["fundNameThai"],
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True,
                    },
                    {"type": "separator", "margin": "md"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "NAV",
                                        "size": "sm",
                                        "color": "#555555",
                                        "flex": 2,
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{fund_data['NAV']} บาท",
                                        "size": "sm",
                                        "color": "#111111",
                                        "align": "end",
                                        "flex": 3,
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "เปลี่ยนแปลง (1D)",
                                        "size": "sm",
                                        "color": "#555555",
                                        "flex": 2,
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{fund_data['return1D']}%",
                                        "size": "sm",
                                        "color": return1D_color,
                                        "align": "end",
                                        "flex": 3,
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "ผลตอบแทน YTD",
                                        "size": "sm",
                                        "color": "#555555",
                                        "flex": 2,
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{fund_data['returnYTD']}%",
                                        "size": "sm",
                                        "color": returnYTD_color,
                                        "align": "end",
                                        "flex": 3,
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "Risk Level",
                                        "size": "sm",
                                        "color": "#555555",
                                        "flex": 2,
                                    },
                                    {
                                        "type": "text",
                                        "text": (
                                            f"{fund_data['riskSpectrum']} (สูง)"
                                            if fund_data["riskSpectrum"] >= 5
                                            else f"{fund_data['riskSpectrum']} (ปานกลาง)"
                                        ),
                                        "size": "sm",
                                        "color": "#111111",
                                        "align": "end",
                                        "flex": 3,
                                    },
                                ],
                            },
                        ],
                    },
                    {"type": "separator", "margin": "md"},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"ข้อมูล ณ วันที่ {str(fund_data['NAVDate'])[:4]}-{str(fund_data['NAVDate'])[4:6]}-{str(fund_data['NAVDate'])[6:]}",
                                "size": "xs",
                                "color": "#999999",
                                "flex": 1,
                                "align": "start",
                            }
                        ],
                    },
                ],
            },
        }

        json_object = json.dumps(flex_message)
        result_products_list.append(FlexContainer.from_json(json_object))

    carousel_flex_message = FlexMessage(
        alt_text=f"ผลการค้นหาสินค้า: {search_query}",
        contents=FlexCarousel(
            type="carousel",
            contents=result_products_list,
        ),
    )
    summary_text = response_dict["summary"]["summaryText"]
    messages_list = [TextMessage(text=summary_text), carousel_flex_message]
    if additional_explain:
        messages_list.insert(0, TextMessage(text=additional_explain))

    line_bot_api.reply_message(
        ReplyMessageRequest(reply_token=event.reply_token, messages=messages_list)
    )
