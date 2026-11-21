"""Shared helpers for the concurrency tests."""

import threading


def run_concurrently(fns, timeout=30):
    """Start every callable in its own thread behind a Barrier.

    Returns a list of ("ok", value) or ("err", exception), in input order.
    """
    barrier = threading.Barrier(len(fns))
    results = [None] * len(fns)

    def worker(i, fn):
        barrier.wait()
        try:
            results[i] = ("ok", fn())
        except Exception as exc:  # noqa: BLE001
            results[i] = ("err", exc)

    threads = [threading.Thread(target=worker, args=(i, f)) for i, f in enumerate(fns)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout)
        assert not t.is_alive(), "worker thread hung (possible deadlock)"
    return results
