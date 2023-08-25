import m5
from m5.objects import *
from gem5.components.memory import *
from gem5.components.cachehierarchies.classic.caches.l1dcache import L1DCache

# initialize system
system                           = System()
system.clk_domain                = SrcClockDomain()
system.clk_domain.clock          = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode                  = "timing"

# initialize global memory
system.global_mem = SingleChannelDDR3_1600("8GiB")
system.mem_ranges = [AddrRange(start=0x0, size=system.global_mem.get_size())]
system.global_mem.set_memory_range(system.mem_ranges)

# initialize global memory bus
system.global_membus                   = SystemXBar()
system.global_membus.badaddr_responder = BadAddr()
system.global_membus.default           = system.global_membus.badaddr_responder.pio

# connect global memory controller to global memory bus 
system.system_port = system.global_membus.cpu_side_ports
for cntr in system.global_mem.get_memory_controllers():
    cntr.port = system.global_membus.mem_side_ports

# initial petiles (connect to cache each)
num_tiles = 2

simplePEs =  []
caches = []

for tile_idx in range(num_tiles):
    simplePEs.append(SimplePE())
    caches.append(L1DCache(size="64kB"))

    simplePEs[tile_idx].mem_side = caches[tile_idx].cpu_side
    caches[tile_idx].mem_side = system.global_membus.cpu_side_ports

system.simplePEs = simplePEs
system.caches  = caches

root = Root(full_system=False, system=system)
m5.instantiate()

system.simplePEs[1].addTraffic(1234, 1)     # write
system.simplePEs[0].addTraffic(1234, 2)     # delay
system.simplePEs[0].addTraffic(1234, 0)     # read

for simplePE in system.simplePEs:
    simplePE.start()

print("Beginning simulation!")
exit_event = m5.simulate()
print("Exiting @ tick %i because %s" % (m5.curTick(), exit_event.getCause())) 