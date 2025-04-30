def avg_wait_time(gantt, procs_num):
    total_wait_time = 0
    for i in range(procs_num):
        total_wait_time += sum(value[0] for key, value in gantt if key == f"P{i+1}") #tempo di attesa totale del i-esimo processo
    return total_wait_time/procs_num

def print_gantt(gantt):
    print("Gantt:  ", end="")
    for key, value in gantt:
        proc_time = value[1] - value[0]
        print(f"{key}({proc_time}) -> ", end="")

procs_num = int(input("Inserire il numero dei processi in coda: "))

#indico in che ordine arrivano
procs_order = input("Indica l'ordine di arrivo dei processi in coda. Ad esempio, "
          "scrivendo 2,3,1 stai indicando che i processi arrivano nell'ordine P2, P3, P1 ")

time_slice = int(input("Indica il quanto di tempo (in secondi): "))
table = {} #table:   {Processo: CPU_burst}
for i in range(procs_num):
    n = procs_order.split(",")[i]
    cpu_burst = int(input(f"Durata picco del processo P{n} (in secondi)"))
    table[f"P{n}"] = cpu_burst

#calcolo per ogni processo il momento di entrata e il momento di uscita dalla coda (in secondi) e li inserisco nella tupla
gantt = [] #lista di tuple (non uso il dizionario perchè ci saranno elementi con lo stesso nome di chiave [(Processo, (momento di entrata, momento di uscita))}
t = 0
wait_time = 0 #tempo di totale
#continuo finche tutti i cpu_burst non sono tutti nulli
while list(table.values()) != [0]*procs_num:
    for i in range(procs_num):
        current_cpu_burst = table[f"P{i+1}"]
        match current_cpu_burst:
            case 0:
                i += 1 # il processo ha finito quindi si passa al prossimo
            case _: #tutti gli altri casi
                if table[f"P{i+1}"] != 0:
                    cpu_burst = table[f"P{i+1}"]
                    if cpu_burst < time_slice: #il processo sarà eseguito tutto ed eliminato
                        gantt.append((f"P{i + 1}", (t, t + cpu_burst)))
                        t += cpu_burst
                        table[f"P{i+1}"] = 0
                    else:
                        gantt.append((f"P{i + 1}", (t, t + time_slice)))
                        t += time_slice
                        table[f"P{i+1}"] -= time_slice #si riduce il cpu burst di un time slice
print_gantt(gantt)
avg_wait_time = avg_wait_time(gantt, procs_num)
print(" ")
print(f"tempo di attesa medio: {avg_wait_time}")