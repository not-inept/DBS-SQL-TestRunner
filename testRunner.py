import MySQLdb as mdb
from json import load
import filecmp
import time
import os


configFile = open('testRunner.config')
config = load(configFile)
configFile.close()

filesAvail = config['answersAvailable']
filesLoc = config['answersLocation']
resultsLoc = config['resultsLocation']
myResultsLoc = resultsLoc + config['name'] + '/'
resultsSuffix = config['resultsSuffix']


def runSQLFiles(connection):
    for f in filesAvail:
        fileName = filesLoc + f
        start = time.time()

        file = open(fileName, 'r')
        sql = " ".join(file.readlines())
        print('\n\n' + fileName)
        print('Start executing at: ' + str(start))
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()

        end = time.time()
        print('Time elapsed to run the query:')
        print(str((end - start) * 1000) + ' ms')

        res = cursor.fetchall()
        of = open(myResultsLoc + f + resultsSuffix, 'w+')
        of.write(str(res))
        of.close()
        file.close()


def compareFiles():
    resFiles = [s + resultsSuffix for s in filesAvail]
    for root, dirs, files in os.walk(resultsLoc):
        root = root + '/'
        if root != myResultsLoc:
            for name in files:
                if name in resFiles:
                    print(myResultsLoc + name + " compared to " + root + name)
                    print("Result: " + str(filecmp.cmp(myResultsLoc + name, root + name)) + "\n")


def main():
    connection = mdb.connect('localhost', 'baseball', 'baseball', 'stats')
    runSQLFiles(connection)
    connection.close()
    compareFiles()

if __name__ == '__main__':
    main()
