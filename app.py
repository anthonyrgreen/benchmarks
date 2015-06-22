from argparse import ArgumentParser
from ConfigParser import ConfigParser
from os.path import join, exists
from os import makedirs
from subprocess import call
from datetime import datetime

config = ConfigParser()
config.read("config.cfg")
benchmarksDir = config.get("dirs", "benchmark_dirs")

# Load two benchmarks into memory, then compare them one by one
def compareBenchmarks(args):
    
    
    
# Create a folder for a benchmark and then run the benchmark n times to fill it
def createBenchmark(args):
    newDir = join(benchmarksDir, args.benchmark_name)
    benchmarkCommand = ["echo", "TODO!!!"]
    if not exists(newDir):
        makedirs(newDir)
    for i in range(args.trials):
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
        filepath = join(newDir, filename)
        with open(filepath, "wb") as benchmark:
            call(benchmarkCommand, stdout=benchmark, shell=False)
        

main_parser = ArgumentParser(description="Make and compare openmpi benchmarks")
subparser = main_parser.add_subparsers(help="Where does this show up?")

create_parser = subparser.add_parser('create', help="Create a new benchmark test.")
create_parser.add_argument("test_program_path")
create_parser.add_argument("benchmark_name")
create_parser.add_argument("--trials", "-n", type=int, default=5)
create_parser.set_defaults(func=createBenchmark)

compare_parser = subparser.add_parser('compare', help="Compare two existing benchmarks.")
compare_parser.add_argument("benchmark1")
compare_parser.add_argument("benchmark2")
compare_parser.set_defaults(func=compareBenchmarks)

args = main_parser.parse_args()
args.func(args)
