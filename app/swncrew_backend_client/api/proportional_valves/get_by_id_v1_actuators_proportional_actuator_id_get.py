from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.proportional_valve import ProportionalValve
from ...types import Response


def _get_kwargs(
    actuator_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/actuators/proportional/{actuator_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ProportionalValve]]:
    if response.status_code == 200:
        response_200 = ProportionalValve.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ProportionalValve]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    actuator_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, ProportionalValve]]:
    """Get By Id

     Retrieve a specific actuator by its ID.

    Args:
        actuator_id (int): The ID of the actuator to retrieve.

    Returns:
        service.item_type: The actuator object with the specified ID.

    Args:
        actuator_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ProportionalValve]]
    """

    kwargs = _get_kwargs(
        actuator_id=actuator_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    actuator_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, ProportionalValve]]:
    """Get By Id

     Retrieve a specific actuator by its ID.

    Args:
        actuator_id (int): The ID of the actuator to retrieve.

    Returns:
        service.item_type: The actuator object with the specified ID.

    Args:
        actuator_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ProportionalValve]
    """

    return sync_detailed(
        actuator_id=actuator_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    actuator_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, ProportionalValve]]:
    """Get By Id

     Retrieve a specific actuator by its ID.

    Args:
        actuator_id (int): The ID of the actuator to retrieve.

    Returns:
        service.item_type: The actuator object with the specified ID.

    Args:
        actuator_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ProportionalValve]]
    """

    kwargs = _get_kwargs(
        actuator_id=actuator_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    actuator_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, ProportionalValve]]:
    """Get By Id

     Retrieve a specific actuator by its ID.

    Args:
        actuator_id (int): The ID of the actuator to retrieve.

    Returns:
        service.item_type: The actuator object with the specified ID.

    Args:
        actuator_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ProportionalValve]
    """

    return (
        await asyncio_detailed(
            actuator_id=actuator_id,
            client=client,
        )
    ).parsed
