from copy import deepcopy
import pandas as pd
import re

def averageBenchmarks(*filenames):
    benchmarks = [parseBenchmark(filename) for filename in filenames]
    combinedBenchmarks = mergeDicts(*benchmarks)
    averagedBenchmarks = { key : averageSections(*combinedBenchmarks[key])
                           for key in combinedBenchmarks }
    return averagedBenchmarks

def compareBenchmarks(benchmark1, benchmark2):
    unusedKeys = [key for key in benchmark1 if key not in benchmark2]
    unusedKeys.append([key for key in benchmark2 if key not in benchmark1])
    compared = { key : differenceSections(benchmark1[key], benchmark2[key])
                 for key in benchmark1 if key in benchmark2 }
    return compared
    
def parseBenchmark(filename):
    benchmark = {}
    with open(filename, "rb") as file:
        input = file.read()
        sections = getSections(input)[1:]
        for header, body in sections:
            benchmark[header] = parseSection(body)
    return benchmark

def getSections(input):
    # delimeter matches a test header
    delimeter = r"#-+\n(?:#\s[^\n]*\n)*#-+\n"
    delimeter = re.compile(delimeter)
    headers = delimeter.findall(input)
    bodies = delimeter.split(input)[1:]
    return zip(headers, bodies)

def parseSection(body):
    # Remove the newlines and any extra BS
    body = body.split('\n')
    body = body[:body.index('')]
    body = map(str.split, body)

    # Separate column names from data
    columnLabels = body[0]
    columnIndices = [label for label in columnLabels if label.startswith('#')]
    rows = body[1:]
    
    # Create and format DataFrame
    data = pd.DataFrame(rows, columns=columnLabels)
    data = data.set_index(columnIndices)
    data = data.astype(float)
    
    return data

def averageSections(*benchmarks):
    combinedBenchmarks = pd.Panel({n: df for n, df in enumerate(benchmarks)})
    return combinedBenchmarks.mean(axis=0)


def differenceSections(bench1, bench2):
    return bench1 - bench2

def mergeDicts(*dicts):
    """Return a new dictionary with the keys of all elements in dicts, where
    the values are placed in lists so as not to lose any elements.
    EG: mergeDicts({'a' : 1, 'b' : 2}, {'a' : 3}) = {'a': [1,3], 'b' : [2]}"""
    newDict = {}
    for dict in dicts:
        for key in dict:
            if key in newDict:
                newDict[key].append(deepcopy(dict[key]))
            else:
                newDict[key] = [deepcopy(dict[key])]
    return newDict
