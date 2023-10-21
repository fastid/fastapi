import uuid

import httpx
import pytest
from fastapi.applications import FastAPI
from httpx import ConnectTimeout
from pytest_httpx import HTTPXMock

from fastid.http_base_client import http_base_client
from fastid.logger import cxt_request_id

URL_HTTP_TEST_SERVER = 'https://render.httpbin.dmuth.org/'


async def test_http_base_client(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={
            'args': {},
            'headers': {
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9',
                'Host': 'httpbin.org',
                'User-Agent': 'Iperon',
                'X-Amzn-Trace-Id': 'Root=1-63e13139-236293ce7f43fb367d5cb2a1',
            },
            'origin': '8.8.8.8',
            'url': f'{URL_HTTP_TEST_SERVER}/get',
        },
    )

    async with http_base_client() as client:
        response: httpx.Response = await client.get(url=f'{URL_HTTP_TEST_SERVER}/get')
        assert response.json().get('headers').get('Accept')
        assert response.json().get('headers').get('Accept-Encoding')
        assert response.json().get('headers').get('Accept-Language')
        assert response.json().get('headers').get('User-Agent')


async def test_http_base_errors(app: FastAPI, client: httpx.AsyncClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=httpx.codes.INTERNAL_SERVER_ERROR)
    async with http_base_client() as client:
        response: httpx.Response = await client.get(url=f'{URL_HTTP_TEST_SERVER}/status/500')

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            assert exc.response.status_code == httpx.codes.INTERNAL_SERVER_ERROR
            assert exc.request.url == f'{URL_HTTP_TEST_SERVER}/status/500'


async def test_http_timeout(app: FastAPI, client: httpx.AsyncClient):
    async with http_base_client(timeout=0.01) as client:
        try:
            await client.get(url=f'{URL_HTTP_TEST_SERVER}/get')
        except ConnectTimeout:
            assert 1 == 1

    with pytest.raises(ConnectTimeout):
        async with http_base_client(timeout=0.01) as client:
            await client.get(url=f'{URL_HTTP_TEST_SERVER}/get')


async def test_http_base_client_request_id(httpx_mock: HTTPXMock):
    request_id = str(uuid.uuid4())

    httpx_mock.add_response(
        json={
            'args': {},
            'headers': {
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9',
                'Request-Id': f'{request_id}',
                'Host': 'httpbin.org',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                'X-Amzn-Trace-Id': 'Root=1-63e1345b-509ee9773d534eaa0290bfeb',
            },
            'origin': '8.8.8.8',
            'url': f'{URL_HTTP_TEST_SERVER}/get',
        },
    )

    cxt_request_id.set(request_id)

    async with http_base_client() as client:
        response: httpx.Response = await client.get(url=f'{URL_HTTP_TEST_SERVER}/get')
        assert response.json().get('headers').get('Request-Id') == request_id
