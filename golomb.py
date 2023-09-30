from ortools.sat.python import cp_model

def golomb(order, max_length=-1):
    if max_length < 0:
        max_length = (order - 1) ** 2

    model = cp_model.CpModel()

    marks = [model.NewIntVar(0, max_length, f"M{i}") for i in range(order)]

    differences = []
    for i in range(1, order):
        for j in range(0, i):
            diff = model.NewIntVar(1, max_length, f"diff_{i}_{j}")
            model.Add(diff == marks[i] - marks[j])
            differences.append(diff)

    model.AddAllDifferent(differences)
    model.Add(marks[0] == 0)
    for i in range(1, order):
        model.Add(marks[i] > marks[i - 1])
    model.Add((marks[1] - marks[0]) < (marks[order - 1] - marks[order - 2]))

    model.Minimize(marks[order - 1])

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10

    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return {
            "status": solver.StatusName(status),
            "marks": [solver.Value(mark) for mark in marks],
            "solve_time": solver.WallTime()
        }
    else:
        return {
            "status": solver.StatusName(status),
            "marks": [],
            "solve_time": solver.WallTime()
        }

result = golomb(5)

print("Solution:", result["status"])
if result["marks"]:
    print("Position of ruler marks:", " ".join(str(mark) for mark in result["marks"]))
print(f"Solve time: {result['solve_time']}s")
