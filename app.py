#!/usr/bin/env python

from argparse import ArgumentParser
from ConfigParser import ConfigParser
from parse import averageBenchmarks, compareBenchmarks
from os.path import join, exists, isfile
from os import makedirs, listdir
from subprocess import call
from datetime import datetime

config = ConfigParser()
config.read("config.cfg")
benchmarksDir = config.get("dirs", "benchmark_dirs")

# Load two benchmarks into memory, then compare them one by one
def compare(args):
    benchmark1Dir = join(benchmarksDir, args.benchmark1)
    benchmark2Dir = join(benchmarksDir, args.benchmark2)
    benchmark1Filenames = [ join(benchmark1Dir, f) for f in listdir(benchmark1Dir) 
                            if isfile(join(benchmark1Dir,f)) ]
    benchmark2Filenames = [ join(benchmark2Dir, f) for f in listdir(benchmark2Dir) 
                            if isfile(join(benchmark2Dir,f)) ]
    benchmark1 = averageBenchmarks(*benchmark1Filenames)
    benchmark2 = averageBenchmarks(*benchmark2Filenames)
    comparison = compareBenchmarks(benchmark1, benchmark2)
    for key in comparison:
        print key
        print comparison[key]
        print ""
    
# Create a folder for a benchmark and then run the benchmark n times to fill it
def create(args):
    newDir = join(benchmarksDir, args.benchmark_name)
    benchmarkCommand = [args.test_program_path]
    if not exists(newDir):
        makedirs(newDir)
    for i in range(args.trials):
        filename = datetime.now().strftime("test-%Y-%m-%d-%H-%M-%S-%f")
        filepath = join(newDir, filename)
        with open(filepath, "wb") as benchmark:
            call(benchmarkCommand, stdout=benchmark, shell=False)
        

main_parser = ArgumentParser(description="Make and compare openmpi benchmarks")
subparser = main_parser.add_subparsers(help="This program can be run in one of two modes:")

create_parser = subparser.add_parser('create', help="Create and store a new benchmark test.")
create_parser.add_argument("test_program_path", help="The path to the benchmarking program to run.")
create_parser.add_argument("benchmark_name", help="The name of this particular test.")
create_parser.add_argument("--trials", "-n", type=int, default=5, help="How many trials to run.")
create_parser.set_defaults(func=create)

compare_parser = subparser.add_parser('compare', help="Compare two existing benchmarks and display results.")
compare_parser.add_argument("benchmark1", help="The first benchmark name.")
compare_parser.add_argument("benchmark2", help="The second benchmark name.")
compare_parser.set_defaults(func=compare)

args = main_parser.parse_args()
args.func(args)
