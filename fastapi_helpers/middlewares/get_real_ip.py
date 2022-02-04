from typing import Dict
from fastapi import Request

def get_real_ip_from_headers(
    headers: Dict,
    real_ip: str
) -> str:
    if('x-real-ip' in headers):
        return headers['x-real-ip']
    if('x-forwarded-for' in headers):
        val:str = headers['x-forwarded-for']
        val = val.split(',')[0]
        return val
    return real_ip

def get_real_ip(
    request: Request,
) -> str:
    headers = dict(request.headers)
    return get_real_ip_from_headers(headers, request.client.host)
