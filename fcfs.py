"""CPU Scheduling Algorithm that schedules processes basing on First Come, First Server paradigm"""
procs_num = int(input("Inserire il numero dei processi in coda: "))

#indico in che ordine arrivano
procs_order = input("Indica l'ordine di arrivo dei processi in coda. Ad esempio, "
          "scrivendo 2,3,1 stai indicando che i processi arrivano nell'ordine P2, P3, P1 ")

table = {} #table:   Processo: [CPU_burst, (momento in entrata del processo, momento in uscita)]
for i in range(procs_num):
    n = procs_order.split(",")[i]
    cpu_burst = int(input(f"Durata picco del processo P{n} (in secondi)"))
    table[f"P{n}"] = [cpu_burst]

#calcolo per ogni processo il momento di entrata e il momento di uscita dalla coda (in secondi) e li inserisco nella tupla
t = 0
wait_time = 0 #tempo di attesa totale
print("Gantt: ", end="")
for key,value in table.items():
    cpu_burst = value[0]
    value.append((t, t+cpu_burst))
    wait_time += t
    t = t + cpu_burst
    print(f"{key}({cpu_burst}) -> ", end="")

print(table)
print(f"tempo di attesa medio: {wait_time/procs_num}")

