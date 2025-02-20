import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEETS_CREDENTIALS

def get_affiliate_products():
    creds = json.loads(GOOGLE_SHEETS_CREDENTIALS)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
    client = gspread.authorize(credentials)

    sheet = client.open("Your Google Sheet Name").sheet1
    return sheet.get_all_records()

def match_product(problem):
    products = get_affiliate_products()
    for product in products:
        if product["keyword"].lower() in problem.lower():
            return product["name"], product["link"]
    return None, None
