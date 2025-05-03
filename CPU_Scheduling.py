import sys, random
class CPU_Scheduling:
    def __init__(self, response):
        self.response = response
        self.procs_num, self.procs_order = self.get_data()


    def get_data(self):
        procs_num = int(input("Inserire il numero dei processi in coda: "))

        procs_order = input("Indica l'ordine di arrivo dei processi in coda. Ad esempio, "
                            "scrivendo 2,3,1 stai indicando che i processi arrivano nell'ordine P2, P3, P1 ")
        return procs_num, procs_order

    def wait_time(self, gantt, procs_order, procs_num):
        total_wait_time = 0
        wait_times = []
        procs = procs_order.split(",")
        for i in range(len(procs)):
            n = procs[i]
            wait_times.append(
                sum(value[0] for key, value in gantt if key == f"P{n}"))  # tempo di attesa totale del i-esimo processo
            print(f"Tempo di attesa di P{n}: {wait_times[i]}")
            total_wait_time += wait_times[i]
        avg_wait_time = total_wait_time / procs_num
        print(f"Tempo di attesa medio: {avg_wait_time}")

    def print_gantt(self, gantt):
        print("Gantt: ", end="")
        for key, value in gantt:
            proc_time = value[1] - value[0]
            if value == gantt[-1][1]: #ultimo valore non printare la freccia
                print(f"{key}({proc_time}) ", end="")
            else: print(f"{key}({proc_time}) -> ", end="")
        print(" ")

    def check_arrival_time(self, list):  # controllo che l'ordine dei processi inseriti corrisponda con i tempi di arrivo inseriti
        return list == sorted(list)

    def choose_process(self, table, t):
        filtered_table = {key: value for key, value in table.items() if (value[1] != 0 and value[
            0] <= t)}  # nuova tabella con i processi che hanno un tempo di arrivo minore di un certo valore t e che non siano stati già scelti
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
        return min_burst_procs, choosen_proc

    def create_table_0_3(self, procs_num, procs_order): #fcfs e roun robin
        table = {}  # table:   {Processo: CPU_burst}
        for i in range(procs_num):
            n = procs_order.split(",")[i]
            cpu_burst = int(input(f"Durata picco del processo P{n} (in secondi)"))
            table[f"P{n}"] = cpu_burst
        return table

    def create_table_1_2(self, procs_num, procs_order): #sfj non preemptive e sfj preemptive
        table = {}  # table:   {Processo: [Arrival time, CPU_burst]}
        arrival_times_list = []
        print("Il tempo di arrivo può essere anche in decimale")
        for i in range(procs_num):
            n = procs_order.split(",")[i]
            arrival_time = float(input(f"Tempo di arrivo di P{n}: "))
            arrival_times_list.append(arrival_time)
            cpu_burst = int(input(f"Durata picco di P{n}: "))
            table[f"P{n}"] = [arrival_time, cpu_burst]

        # controllo i tempi di arrivo
        if not self.check_arrival_time(arrival_times_list):
            sys.exit("I tempi di arrivo inseriti non corrispondono con l'ordine di arrivo dei processi!")
        return table

    def create_gantt_0(self, table, t, gantt): #fcfs
        for key, value in table.items():
            cpu_burst = value
            gantt.append((f"{key}", (t, t + cpu_burst)))
            t = t + cpu_burst
        return gantt

    def create_gantt_1(self, table, t, gantt): #sfj non preemptive
        while any(value[1] > 0 for value in table.values()):
            min_burst_procs, choosen_proc = self.choose_process(table, t)

            # aggiorno le informazioni dopo aver scelto il processo
            choosen_proc_cpu_burst = min_burst_procs[choosen_proc][1]
            gantt.append((f"{choosen_proc}", (t, t + choosen_proc_cpu_burst)))
            t += choosen_proc_cpu_burst
            table[f"{choosen_proc}"][1] = 0
        return gantt

    def create_gantt_2(self, table, t, gantt):
        arrival_times_list = [value[0] for key, value in table.items()]
        while t < max(arrival_times_list):  # la prelazione viene attuata in questo momento
            min_burst_procs, choosen_proc = self.choose_process(table, t)

            # aggiorno le informazioni dopo aver scelto il processo
            # prendo il tempo di arrivo del prossimo processo che diventerà il cpu burst del processo scelto
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
        gantt = self.create_gantt_1(table, t, gantt)
        return gantt


    def create_gantt_3(self, table, t, gantt):
        time_slice = int(input("Indica il quanto di tempo (in secondi): "))
        # continuo finche tutti i cpu_burst non sono tutti nulli
        while any(value > 0 for value in table.values()):
            for i in range(self.procs_num):
                current_cpu_burst = table[f"P{i + 1}"]
                match current_cpu_burst:
                    case 0:
                        i += 1  # il processo ha finito quindi si passa al prossimo
                    case _:  # tutti gli altri casi
                        cpu_burst = table[f"P{i + 1}"]
                        if cpu_burst < time_slice:  # il processo sarà eseguito tutto ed eliminato
                            gantt.append((f"P{i + 1}", (t, t + cpu_burst)))
                            t += cpu_burst
                            table[f"P{i + 1}"] = 0
                        else:
                            gantt.append((f"P{i + 1}", (t, t + time_slice)))
                            t += time_slice
                            table[f"P{i + 1}"] -= time_slice  # si riduce il cpu burst di un time slice
        return gantt


    def run_fcfs(self, procs_num, procs_order, t, gantt):
        table = self.create_table_0_3(procs_num, procs_order)
        gantt = self.create_gantt_0(table, t, gantt)
        self.print_gantt(gantt)
        self.wait_time(gantt, procs_order, procs_num)

    def run_sfj_non_preemptive(self, procs_num, procs_order, t, gantt):
        table = self.create_table_1_2(procs_num, procs_order)
        gantt = self.create_gantt_1(table, t, gantt)
        self.print_gantt(gantt)
        self.wait_time(gantt, procs_order, procs_num)

    def run_sfj_preemptive(self, procs_num, procs_order, t, gantt):
        table = self.create_table_1_2(procs_num, procs_order)
        gantt = self.create_gantt_2(table, t, gantt)
        self.print_gantt(gantt)
        self.wait_time(gantt, procs_order, procs_num)

    def run_round_robin(self, procs_num, procs_order, t, gantt):
        table = self.create_table_0_3(procs_num, procs_order)
        gantt = self.create_gantt_3(table, t, gantt)
        self.print_gantt(gantt)
        self.wait_time(gantt, procs_order, procs_num)

    def run(self):
        t = 0
        gantt = []
        match self.response:
            case 0:
                self.run_fcfs(self.procs_num, self.procs_order, t, gantt)
            case 1:
                self.run_sfj_non_preemptive(self.procs_num, self.procs_order, t, gantt)
            case 2:
                self.run_sfj_preemptive(self.procs_num, self.procs_order, t, gantt)
            case 3:
                self.run_round_robin(self.procs_num, self.procs_order, t, gantt)

