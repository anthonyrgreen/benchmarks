import os
import ConfigParser
basePath = os.path.dirname(os.path.abspath(__file__))
benchmarkDirname = "benchmarks"
benchmarkPath = os.path.join(basePath, benchmarkDirname)
if not os.path.exists(benchmarkPath):
    os.makedirs(benchmarkPath)

config = ConfigParser.RawConfigParser()
config.add_section("dirs")
config.set("dirs", "benchmark_dirs", benchmarkPath)

with open("config.cfg", "wb") as configFile:
    config.write(configFile)
