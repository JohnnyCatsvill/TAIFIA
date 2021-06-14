from LL1 import *

RULES = [
    ["Z", ["E $"]],
    ["E", ["E + E"]],
    ["E", ["i"]]
]


table = Run(RULES, "LR", "FR", "", show_all=True )

runner = Runner_cl(1, table, "$")

word = "(())"

for i in range(len(word)):
    runner.Run(word[i], i)

is_end = runner.Run("$", "end_end")
if is_end:
    print("EVERYTHING IS FINE, BUT MY MENTAL HEALTH")
else:
    print("WERE F**CKED")

