
def print_file(filename):
    with open(filename) as file:
        lines = file.readlines()
        count = 0
        # Strips the newline character
        for line in lines:
            print("Line{}: {}".format(count, line.strip()))
            count += 1


print_file("primary1.txt")
print_file("primary2.txt")