def sum_equals(a):
    sum = 0
    for x in a:
        sum += x
    return sum

def count_int(a):
    count = 0
    for x in a:
        if isinstance(x, int):
            count += 1
    return count

def print_3and7(min, max):
    output = []
    for x in range(min, max+1):
        if x % 3 == 0 or x % 7 == 0:
            output.append(x)
    return output

def reverse_list(a):
    return a[::-1]

def is_n_times(s, n, sn):
    if sn == s*n:
        return True
    else:
        return False

def print_graph(a):
    for x in a:
        current = ""
        for y in range(int(x*10)):
            current += "#"
        print(current)

def to_str(x, y, z):
    return "(" + str(x) + ", " + str(y) + ", " + str(z) + ") = (" + format(x, 'x') + ", " + format(y, 'x') + ", " + format(z, 'x') + ")"

# Das Else wird dann wirksam wenn die for loop erfolgreich
# durchläuft und nicht durch ein break oder return beendet wird.
# Wie in diesem Beispiel schön demonstriert, kann man damit
# schauen ob ein Item in einer Liste vorhanden ist, oder nicht.
# Ist es vorhanden, wird die Loop durch ein return beendet -> kein else
# Ist es nicht vorhanden, läuft die schleife komplett durch -> else
def demo_loop_else():
    items = ["banane", "apfel", "birne"]
    for item in items:
        if item == "banane":
            return("gefunden")
    else:
        return("item nicht gefunden")

def main_method():
    print("sum_equals:")
    print(sum_equals([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]))
    print("\ncount_int:")
    print(count_int([1.0, 1, 2, 3, 4.0, "string", 4]))
    print("\nprint_3and7:")
    print(print_3and7(1, 14))
    print("\nreverse_list:")
    print(reverse_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]))
    print("\nis_n_times")
    print("T: " + str(is_n_times("hallo", 3, "hallohallohallo")))
    print("F: " + str(is_n_times("hallo", 4, "hallohallohallo")))
    print("\nPrint graph:")
    print_graph([0.35, 1, 0.54])
    print("\nto_str:")
    print(to_str(32, 5, 255))
    print("\ndemo_loop_else:")
    print(demo_loop_else())


main_method()