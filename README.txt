=========
BENCHMARKING
=========
This program is designed to capture the output of the intel MPI benchmarks
program, currently found at
https://software.intel.com/en-us/articles/intel-mpi-benchmarks. Using this
application, a user can save that output and compare it against subsequent
runs of the benchmarking software.

To install the program, simply run the "setup" script. This must be done prior
to first use.

Note that this program uses Rython's dictionary comprehensions, which were not
available prior to Python 2.7. It also uses the "argparse" and "pandas"
modules. The bash wrapper script simply loads the anaconda2 module, which
supplies all of these features.

There are only two modes in which this program can be run: "create" and
"compare". 

=========
./app create [-h] [--trials TRIALS] test_program_path benchmark_name:
=========
This mode runs the benchmarking program, located at "test_program_path", and
stores the results with the name "benchmark_name". For example:

> [grundoon]$ BENCHMARK_EXEC="/tmp/argreen/imb/src/imb/src/IMB-MPI1"
> [grundoon]$ ./app create $BENCHMARK_EXEC test1

By default, the benchmarking program will be run 5 times. These runs will be
averaged together at comparison-time. The "--trials", or "-n" argument can be
used to specify more or fewer runs. For instance, to store ten runs under the
name test2, one would type:

> [grundoon]$ ./app create $BENCHMARK_EXEC test2 --trials 10

Note that tests are usually stored in the "benchmarks/" subdirectory of the
application's home folder. To store them in a custom folder, simply make
"benchmark_name" into an absolute path, as in the following example:

> [grundoon]$ ./app create $BENCHMARK_EXEC /tmp/grundoon/customBenchmarkFolder/test3



=========
app.py compare [-h] [--verbose] benchmark1 benchmark2
=========
This is the comparison mode. The inputs are simple: "benchmark1" and
"benchmark2" are just the names of the benchmarks we want to compare. The
program will go through them, section by section, and calculate the percentage
changes from benchmark1 to benchmark2. By default, three statistics will be
shown: the maximum change, the minimum change, and the average change. An
example would be:

> [grundoon]$ ./app compare test1 test2

To display more than summary statistics -- that is, to actually show every
single row-by-row change from benchmark1 to benchmark2 -- use the "--verbose",
or "-v" tag. A good use pattern might be to use the summary statistics to
identify tests with large changes, and then to examine those tests in
particular using the verbose mode.

By default, the application looks for test names in its own benchmarks folder.
To use a custom test, simply write the tests absolute path, as in:

> [grundoon]$ ./app compare test2 /tmp/grundoon/customBenchmarkFolder/test3
