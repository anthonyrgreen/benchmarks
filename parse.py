import pandas as pd
import re

def parseSection(header, body):
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
    
    return (header, data)

def averageBenchmarks(*benchmarks):
    combinedBenchmarks = pd.Panel({n: df for n, df in enumerate(benchmarks)})
    return combinedBenchmarks.mean(axis=0)


def differenceBenchmarks(bench1, bench2):
    return bench1 - bench2

def getSections(input):
    # delimeter matches a test header
    delimeter = r"#-+\n(?:#\s[^\n]*\n)*#-+\n"
    delimeter = re.compile(delimeter)
    headers = delimeter.findall(input)
    bodies = delimeter.split(input)[1:]
    return zip(headers, bodies)
 