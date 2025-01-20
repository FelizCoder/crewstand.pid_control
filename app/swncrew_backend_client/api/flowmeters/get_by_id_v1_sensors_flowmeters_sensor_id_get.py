from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.sensor import Sensor
from ...types import Response


def _get_kwargs(
    sensor_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/sensors/flowmeters/{sensor_id}",
    }

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
) -> Response[Union[HTTPValidationError, Sensor]]:
    """Get By Id

     Retrieve a specific sensor by its ID.

    Args:
        sensor_id (int): The ID of the sensor to retrieve.

    Returns:
        self.service.item_type: The sensor object with the specified ID.

    Args:
        sensor_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Sensor]]
    """

    kwargs = _get_kwargs(
        sensor_id=sensor_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sensor_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, Sensor]]:
    """Get By Id

     Retrieve a specific sensor by its ID.

    Args:
        sensor_id (int): The ID of the sensor to retrieve.

    Returns:
        self.service.item_type: The sensor object with the specified ID.

    Args:
        sensor_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Sensor]
    """

    return sync_detailed(
        sensor_id=sensor_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    sensor_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, Sensor]]:
    """Get By Id

     Retrieve a specific sensor by its ID.

    Args:
        sensor_id (int): The ID of the sensor to retrieve.

    Returns:
        self.service.item_type: The sensor object with the specified ID.

    Args:
        sensor_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Sensor]]
    """

    kwargs = _get_kwargs(
        sensor_id=sensor_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sensor_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, Sensor]]:
    """Get By Id

     Retrieve a specific sensor by its ID.

    Args:
        sensor_id (int): The ID of the sensor to retrieve.

    Returns:
        self.service.item_type: The sensor object with the specified ID.

    Args:
        sensor_id (int):

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
        )
    ).parsed
