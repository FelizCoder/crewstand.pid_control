from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flowmeter_type import FlowmeterType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sensor_reading import SensorReading


T = TypeVar("T", bound="Flowmeter")


@_attrs_define
class Flowmeter:
    """Model for a flowmeter sensor.

    Attributes:
        id (int):
        setpoint (Union[None, Unset, float]):
        type_ (Union[Unset, FlowmeterType]):  Default: FlowmeterType.FLOWMETER.
        unit (Union[Unset, str]):  Default: 'l/min'.
        current_reading (Union['SensorReading', None, Unset]):
    """

    id: int
    setpoint: Union[None, Unset, float] = UNSET
    type_: Union[Unset, FlowmeterType] = FlowmeterType.FLOWMETER
    unit: Union[Unset, str] = "l/min"
    current_reading: Union["SensorReading", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.sensor_reading import SensorReading

        id = self.id

        setpoint: Union[None, Unset, float]
        if isinstance(self.setpoint, Unset):
            setpoint = UNSET
        else:
            setpoint = self.setpoint

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        unit = self.unit

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
                "id": id,
            }
        )
        if setpoint is not UNSET:
            field_dict["setpoint"] = setpoint
        if type_ is not UNSET:
            field_dict["type"] = type_
        if unit is not UNSET:
            field_dict["unit"] = unit
        if current_reading is not UNSET:
            field_dict["current_reading"] = current_reading

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.sensor_reading import SensorReading

        d = src_dict.copy()
        id = d.pop("id")

        def _parse_setpoint(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        setpoint = _parse_setpoint(d.pop("setpoint", UNSET))

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, FlowmeterType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = FlowmeterType(_type_)

        unit = d.pop("unit", UNSET)

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

        flowmeter = cls(
            id=id,
            setpoint=setpoint,
            type_=type_,
            unit=unit,
            current_reading=current_reading,
        )

        flowmeter.additional_properties = d
        return flowmeter

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
