import functions_framework
import logging
from flask import jsonify
from financial_crew_ai_workflow import create_ai_financial_news_workflow

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

    try:
        text = create_ai_financial_news_workflow()
        return jsonify(
            {
                "text": text,
            }
        )

    except Exception as e:
        error_message = str(e)
        logger.error(error_message)
        return f"Error: {error_message}", 500

    return "OK"
