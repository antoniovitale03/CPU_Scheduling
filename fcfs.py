def create_table(procs_num, procs_order):
    table = {} #table:   {Processo: CPU_burst}
    for i in range(procs_num):
        n = procs_order.split(",")[i]
        cpu_burst = int(input(f"Durata picco del processo P{n} (in secondi)"))
        table[f"P{n}"] = cpu_burst
    return table
def wait_time(gantt, procs_order):
    total_wait_time = 0
    wait_times = []
    procs = procs_order.split(",")
    for i in range(len(procs)):
        n = procs[i]
        wait_times.append(sum(value[0] for key, value in gantt if key == f"P{n}"))#tempo di attesa totale del i-esimo processo
        print(f"Tempo di attesa di P{n}: {wait_times[i]}")
        total_wait_time += wait_times[i]
    avg_wait_time = total_wait_time/procs_num
    print(f"Tempo di attesa medio: {avg_wait_time}")

def print_gantt(gantt):
    print("Gantt:  ", end="")
    for key, value in gantt:
        proc_time = value[1] - value[0]
        print(f"{key}({proc_time}) -> ", end="")

procs_num = int(input("Inserire il numero dei processi in coda: "))
#indico in che ordine arrivano
procs_order = input("Indica l'ordine di arrivo dei processi in coda. Ad esempio, "
          "scrivendo 2,3,1 stai indicando che i processi arrivano nell'ordine P2, P3, P1 ")
table = create_table(procs_num, procs_order)

#calcolo per ogni processo il momento di entrata e il momento di uscita dalla coda (in secondi) e li inserisco nella tupla
gantt = [] #gantt: [(Processo, (momento di entrata, momento di uscita))
t = 0
for key,value in table.items():
    cpu_burst = value
    gantt.append((f"{key}", (t, t + cpu_burst)))
    t = t + cpu_burst

print_gantt(gantt)
wait_time(gantt, procs_order)

