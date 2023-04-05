from dataclasses import dataclass
from queue import Queue
from device import Device
from demand import Demand


@dataclass
class Configuration:
    mu: float
    lambd: float
    queue = []
    device: Device = Device()

    def putDemand(self, demand: Demand):
        self.queue.append(demand)
        self.queue.sort(key=lambda x: x.service_time)

    def getDemand(self) -> Demand:
        return self.queue.pop(0)
