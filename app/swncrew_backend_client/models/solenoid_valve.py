from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.solenoid_valve_type import SolenoidValveType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SolenoidValve")


@_attrs_define
class SolenoidValve:
    """Model representing a solenoid valve actuator.

    Attributes:
        id (int):
        state (bool):
        type_ (Union[Unset, SolenoidValveType]):  Default: SolenoidValveType.SOLENOID_VALVE.
    """

    id: int
    state: bool
    type_: Union[Unset, SolenoidValveType] = SolenoidValveType.SOLENOID_VALVE
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        state = self.state

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        state = d.pop("state")

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, SolenoidValveType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = SolenoidValveType(_type_)

        solenoid_valve = cls(
            id=id,
            state=state,
            type_=type_,
        )

        solenoid_valve.additional_properties = d
        return solenoid_valve

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
