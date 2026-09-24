import time


print("\033[2J")
time.sleep(0.5)
print('\033[H',end="")
time.sleep(0.5)
print("""wefwefwef
Ohio
Sibidi
Rixz""", end="")

print('\033[H',end="")
time.sleep(0.5)
# Clear and move down
for _ in range(3):
    print('\033[2K\033[B', end="", flush=True)
    print("Hi", end="", flush=True)
    time.sleep(0.5)
print(f'\033[{3}F', end="")