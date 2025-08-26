import asyncio
import os, sys, time

class TerminalUI:
    def __init__(self, collector, refresh=1.0):
        self.collector = collector
        self.refresh = refresh
        self._task = None
        self._running = False

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._loop())

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _loop(self):
        while self._running:
            self.render()
            await asyncio.sleep(self.refresh)

    def clear(self):
        if sys.stdout.isatty():
            os.system('cls' if os.name == 'nt' else 'clear')

    def render(self):
        snap = self.collector.snapshot()
        self.clear()
        print(f"LOOM — live tasks snapshot (t={snap['timestamp']:.2f})\n")
        tasks = snap['tasks']
        if not tasks:
            print('(no tasks recorded yet)')
            return
        for t in tasks:
            created = t.get('created_at',0)
            started = t.get('started_at')
            done = t.get('done')
            print(f"- {t.get('name')} id={t.get('id')} created={created:.2f} started={started if started else '-'} done={done}")
