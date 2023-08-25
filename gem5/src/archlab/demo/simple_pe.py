from m5.params import *
from m5.proxy import *
from m5.SimObject import *
from m5.objects.ClockedObject import ClockedObject

class SimplePE(ClockedObject):
    type = 'SimplePE'
    cxx_header = "archlab/demo/simple_pe.hh"
    cxx_class = "gem5::SimplePE"

    # System used to determine the mode of the memory system
    system           = Param.System(Parent.any, "System this pe is part of")

    # Port used for sending requests and receiving responses
    mem_side      = RequestPort("This port sends requests and receives responses")

    # These additional parameters allow TrafficGen to be used with scripts
    # that expect a BaseCPU
    cpu_id     = Param.Int(-1, "CPU identifier")
    socket_id  = Param.Unsigned(0, "Physical Socket identifier")
    numThreads = Param.Unsigned(1, "number of HW thread contexts")

    @cxxMethod
    def start(self):
        pass

    @cxxMethod
    def addTraffic(self, addr, type):
        pass

    @classmethod
    def memory_mode(cls):
        return "timing"

    @classmethod
    def require_caches(cls):
        return False

    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports
    
    def connectCache(self, cache):
        self.mem_side = cache.cpu_side
        self._cached_ports = ["dcache.mem_side"]