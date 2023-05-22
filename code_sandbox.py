import pandas as pd

a1_choices = [1,2,2,3,3,4,4,5]
a2_choices = [5,5,2,2,4,4,1,1]
choices = [a1_choices, a2_choices]

data = []
for p in range(len(choices)):
    for t in range(len(choices[p])):
        data.append({'id': p, 't': t, 'choice': choices[p][t]})

print(data)