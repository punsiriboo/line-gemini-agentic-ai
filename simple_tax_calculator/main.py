import functions_framework
import logging
from flask import jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@functions_framework.http
def callback(request):
    logger.info("--- Incoming Request Details ---")
    logger.info(f"Method: {request.method}")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"URL: {request.url}")
    logger.info(f"Arguments: {dict(request.args)}")

    # Accessing arguments from the request
    request_args = request.args

    # get request body as text
    body = request.get_data(as_text=True)
    logger.info("Request body: " + body)

    try:
        # Try to parse the body as JSON
        request_json = request.get_json(silent=True)
        if request_json and isinstance(request_json, dict):
            logger.info("Request body is JSON")
            # Extract data from JSON body
            monthly_income = int(request_json.get("monthly_income", 0))
            use_personal_allowance = request_json.get("use_personal_allowance", False)
            use_spouse_allowance = request_json.get("use_spouse_allowance", False)
            num_children = int(request_json.get("num_children", 0))
            insurance_premium = int(request_json.get("insurance_premium", 0))
            social_security = int(request_json.get("social_security", 0))
        else:
            logger.info("Request body is NOT JSON, using query parameters")
            # Example of getting specific arguments from query parameters, with default values if not present
            monthly_income = int(request_args.get("monthly_income", 0))
            use_personal_allowance = (
                request_args.get("use_personal_allowance", "False").lower() == "true"
            )
            use_spouse_allowance = (
                request_args.get("use_spouse_allowance", "False").lower() == "true"
            )
            num_children = int(request_args.get("num_children", 0))
            insurance_premium = int(request_args.get("insurance_premium", 0))
            social_security = int(request_args.get("social_security", 0))

        # Calculate tax
        tax, total_deductions, gross_income = calculate_personal_income_tax(
            monthly_income,
            use_personal_allowance,
            use_spouse_allowance,
            num_children,
            insurance_premium,
            social_security,
        )
        logger.info(f"ภาษีที่ต้องชำระ: {tax:.2f} บาท")
        return jsonify(
            {
                "total_deductions": f"{total_deductions:.2f}",
                "gross_income": f"{gross_income:.2f}",
                "tax_to_pay": f"{tax:.2f}",
            }
        )

    except Exception as e:
        error_message = str(e)
        logger.error(error_message)
        return f"Error: {error_message}", 500

    return "OK"


# ฟังก์ชันคำนวณภาษีเงินได้บุคคลธรรมดา
def calculate_personal_income_tax(
    monthly_income,
    use_personal_allowance=True,
    use_spouse_allowance=False,
    num_children=0,
    insurance_premium=0,
    social_security=0,
):
    # คำนวณรายได้รวมต่อปี
    gross_income = monthly_income * 12

    # กำหนดค่าลดหย่อน
    personal_allowance_amount = 60000 if use_personal_allowance else 0
    spouse_allowance_amount = 60000 if use_spouse_allowance else 0
    children_allowance_amount = num_children * 30000

    # รวมค่าลดหย่อนทั้งหมด
    total_deductions = (
        personal_allowance_amount
        + spouse_allowance_amount
        + children_allowance_amount
        + insurance_premium
        + social_security
    )

    # คำนวณเงินได้สุทธิ
    net_income = gross_income - total_deductions

    # อัตราภาษีตามขั้นเงินได้สุทธิ
    tax_brackets = [
        (5000000, 0.35),
        (2000000, 0.30),
        (1000000, 0.25),
        (750000, 0.20),
        (500000, 0.15),
        (300000, 0.10),
        (150000, 0.05),
        (0, 0.00),
    ]

    # คำนวณภาษี
    tax = 0
    for bracket in tax_brackets:
        if net_income > bracket[0]:
            tax += (net_income - bracket[0]) * bracket[1]
            net_income = bracket[0]

    return tax, total_deductions, gross_income


# ตัวอย่างการใช้งาน
# monthly_income = 50000      # รายได้ต่อเดือน
# personal_allowance = True   # ใช้ค่าลดหย่อนส่วนตัว
# spouse_allowance = False    # ไม่มีคู่สมรสที่ไม่มีรายได้
# num_children = 2            # จำนวนบุตร
# insurance_premium = 20000   # เบี้ยประกันชีวิต
# social_security = 9000      # ประกันสังคม

# # เรียกใช้ฟังก์ชัน
# tax = calculate_personal_income_tax(monthly_income, personal_allowance,
#                                     spouse_allowance, num_children,
#                                     insurance_premium, social_security)

# print(f'ภาษีที่ต้องชำระ: {tax:.2f} บาท')
