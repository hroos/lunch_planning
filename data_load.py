import pandas as pd
from pulp import LpMinimize, LpProblem, LpVariable, lpSum

class Team:
    def __init__(self, name, num_people, priority, feasible_intervals):
        self.name = name
        self.num_people = num_people
        self.priority = priority
        self.feasible_intervals = feasible_intervals # for instance [("11:00", "12:00"), ("13:00", "13:30")]

    def nice_interval(self):
        tmp = ""
        for interval in self.feasible_intervals:
            tmp += (f'{interval[0].strftime("%H:%M")} - {interval[1].strftime("%H:%M")}') + " "
        return tmp

    def __str__(self):
        return self.name + " " + str(self.num_people) + " " + str(self.priority) + " " + self.nice_interval()
    
   
            

def data_load(file_path): 
    # Load excel file teams.xlsx
    data = pd.read_excel(file_path)
    
    teams = []
    
    # Iterate through the rows of the dataframe and create Team objects
    for _, row in data.iterrows():
        name = row['namn']
        num_people = row['antal_personer']
        priority = row['prioritet']
        start_time_1 = (row['start_intervall_1']) if not pd.isnull(row['start_intervall_1']) else None
        end_time_1 = (row['slut_intevall_1']) if not pd.isnull(row['slut_intevall_1']) else None
        start_time_2 = (row['start_intervall_2']) if not pd.isnull(row['start_intervall_2']) else None
        end_time_2 = (row['slut_intevall_2']) if not pd.isnull(row['slut_intevall_2']) else None
        start_time_3 = (row['start_intervall_3']) if not pd.isnull(row['start_intervall_3']) else None
        end_time_3 = (row['slut_intevall_3']) if not pd.isnull(row['slut_intevall_3']) else None

        # interval can for instance look like this [("11:00", "12:00"), ("13:00", "13:30")]
        # when start_time_1 = 11:00 , end_time_1 = 12:00 , start_time_2 = 13:00 , end_time_2 = 13:30,  start_time_3 = None , end_time_2 = None
        intervals = []
        if start_time_1 is not None and end_time_1 is not None:
            intervals.append((start_time_1, end_time_1))
        if start_time_2 is not None and end_time_2 is not None:
            intervals.append((start_time_2, end_time_2))
            print(start_time_2)
            print(end_time_2)
        if start_time_3 is not None and end_time_3 is not None:
            intervals.append((start_time_3, end_time_3))
        

       
        # assert that intervals is not empty
        assert len(intervals) > 0

        team = Team(name, num_people, priority, intervals)
        teams.append(team)
        print(f'interval {intervals}')
    
    return teams

# Convert time object to minutes
#def time_to_minutes(time_obj):
#    if time_obj is None:
#        return None
#    return time_obj.hour * 60 + time_obj.minute



if __name__ == "__main__":
    teams = data_load("teams.xlsx")
    for team in teams:
        print(team)