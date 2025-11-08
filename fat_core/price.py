import asyncio, random, time
from typing import Optional

class Backoff:
    def __init__(self, start=0.5, cap=8.0, factor=2.0):
        self.start, self.cap, self.factor, self.cur = start, cap, factor, start
    async def sleep(self): 
        t = self.cur
        await asyncio.sleep(t)
        self.cur = min(self.cap, self.cur * self.factor)
    def reset(self): self.cur = self.start

class PriceFeed:
    """
    Async price feed wrapper supporting 'sim', 'binance', 'pyth'.
    Only the chosen adapter is imported/used (lazy), so tests don’t need
    network deps unless you select a live adapter.
    """
    def __init__(self, source: str, symbol: str = "SOLUSDT"):
        self.source = source.lower()
        self.symbol = symbol
        self._price: Optional[float] = None
        # sim state
        self._sim_px = 100.0 + random.random()

    async def get(self) -> float:
        if self.source == "sim":
            # tiny random walk
            self._sim_px *= (1.0 + random.uniform(-0.002, 0.002))
            return float(self._sim_px)

        if self.source == "binance":
            import aiohttp  # lazy import
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={self.symbol}"
            back = Backoff()
            while True:
                try:
                    async with aiohttp.ClientSession() as s:
                        async with s.get(url, timeout=5) as r:
                            r.raise_for_status()
                            data = await r.json()
                            px = float(data["price"])
                            back.reset()
                            return px
                except Exception:
                    await back.sleep()

        if self.source == "pyth":
            # Minimal REST read via Pyth price service (symbol mapping left to config).
            import aiohttp
            # NOTE: You’ll wire the correct feed URL/id later; this is a safe placeholder.
            url = "https://hermes.pyth.network/api/latest_price_feeds?ids[]=SOL/USD"
            back = Backoff()
            while True:
                try:
                    async with aiohttp.ClientSession() as s:
                        async with s.get(url, timeout=5) as r:
                            r.raise_for_status()
                            arr = await r.json()
                            # expect an array; choose first item with price.price
                            px = float(arr[0]["price"]["price"])
                            back.reset()
                            return px
                except Exception:
                    await back.sleep()

        raise ValueError(f"Unknown price source: {self.source}")
