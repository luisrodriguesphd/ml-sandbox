import time
import asyncio
from typing import Optional, Union, Any, AsyncGenerator
from contextlib import AbstractAsyncContextManager, asynccontextmanager

class Timer(AbstractAsyncContextManager):
    """A flexible async timer context manager with customizable formatting options.
    
    Args:
        name (str, optional): Name to identify this timer. Defaults to "Timer".
        format (str, optional): Custom format string. Available variables:
            {name}: Timer name
            {seconds}: Time in seconds
            {milliseconds}: Time in milliseconds
            Defaults to "{name}: {seconds:.3f}s"
        unit (str, optional): Time unit to return. Either "s" or "ms". Defaults to "s".
        auto_print (bool, optional): Whether to print timing automatically. Defaults to True.
    
    Example:
        >>> # Basic usage with automatic printing
        >>> async with Timer(name="Task"):
        ...     await asyncio.sleep(1)  # Some async work here
        Task: 1.001s
        
        >>> # Custom format and manual timing access
        >>> async with Timer(name="Processing", auto_print=False) as timer:
        ...     await asyncio.sleep(0.5)  # Some async work here
        ...     elapsed = timer.elapsed  # Get elapsed time
        >>> print(f"Took {elapsed:.2f} seconds")
        Took 0.50 seconds
        
        >>> # Using milliseconds
        >>> async with Timer(name="Quick task", unit="ms"):
        ...     await asyncio.sleep(0.1)  # Some async work here
        Quick task: 100.234ms
    """
    
    def __init__(
        self,
        name: str = "Timer",
        format: str = "{name}: {seconds:.3f}s",
        unit: str = "s",
        auto_print: bool = True
    ):
        self.name = name
        self.format = format
        self.unit = unit.lower()
        self.auto_print = auto_print
        
        if self.unit not in ("s", "ms"):
            raise ValueError("Unit must be either 's' or 'ms'")
        
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None
    
    async def __aenter__(self) -> "Timer":
        self._start_time = time.perf_counter()
        return self
    
    async def __aexit__(self, exc_type: Optional[type], exc_val: Optional[Exception], 
                        exc_tb: Optional[Any]) -> None:
        self._end_time = time.perf_counter()
        if self.auto_print:
            print(str(self))
    
    @property
    def elapsed(self) -> float:
        """Get the elapsed time in the configured unit (seconds or milliseconds)."""
        if self._start_time is None:
            raise RuntimeError("Timer hasn't been started")
        
        end_time = self._end_time if self._end_time is not None else time.perf_counter()
        seconds = end_time - self._start_time
        
        return seconds * 1000 if self.unit == "ms" else seconds
    
    def __str__(self) -> str:
        """Return the formatted timing string."""
        elapsed = self.elapsed
        seconds = elapsed / 1000 if self.unit == "ms" else elapsed
        milliseconds = elapsed if self.unit == "ms" else elapsed * 1000
        
        return self.format.format(
            name=self.name,
            seconds=seconds,
            milliseconds=milliseconds
        )

@asynccontextmanager
async def timer(name: str = "Timer", format: str = "{name}: {seconds:.3f}s", unit: str = "s", auto_print: bool = True) -> AsyncGenerator[dict, None]:
    """A simpler timer implementation using the asynccontextmanager decorator.
    
    Args:
        name (str, optional): Name to identify this timer. Defaults to "Timer".
        format (str, optional): Custom format string. Same variables as Timer class.
            Defaults to "{name}: {seconds:.3f}s"
        unit (str, optional): Time unit to return. Either "s" or "ms". Defaults to "s".
        auto_print (bool, optional): Whether to print timing automatically. Defaults to True.
    
    Example:
        >>> async with timer(name="Quick task"):
        ...     await asyncio.sleep(1)
        Quick task: 1.001s
    """
    if unit not in ("s", "ms"):
        raise ValueError("Unit must be either 's' or 'ms'")
        
    start = time.perf_counter()
    try:
        yield {"name": name, "format": format, "unit": unit}
    finally:
        elapsed = time.perf_counter() - start
        if unit == "ms":
            elapsed *= 1000
        if auto_print:
            print(format.format(
                name=name,
                seconds=elapsed/1000 if unit == "ms" else elapsed,
                milliseconds=elapsed if unit == "ms" else elapsed*1000
            ))

async def example():
    print("\nClass-based Timer:")
    # Basic usage with class
    async with Timer(name="Basic Example"):
        await asyncio.sleep(1)  # Simulate some async work
    
    # Custom format with milliseconds using class
    async with Timer(name="Custom Format", format="{name} took {milliseconds:.2f}ms", unit="ms"):
        await asyncio.sleep(0.5)  # Simulate some async work
    
    # Manual timing access with class
    async with Timer(name="Manual Timer", auto_print=False) as t:
        await asyncio.sleep(0.75)  # Simulate some async work
        print(f"Custom message: {t.elapsed:.2f}s")
    
    print("\nDecorator-based timer:")
    # Basic usage with decorator
    async with timer(name="Basic Example"):
        await asyncio.sleep(1)  # Simulate some async work
    
    # Custom format with milliseconds using decorator
    async with timer(name="Custom Format", format="{name} took {milliseconds:.2f}ms", unit="ms"):
        await asyncio.sleep(0.5)  # Simulate some async work

if __name__ == "__main__":
    asyncio.run(example())
