import asyncio
import time
from typing import Dict, Any

class TaskRecord:
    def __init__(self, task: asyncio.Task):
        self.id = id(task)
        self.name = getattr(task, 'get_name', lambda: f"task-{self.id}")()
        self.created_at = time.time()
        self.started_at = None
        self.done_at = None
        self.done = False

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'done_at': self.done_at,
            'done': self.done,
        }

class Tracer:
    def __init__(self):
        self._records = {}
        self._orig_factory = None

    def install(self, loop: asyncio.AbstractEventLoop):
        # wrap task factory so tasks get recorded
        self._orig_factory = loop.get_task_factory()
        loop.set_task_factory(self._task_factory)

    def uninstall(self, loop: asyncio.AbstractEventLoop):
        if self._orig_factory is not None:
            loop.set_task_factory(self._orig_factory)

    def _task_factory(self, loop, coro):
        task = (self._orig_factory(loop, coro) if self._orig_factory else asyncio.tasks.Task(coro, loop=loop))
        rec = TaskRecord(task)
        self._records[id(task)] = rec

        # when task starts (first step) mark started
        def _on_step(_):
            if rec.started_at is None:
                rec.started_at = time.time()
        # attach callbacks
        task.add_done_callback(self._on_done)
        # instrumenting the task by wrapping its _step is intrusive; instead we mark started the first time the task becomes running via loop.call_soon
        loop.call_soon(_on_step, None)
        return task

    def _on_done(self, task):
        rec = self._records.get(id(task))
        if rec:
            rec.done = True
            rec.done_at = time.time()

    def snapshot(self):
        # return list of current task records as dicts
        return [r.to_dict() for r in self._records.values()]
