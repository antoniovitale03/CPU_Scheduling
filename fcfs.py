procs_num = int(input("Inserire il numero dei processi in coda: "))

#indico in che ordine arrivano
procs_order = input("Indica l'ordine di arrivo dei processi in coda. Ad esempio, "
          "scrivendo 2,3,1 stai indicando che i processi arrivano nell'ordine P2, P3, P1 ")

table = {} #table:   {Processo: CPU_burst}
for i in range(procs_num):
    n = procs_order.split(",")[i]
    cpu_burst = int(input(f"Durata picco del processo P{n} (in secondi)"))
    table[f"P{n}"] = cpu_burst

#calcolo per ogni processo il momento di entrata e il momento di uscita dalla coda (in secondi) e li inserisco nella tupla
gantt = {} #gantt: {Processo: (momento di entrata, momento di uscita)}
t = 0
wait_time = 0 #tempo di attesa totale
print("Gantt: ", end="")
for key,value in table.items():
    cpu_burst = value
    gantt[f"{key}"] = (t, t + cpu_burst)
    t = t + cpu_burst

def avg_wait_time(gantt, procs_num):
    total_wait_time = sum(start for start, _ in gantt.values())
    return total_wait_time/procs_num

def print_gantt(gantt):
    print("Gantt:  ", end="")
    for key, value in gantt.items():
        proc_time = value[1] - value[0]
        print(f"{key}({proc_time}) -> ", end="")

print(table)
print(gantt)
avg_wait_time = avg_wait_time(gantt, procs_num)
print_gantt(gantt)
print(f"tempo di attesa medio: {avg_wait_time}")
