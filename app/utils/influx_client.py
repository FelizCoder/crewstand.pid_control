from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from simple_pid import PID

from app.utils.config import config
from app.utils.logger import logger


class InfluxConnector:
    """
    InfluxConnector is a class that provides methods to connect
    to an InfluxDB instance and write PID controller data.

    Attributes
    bucket : str
        The InfluxDB bucket where data will be written.
    client : InfluxDBClient
        The client instance used to interact with InfluxDB.
    write_api : WriteApi
        The API instance used to write data to InfluxDB.

    Methods
    __init__(
        url=config.INFLUXDB_URL.unicode_string(),
        token=config.INFLUXDB_TOKEN,
        org=config.INFLUXDB_ORG,
        bucket=config.INFLUXDB_BUCKET
    )
        Initializes the InfluxConnector with the specified InfluxDB connection parameters.
    write_pid(pid: PID, timestamp_ns: int)
        Writes PID controller data to InfluxDB.
    _write(point)
        Writes a data point to InfluxDB and handles exceptions.
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
        """
        Write PID controller data to InfluxDB.
        Parameters
        ----------
        pid : PID
            An instance of the PID controller containing the PID components and settings.
        timestamp_ns : int
            The timestamp in nanoseconds to associate with the data point.
        Returns
        -------
        None
        """

        (p, i, d) = pid.components

        point = (
            Point("PID")
            .field("P", float(p))
            .field("I", float(i))
            .field("D", float(d))
            .field("setpoint", float(pid.setpoint))
            .field("auto_mode", bool(pid.auto_mode))
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
