import sys, random
def check_arrival_time(list): #controllo che l'ordine dei processi inseriti corrisponda con i tempi di arrivo inseriti
    if list == sorted(list):
        return True
    else:
        return False


procs_num = int(input("Inserire il numero dei processi in coda: "))
procs_order = input("Indica l'ordine di arrivo dei processi in coda. Ad esempio, "
          "scrivendo 2,3,1 stai indicando che i processi arrivano nell'ordine P2, P3, P1 ")

table = {} #table:   Processo: [Arrival time, CPU_burst]
arrival_time_list = [] #creo questa lista per vedere se i tempi di arrivo sono in ordine
for i in range(procs_num):
    n = procs_order.split(",")[i]
    print("Il tempo di arrivo può essere anche in decimale")
    arrival_time = float(input(f"Tempo di arrivo di P{n}: "))
    arrival_time_list.append(arrival_time)
    cpu_burst = int(input(f"Durata picco di P{n}: "))
    table[f"P{n}"] = [arrival_time, cpu_burst]

#controllo i tempi di arrivo
if not check_arrival_time(arrival_time_list):
    sys.exit("I tempi di arrivo inseriti non corrispondono con l'ordine di arrivo dei processi!")


gantt = {} #gantt: {Processo: (momento di entrata, momento di uscita)}
#scelgo come primo processo il primo che è arrivato in coda (quindi il primo della tabella ordinata)
t = 0
wait_time = 0 #tempo di attesa totale
first_process = list(table.keys())[0]
first_process_cpu_burst = list(table.values())[0][1]
gantt[f"{first_process}"] = ((t, t + first_process_cpu_burst))
t += first_process_cpu_burst
table[first_process] = ["X", "X"]

k=0
for k in range(procs_num-1):
    filtered_table = {key: value for key, value in table.items() if (value[0] != "X" and value[0] < t)} #nuova tabella con i processi che hanno un tempo di arrivo minore di un certo valore t e che non siano stati già scelti
    shortest_job = min(value[1] for value in filtered_table.values()) #minimo cpu burst

    # Trovo i processi che hanno il minimo cpu burst
    min_burst_procs = {key: value for key, value in filtered_table.items() if value[1] == shortest_job}

    #Se è solo uno con il minimo cpu burst, lo seleziono
    if len(min_burst_procs) == 1:
        choosen_proc = list(min_burst_procs.keys())[0]
    #Se sono più di 1, seleziono quello con il tempo di arrivo minore
    else:
        min_arrival_time = min(value[0] for value in min_burst_procs.values())
        choosen_procs = [key for key, value in min_burst_procs.items() if value[0] == min_arrival_time]
        #se c'è solo un processo, lo scelgo
        if len(choosen_procs) == 1:
            choosen_proc = choosen_procs[0]
        else: #se ci sono più processi che hanno lo stesso minimo cpu burst e stesso tempo di arrivo, ne scelgo uno casuale
            k = random.randint(0, len(choosen_procs))
            choosen_proc = choosen_procs[k]

    #aggiorno le informazioni dopo aver scelto il processo
    choosen_proc_cpu_burst = min_burst_procs[choosen_proc][1]
    gantt[f"{choosen_proc}"] = ((t, t + choosen_proc_cpu_burst))
    t += choosen_proc_cpu_burst
    table[f"{choosen_proc}"] = ["X", "X"]

print(table)
print(gantt)





