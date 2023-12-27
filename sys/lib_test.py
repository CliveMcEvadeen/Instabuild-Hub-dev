import magic

with open("C:\\Users\\ADAN COMPUTER\\Desktop\\instabuildhub\sys\\lib_test.py", 'r') as file:
    first_line = file.readline().strip()
    if first_line.startswith("#!") and "python" in first_line.lower():
        print("The file appears to be a Python script.")
    else:
        print("The file may not be a Python script.")
