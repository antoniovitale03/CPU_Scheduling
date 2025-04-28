"""CPU Scheduling Algorithm that schedules processes basing on First Come, First Server paradigm"""
procs_num = int(input("Inserire il numero dei processi in coda: "))
table = {}
for i in range(procs_num):
    table[f"P{i+1}"] = int(input(f"Durata picco del processo P{i+1}"))
print(table)