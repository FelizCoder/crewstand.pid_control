from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Setpoint")


@_attrs_define
class Setpoint:
    """
    Attributes:
        setpoint (Union[None, Unset, float]):
    """

    setpoint: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        setpoint: Union[None, Unset, float]
        if isinstance(self.setpoint, Unset):
            setpoint = UNSET
        else:
            setpoint = self.setpoint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if setpoint is not UNSET:
            field_dict["setpoint"] = setpoint

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_setpoint(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        setpoint = _parse_setpoint(d.pop("setpoint", UNSET))

        setpoint = cls(
            setpoint=setpoint,
        )

        setpoint.additional_properties = d
        return setpoint

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
