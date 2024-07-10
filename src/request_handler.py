import json
from typing import Any, Dict


def get_headers() -> dict:
    headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "OPTIONS, GET, PUT, POST",
               "Access-Control-Allow-Headers": "*", 'Access-Control-Allow-Credentials': True,
               "Content-Type": "application/json"}
    return headers


def data_response(data) -> Dict[str, Any]:
    """
    Formats a successful API response as a dictionary object with status code 200.
    """
    return {'statusCode': 200, 'headers': get_headers(), 'body': json.dumps(data)}
