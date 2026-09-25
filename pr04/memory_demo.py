import multiprocessing
import threading

shared_list = [1, 2, 3]

def thread_worker():
    shared_list.append(4)
    print("Внутри потока:", shared_list, flush=True)

def process_worker():
    shared_list.append(5)
    print("Внутри процесса:", shared_list, flush=True)

def main():
    print("Исходный список:", shared_list)

    thread = threading.Thread(target=thread_worker)
    thread.start()
    thread.join()

    print("После потока:", shared_list)

    process = multiprocessing.Process(target=process_worker)
    process.start()
    process.join()

    print("После процесса:", shared_list)

if __name__ == "__main__":
    main()
