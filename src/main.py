PAGE_SIZE = 1
FILE_SIZE = 1
MAX_FIELDS = 1
MAX_TYPE_LENGTH = 1
MAX_FIELD_LENGTH = 1


with open("input.txt", "r") as file:
    lines = [line.strip().split(" ") for line in file.readlines()]
    for line in lines:
        if line[0] == "create":
            if line[1] == "type":
                pass
            elif line[1] == "record":
                pass
        elif line[0] == "delete":
            pass
        elif line[0] == "search":
            pass
    print(lines)