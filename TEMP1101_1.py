from Phidget22.Phidget import *
from Phidget22.Devices.TemperatureSensor import *
import time
from dataclasses import dataclass

"""
Used with Phidgets TEMP1101_1
"""


@dataclass
class phidget_temp_sensor:
    port: int
    sensor: TemperatureSensor
    t_max: float
    t_min: float
    temps: list


def onTemperatureChange(self, temperature):
    local_time = time.localtime()
    print(
        f"Temperature {self.getChannel()}: {temperature:0.3f}°C | {time.asctime(local_time)}"
    )


def default_example():
    """
    Example provided by Phidgets.
    """
    temperatureSensor0 = TemperatureSensor()
    temperatureSensor1 = TemperatureSensor()
    temperatureSensor4 = TemperatureSensor()  # Built in IC

    temperatureSensor0.setChannel(0)
    temperatureSensor1.setChannel(1)
    temperatureSensor4.setChannel(4)

    temperatureSensor0.setOnTemperatureChangeHandler(onTemperatureChange)
    temperatureSensor1.setOnTemperatureChangeHandler(onTemperatureChange)
    temperatureSensor4.setOnTemperatureChangeHandler(onTemperatureChange)

    temperatureSensor0.openWaitForAttachment(5000)
    temperatureSensor1.openWaitForAttachment(5000)
    temperatureSensor4.openWaitForAttachment(5000)

    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass

    temperatureSensor0.close()
    temperatureSensor1.close()
    temperatureSensor4.close()


def fetch_with_events():
    """
    Fetches temperature when a change is detected.
    """
    ports = [0, 1, 2]
    ports.append(4)  # Port 4 is a built in IC

    temp_sensors = []
    for port in ports:
        sensor = TemperatureSensor()
        sensor.setChannel(port)
        sensor.setOnTemperatureChangeHandler(
            onTemperatureChange
        )  # event handler that triggers on temperature change
        # temp_sensors.append(phidget_temp_sensor(port=port, sensor=sensor))
        temp_sensors.append(sensor)
        sensor.openWaitForAttachment(5000)

    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass

    for sensor in temp_sensors:
        sensor.close()


def periodic_fetch():
    """
    Fetches temperature with a consistent refresh rate.
    """

    ports = [0, 1, 2]
    ports.append(4)  # Port 4 is a built in IC
    SAMPLE_FREQ = 1  # Hz

    temp_sensors = []
    for port in ports:
        sensor = TemperatureSensor()
        sensor.setChannel(port)
        temp_sensors.append(
            phidget_temp_sensor(
                port=port,
                sensor=sensor,
                t_max=None,
                t_min=None,
                temps=[],
            )
        )
        sensor.openWaitForAttachment(5000)

    print("\n --- Press any CTRL+C to stop ---\n")
    time.sleep(1)

    try:
        while True:
            for s in temp_sensors:
                t = s.sensor.getTemperature()
                s.temps.append(t)
                if s.t_max is None:
                    s.t_max = t
                elif s.t_min is None:
                    s.t_min = t
                elif t > s.t_max:
                    s.t_max = t
                elif t < s.t_min:
                    s.t_min = t
                onTemperatureChange(s.sensor, t)
            print()
            time.sleep(1 / SAMPLE_FREQ)
    except KeyboardInterrupt:
        # Exits while loop if "CTRL + C" is pressed
        pass

    for s in temp_sensors:
        avg = sum(s.temps) / len(s.temps)
        print(f"C{s.port} | MAX: {s.t_max} | MIN: {s.t_min} | AVG: {avg:0.3f}")
        s.sensor.close()


def main():
    periodic_fetch()


main()
