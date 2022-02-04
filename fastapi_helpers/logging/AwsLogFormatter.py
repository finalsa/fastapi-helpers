import logging
from orjson import dumps
from typing import Mapping
from watchtower import _json_serialize_default


class AwsLogFormatter(logging.Formatter):

    def __init__(self, msg, *args, json_serialize_default: callable = None, add_log_record_attrs: tuple = None, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.json_serialize_default = _json_serialize_default
        if json_serialize_default is not None:
            self.json_serialize_default = json_serialize_default
        if add_log_record_attrs is not None:
            self.add_log_record_attrs = add_log_record_attrs
        else:
            self.add_log_record_attrs = []

    def format(self, record: logging.LogRecord):
        
        msg = {
            "log_level": record.levelname,
            "message":  super().format(record)
        }
        if record.exc_info and not record.exc_text:
            msg["message.exception"] = self.formatException(record.exc_info)    
        if record.exc_text:
            msg["message.exc_text"] = record.exc_text
        if record.stack_info:
            msg["stack_trace"] = self.formatStack(record.stack_info,)
      
        """
        items = record.__dict__
        
        for item in items:
            msg[item] = items[item]
        """
        for field in self.add_log_record_attrs:
            value = getattr(record, field, None)
            if(value):
                msg[field] = value
        
        record.msg = msg        
        return dumps(record.msg, default=self.json_serialize_default).decode("utf-8")
