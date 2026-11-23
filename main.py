import random
import subprocess
import platform
from testerr import argerr

INT_MIN = -2147483648
INT_MAX = 2147483647

NB_ARG = []

nb = input("Enter how many numbers you want to test (ex : 10 25 500) : ")
NB_ARG = nb.split()

nb_test = int(input("How many test per size : "))
while nb_test < 1:
    input("Enter a valid number.")
    nb_test = int(input("How many test per size : "))

def know_os():
    user = platform.system()
    return(user)

def checker_ps(user):
    if user == "Darwin":
        return("./checker_Mac")
    if user == "Linux":
        return("./checker_linux")
    else:
        return("./checker_fedora")

def generate_numbers(i, NB_ARG):
    args = ["./push_swap", "--adaptive"]
    while len(args) - 2 < int(NB_ARG[i]):
        nombre = random.randint(INT_MIN, INT_MAX)

        if str(nombre) not in args:
            args.append(str(nombre))

    return(args)

def test_forsize(op, oklst, kolst, j, t):
    checker = checker_ps(know_os())
    size = NB_ARG.index(t)
    while j < nb_test:
        t = generate_numbers(size, NB_ARG)
        j += 1
        result = subprocess.run(t, capture_output=True, text=True)
        nb_op = result.stdout.splitlines()

        if result.returncode != 0:
            kolst.append("KO")
            continue

        result_checker = subprocess.run([checker] + t[2:], input=result.stdout, capture_output=True, text=True)

        if compteur(result_checker, oklst, kolst) == 1:
            op.append(len(nb_op))

def env_gennbr_to_ps(NB_ARG, i):
    for t in NB_ARG:
        print(f"[Number {NB_ARG[i]}]")
        op = []
        j = 0
        oklst = []
        kolst = []

        test_forsize(op, oklst, kolst, j, t)

        if len(op) > 0:
            avg = int(sum(op)) / int(len(op))
            print(f"OK : {len(oklst)}\nKO : {len(kolst)}\nMin ops : {min(op)}\nMax ops : {max(op)}\nAvg ops : {avg}")
        else:
            print(f"OK : {len(oklst)}\nKO : {len(kolst)}\nNo valid operations")
        print("\n")
        i += 1

def compteur(result_checker, oklst, kolst):
    if result_checker.returncode == 0 and result_checker.stdout.strip() == "OK":
        oklst.append("OK")
        return (1)
    else:
        kolst.append("KO")
        return (0)


if __name__ == "__main__":
    i = 0
    argerr()
    env_gennbr_to_ps(NB_ARG, i)
