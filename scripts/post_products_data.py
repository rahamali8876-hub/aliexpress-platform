# # import requests
# # import time
# # import uuid
# # import logging
# # from typing import Dict

# # from prometheus_client import (
# #     start_http_server,
# #     Histogram,
# #     Counter,
# # )


# # class ProductLoadTester:
# #     """
# #     Load tester for Product API with Prometheus metrics
# #     """

# #     # ---------------- PROMETHEUS METRICS ---------------- #

# #     request_duration = Histogram(
# #         "product_api_request_duration_seconds",
# #         "Time spent processing product API requests",
# #         buckets=(0.1, 0.3, 0.5, 1, 2, 5, 10),
# #     )

# #     requests_total = Counter(
# #         "product_api_requests_total",
# #         "Total number of product API requests",
# #     )

# #     requests_failed = Counter(
# #         "product_api_requests_failed_total",
# #         "Total number of failed product API requests",
# #     )

# #     # ---------------- INIT ---------------- #

# #     def __init__(
# #         self,
# #         url: str,
# #         total_requests: int = 1000,
# #         timeout: int = 5,
# #         metrics_port: int = 8001,
# #     ) -> None:
# #         self.url = url
# #         self.total_requests = total_requests
# #         self.timeout = timeout

# #         self.success = 0
# #         self.failures = 0

# #         self.logger = self._setup_logger()

# #         # Start Prometheus metrics server
# #         start_http_server(metrics_port)
# #         self.logger.info(
# #             "Prometheus metrics exposed on :%s/metrics",
# #             metrics_port,
# #         )

# #     # ---------------- LOGGER ---------------- #

# #     @staticmethod
# #     def _setup_logger() -> logging.Logger:
# #         logging.basicConfig(
# #             level=logging.INFO,
# #             format="%(asctime)s | %(levelname)s | %(message)s",
# #         )
# #         return logging.getLogger(__name__)

# #     # ---------------- PAYLOAD ---------------- #

# #     @staticmethod
# #     def build_payload() -> Dict:
# #         return {
# #             "seller_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
# #             "title": f"Wireless Mouse {uuid.uuid4().hex[:6]}",
# #             "price": 15.99,
# #             "stock": 100,
# #         }

# #     # ---------------- REQUEST ---------------- #

# #     def _send_request(
# #         self,
# #         session: requests.Session,
# #         index: int,
# #     ) -> None:
# #         payload = self.build_payload()
# #         self.requests_total.inc()

# #         start_time = time.perf_counter()

# #         try:
# #             response = session.post(
# #                 self.url,
# #                 json=payload,
# #                 timeout=self.timeout,
# #             )

# #             duration = time.perf_counter() - start_time
# #             self.request_duration.observe(duration)

# #             if response.status_code in (200, 201):
# #                 self.success += 1
# #             else:
# #                 self.failures += 1
# #                 self.requests_failed.inc()
# #                 self.logger.warning(
# #                     "Request %s failed | Status=%s",
# #                     index,
# #                     response.status_code,
# #                 )

# #         except requests.RequestException as exc:
# #             duration = time.perf_counter() - start_time
# #             self.request_duration.observe(duration)

# #             self.failures += 1
# #             self.requests_failed.inc()

# #             self.logger.error(
# #                 "Request %s exception: %s",
# #                 index,
# #                 exc,
# #             )

# #     # ---------------- RUN ---------------- #

# #     def run(self) -> None:
# #         self.logger.info("Starting load test")

# #         overall_start = time.perf_counter()

# #         with requests.Session() as session:
# #             for index in range(self.total_requests):
# #                 self._send_request(session, index)

# #                 if index % 100 == 0:
# #                     self.logger.info(
# #                         "Progress: %s/%s",
# #                         index,
# #                         self.total_requests,
# #                     )

# #         total_time = time.perf_counter() - overall_start
# #         self._print_summary(total_time)

# #     # ---------------- SUMMARY ---------------- #

# #     def _print_summary(self, total_time: float) -> None:
# #         self.logger.info("Load test completed")
# #         self.logger.info("Total Requests: %s", self.total_requests)
# #         self.logger.info("Success: %s", self.success)
# #         self.logger.info("Failures: %s", self.failures)
# #         self.logger.info("Total Time: %.2f seconds", total_time)
# #         self.logger.info(
# #             "Requests/sec: %.2f",
# #             self.total_requests / total_time,
# #         )


# # # ---------------- ENTRYPOINT ---------------- #

# # if __name__ == "__main__":
# #     tester = ProductLoadTester(
# #         url="http://localhost:8000/api/v1/products/",
# #         total_requests=1000000,
# #         timeout=5,
# #         metrics_port=8001,
# #     )
# #     tester.run()
# # # 17658


# import asyncio
# import time
# import uuid
# import logging
# from typing import Dict

# import aiohttp
# from prometheus_client import start_http_server, Histogram, Counter


# class AsyncProductLoadTester:
#     """
#     High-performance async load tester using aiohttp
#     """

#     request_duration = Histogram(
#         "product_api_request_duration_seconds",
#         "Product API request latency",
#         buckets=(0.05, 0.1, 0.3, 0.5, 1, 2, 5),
#     )

#     requests_total = Counter(
#         "product_api_requests_total",
#         "Total requests sent",
#     )

#     requests_failed = Counter(
#         "product_api_requests_failed_total",
#         "Total failed requests",
#     )

#     def __init__(
#         self,
#         url: str,
#         total_requests: int = 10000,
#         concurrency: int = 200,
#         timeout: int = 5,
#         metrics_port: int = 8001,
#     ) -> None:
#         self.url = url
#         self.total_requests = total_requests
#         self.concurrency = concurrency
#         self.timeout = timeout

#         self.success = 0
#         self.failures = 0

#         self.logger = self._setup_logger()

#         start_http_server(metrics_port)
#         self.logger.info(
#             "Prometheus metrics at :%s/metrics",
#             metrics_port,
#         )

#         self.semaphore = asyncio.Semaphore(concurrency)

#     # ---------------- LOGGING ---------------- #

#     @staticmethod
#     def _setup_logger() -> logging.Logger:
#         logging.basicConfig(
#             level=logging.INFO,
#             format="%(asctime)s | %(levelname)s | %(message)s",
#         )
#         return logging.getLogger(__name__)

#     # ---------------- PAYLOAD ---------------- #

#     @staticmethod
#     def build_payload() -> Dict:
#         return {
#             "seller_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#             "title": f"Wireless Mouse {uuid.uuid4().hex[:6]}",
#             "price": 15.99,
#             "stock": 100,
#         }

#     # ---------------- REQUEST ---------------- #

#     async def _send_request(
#         self,
#         session: aiohttp.ClientSession,
#         index: int,
#     ) -> None:
#         async with self.semaphore:
#             self.requests_total.inc()
#             payload = self.build_payload()

#             start = time.perf_counter()

#             try:
#                 async with session.post(
#                     self.url,
#                     json=payload,
#                     timeout=self.timeout,
#                 ) as response:
#                     duration = time.perf_counter() - start
#                     self.request_duration.observe(duration)

#                     if response.status in (200, 201):
#                         self.success += 1
#                     else:
#                         self.failures += 1
#                         self.requests_failed.inc()

#             except Exception as exc:
#                 duration = time.perf_counter() - start
#                 self.request_duration.observe(duration)
#                 self.failures += 1
#                 self.requests_failed.inc()

#                 self.logger.debug(
#                     "Request %s failed: %s",
#                     index,
#                     exc,
#                 )

#     # ---------------- RUN ---------------- #

#     async def run(self) -> None:
#         self.logger.info(
#             "Starting async load test | requests=%s concurrency=%s",
#             self.total_requests,
#             self.concurrency,
#         )

#         timeout = aiohttp.ClientTimeout(total=self.timeout)

#         start_time = time.perf_counter()

#         async with aiohttp.ClientSession(timeout=timeout) as session:
#             tasks = [self._send_request(session, i) for i in range(self.total_requests)]
#             await asyncio.gather(*tasks)

#         total_time = time.perf_counter() - start_time
#         self._print_summary(total_time)

#     # ---------------- SUMMARY ---------------- #

#     def _print_summary(self, total_time: float) -> None:
#         self.logger.info("Load test completed")
#         self.logger.info("Total Requests: %s", self.total_requests)
#         self.logger.info("Success: %s", self.success)
#         self.logger.info("Failures: %s", self.failures)
#         self.logger.info("Total Time: %.2f sec", total_time)
#         self.logger.info(
#             "Requests/sec: %.2f",
#             self.total_requests / total_time,
#         )


# # ---------------- ENTRYPOINT ---------------- #

# if __name__ == "__main__":
#     tester = AsyncProductLoadTester(
#         url="http://localhost:8000/api/v1/products/",
#         total_requests=20000,
#         concurrency=300,
#         timeout=5,
#         metrics_port=8001,
#     )

#     asyncio.run(tester.run())


import time
import uuid
import logging
import requests
from multiprocessing import Process, Value, Lock, current_process
from typing import Dict


URL = "http://localhost:8000/api/v1/products/"
TOTAL_REQUESTS = 5000
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
