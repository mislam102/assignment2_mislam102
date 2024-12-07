#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: "mislam102"
Semester: "fall"

The python code in this file is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: All functions working and all parts commented

'''

import argparse
import os, sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    # check the docs for an argparse option to store this as a boolean.
    parser.add_argument('-H', '--human-readable', action='store_true', help='Prints sizes in human readable format') # arguement for human readable using -H
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use is not.")
    args = parser.parse_args()
    return args
# create argparse function
# -H human readable
# -r running only

def percent_to_graph(percent: float, length: int=20) -> str:
    if percent < 0.0:   # this ensures that the float value is between 0.0 and 1.0
        percent = 0.0
    elif percent > 1.0:
        percent = 1.0

    # Scale the value to the length of the string
    num_hashes = int(round(percent * length)) # round is used to bring the value to nearest integer
    num_spaces = length - num_hashes # this will calculate the number of spaces needed
    
    # Generate the output string
    return '#' * num_hashes + ' ' * num_spaces # this finally returns number of has symbols with rest as num_spaces

def get_sys_mem() -> int:
    #"return total system memory (used or available) in kB"
    f = open('/proc/meminfo', 'r')  # This open the memory file as variable f
    for line in f:
        if 'MemTotal' in line:  # it finds that if MemTotal exists inside the line of f
            total_mem = int(line.split()[1])   # total mem variable give the Total memory which is found in file
            f.close() # this closes the opened file
            return total_mem  # this return the total mem variable 

    return None


def get_avail_mem() -> int:
    #"return total memory that is currently in use"
    f = open('/proc/meminfo', 'r')    # This open the process file which contains the memory which is opned as f
    for line in f:      
        if 'MemAvailable' in line:  # This find out is 'MemAvailbe' exists in the line 
            availmem_kb = int(line.split()[1]) # variable to give the aviaible memory
            f.close()   # This closes the opened file
            return availmem_kb # 
    
    return None
    
    

def pids_of_prog(app_name: str) -> list:
    #given an app name, return all pids associated with app"
    output = os.popen('pidof ' + app_name).read().strip()  #this executes the command using popen and read all pids
    return output.split() if output else []  #this return the pids of the appname if the pid is empty it return an empty list


def rss_mem_of_pid(proc_id: str) -> int:
    #given a process id, return the resident memory used, zero if not found"
    ...
    file_path = f"/proc/{proc_id}/smaps" # file path in smaps for processes
    rss_kb = 0  # Initialize RSS value
    
    try:
        with open(file_path, "r") as file: # open the file as read 
            for line in file: #iterates through each line 
                if line.startswith("Rss"): # looks for line starting with Rss
                    parts = line.split()
                    if len(parts) > 1:
                        rss_kb += int(parts[1])  # Convert directly to int and add
    except IOError: # if file cannot open gives out error opening file
        print(f"Error opening file {file_path}.")
        return 0

    return rss_kb

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    #turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

def display_memory_usage(program: str, length: int, human_readable: bool):
    "This Function i created so i can display memory usage of function in better way"
    pids = pids_of_prog(program)
    if not pids:
        print(f"{program} not found.") # an if statement if the specific program is running or not
        return

    total_rss_bytes = 0  # Initialize total memory usage
    for pid in pids:  # Loop through each process ID
     rss_bytes = rss_mem_of_pid(pid)  # Get memory usage for the process
     total_rss_bytes += rss_bytes
     rss_str = bytes_to_human_r(rss_bytes) if human_readable else str(rss_bytes) + " B"
     graph = percent_to_graph(rss_bytes / total_rss_bytes, length)  # Generate graph
     pid_str = str(pid)  # Convert PID to string
     print(pid_str + " [" + graph + " |  %  " + rss_str + "]")  # Print process details

    total_rss_str = bytes_to_human_r(total_rss_bytes) if human_readable else str(total_rss_bytes) + " B"
    graph_total = percent_to_graph(1, length)  # 100% graph for total usagess
    print(program + " [" + graph_total + " |  % " + total_rss_str + "]")  # Print program details



if __name__ == "__main__":
    args = parse_command_args() # process agrs

    if not args.program: # if no parameter passed, 
        
        total_mem = get_sys_mem()  # open meminfo.
        avail_mem = get_avail_mem() # get total memory
        used_mem = total_mem - avail_mem  # get used memory
        used_mem_percent = (used_mem / total_mem) if total_mem > 0 else 0 #
        graph = percent_to_graph(used_mem_percent, args.length) # call precent to graph
        final_percent = f"{used_mem_percent * 100:.0f}" # fstring to display round percentage and no decimal

        used_mem_str = bytes_to_human_r(used_mem) if args.human_readable else f"{used_mem} B" # use to define the used memory in bytes and gibs if asked in human readble format by user
        total_mem_str = bytes_to_human_r(total_mem) if args.human_readable else f"{total_mem} B" # similar to above just here total mem is used

        print("Memory         [" + graph + " |" + str(final_percent) + "%] " + used_mem_str + "/" + total_mem_str) # prints the final output in a readable format
    else:
        display_memory_usage(args.program, args.length, args.human_readable) # this calls the display memory usage function which i created above as extra
        ...
    

    
