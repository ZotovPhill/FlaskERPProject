from typing import Union
from marshmallow import Schema, fields


class BaseJsonLogSchema(Schema):
    """
    Схема основного тела лога в формате JSON
    """
    thread: Union[int, str] = fields.String()
    level: int = fields.Integer()
    level_name: str = fields.String()
    message: str = fields.String()
    source: str = fields.String()
    timestamp: str = fields.DateTime()
    app_name: str = fields.String()
    app_version: str = fields.String()
    app_env: str = fields.String()
    duration: int = fields.Integer()
    exceptions: Union[list[str], str] = fields.List(fields.String)
    trace_id: str = fields.String(default=None)
    span_id: str = fields.String(default=None)
    parent_id: str = fields.String(default=None)


class RequestJsonLogSchema(Schema):
    """
    Схема части запросов-ответов лога в формате JSON
    """
    request_uri: str = fields.String()
    request_referer: str = fields.String()
    request_protocol: str = fields.String()
    request_method: str = fields.String()
    request_path: str = fields.String()
    request_host: str = fields.String()
    request_size: int = fields.Integer()
    request_content_type: str = fields.String()
    request_headers: str = fields.String()
    request_body: str = fields.String()
    request_direction: str = fields.String()
    remote_ip: str = fields.String()
    remote_port: str = fields.String()
    response_status_code: int = fields.Integer()
    response_size: int = fields.Integer()
    response_headers: str = fields.String()
    response_body: str = fields.String()
    duration: int = fields.Integer()