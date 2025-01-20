from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SensorReading")


@_attrs_define
class SensorReading:
    """Base model for a sensor reading.

    Attributes:
        value (float):
        timestamp_ns (int): Timestamp of the reading in nanoseconds since Epoch
    """

    value: float
    timestamp_ns: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        timestamp_ns = self.timestamp_ns

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "timestamp_ns": timestamp_ns,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        timestamp_ns = d.pop("timestamp_ns")

        sensor_reading = cls(
            value=value,
            timestamp_ns=timestamp_ns,
        )

        sensor_reading.additional_properties = d
        return sensor_reading

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
