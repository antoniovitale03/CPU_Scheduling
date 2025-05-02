import sys
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
        print("Gantt:  ", end="")
        for key, value in gantt:
            proc_time = value[1] - value[0]
            print(f"{key}({proc_time}) -> ", end="")

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
        if not check_arrival_time(arrival_times_list):
            sys.exit("I tempi di arrivo inseriti non corrispondono con l'ordine di arrivo dei processi!")
        return table

    def create_gantt_0(self, table): #fcfs
        gantt = []  # gantt: [(Processo, (momento di entrata, momento di uscita))
        t = 0
        for key, value in table.items():
            cpu_burst = value
            gantt.append((f"{key}", (t, t + cpu_burst)))
            t = t + cpu_burst
        return gantt

    def create_gantt_1(self, table): #sfj non preemptive
        t = 0
        gantt = []  # gantt: [(Processo, (momento di entrata, momento di uscita)
        while any(value[1] > 0 for value in table.values()):
            min_burst_procs, choosen_proc = choose_process(table, t)

            # aggiorno le informazioni dopo aver scelto il processo
            choosen_proc_cpu_burst = min_burst_procs[choosen_proc][1]
            gantt.append((f"{choosen_proc}", (t, t + choosen_proc_cpu_burst)))
            t += choosen_proc_cpu_burst
            table[f"{choosen_proc}"][1] = 0
        return gantt







    def run_fcfs(self, procs_num, procs_order):
        table = self.create_table_0_3(procs_num, procs_order)
        gantt = self.create_gantt_0(table)
        self.print_gantt(gantt)
        self.wait_time(gantt, procs_order)


    def run(self):
        match self.response:
            case 0:
                self.run_fcfs(self.procs_num, self.procs_order)
            case 1:
                run_sfj_non_preemptive()
            case 2:
                run_sfj_preemptive()
            case 3:
                run_round_robin()

