import time
import json
import math
import http
import logging
from werkzeug.wrappers import Request, Response
from app.orm.schemas.logging import RequestJsonLogSchema
from flask.logging import default_handler


logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, app):
        self.app = app
    
    """
    Middleware для обработки запросов и ответов с целью журналирования
    """
    @staticmethod
    async def get_protocol(request: Request) -> str:
        protocol = str(request.scope.get('type', ''))
        http_version = str(request.scope.get('http_version', ''))
        if protocol.lower() == 'http' and http_version:
            return f'{protocol.upper()}/{http_version}'
        return {}

    @staticmethod
    async def set_body(request: Request, body: bytes) -> None:
        async def receive() -> dict:
            return {'type': 'http.request', 'body': body}

        request._receive = receive

    async def get_body(self, request: Request) -> bytes:
        body = await request.data
        await self.set_body(request, body)
        return body

    async def __call__(self, environ, start_response):
        start_time = time.time()
        exception_object = None
        # Request Side
        request = Request(environ)
        try:
            raw_request_body = await request.data
            # Последующие действия нужны, 
            # чтобы не перезатереть тело запроса
						# и не уйти в зависание event-loop'a
            # при последующем получении тела ответа
            await self.set_body(request, raw_request_body)
            raw_request_body = await self.get_body(request)
            request_body = raw_request_body.decode()
        except Exception:
            request_body = {}

        server: tuple = request.get('server', ('localhost', '5000'))
        request_headers: dict = dict(request.headers.items())
        # Response Side
        try:
            response = await start_response()
        except Exception as ex:
            response_body = bytes(
                http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase.encode()
            )
            response = Response(
                response_body,
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR.real,
            )
            exception_object = ex
            response_headers = {}
        else:
            response_headers = dict(response.headers.items())
            response_body = b''
            async for chunk in response.body_iterator:
                response_body += chunk
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
        duration: int = math.ceil((time.time() - start_time) * 1000)
				# Инициализация и формирования полей для запроса-ответа
        request_json_fields = RequestJsonLogSchema(
            request_uri=str(request.url),
            request_referer=request_headers.get('referer', {}),
            request_protocol=await self.get_protocol(request),
            request_method=request.method,
            request_path=request.url.path,
            request_host=f'{server[0]}:{server[1]}',
            request_size=int(request_headers.get('content-length', 0)),
            request_content_type=request_headers.get('content-type', {}),
            request_headers=json.dumps(request_headers),
            request_body=request_body,
            request_direction='in',
            remote_ip=request.client[0],
            remote_port=request.client[1],
            response_status_code=response.status_code,
            response_size=int(response_headers.get('content-length', 0)),
            response_headers=json.dumps(response_headers),
            response_body=response_body.decode(),
            duration=duration
        ).dict()
        message = f'{"Error" if exception_object else "Response"} ' \
                  f'with status code {response.status_code} ' \
                  f'on request {request.method} \"{str(request.url)}\", ' \
                  f'in {duration} ms'
        logger.info(
            message,
            extra={
                'request_json_fields': request_json_fields,
                'to_mask': True,
            },
            exc_info=exception_object,
        )
        return response