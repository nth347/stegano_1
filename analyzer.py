# Function to count how many bytes in a file
def count_bytes(file):
    count = 0
    with open(file, 'rb') as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            count += 1
        return count

# The main program
if __name__ == "__main__":
    length_before = count_bytes('container_before.txt')
    length_after = count_bytes('container_after.txt')
    print("Length before: {} bytes".format(length_before))
    print("Length after: {} bytes".format(length_after))
    print("Difference: {:.2f} %". format((abs(length_after - length_before) / length_before) * 100))