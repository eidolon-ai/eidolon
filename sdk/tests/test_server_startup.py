import asyncio
import logging
import time
from typing import Iterator
from unittest import mock

import pytest
import uvicorn
from fastapi import FastAPI

from eidolon_ai_sdk.bin.server import start_os


class ExceptionThrowing(Iterator):
    def __init__(self, exception: Exception):
        self.exception = exception

    def __iter__(self):
        return self

    def __next__(self):
        raise self.exception


async def test_server_logs_startup_errors():
    with pytest.raises(Exception), mock.patch("eidolon_ai_sdk.bin.server.logger.exception") as exception_logger:
        async with start_os(
            FastAPI(),
            ExceptionThrowing(Exception("mocked exception")),
            "test_machine",
            log_level=logging.INFO,
        ):
            pass
    assert exception_logger.called

