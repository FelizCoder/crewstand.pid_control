from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.pump_type import PumpType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Pump")


@_attrs_define
class Pump:
    """Model representing a pump actuator.

    Attributes:
        id (int):
        state (bool):
        type_ (Union[Unset, PumpType]):  Default: PumpType.PUMP.
    """

    id: int
    state: bool
    type_: Union[Unset, PumpType] = PumpType.PUMP
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
        type_: Union[Unset, PumpType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = PumpType(_type_)

        pump = cls(
            id=id,
            state=state,
            type_=type_,
        )

        pump.additional_properties = d
        return pump

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
