from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("DegreeOfSeperation")
sc = SparkContext(conf = conf)

# The characters we wish to find degre of separation  between:
startCharacterID = 5306
targetCharacterID = 14

# Our accumulator, used to signal when we find the target character uring our BFS traversal
hitCounter = sc.accumulator(0)

def convertToBFS(line):
    fields = line.split()
    heroID = int(fields[0])
    connections = []
    for connection in fields[1:]:
        connections.append(int(connection))

    color = 'WHITE'
    distance = 9999

    if (heroID == startCharacterID):
        color = 'GRAY'
        distance = 0

    return (heroID, (connections, distance, color))

def createStartingRdd():
    inputFile = sc.textFile("")
    return inputFile.map(convertToBFS)

def bfsMap(node):
    characterID = node[0]
    data =  node[1]
    connections = data[0]
    distance = data[1]
    color = data[2]

    results = []

    # If this node needs to be expanded...
    if (color == 'GRAY'):
        for connection in connections:
            newCharacterID = connection
            newDistance = distance + 1
            newColor = 'GRAY'
            if (targetCharacterID == connection):
                hitCounter.add(1)
        
        newEntry = (newCharacterID, ([], newDistance, newColor))
        results.append(newEntry)

        # we've processed this node, so color it black
        color = 'BLACK'

    # Emit the inpuyt node so we don't lose it.
    results.append( (characterID, (connections, distance, color)) )
    return results 
