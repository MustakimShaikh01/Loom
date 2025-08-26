import argparse, asyncio, importlib.util, sys, os
from .tracer import Tracer
from .collector import Collector
from .ui_terminal import TerminalUI
import runpy

def load_module_from_path(path):
    spec = importlib.util.spec_from_file_location('user_module', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

async def _run_module_async(path):
    # Expect the module to define an 'async def main()' coroutine function.
    mod = load_module_from_path(path)
    if not hasattr(mod, 'main'):
        raise SystemExit("Target script must expose an async 'main()' coroutine function.")
    coro = getattr(mod, 'main')
    task = asyncio.create_task(coro())
    await task

def run(path, refresh=1.0):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tracer = Tracer()
    tracer.install(loop)
    collector = Collector(tracer)
    ui = TerminalUI(collector, refresh=refresh)

    async def _main():
        await ui.start()
        try:
            await _run_module_async(path)
        finally:
            await ui.stop()

    try:
        loop.run_until_complete(_main())
    finally:
        tracer.uninstall(loop)
        loop.close()

def main():
    p = argparse.ArgumentParser('loom-runner')
    p.add_argument('path', help='path to python script (must define async def main())')
    p.add_argument('--refresh', help='ui refresh seconds', type=float, default=1.0)
    args = p.parse_args()
    run(args.path, refresh=args.refresh)

if __name__ == '__main__':
    main()
