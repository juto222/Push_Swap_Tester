import subprocess
import shlex

def argerr():
    args = ["./push_swap", "./push_swap 1 2 2 3", "./push_swap 1 abc 2", "./push_swap 1 2147483648",
            "./push_swap -2147483649 2", "./push_swap --bench --bench 3 2 1", "./push_swap --simple --complex 3 2 1",
            "./push_swap --unknown 3 2 1", "./push_swap --unknown 3 2 1", "./push_swap --bench"]
    for t in args:
        outp = subprocess.run(shlex.split(t), capture_output=True, text=True)
        if outputerr(outp, t) == 1:
            print(f"[PASS] {t}")
        else:
            print(f"[FAIL] {t}")
    print("\n")

def outputerr(outp, t):
    if t == "./push_swap":
        if outp.stderr == "" and outp.stdout == "":
            return(1)
    elif outp.stderr.strip() == "Error":
        return(1)
    return(0)