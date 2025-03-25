import tracemalloc

# Start tracing Python memory allocations.
tracemalloc.start()

# Doing something
biglist = list(range(1000000))
current, peak = tracemalloc.get_traced_memory()

# Print memory stats
print(f"Current memory usage: {current / 1024:.2f} KB")
print(f"Peak memory usage: {peak / 1024:.2f} KB")

tracemalloc.stop()