import time
import uuid
import logging
import requests
from multiprocessing import Process, Value, Lock, current_process
from typing import Dict


URL = "http://localhost:8000/api/v1/products/"
TOTAL_REQUESTS = 1000
PROCESSES = 4
TIMEOUT = 5


# ---------------- LOGGING ---------------- #

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(processName)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------- PAYLOAD ---------------- #


def build_payload() -> Dict:
    return {
        "seller_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "title": f"Wireless Mouse {uuid.uuid4().hex[:6]}",
        "price": 15.99,
        "stock": 100,
    }


# ---------------- WORKER ---------------- #


def worker(
    requests_per_process: int,
    success: Value,
    failures: Value,
    lock: Lock,
) -> None:
    session = requests.Session()
    name = current_process().name

    for i in range(requests_per_process):
        payload = build_payload()

        try:
            response = session.post(
                URL,
                json=payload,
                timeout=TIMEOUT,
            )

            with lock:
                if response.status_code in (200, 201):
                    success.value += 1
                else:
                    failures.value += 1

        except requests.RequestException:
            with lock:
                failures.value += 1

        # 🔥 LIVE VISIBILITY (controlled)
        if i % 100 == 0:
            logger.info(
                "Progress: %s | Sent=%s",
                name,
                i,
            )

    logger.info("%s finished", name)


# ---------------- MAIN ---------------- #


def run_load_test() -> None:
    start_time = time.perf_counter()

    success = Value("i", 0)
    failures = Value("i", 0)
    lock = Lock()

    requests_per_process = TOTAL_REQUESTS // PROCESSES

    processes = []

    logger.info(
        "Starting multiprocessing load test | processes=%s total_requests=%s",
        PROCESSES,
        TOTAL_REQUESTS,
    )

    for _ in range(PROCESSES):
        p = Process(
            target=worker,
            args=(requests_per_process, success, failures, lock),
        )
        processes.append(p)
        p.start()

    # 🔥 LIVE GLOBAL STATUS
    while any(p.is_alive() for p in processes):
        with lock:
            logger.info(
                "GLOBAL STATUS | success=%s failures=%s",
                success.value,
                failures.value,
            )
        time.sleep(2)

    for p in processes:
        p.join()

    total_time = time.perf_counter() - start_time

    logger.info("Load test completed")
    logger.info("Success: %s", success.value)
    logger.info("Failures: %s", failures.value)
    logger.info("Total Time: %.2f sec", total_time)
    logger.info(
        "Requests/sec: %.2f",
        TOTAL_REQUESTS / total_time,
    )


# ---------------- ENTRYPOINT ---------------- #

if __name__ == "__main__":
    run_load_test()
