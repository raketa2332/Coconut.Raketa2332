import json
import logging
import os

import requests
from pydantic import BaseModel


class CustomRequester:
    """Кастомный реквестер для стандартизации и упрощения HTTP-запросов."""

    base_headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(self, method, endpoint, params=None, data=None, expected_status=200, need_logging=True):
        if isinstance(data, BaseModel):
            data = json.loads(data.model_dump_json(by_alias=True, exclude_unset=True))

        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method=method, url=url, json=data, headers=self.headers, params=params)

        if need_logging:
            self.log_request_and_response(response)

        if response.status_code != expected_status:
            raise ValueError(f"Unexpected status code: {response.status_code}. Expected: {expected_status}")

        return response

    def update_session_headers(self, **kwargs):
        self.headers.update(kwargs)
        self.session.headers.update(self.headers)

    # def log_request_and_response(self, response):
    #     try:
    #         request = response.request
    #         GREEN = "\033[32m"
    #         RED = "\033[31m"
    #         RESET = "\033[0m"
    #         headers = "\\\n".join([f"-H'{header}: {value}'" for header, value in request.headers.items()])
    #         full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace('(call)', '')}"
    #
    #         body = ""
    #         if hasattr(request, "body") and request.body is not None:
    #             if isinstance(request.body, bytes):
    #                 body = request.body.decode("utf-8")
    #             body = f"-d '{body}' \n" if body != "{}" else ""
    #
    #         # Логируем запрос
    #         self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
    #         self.logger.info(
    #             f"{GREEN}{full_test_name}{RESET}\ncurl -X {request.method} '{request.url}'{headers} \\\n{body}"
    #         )
    #
    #         # Обрабатываем ответ
    #         response_status = response.status_code
    #         is_success = response.ok
    #         response_data = response.text
    #
    #         # Попытка форматировать JSON
    #         try:
    #             response_data = json.dump(json.load(response.text), indent=4, ensure_ascii=False)
    #         except json.JSONDecodeError:
    #             pass  # Оставляем текст, если это не JSON
    #
    #         # Логируем ответ
    #         self.logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
    #         if not is_success:
    #             self.logger.info(f"\nSTATUS_CODE: {RED}{response_status}{RESET}\nDATA: {RED}{response_data}{RESET}")
    #         else:
    #             self.logger.info(f"\nSTATUS_CODE: {GREEN}{response_status}{RESET}\nDATA:\n{response_data}")
    #
    #         self.logger.info(f"{'=' * 80}\n")
    #     except Exception as e:
    #         self.logger.error(f"\nLogging failed {type(e)} - {e}")
    def log_request_and_response(self, response):
        """
        Логгирование запросов и ответов. Настройки логгирования описаны в pytest.ini
        Преобразует вывод в curl-like (-H хэдэеры), (-d тело)

        :param response: Объект response получаемый из метода "send_request"
        """
        try:
            request = response.request
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                elif isinstance(request.body, str):
                    body = request.body
                body = f"-d '{body}' \n" if body != '{}' else ''

            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_status = response.status_code
            is_success = response.ok
            response_data = response.text
            if not is_success:
                self.logger.info(f"\tRESPONSE:"
                                 f"\nSTATUS_CODE: {RED}{response_status}{RESET}"
                                 f"\nDATA: {RED}{response_data}{RESET}")
        except Exception as e:
            self.logger.info(f"\nLogging went wrong: {type(e)} - {e}")