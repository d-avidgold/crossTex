import sys

# Opens file and reads the first line "<ACROSS LITE...>" and the next

f = open(sys.argv[1], "r")
line = f.readline()
line = f.readline()
details = {}

# Given the 'size' of the board, split into an array [#cols, #rows]

def readSize(string):
    lst = string.split("x")
    lst2 = []
    for i in lst:
        lst2.append(int(i))
    return lst2

cols = -1
rows = -1

# Read the 'preamble:' title, authors, copyright, size, and grid

while line:
    line = line.strip()
    if line[0] == "<":
        if line[1] == "T" or line[1] == "A" or line[1] == "C":
            # Read title, author, and copyright.
            tit = line[1:-1]
            line = (f.readline()).strip()
            details[tit] = line
        elif line[1] == "S":
            # Read size: rows and columns
            line = (f.readline()).strip()
            sz = readSize(line)
            rows = sz[1]
            cols = sz[0]
            details["ROWS"] = rows
            details["COLS"] = cols
        else:
            # Read grid, then break to set it up.
            grid = []
            line = (f.readline()).strip()
            while line[0] != "<":
                grid.append(line)
                line = (f.readline()).strip()
            break

    line = f.readline()

# Make sure the grid is as it should be!

if len(grid) != rows or len(grid[0]) != cols:
    print("Error! Row and Column Lengths do not match.")

# Figure out how numbering should work: any time we start a new across or down word,
#     we need to put a number in. They should increase as we go, right to left, and
#     top to bottom.

else:
    gridNum = []
    acrossNums = []
    downNums = []
    curr = 1
    readyForDown = [True for x in range(cols)]
    readyForAcross = True
    for rowString in grid:
        numbering = []
        i = 0
        for letter in rowString:
            if letter == ".":
                numbering.append("*")
                readyForAcross = True
                readyForDown[i] = True
            elif readyForAcross and readyForDown[i]:
                readyForAcross = False
                readyForDown[i] = False
                acrossNums.append(curr)
                downNums.append(curr)
                numbering.append("[" + str(curr) + "]" + letter)
                curr += 1
            elif readyForAcross:
                readyForAcross = False
                numbering.append("[" + str(curr) + "]" + letter)
                acrossNums.append(curr)
                curr += 1
            elif readyForDown[i]:
                readyForDown[i] = False
                numbering.append("[" + str(curr) + "]" + letter)
                downNums.append(curr)
                curr += 1
            else:
                numbering.append(letter)
            i += 1
        gridNum.append(numbering)
        readyForAcross = 1

    # Now time to read across clues!
    
    line = (f.readline()).strip()
    i = 0
    acrossClues = {}
    while line[0] != "<":
        acrossClues[acrossNums[i]] = line
        i += 1
        line = (f.readline()).strip()
        
    # Now time to read down clues!
    
    line = (f.readline()).strip()
    i = 0
    downClues = {}
    while line and line[0] != "<":
        downClues[downNums[i]] = line
        i += 1
        line = (f.readline()).strip()

# print(gridNum)
# print(acrossClues)
# print(downClues)
# f.close()

# Write to a new file: when compiled in LaTeX, this will make a pretty grid!

f2 = open(sys.argv[2], "w")
f2.write("\\begin{Puzzle}{" + str(cols) + "}{" + str(rows) + "}%\n")
for rowNumbering in gridNum:
    f2.write("\t|")
    for specificNumber in rowNumbering:
        f2.write(specificNumber + "|")
    f2.write(".\n")
f2.write("\\end{Puzzle}\n")
f2.close()
