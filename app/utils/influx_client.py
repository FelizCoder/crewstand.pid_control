from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from simple_pid import PID

from .config import config


class InfluxConnector:
    """
    Summary
    ----------
    Provides a synchronous interface for writing data to an InfluxDB instance.
    Handles sensor and actuator data writes with automatic point generation.

    Parameters
    ----------
    url : str, optional
        InfluxDB server URL ( defaults to `settings.INFLUXDB_URL.unicode_string()` )
    token : str, optional
        InfluxDB authentication token ( defaults to `settings.INFLUXDB_TOKEN` )
    org : str, optional
        InfluxDB organization ( defaults to `settings.INFLUXDB_ORG` )
    bucket : str, optional
        Target InfluxDB bucket for writes ( defaults to `settings.INFLUXDB_BUCKET` )

    Attributes
    ----------
    bucket : str
        Target InfluxDB bucket for writes.
    client : InfluxDBClient
        Underlying InfluxDB client instance.
    write_api : WriteApi
        Synchronous write API for the InfluxDB client.

    Methods
    ----------
    write_sensor(sensor)
        Writes a sensor reading to InfluxDB.
    write_actuator(actuator, timestamp_ns)
        Writes an actuator state to InfluxDB with a specified timestamp.
    _write(point)
        Internal method for writing a pre-constructed InfluxDB point.

    Raises
    ----------
    ConnectionError
        If a connection issue occurs while writing to InfluxDB, an error is logged.

    Notes
    -----
    This class is designed for synchronous use. For asynchronous operations, consider using the asynchronous InfluxDB client.
    Instance configuration is primarily driven by the application's settings module.
    """

    def __init__(
        self,
        url=config.INFLUXDB_URL.unicode_string(),
        token=config.INFLUXDB_TOKEN,
        org=config.INFLUXDB_ORG,
        bucket=config.INFLUXDB_BUCKET,
    ):

        self.bucket = bucket
        self.client = InfluxDBClient(
            url=url,
            token=token,
            org=org,
            debug=(config.DEBUG_LEVEL == "DEBUG"),
            timeout=250,
        )

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_pid(self, pid: PID, timestamp_ns: int):
        
        (p,i,d) = pid.components
        
        point = (
            Point("PID")
            .field("P", p)
            .field("I", i)
            .field("D", d)
            .field("setpoint", pid.setpoint)
            .field("auto_mode", pid.auto_mode)
            .time(timestamp_ns, WritePrecision.NS)
            .tag("sensor_id", config.SENSOR_ID)
        )
        
        self._write(point)
        
    
    def _write(self, point):
        try:
            self.write_api.write(bucket=self.bucket, record=point)
        except Exception as e:
            logger.error(f"Failed to write to InfluxDB: {e}")


influx_connector = InfluxConnector()
