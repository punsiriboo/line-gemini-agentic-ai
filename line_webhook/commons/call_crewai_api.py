def crewai_analyze_news(line_user_id:str):
    import requests
    import json

    url = "https://asia-southeast1-dataaibootcamp.cloudfunctions.net/call_crew_ai_execution"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "line_user_id": line_user_id
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # ตรวจสอบว่าคำขอสำเร็จหรือไม่
        print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error:", e)