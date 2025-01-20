from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.sensor import Sensor
from ...models.sensor_reading import SensorReading
from ...types import Response


def _get_kwargs(
    sensor_id: int,
    *,
    body: SensorReading,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/v1/sensors/flowmeters/{sensor_id}/reading",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, Sensor]]:
    if response.status_code == 200:
        response_200 = Sensor.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, Sensor]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sensor_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SensorReading,
) -> Response[Union[HTTPValidationError, Sensor]]:
    """Post Reading

     Post a new reading for a specific sensor.

    Args:
        sensor_id (int): The ID of the sensor.
        reading (SensorReading): The new reading to update.

    Returns:
        self.service.item_type: The updated sensor object.

    Args:
        sensor_id (int):
        body (SensorReading): Base model for a sensor reading.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Sensor]]
    """

    kwargs = _get_kwargs(
        sensor_id=sensor_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sensor_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SensorReading,
) -> Optional[Union[HTTPValidationError, Sensor]]:
    """Post Reading

     Post a new reading for a specific sensor.

    Args:
        sensor_id (int): The ID of the sensor.
        reading (SensorReading): The new reading to update.

    Returns:
        self.service.item_type: The updated sensor object.

    Args:
        sensor_id (int):
        body (SensorReading): Base model for a sensor reading.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Sensor]
    """

    return sync_detailed(
        sensor_id=sensor_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    sensor_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SensorReading,
) -> Response[Union[HTTPValidationError, Sensor]]:
    """Post Reading

     Post a new reading for a specific sensor.

    Args:
        sensor_id (int): The ID of the sensor.
        reading (SensorReading): The new reading to update.

    Returns:
        self.service.item_type: The updated sensor object.

    Args:
        sensor_id (int):
        body (SensorReading): Base model for a sensor reading.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Sensor]]
    """

    kwargs = _get_kwargs(
        sensor_id=sensor_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sensor_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SensorReading,
) -> Optional[Union[HTTPValidationError, Sensor]]:
    """Post Reading

     Post a new reading for a specific sensor.

    Args:
        sensor_id (int): The ID of the sensor.
        reading (SensorReading): The new reading to update.

    Returns:
        self.service.item_type: The updated sensor object.

    Args:
        sensor_id (int):
        body (SensorReading): Base model for a sensor reading.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Sensor]
    """

    return (
        await asyncio_detailed(
            sensor_id=sensor_id,
            client=client,
            body=body,
        )
    ).parsed
