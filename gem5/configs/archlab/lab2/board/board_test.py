from gem5.components.boards.test_board import TestBoard

from gem5.components.processors.linear_generator import *
from gem5.components.processors.random_generator import *

from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy \
    import PrivateL1CacheHierarchy
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy \
    import PrivateL1SharedL2CacheHierarchy
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy \
    import PrivateL1PrivateL2CacheHierarchy

from gem5.components.memory import *

import m5
from m5.objects import Root


memory = SingleChannelDDR3_1600("1GiB")
cache_hierarchy = PrivateL1SharedL2CacheHierarchy(l1d_size="64kB", l1i_size="64kB", l2_size="128kB")
generator = LinearGenerator(
    duration="250us",
    rate="40GB/s",
    num_cores=1,
    max_addr=memory.get_size(),
    data_limit=64
)

# add components to the Test boards
board = TestBoard(
    clk_freq="3GHz",
    generator=generator,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# set up system with board object, choose SE mode
root = Root(full_system=False, system=board)
# interconnection between components
board._pre_instantiate()
m5.instantiate()

# start the traffic generator
generator.start_traffic()

# start gem5 simulation
print("Beginning simulation!")
exit_event = m5.simulate()
print("Exiting @ tick %i because %s" % (m5.curTick(), exit_event.getCause())) 