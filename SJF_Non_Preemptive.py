def check_arrival_time(): #controllo che l'ordine dei processi inseriti corrisponda con i tempi di arrivo inseriti
    print("j")
procs_num = int(input("Inserire il numero dei processi in coda: "))

table = {} #table:   Processo: [Arrival time, CPU_burst, (momento in entrata del processo, momento in uscita)]

for i in range(procs_num):
    n = i + 1
    arrival_time = float(input(f"Tempo di arrivo di P{n} (ammesso anche numero decimale): "))
    cpu_burst = int(input(f"Durata picco di P{n}: "))
    table[f"P{n}"] = [arrival_time, cpu_burst]

table = dict(sorted(table.items(), key=lambda x: x[1][0])) #ordino la tabella in ordine crescente sulla basse del tempo di arrivo
print(table)
#print("Gantt: ", end="")
#scelgo il primo processo che è arrivato in coda (quindi il primo della tabella ordinata)
t = 0
wait_time = 0 #tempo di attesa totale
first_process = list(table.keys())[0]
first_process_cpu_burst = list(table.values())[0][1]
table["P1"].append((t, t + first_process_cpu_burst))
#print(f"P1({first_process_cpu_burst}) -> ", end="")
#una volta scelto, setto arrival_time e cpu_burst a "X"
#table["P1"] = ["X", "X"]
#scelta del prossimo processo
arrival_time_list = []
cpu_burst_list = []
values_list = list(table.values())
for i in range(procs_num):
    arrival_time = values_list[i][0]
    arrival_time_list.append(arrival_time)
    cpu_burst_ = values_list[i][1]
    cpu_burst_list.append(cpu_burst_)
print(arrival_time_list, cpu_burst_list)




