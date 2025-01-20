from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.proportional_valve_type import ProportionalValveType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProportionalValve")


@_attrs_define
class ProportionalValve:
    """Model representing a proportional valve actuator.

    Attributes:
        id (int):
        state (float):
        type_ (Union[Unset, ProportionalValveType]):  Default: ProportionalValveType.PROPORTIONAL_VALVE.
        current_position (Union[None, Unset, float]):
    """

    id: int
    state: float
    type_: Union[Unset, ProportionalValveType] = ProportionalValveType.PROPORTIONAL_VALVE
    current_position: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        state = self.state

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        current_position: Union[None, Unset, float]
        if isinstance(self.current_position, Unset):
            current_position = UNSET
        else:
            current_position = self.current_position

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "state": state,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if current_position is not UNSET:
            field_dict["current_position"] = current_position

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        state = d.pop("state")

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, ProportionalValveType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ProportionalValveType(_type_)

        def _parse_current_position(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        current_position = _parse_current_position(d.pop("current_position", UNSET))

        proportional_valve = cls(
            id=id,
            state=state,
            type_=type_,
            current_position=current_position,
        )

        proportional_valve.additional_properties = d
        return proportional_valve

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
