import functions
import os
import time
import sys

MAX_FIELDS = 6
MAX_TYPE_LENGTH = 12
MAX_FIELD_LENGTH = 20
input_file = sys.argv[1]


def log(time, input, result):
    if not os.path.exists("log.txt"):
        with open("log.txt", "a") as file:
            file.write(f"{time}, {input.strip()}, {result}\n")
            return
    with open("log.txt", "a") as file:
        file.write(f"{time}, {input.strip()}, {result}\n")
        return


open(functions.OUTPUT_FILE, "w").close()
with open(input_file, "r") as file:
    lines = [line for line in file.readlines()]
    for line in lines:
        line_lst = line.strip().split(" ")
        if line_lst[0] == "create":
            if line_lst[1] == "type":
                # try:
                if len(line_lst) != int(line_lst[3]) * 2 + 5:
                    # print("Invalid number of arguments: ", len(line_lst), int(line_lst[3]) * 2 + 5)
                    log(int(time.time()), line, "failure")
                elif len(line_lst[2]) > MAX_TYPE_LENGTH:
                    # print("Invalid type name")
                    log(int(time.time()), line, "failure")
                else:
                    fields = {}
                    for i in range(5, len(line_lst), 2):
                        if len(line_lst[i]) > MAX_FIELD_LENGTH:
                            # print("Invalid field name")
                            log(int(time.time()), line, "failure")
                            break
                        fields[line_lst[i]] = line_lst[i + 1]
                    res = functions.create_type(line_lst[2], line_lst[3], line_lst[4], fields)
                    if res:
                        log(int(time.time()), line, "success")
                    else:
                        log(int(time.time()), line, "failure")
                # except:
                #    print("ERROR 1")
                #    log(int(time.time()), line, "failure")
            elif line_lst[1] == "record":
                if len(line_lst) > MAX_FIELDS + 3:
                    print("Invalid number of arguments")
                    log(int(time.time()), line, "failure")
                else:
                    res = functions.create_record(line_lst[2], line_lst[3:])
                    if res:
                        log(int(time.time()), line, "success")
                    else:
                        log(int(time.time()), line, "failure")
        elif line_lst[0] == "delete":
            if len(line_lst) != 4:
                print("Invalid number of arguments")
                log(int(time.time()), line, "failure")
            else:
                res = functions.delete(line_lst[2], line_lst[3])
                if res:
                    log(int(time.time()), line, "success")
                else:
                    log(int(time.time()), line, "failure")
        elif line_lst[0] == "search":
            if len(line_lst) != 4:
                print("Invalid number of arguments")
                log(int(time.time()), line, "failure")
            else:
                res = functions.search(line_lst[2], line_lst[3], True)
                if res:
                    log(int(time.time()), line, "success")
                else:
                    log(int(time.time()), line, "failure")
