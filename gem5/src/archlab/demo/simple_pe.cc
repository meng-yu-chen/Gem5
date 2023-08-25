#include "params/SimplePE.hh"
#include "archlab/demo/simple_pe.hh"
#include "debug/SimplePE.hh"
#include "sim/system.hh"
#include "sim/sim_exit.hh"
#include "base/logging.hh"

namespace gem5
{
/** static active pe checker */
uint64_t SimplePE::remain_pes = 0;

SimplePE::SimplePE(const SimplePEParams &p)
  : ClockedObject(p),
    system(p.system),
    requestorId(system->getRequestorId(this)),
    cache_line_size(system->cacheLineSize()),
    sendReqEvent([this]{ sendReq(); }, name()),
    memSidePort(name() + ".mem_side_port", *this),
    cur_traffic(0)
{ 
    DPRINTF(SimplePE, "%s: requestorId: %d\n", __func__, requestorId);
    remain_pes++;
}
    
SimplePE::~SimplePE()
{ }

Port &
SimplePE::getPort(const std::string &if_name, PortID idx)
{
    if (if_name == "mem_side")
        return memSidePort;
    else
        return ClockedObject::getPort(if_name, idx);

}

void
SimplePE::init()
{
    ClockedObject::init();

    if (!memSidePort.isConnected())
        fatal("The port of %s is not connected!\n", name());
}

bool
SimplePE::recvTimingResp(PacketPtr pkt)
{
    DPRINTF(SimplePE, "%s: recv %c response, addr=0x%x\n", 
                      __func__, pkt->isRead() ? 'r' : 'w', pkt->getAddr());


    auto iter = waitingResp.find(pkt->req);

    panic_if(iter == waitingResp.end(), "Received unknown response\n");

    waitingResp.erase(pkt->req);

    if(waitingResp.empty() &&
       cur_traffic >= traffic_list.size()) {
        if(--remain_pes == 0)
            exitSimLoop(name() + " has encountered the exit state and will "
                        "terminate the simulation.\n");
    }

    return true;
}

void
SimplePE::addTraffic(Addr addr, int type)
{
    if (type == 2) 
        DPRINTF(SimplePE, "%s: Adding traffic delay for %lu ticks to traffic list\n",
                        __func__, addr);
    else
        DPRINTF(SimplePE, "%s: Adding traffic addr=0x%x, type=%c to traffic list\n",
                        __func__, addr, type==0 ? 'r' : 'w');
    traffic_list.emplace_back(new Traffic(addr, type));
}

void
SimplePE::sendReq()
{
    if (cur_traffic >= traffic_list.size()) {
        if (waitingResp.empty()) {
            if(--remain_pes == 0)
                exitSimLoop(name() + " has encountered the exit state and will "
                        "terminate the simulation.\n");
        }
        return;
    }

    if(traffic_list[cur_traffic]->type == TrafficType::DELAY) {
        DPRINTF(SimplePE, "%s: Delay for %lu tick\n", __func__, traffic_list[cur_traffic]->addr);
        schedule(sendReqEvent, curTick() + traffic_list[cur_traffic]->addr);
    } else {
        DPRINTF(SimplePE, "%s: Sending request traffic index: %lu\n",
                      __func__, cur_traffic);

        Addr addr     = traffic_list[cur_traffic]->addr / cache_line_size * cache_line_size;
        unsigned size = cache_line_size;
        MemCmd cmd    = traffic_list[cur_traffic]->type == TrafficType::READ ? MemCmd::ReadReq : MemCmd::WriteReq;

        RequestPtr req = std::make_shared<Request>(addr, size, 0, requestorId);

        req->setPC(((Addr)requestorId) << 2);

        PacketPtr pkt = new Packet(req, cmd);

        uint8_t* pkt_data = new uint8_t[req->getSize()];
        pkt->dataDynamic(pkt_data);

        if (cmd.isWrite()) {
            std::fill_n(pkt_data, req->getSize(), (uint8_t)requestorId);
        }

        DPRINTF(SimplePE, "%s: Sending pkt: %s to memory side port\n",
                        __func__, pkt->print());


        bool success = memSidePort.sendTimingReq(pkt);

        panic_if (!success, "%s: SimplePE does not handle request rejected condition\n", 
                            __func__);
        
        waitingResp.insert(std::make_pair(pkt->req, curTick()));

        schedule(sendReqEvent, curTick() + 1);
    }

    cur_traffic++;
}

void
SimplePE::start()
{
    DPRINTF(SimplePE, "%s: Start operating %u traffic\n",
                      __func__, traffic_list.size());

    if (traffic_list.empty()) {
        if(--remain_pes == 0)
            exitSimLoop(name() + " has encountered the exit state and will "
                        "terminate the simulation.\n");
    } else
        schedule(sendReqEvent, curTick() + 1);
}

} // namespace gem5