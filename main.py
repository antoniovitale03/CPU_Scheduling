from CPU_Scheduling import CPU_Scheduling
answer = int(input("Quale algoritmo vuoi usare?\n"
                   "FCFS[0]\n"
                   "SFJ_NON_PREEMPTIVE[1]\n"
                   "SFJ_PREEMPTIVE[2]\n"
                   "ROUND ROBIN[3]\n "))

obj = CPU_Scheduling(answer)
obj.run()