import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio, sys, yaml, os
from pydantic import BaseModel
from fat_core.agent import Agent, AgentConfig

class Common(BaseModel):
    exchange: str
    base: str
    quote: str
    poll_ms: int = 1200
    log_dir: str

class AgentOverrides(BaseModel):
    trigger: dict = {}
    limits: dict = {}
    schedule: dict = {}

def load_cfg(name: str):
    with open(os.path.expanduser("~/FAT/configs/common.yaml")) as f:
        common = Common(**yaml.safe_load(f))
    with open(os.path.expanduser(f"~/FAT/configs/{name}.yaml")) as f:
        _ = AgentOverrides(**yaml.safe_load(f))
    return AgentConfig(name=name, poll_ms=common.poll_ms, log_dir=common.log_dir)

async def main(name: str):
    cfg = load_cfg(name)
    agent = Agent(cfg)
    await agent.run()

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "huey"
    asyncio.run(main(name))
