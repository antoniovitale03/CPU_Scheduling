import sys, random

def create_table(procs_num, procs_order):
    table = {}  # table:   {Processo: [Arrival time, CPU_burst]}
    arrival_time_list = []
    print("Il tempo di arrivo può essere anche in decimale")
    for i in range(procs_num):
        n = procs_order.split(",")[i]
        arrival_time = float(input(f"Tempo di arrivo di P{n}: "))
        arrival_time_list.append(arrival_time)
        cpu_burst = int(input(f"Durata picco di P{n}: "))
        table[f"P{n}"] = [arrival_time, cpu_burst]

    # controllo i tempi di arrivo
    if not check_arrival_time(arrival_time_list):
        sys.exit("I tempi di arrivo inseriti non corrispondono con l'ordine di arrivo dei processi!")
    return table

def check_arrival_time(list): #controllo che l'ordine dei processi inseriti corrisponda con i tempi di arrivo inseriti
    return list == sorted(list)

def wait_time(gantt, procs_order):
    total_wait_time = 0
    wait_times = []
    procs = procs_order.split(",")
    for i in range(len(procs)):
        wait_times.append(sum(value[0] for key, value in gantt if key == f"P{procs[i]}"))#tempo di attesa totale del i-esimo processo
        print(f"Tempo di attesa di P{procs[i]}: {wait_times[i]}")
        total_wait_time += wait_times[i]
    avg_wait_time = total_wait_time/procs_num
    print(f"Tempo di attesa medio: {avg_wait_time}")

def sjf_preemptive(table):
    t = 0
    gantt = [] #lista di tupla [(Processo, (momento di entrata, momento di uscita))]
    arrival_times_list = [value[0] for key, value in table.items()]

    while t < max(arrival_times_list): #la prelazione viene attuata in questo momento
        filtered_table = {key: value for key, value in table.items() if (value[1] != 0 and value[0] <= t)}
        shortest_job = min(value[1] for value in filtered_table.values())  # minimo cpu burst

        # Trovo i processi che hanno il minimo cpu burst
        min_burst_procs = {key: value for key, value in filtered_table.items() if value[1] == shortest_job}

        # Se è solo uno con il minimo cpu burst, lo seleziono
        if len(min_burst_procs) == 1:
            choosen_proc = list(min_burst_procs.keys())[0]
        # Se sono più di 1, seleziono quello con il tempo di arrivo minore
        else:
            min_arrival_time = min(value[0] for value in min_burst_procs.values())
            choosen_procs = [key for key, value in min_burst_procs.items() if value[0] == min_arrival_time]
            # se c'è solo un processo, lo scelgo
            if len(choosen_procs) == 1:
                choosen_proc = choosen_procs[0]
            else:  # se ci sono più processi che hanno lo stesso minimo cpu burst e stesso tempo di arrivo, ne scelgo uno casuale
                k = random.randint(0, len(choosen_procs))
                choosen_proc = choosen_procs[k]


        #aggiorno le informazioni dopo aver scelto il processo
        #prendo il tempo di arrivo del prossimo processo che diventerà il cpu burst del processo scelto
        arrival_time_choosen_proc = table[choosen_proc][0]
        arrival_times_list = [value for value in arrival_times_list if value > arrival_time_choosen_proc]
        cpu_burst = min(arrival_times_list)
        temp_t = t
        while temp_t < int(cpu_burst):
            if table[choosen_proc][1] > 0:
                temp_t += 1
                table[choosen_proc][1] -= 1
        gantt.append((f"{choosen_proc}", (t, temp_t)))
        t = temp_t
    return gantt, table, t

def sfj_non_preemptive(gantt, table, t):
    while any(value[1] > 0 for value in table.values()):
        filtered_table = {key: value for key, value in table.items() if (value[1] != 0 and value[0] <= t)}  # nuova tabella con i processi che hanno un tempo di arrivo minore di un certo valore t e che non siano stati già scelti
        shortest_job = min(value[1] for value in filtered_table.values())  # minimo cpu burst

        # Trovo i processi che hanno il minimo cpu burst
        min_burst_procs = {key: value for key, value in filtered_table.items() if value[1] == shortest_job}

        # Se è solo uno con il minimo cpu burst, lo seleziono
        if len(min_burst_procs) == 1:
            choosen_proc = list(min_burst_procs.keys())[0]
        # Se sono più di 1, seleziono quello con il tempo di arrivo minore
        else:
            min_arrival_time = min(value[0] for value in min_burst_procs.values())
            choosen_procs = [key for key, value in min_burst_procs.items() if value[0] == min_arrival_time]
            # se c'è solo un processo, lo scelgo
            if len(choosen_procs) == 1:
                choosen_proc = choosen_procs[0]
            else:  # se ci sono più processi che hanno lo stesso minimo cpu burst e stesso tempo di arrivo, ne scelgo uno casuale
                k = random.randint(0, len(choosen_procs))
                choosen_proc = choosen_procs[k]

        print(choosen_proc)
        # aggiorno le informazioni dopo aver scelto il processo
        choosen_proc_cpu_burst = min_burst_procs[choosen_proc][1]
        gantt.append((f"{choosen_proc}", (t, t + choosen_proc_cpu_burst)))
        t += choosen_proc_cpu_burst
        table[f"{choosen_proc}"][1] = 0
    return gantt


def print_gantt(gantt):
    print("Gantt:  ", end="")
    for key, value in gantt:
        proc_time = value[1] - value[0]
        print(f"{key}({proc_time}) -> ", end="")


procs_num = int(input("Inserire il numero dei processi in coda: "))
procs_order = input("Indica l'ordine di arrivo dei processi in coda. Ad esempio, "
                        "scrivendo 2,3,1 stai indicando che i processi arrivano nell'ordine P2, P3, P1 ")
table = create_table(procs_num, procs_order)
gantt, table, t = sjf_preemptive(table)  #applico la prelazione ai processi
gantt = sfj_non_preemptive(gantt, table, t)  #proseguo con lo stesso metodo del sfj preemptive, non applico più prelazione

print_gantt(gantt)
wait_time(gantt, procs_order)
