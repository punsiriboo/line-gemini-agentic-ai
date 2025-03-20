import functions_framework
import logging
from flask import jsonify
from vertex_agent_search import vertex_search_fund

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
        request_json = request.get_json(silent=True)
        if request_json and isinstance(request_json, dict):
            logger.info("Request body is JSON")
            # Extract data from JSON body
            search_query = int(request_json.get("search_query", 0))
            result_json = vertex_search_fund(search_query=search_query)
            return jsonify(result_json)
        else:   
            return "Error: Request body is NOT JSON", 400
    except Exception as e:
        error_message = str(e)
        logger.error(error_message)
        return f"Error: {error_message}", 500

