from random import expovariate

from clock import Clock
from configuration import Configuration
from demand import Demand
from statistics import Statistics


def run(mu: float, lambd: float, simulation_time: float) -> None:
    times = Clock()
    system = Configuration(mu=mu, lambd=lambd)
    statistics = Statistics()

    loop(simulation_time, times, system, statistics)


def loop(simulation_time: float,
         times: Clock,
         system: Configuration,
         statistics: Statistics) -> None:
    times.update_arrival_time(system.lambd)
    while times.current <= simulation_time:
        times.current = get_time_of_nearest_event(times)
        if times.current == times.arrival:
            arrival_demand(times, system)
            continue
        if times.current == times.service_start:
            service_demand(times, system)
            continue
        if times.current == times.leaving:
            leaving_demand(times, system, statistics)
            continue
    print(statistics.average_time / statistics.leaving_count)


def arrival_demand(times: Clock,
                   system: Configuration) -> None:
    print("I. Arrival demand", times.current, end="\t###\t")
    demand = Demand(times.arrival, expovariate(system.mu))
    print("demand ID:", demand.id)
    if len(system.queue) == 0 and not system.device.serves:
        times.service_start = times.current
    system.putDemand(demand)
    times.update_arrival_time(system.lambd)


def service_demand(times: Clock,
                   system: Configuration) -> None:
    print("II. Start service demand", times.current, end="\t###\t")
    system.device.to_occupy(system.getDemand())
    times.leaving = times.current + system.device.demand.service_time
    print("demand ID:", system.device.demand.id)
    system.device.demand.service_start_time = times.current
    times.service_start = float('inf')


def leaving_demand(times: Clock,
                   system: Configuration,
                   statistics: Statistics) -> None:
    print("III. Leaving demand", times.current, end="\t###\t")
    demand = system.device.get_demand()
    print("demand ID:", demand.id)
    system.device.to_free()
    demand.set_leaving_time(times.current)
    statistics.update(demand)

    if not len(system.queue) == 0:
        times.service_start = times.current
    times.leaving = float('inf')


def get_time_of_nearest_event(times: Clock) -> float:
    return min(times.arrival, times.service_start, times.leaving)
