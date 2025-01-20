from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.proportional_valve import ProportionalValve
from ...models.pump import Pump
from ...models.solenoid_valve import SolenoidValve
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/actuators/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list[Union["ProportionalValve", "Pump", "SolenoidValve"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:

            def _parse_response_200_item(data: object) -> Union["ProportionalValve", "Pump", "SolenoidValve"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    response_200_item_type_0 = SolenoidValve.from_dict(data)

                    return response_200_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    response_200_item_type_1 = ProportionalValve.from_dict(data)

                    return response_200_item_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_item_type_2 = Pump.from_dict(data)

                return response_200_item_type_2

            response_200_item = _parse_response_200_item(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list[Union["ProportionalValve", "Pump", "SolenoidValve"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[list[Union["ProportionalValve", "Pump", "SolenoidValve"]]]:
    """Get All Actuators

     Retrieve a list of all actuators, including solenoid valves, proportional valves, and pumps.

    Returns:
        List[Union[SolenoidValve, ProportionalValve, Pump]]: A list containing all the actuators.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[Union['ProportionalValve', 'Pump', 'SolenoidValve']]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[list[Union["ProportionalValve", "Pump", "SolenoidValve"]]]:
    """Get All Actuators

     Retrieve a list of all actuators, including solenoid valves, proportional valves, and pumps.

    Returns:
        List[Union[SolenoidValve, ProportionalValve, Pump]]: A list containing all the actuators.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[Union['ProportionalValve', 'Pump', 'SolenoidValve']]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[list[Union["ProportionalValve", "Pump", "SolenoidValve"]]]:
    """Get All Actuators

     Retrieve a list of all actuators, including solenoid valves, proportional valves, and pumps.

    Returns:
        List[Union[SolenoidValve, ProportionalValve, Pump]]: A list containing all the actuators.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[Union['ProportionalValve', 'Pump', 'SolenoidValve']]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[list[Union["ProportionalValve", "Pump", "SolenoidValve"]]]:
    """Get All Actuators

     Retrieve a list of all actuators, including solenoid valves, proportional valves, and pumps.

    Returns:
        List[Union[SolenoidValve, ProportionalValve, Pump]]: A list containing all the actuators.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[Union['ProportionalValve', 'Pump', 'SolenoidValve']]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
