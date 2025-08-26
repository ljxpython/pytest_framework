"""

http 接口封装

"""

import json

from requests import Response, Session

from conf.config import settings
from src.utils.log_moudle import logger

CUSTOM_USER_AGENT = "LiJiaXin/QA/ {}"


def logger_hook(resp: Response, *args, **kwargs) -> None:
    req = resp.request
    logger.debug(f"{req.method} {resp.url}")
    request_headers = json.dumps(dict(req.headers), indent=2, ensure_ascii=False)
    logger.debug(f"Request Headers is: {request_headers}")
    req_content_type = req.headers.get("content-type", "")
    req_body = req.body or ""
    try:
        if "application/json" in req_content_type:
            req_body = json.dumps(json.loads(req_body), indent=2, ensure_ascii=False)
    except Exception as ex:
        logger.error(f"{req_body=}")
        logger.error(ex)
    if isinstance(req_body, bytes):
        req_body = req_body.decode("utf-8")
    logger.debug(f"Request Body is: {req_body}")
    content_type = resp.headers.get("content-type", "")
    is_error = False
    try:
        if "application/json" in content_type:
            json_data = resp.json()
            content = json.dumps(json_data, indent=2, ensure_ascii=False)
            is_error = "Error" in json_data.get("ResponseMetadata", {})
        else:
            content = resp.text[:200]
    except Exception as ex:
        content = resp.text[:200]
        logger.error(ex)
    if is_error:
        logger.warning(f"Respone Body is: {content}")
    else:
        logger.debug(f"Respone Body is: {content}")


class BaseClient(object):
    def __init__(self, host, timeout=10):
        self.host = host
        self.timeout = timeout
        self.session = Session()
        if settings.get("logger_hook", True):
            self.session.hooks["response"].append(logger_hook)
        # 更新 User-Agent 方便服务端日志排查
        headers = self.session.headers
        origin_user_agent = headers.get("User-Agent", "")
        new_user_agent = CUSTOM_USER_AGENT.format(origin_user_agent)
        headers["User-Agent"] = new_user_agent
        headers["Content-Type"] = "application/json; charset=utf-8"

    def request(
        self,
        method,
        path,
        params=None,
        data=None,
        json=None,
        headers=None,
        *args,
        **kwargs,
    ):
        url = self.host + path
        response = self.session.request(
            method,
            url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            timeout=self.timeout,
            *args,
            **kwargs,
        )
        return response

    def get(
        self, path, params=None, data=None, json=None, headers=None, *args, **kwargs
    ):
        return self.request(
            "GET",
            path,
            params=params,
            data=data,
            json=json,
            headers=headers,
            *args,
            **kwargs,
        )

    def post(
        self, path, params=None, data=None, json=None, headers=None, *args, **kwargs
    ):
        return self.request(
            "POST",
            path,
            params=params,
            data=data,
            json=json,
            headers=headers,
            *args,
            **kwargs,
        )

    def put(
        self, path, params=None, data=None, json=None, headers=None, *args, **kwargs
    ):
        return self.request(
            "PUT",
            path,
            params=params,
            data=data,
            json=json,
            headers=headers,
            *args,
            **kwargs,
        )

    def delete(
        self, path, params=None, data=None, json=None, headers=None, *args, **kwargs
    ):
        return self.request(
            "DELETE",
            path,
            params=params,
            data=data,
            json=json,
            headers=headers,
            *args,
            **kwargs,
        )
