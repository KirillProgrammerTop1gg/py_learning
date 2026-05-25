from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal
from concurrent.futures import ProcessPoolExecutor
from contextlib import asynccontextmanager
import asyncio
import math
import time
import os
import numpy as np
import heapq

executor: ProcessPoolExecutor | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global executor
    executor = ProcessPoolExecutor(max_workers=os.cpu_count())

    yield

    if executor:
        executor.shutdown(wait=True)


app = FastAPI(lifespan=lifespan)


class CalculateRequest(BaseModel):
    operation: Literal["factorial", "primes", "matrix", "stats"]

    number: int | None = Field(default=None, ge=0, le=1000)

    start: int | None = Field(default=None, ge=0)
    end: int | None = Field(default=None, ge=2, le=10_000_000)

    matrix_size: int | None = Field(default=None, ge=1, le=200)

    array: list[float] | None = Field(
        default=None,
        min_length=1,
        max_length=1_000_000,
    )

    @field_validator("array")
    @classmethod
    def validate_array(cls, v):
        if v is not None:
            for x in v:
                if math.isnan(x) or math.isinf(x):
                    raise ValueError("Array contains NaN or Inf")
        return v

    @model_validator(mode="after")
    def validate_fields(self):
        if self.operation == "factorial" and self.number is None:
            raise ValueError("number required")

        if self.operation == "primes":
            if self.start is None or self.end is None:
                raise ValueError("start and end required")

            if self.start > self.end:
                raise ValueError("start must be <= end")

        if self.operation == "matrix" and self.matrix_size is None:
            raise ValueError("matrix_size required")

        if self.operation == "stats" and self.array is None:
            raise ValueError("array required")

        return self


def factorial_worker(n: int):
    result = math.factorial(n)

    return {"result": str(result), "digits": len(str(result))}


def is_prime(n: int):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = int(math.sqrt(n)) + 1
    for i in range(3, limit, 2):
        if n % i == 0:
            return False

    return True


def primes_worker(start: int, end: int):
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)

    return primes


def matrix_worker(size: int):
    a = np.random.rand(size, size)
    b = np.random.rand(size, size)
    result = np.dot(a, b)

    return {
        "shape": [size, size],
        "first_row": result[0].tolist(),
        "checksum": float(result.sum()),
    }


def stats_worker(arr: list[float]):
    a = np.array(arr, dtype=np.float64)
    return {
        "mean": float(np.mean(a)),
        "median": float(np.median(a)),
        "std": float(np.std(a)),  # population std, як і зараз
    }


async def run_process(func, *args):
    global executor
    if executor is None:
        raise RuntimeError("Executor not initialized")
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, func, *args)


@app.post("/calculate")
async def calculate(data: CalculateRequest):
    start_time = time.perf_counter()

    try:
        if data.operation == "factorial":
            result = await asyncio.wait_for(
                run_process(factorial_worker, data.number), timeout=30
            )

        elif data.operation == "primes":
            start_num = max(2, data.start)
            end_num = data.end
            total = end_num - start_num + 1
            workers = os.cpu_count() or 4
            chunk_size = max(1, total // workers)
            tasks = []
            current = start_num
            while current <= end_num:
                chunk_end = min(current + chunk_size - 1, end_num)
                tasks.append(
                    asyncio.wait_for(
                        run_process(primes_worker, current, chunk_end), timeout=30
                    )
                )
                current = chunk_end + 1
            results = await asyncio.gather(*tasks)
            primes = []
            for chunk in results:
                primes.extend(chunk)
            result = primes

        elif data.operation == "matrix":
            result = await asyncio.wait_for(
                run_process(matrix_worker, data.matrix_size), timeout=30
            )

        elif data.operation == "stats":
            result = await asyncio.wait_for(
                run_process(stats_worker, data.array), timeout=30
            )

        else:
            raise HTTPException(status_code=400, detail="Invalid operation")

    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Computation timeout")

    execution_time = round(time.perf_counter() - start_time, 5)

    return {
        "operation": data.operation,
        "execution_time": execution_time,
        "result": result,
    }
