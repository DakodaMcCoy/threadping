# Batch Ping Utility with Multithreading by Dakoda McCoy
# 09/09/2021

from concurrent.futures import ThreadPoolExecutor, as_completed
from termcolor import colored
from datetime import datetime, date
import subprocess
import concurrent.futures.thread
import time
import os
import sys

# Supresses Traceback Errors
sys.tracebacklimit = 0

# Sets Console Window Title
os.system("title Ping Test Utility")

# Assigns today's date to a variable
today = date.today().strftime("%m%d%Y")

# Assigns script current directory to variable
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

# Opens NUL for redirected messages
f = open("nul", "w")

# Initilizes list of down hosts
down_hosts = []

# Gets list filename from user
def getFileName():
    file = input("Enter list filename: ")
    return file


# Gets number of concurrent threads from user
def getThreads():
    try:
        threads = int(input("Number of threads: "))
        return threads
    except ValueError:
        print("Must input an integer. Please try again.")
        getThreads()


# Opens file and raises an error if file does not exist
def openFile(file):
    try:
        hosts = open(os.path.join(dirname, file), "r")
        print("\nUsing File: " + dirname + "\\" + file + "\n")
        return hosts
    except FileNotFoundError:
        print("File name does not exist.")
        getFileName()
        openFile()


# Creates or opens log file with today's date
def openLog(today):
    log = open(today + "pingtest.log", "a")
    log.write("\n=========================================\n")
    return log


# Pings given host twice and outputs up if there is a reply and down if not
# Logs responses in the log file
def pingsweep(host):
    host = host.strip()
    result = subprocess.call(["ping", "-n", "2", host], stdout=f)

    if result == 0:

        dt = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(dt + " " + colored(host, "cyan") + " is " + colored("up", "green"))
        log.write(dt + " " + host + " is up\n")

    else:
        down_hosts.append(host)
        dt = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(dt + " " + colored(host, "cyan") + " is " + colored("down", "red"))
        log.write(dt + " " + host + " is down\n")


# Prints a summary of down hosts and gives location of the log file.
def printSummary():
    print("\nList of down hosts:\n")
    log.write("\nList of down hosts:\n")
    for x in down_hosts:
        print(x)
        log.writelines(x + "\n")

    log.write("\n=========================================\n")

    hosts.close()
    log.close()

    print("\nResults saved in " + dirname + "\\" + today + "pingtest.log")
    input("Press enter to exit.")


file = getFileName()
# threads = getThreads() # Currently disabled to prevent user from inputing too many threads
hosts = openFile(file)
log = openLog(today)

# Creates given number of threads to execute pingsweep function. Kills all threads when Ctrl-C is pressed.
with ThreadPoolExecutor(25) as executor:
    ping_hosts = [executor.submit(pingsweep, host) for host in hosts]
    try:
        for future in as_completed(ping_hosts):
            future.result()
    except KeyboardInterrupt:
        executor.shutdown(wait=False, cancel_futures=True)
        executor._threads.clear()
        concurrent.futures.thread._threads_queues.clear()
        time.sleep(2)
        print(colored("\nScan Aborted!\n", "red"))
        log.write("\nScan Aborted!\n")
        raise


printSummary()
