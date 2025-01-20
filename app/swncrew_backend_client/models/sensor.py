from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sensor_enum import SensorEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sensor_reading import SensorReading


T = TypeVar("T", bound="Sensor")


@_attrs_define
class Sensor:
    """Base model for an sensor.

    Attributes:
        type_ (SensorEnum): Enumeration for different types of sensors.
        unit (str):
        id (int):
        setpoint (Union[None, Unset, float]):
        current_reading (Union['SensorReading', None, Unset]):
    """

    type_: SensorEnum
    unit: str
    id: int
    setpoint: Union[None, Unset, float] = UNSET
    current_reading: Union["SensorReading", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.sensor_reading import SensorReading

        type_ = self.type_.value

        unit = self.unit

        id = self.id

        setpoint: Union[None, Unset, float]
        if isinstance(self.setpoint, Unset):
            setpoint = UNSET
        else:
            setpoint = self.setpoint

        current_reading: Union[None, Unset, dict[str, Any]]
        if isinstance(self.current_reading, Unset):
            current_reading = UNSET
        elif isinstance(self.current_reading, SensorReading):
            current_reading = self.current_reading.to_dict()
        else:
            current_reading = self.current_reading

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "unit": unit,
                "id": id,
            }
        )
        if setpoint is not UNSET:
            field_dict["setpoint"] = setpoint
        if current_reading is not UNSET:
            field_dict["current_reading"] = current_reading

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.sensor_reading import SensorReading

        d = src_dict.copy()
        type_ = SensorEnum(d.pop("type"))

        unit = d.pop("unit")

        id = d.pop("id")

        def _parse_setpoint(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        setpoint = _parse_setpoint(d.pop("setpoint", UNSET))

        def _parse_current_reading(data: object) -> Union["SensorReading", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                current_reading_type_0 = SensorReading.from_dict(data)

                return current_reading_type_0
            except:  # noqa: E722
                pass
            return cast(Union["SensorReading", None, Unset], data)

        current_reading = _parse_current_reading(d.pop("current_reading", UNSET))

        sensor = cls(
            type_=type_,
            unit=unit,
            id=id,
            setpoint=setpoint,
            current_reading=current_reading,
        )

        sensor.additional_properties = d
        return sensor

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
