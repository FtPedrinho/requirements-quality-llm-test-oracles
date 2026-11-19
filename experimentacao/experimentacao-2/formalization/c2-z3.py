from z3 import Int, Solver, sat

properties = {
    "table_limit": Int("n") <= 20,
    "direct_limit": Int("n") <= 30,
    "z3_row_limit": Int("n") <= 4096,
    "pair_limit": Int("n") <= 1000,
    "z3_timeout": Int("n") <= 60,
}

for name, formula in properties.items():
    solver = Solver()
    solver.add(formula)
    result = solver.check()
    print(name, "SAT" if result == sat else "NOT-SAT")
