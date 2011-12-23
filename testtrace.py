import sys
import trace
import unittest
from main import Scm
tracer = trace.Trace(
    ignoredirs=[sys.prefix, sys.exec_prefix],
    trace=1,
    count=1)
tracer.run('Scm()')

r = tracer.results()
r.write_results(show_missing=True, coverdir="/tmppp")
