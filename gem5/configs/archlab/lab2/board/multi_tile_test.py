from gem5.components.processors.linear_generator import *
from gem5.components.processors.random_generator import *

from gem5.components.cachehierarchies.lab447.lab447_private_l1_cache_hierarchy \
    import Lab447PrivateL1CacheHierarchy
from gem5.components.cachehierarchies.lab447.lab447_private_l1_private_l2_cache_hierarchy \
    import Lab447PrivateL1PrivateL2CacheHierarchy
from gem5.components.cachehierarchies.lab447.lab447_private_l1_shared_l2_cache_hierarchy \
    import Lab447PrivateL1SharedL2CacheHierarchy

from gem5.components.memory import *


import m5
from m5.objects import *

m5.util.addToPath("../")

# system setting
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "3GHz"
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = "timing"

# memory object
system.memory = SingleChannelDDR3_1600("1GiB")
system.mem_ranges = [AddrRange(system.memory.get_size())]
system.memory.set_memory_range(system.mem_ranges)

# Xbar, interconnection between cache and memory
system.membus = SystemXBar()
system.membus.badaddr_responder = BadAddr()
system.membus.default = system.membus.badaddr_responder.pio

# default connection, don't change
system.system_port = system.membus.cpu_side_ports

# connect Xbar to memory
for cntr in system.memory.get_memory_controllers():
    cntr.port = system.membus.mem_side_ports

# num of tiles
numTiles = 2

# PE object (Simobject array)
system.pe = [RandomGenerator(
        duration="250us",
        rate="40GB/s",
        num_cores=2,
        max_addr=system.memory.get_size(),
        data_limit=64)
        for i in range(numTiles)]

# cache object (Simobject array)
system.cache = [Lab447PrivateL1PrivateL2CacheHierarchy(
        l1d_size="64kB",
        l1i_size="64kB",
        l2_size = "128kB")
        for i in range(numTiles)]

# interconnect with each PE and Cache pair
for i in range(numTiles):
    system.cache[i].incorporate_tile(system.membus, system.pe[i])


# set up system with SE mode
root = Root(full_system=False, system=system)
m5.instantiate()

# start the traffic generator
for i in range(numTiles):
    system.pe[i].start_traffic()

# start gem5 simulation
print("Beginning simulation!")
exit_event = m5.simulate()
print("Exiting @ tick %i because %s" % (m5.curTick(), exit_event.getCause())) 