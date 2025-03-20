import sys
import requests
import os
import linebot
from dotenv import load_dotenv
load_dotenv()

from linebot.v3.messaging import (
    RichMenuRequest,
    CreateRichMenuAliasRequest
)
from linebot.v3.messaging.rest import ApiException
from pprint import pprint


configuration = linebot.v3.messaging.Configuration(
    host="https://api.line.me",
    access_token=os.getenv("CHANNEL_ACCESS_TOKEN")
)

api_client = linebot.v3.messaging.ApiClient(configuration) 
api_instance = linebot.v3.messaging.MessagingApi(api_client)


def create_rich_menus(rich_menu_files):
    """Creates multiple rich menus based on a list of JSON files.

    Args:
        rich_menu_files: A list of paths to rich menu JSON files.
    """

    for rich_menu_file in rich_menu_files:
        try:
            with open(f"{rich_menu_file}", "r") as f:  # Construct path correctly
                richmenu_json = f.read()

            rich_menu_request = RichMenuRequest.from_json(richmenu_json)
            api_response = api_instance.create_rich_menu(rich_menu_request=rich_menu_request) # Corrected parameter name
            print(f"Successfully created rich menu from {rich_menu_file}:")
            pprint(api_response)

            # Extract the rich menu ID from the response for later use (e.g., image upload)
            rich_menu_id = api_response.rich_menu_id
            print(f"Rich menu ID: {rich_menu_id}")
            
        except FileNotFoundError:
            print(f"Error: Rich menu JSON file not found: {rich_menu_file}")
        except ApiException as e:
            print(f"Error creating rich menu from {rich_menu_file}: {e}")
        except Exception as e:  # Catch other potential errors
             print(f"An unexpected error occurred processing {rich_menu_file}: {e}")

        # Example of how to then upload the image:
        image_path = f"{rich_menu_file.replace('.json', '.jpg')}" # Assuming image file follows a naming convention

        try:
            upload_rich_menu_image(rich_menu_id, image_path) 
        except Exception as image_upload_error:
            print(f"Error uploading image for {rich_menu_file}: {image_upload_error}")
        
        create_rich_menu_alias_request = CreateRichMenuAliasRequest(
            rich_menu_alias_id=rich_menu_file.replace('.json', ''),
            rich_menu_id = rich_menu_id
        ) 
        try:
            api_response = api_instance.create_rich_menu_alias(create_rich_menu_alias_request)
            print("The response of MessagingApi->create_rich_menu_alias:\n")
            pprint(api_response)
        except Exception as e:
            print("Exception when calling MessagingApi->create_rich_menu_alias: %s\n" % e)


def upload_rich_menu_image(rich_menu_id, image_path):
    """Uploads an image to a rich menu."""
    headers = {
        'Authorization': f'Bearer {os.getenv("CHANNEL_ACCESS_TOKEN")}',
        'Content-Type': 'image/jpeg'  # Or the appropriate content type
    }
    url = f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content"
    try:
        with open(image_path, "rb") as image_file:
            response = requests.post(url, headers=headers, data=image_file)
            response.raise_for_status()
            print(f"Successfully uploaded image to rich menu {rich_menu_id}")
    except Exception as e:
        raise Exception(f"Error uploading image: {e}")  # Re-raise for the calling function to handle




# Example usage:
list_rich_menu = [
    "rich_menu_content.json",
]
create_rich_menus(list_rich_menu)
