import random
import subprocess
import platform

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

def env_gennbr_to_ps(NB_ARG, i):
    for t in NB_ARG:
        print(f"[{NB_ARG[i]}]")
        op = []
        j = 0
        oklst = []
        kolst = []
        while j < nb_test:
            t = generate_numbers(i, NB_ARG)
            result = subprocess.run(t, capture_output=True, text=True)
            nb_op = result.stdout.splitlines()
            op.append(len(nb_op))

            checker = checker_ps(know_os())
            result_checker = subprocess.run([checker] + t[2:], input=result.stdout, capture_output=True, text=True)
            
            compteur(result_checker, oklst, kolst)
            j += 1
        avg = int(sum(op)) / int(len(op))
        print(f"OK : {len(oklst)}\nKO : {len(kolst)}\nMin ops : {min(op)}\nMax ops : {max(op)}\nAvg ops : {avg}")
        print("\n")
        i += 1

def compteur(result_checker, oklst, kolst):
    if result_checker.stdout.strip() == "OK":
        oklst.append("OK")
    else:
        kolst.append("KO")

if __name__ == "__main__":
    i = 0
    env_gennbr_to_ps(NB_ARG, i)
