import subprocess
"""
Algorithm script to request solution from TwoPhase solver and return solution using PIPES
"""


def start_twophase():
    executable_path = "./rob-twophase/twophase.exe"

    # Create a subprocess with stdout and stderr redirected to a pipe, and stdin as a pipe
    p = subprocess.Popen(executable_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, text=True)

    # Read the first 8 lines from the subprocess output to clear it
    num_lines_to_read = 8
    for i in range(num_lines_to_read):
        line = p.stdout.readline()

    return p 
   
def run_twophase(p, facestring):
    # Write to stdin and flush it after
    p.stdin.write(f'solve {facestring}\n')
    p.stdin.flush()

    # Read and print the resulting 3 lines from the subprocess output
    num_result_lines = 3
    for i in range(num_result_lines):
        line = p.stdout.readline()
        if i == 1: # return only the solution string
            solution = line.strip()
    
    return solution