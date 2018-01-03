import FlowFree
from timeit import default_timer as timer

print("14x14 Puzzle - Smart Backtracking Algorithm")
puzzle = FlowFree.Puzzle('inputs/14x14.txt')
start = timer()
puzzle.smarterBtAlgorithm()
end = timer()
print("Assignments: " + str(puzzle.numAssignments))
print("Run Time: " + str(end - start))
print()
