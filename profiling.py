# !pip install line_profiler

"""
    Prints detailed run times for each line in a decorated function
"""

from decorator import decorator
from line_profiler import LineProfiler

@decorator
def profile_each_line(func, *args, **kwargs):
    profiler = LineProfiler()
    profiled_func = profiler(func)
    try:
        return profiled_func(*args, **kwargs)
    
    finally:
        profiler.print_stats()


"""
    Prints total run time for a decorated function
"""

@decorator
def print_exec_time(func, *args, **kwargs):
  tic = time.time()
  res = func(*args, **kwargs)
  toc = time.time()
  print(str(func.__name__)+ ' Exec time {:.4f} seconds.'.format(toc - tic))
  return res
