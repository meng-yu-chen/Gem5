#ifndef __ARCHLAB_LAB1_SAMPLE_SIMPLE_PE_HH__
#define __ARCHLAB_LAB1_SAMPLE_SIMPLE_PE_HH__

#include <cstdint>
#include <string>
#include <memory>
#include <vector>
#include <unordered_map>

#include "enums/AddrMap.hh"
#include "mem/qport.hh"
#include "sim/clocked_object.hh"
#include "base/types.hh"
#include "mem/packet.hh"
#include "mem/request.hh"

namespace gem5
{   
class System;
struct SimplePEParams;
class SimplePE;
typedef SimplePE *SimplePEPtr;

enum class TrafficType {
  READ  = 0,
  WRITE = 1,
  DELAY = 2
};

struct Traffic {
  Addr addr;
  TrafficType type;

  Traffic (Addr _addr, int _type)
    : addr(_addr), type(TrafficType(_type))
  { }
};

class SimplePE : public ClockedObject
{
  protected: // Params
    /**
     * The system used to determine which mode we are currently operating
     * in.
    */
    System *const system;

    /** The RequestorID used for generating requests */
    const RequestorID requestorId;

    /** Cache line size in the simulated system */
    const Addr cache_line_size;

  public:
    SimplePE(const SimplePEParams &p);

    ~SimplePE();

    Port &getPort(const std::string &if_name,
                  PortID idx=InvalidPortID) override;

    void init() override;

    void addTraffic(Addr addr, int type = 0);

    void start();

  private:
    void recvReqRetry() { }

    bool recvTimingResp(PacketPtr pkt);

    void sendReq();

    EventFunctionWrapper sendReqEvent;

    class MemSidePort : public RequestPort
    {
      public:
        
        MemSidePort(const std::string& name, SimplePE& simplePE)
          : RequestPort(name, &simplePE), simplePE(simplePE)
        { }

      protected:

        void recvReqRetry() { simplePE.recvReqRetry(); }

        bool recvTimingResp(PacketPtr pkt)
        { return simplePE.recvTimingResp(pkt); }

      private:
        SimplePE& simplePE;  
    };

    MemSidePort memSidePort;

    typedef std::vector<Traffic*> TrafficList;
    TrafficList traffic_list;

    uint64_t cur_traffic;

    static uint64_t remain_pes;
    std::unordered_map<RequestPtr, Tick> waitingResp;
};

} // namespace gem5

#endif // __ARCHLAB_LAB1_SAMPLE_SIMPLE_PE_HH__