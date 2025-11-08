import asyncio
from fat_core.agent import Agent, AgentConfig

class DummyFeed:
    def __init__(self, seq): self.seq = iter(seq)
    async def get(self): return next(self.seq)

def make_agent(seq, floor=2.0, rebound=2.0):
    cfg = AgentConfig(
        name="t", poll_ms=5, log_dir="/tmp",
        trigger={"kind":"stable_flip","floor_pct":floor,"rebound_pct":rebound,"min_hold_sec":0},
        schedule={"off_start_hour":23,"off_duration_hours":0},
    )
    a = Agent(cfg); a.feed = DummyFeed(seq); return a

async def drive(a, n): 
    for _ in range(n): await a.tick()

def test_flip_roundtrip():
    a = make_agent([100,100,99,98,97,96,96,97,98,98])
    assert a.mode == "BASE"
    asyncio.run(drive(a, 6));  assert a.mode == "STABLE"
    asyncio.run(drive(a, 4));  assert a.mode == "BASE"
