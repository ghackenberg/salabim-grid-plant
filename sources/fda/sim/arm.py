import salabim as sim
import matplotlib.pyplot as plt

from ..model import Corridor, Machine

from .machine import SimMachine
from .armrobot import SimArmRobot


class SimArm(sim.Component):
    def __init__(self, corridor: Corridor, machines: list[Machine], name: str, env: sim.Environment, store_in: sim.Store, store_out_1: sim.Store, store_out_2: sim.Store, dx: float, y: float):
        super().__init__(name)

        self.corridor = corridor
        self.machines = machines

        self.env = env

        self.store_in = store_in
        self.store_out_1 = store_out_1
        self.store_out_2 = store_out_2

        # Machines
        self.sim_machines: list[SimMachine] = []
        machine_num = 0
        for machine in machines:
            machine_x = (3 + machine_num * 2) * dx
            sim_machine = SimMachine(machine, env, machine_x, y)
            self.sim_machines.append(sim_machine)
            machine_num = machine_num + 1

        # Transversal robot
        if len(machines) != 0:
            self.sim_arm_robot = SimArmRobot(corridor, machines, env, store_in, store_out_1, store_out_2, self.sim_machines, dx, y)

        # Arm horizontal box
        if len(machines) != 0:
            x_len = len(machines) * 2 + 0.26
            x = (0.86 + x_len / 2) * dx
            sim.Animate3dBox(x_len=x_len, y_len=0.25, z_len=0.25, color="green", x=x, y=y, z=2.5)

        # Corridor storage arm vertical box
        if len(machines) != 0:
            sim.Animate3dBox(x_len=0.25, y_len=0.25, z_len=1.5, color="green", x=dx, y=y, z=1.625)
    
    def printStatistics(self):
        print(f"    - Arm {self.name()}:")
        if len(self.machines) != 0:
            self.sim_arm_robot.printStatistics()
        for sim_machine in self.sim_machines:
            sim_machine.printStatistics()
        armBarCharts(self.corridor, self.name(), self.sim_arm_robot, self.sim_machines)


def armBarCharts(corridor: Corridor, name: str, sim_arm_robot: SimArmRobot, sim_machines: list[SimMachine]):
    plt.figure(corridor.name)
    
    # Plot machines
    index = 1
    for sim_machine in sim_machines:
        plt.subplot(1, len(sim_machines) + 1, index)
        sim_machine.plot()
        index = index + 1

    # Plot arm robot
    plt.subplot(1, len(sim_machines) + 1, index)
    sim_arm_robot.plot()

    # Print Graph
    plt.show()
