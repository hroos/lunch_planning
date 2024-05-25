import pulp
import pandas as pd
from datetime import datetime, timedelta
import data_load

# GLOBAL VARIABLES
START_TIME = "11:00"
END_TIME = "14:00"
MAX_NUM_TEAMS = 2
LUNCH_DURATION = 30


def solve_problem(team_list):
    prob = pulp.LpProblem("Lunch_Slot_Planning", pulp.LpMinimize)
    
    start_time = datetime.strptime(START_TIME, "%H:%M")
    end_time = datetime.strptime(END_TIME, "%H:%M") + timedelta(minutes=1)
    time_slots = []

    while start_time < end_time:
        time_slots.append(start_time.strftime("%H:%M"))
        start_time += timedelta(minutes=5)
    start_times = time_slots[:-int(LUNCH_DURATION/5)]  # Exclude the last few slots as they cannot be starting points for a lunch slot
    print(time_slots)

    # Create decision variables using team_list directly
    x = pulp.LpVariable.dicts("x", ((team.name for team in team_list), start_times), cat="Binary")

    # Objective function: minimize the number of times exactly six teams are eating simultaneously
    # Additional binary variables
    y = pulp.LpVariable.dicts("y", start_times, cat="Binary")

    # Constraints
    for team in team_list:
        # Each team must have exactly one lunch slot
        prob += pulp.lpSum([x[team.name][i] for i in start_times]) == 1, f"One_Lunch_Slot_{team.name}"



    # Max number of teams eating simultaneously
    for i in time_slots:
        if i < time_slots[-6]:
            prob += pulp.lpSum([x[team.name][j] for team in team_list for j in start_times if j <= i <= time_slots[time_slots.index(j) + ((LUNCH_DURATION // 5)-1)]]) <= MAX_NUM_TEAMS, f"Max_Six_Teams_{i}"




    # Additional constraints to link y variables
    for i in start_times:
        prob += y[i] >= (pulp.lpSum([x[team.name][j] for team in team_list for j in start_times if j <= i <= time_slots[time_slots.index(j) + ((LUNCH_DURATION // 5)-1)]]) ==  MAX_NUM_TEAMS), f"Link_y_{i}"

    # Objective: minimize the number of times exactly six teams are eating simultaneously
    # prob += pulp.lpSum([y[i] for i in start_times])
    prob += pulp.lpSum(y[time] for time in start_times), "Minimize_Max_Teams_Eating_Simultaneously"

    # print team feasible intervals
    for team in team_list:
        print(team.name)
        for interval in team.feasible_intervals:
            print(interval)

    """example output from above code
    Lag 1
    (datetime.time(11, 0), datetime.time(11, 30))
    (datetime.time(11, 30), datetime.time(12, 45))
    (datetime.time(12, 45), datetime.time(14, 0))
    """

    # Team can only eat within feasible intervals
    for team in team_list:
        for i in start_times:
            i_time = datetime.strptime(i, "%H:%M")
            is_feasible = False
            for start, end in team.feasible_intervals:
                start_time = datetime.strptime(start.strftime("%H:%M"), "%H:%M")
                end_time = datetime.strptime(end.strftime("%H:%M"), "%H:%M")
                if start_time <= i_time <= end_time:
                    is_feasible = True
                    break
            if not is_feasible:
                prob += x[team.name][i] == 0

  

    prob.solve()

    solution = []
    for t in team_list:
        for i in start_times:
            if pulp.value(x[t.name][i]) == 1:
                solution.append({"Team": t.name, "Start Time": i, "End Time": time_slots[time_slots.index(i) + 6]})
                break

    df = pd.DataFrame(solution)
    print(df)
    # Save to an Excel file
    df.to_excel("lunch_slots_solution.xlsx", index=False)
    print("Solution saved to 'lunch_slots_solution.xlsx'")
    
    return prob





if __name__ == "__main__":
    # Load excel file teams.xlsx
    teams = data_load.data_load("teams.xlsx")
    for team in teams:
        print(team)
    prob = solve_problem(teams)
    # print(pulp.LpStatus[prob.status])
    # print(pulp.value(prob.objective))
    # for v in prob.variables():
    #    print(v.name, "=", v.varValue)
    # for constraint in prob.constraints:
    #    print(constraint, prob.constraints[constraint].value())

    



   