import asyncio, json, os, time
from dataclasses import dataclass
from loguru import logger
from tenacity import retry, wait_fixed, stop_after_attempt

@dataclass
class AgentConfig:
    name: str
    poll_ms: int
    log_dir: str

class Agent:
    def __init__(self, cfg: AgentConfig):
        self.cfg = cfg
        os.makedirs(self.cfg.log_dir, exist_ok=True)
        logger.add(os.path.join(self.cfg.log_dir, f"{self.cfg.name}.log"),
                   rotation="5 MB", retention=5, enqueue=True)

    async def tick(self):
        # TODO: plug real strategy here
        logger.info(f"{self.cfg.name}: tick")
        await asyncio.sleep(self.cfg.poll_ms/1000)

    async def run(self):
        logger.info(f"{self.cfg.name} starting…")
        while True:
            try:
                await self.tick()
            except Exception as e:
                logger.exception(f"{self.cfg.name} error: {e}")
                try:
                    os.system(f'notify-send "FAT Alert" "{self.cfg.name}: {e}"')
                except Exception:
                    pass
                await asyncio.sleep(2)
