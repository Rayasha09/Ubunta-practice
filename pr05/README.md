
## Цель работы
Реализовать и сравнить алгоритмы планирования процессов по метрикам ожидания, оборота, отклика и загрузки CPU.

## Реализованные алгоритмы
- FCFS — первым пришёл, первым обслужен.
- SJF — кратчайшая задача первой, без вытеснения.
- SRTF — кратчайшее оставшееся время, с вытеснением.
- Priority — вытесняющее планирование по приоритету; меньшее число означает более высокий приоритет.
- RR — циклическое планирование с настраиваемым квантом.

## Запуск

```bash
python3 sched.py --algo fcfs set1.txt
python3 sched.py --algo sjf set1.txt
python3 sched.py --algo srtf set1.txt
python3 sched.py --algo priority set1.txt
python3 sched.py --algo rr --quantum 3 set1.txt
python3 sched.py --algo fcfs set1.txt
python3 sched.py --algo sjf set1.txt
python3 sched.py --algo srtf set1.txt
python3 sched.py --algo priority set1.txt
python3 sched.py --algo rr --quantum 3 set1.txt
