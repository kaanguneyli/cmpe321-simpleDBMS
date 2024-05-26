import os

RECORDS_PER_PAGE = 10
PAGES_PER_FILE = 10000
OUTPUT_FILE = "output.txt"


def replace_line(file_path, line_number, new_line):
    temp_file_path = file_path + '.tmp'

    with open(file_path, 'r') as input_file, open(temp_file_path, 'w') as output_file:
        current_line = 1
        for line in input_file:
            if current_line == line_number:
                # replaces the record to be deleted with the last record of the given type
                output_file.write(new_line + '\n')
            else:
                # preserves all the other records
                output_file.write(line)
            current_line += 1

    # Replace the original file with the temporary file
    os.replace(temp_file_path, file_path)


def create_type(type_name: str, number_of_fields: str, primary_key_order: str, fields: dict):
    # create a folder under files with given type name
    if os.path.isdir(f"files/{type_name}"):
        # print("Type already exists")
        return False
    if not (os.path.isdir("files")):
        os.mkdir("files")
    os.mkdir(f"files/{type_name}")
    # create header(metadata.txt) and the file(file.txt) containing records
    with open(f"files/{type_name}/metadata.txt", "w") as file:
        file.write(f"{number_of_fields}\n")
        file.write(f"{primary_key_order}\n")
    with open(f"files/{type_name}/file.txt", "w") as file:
        file.write("0\n")
        pass
    return True


def create_record(type_name: str, values: list[str]):
    # find the folder under files and then find the correct type folder
    # finally find the correct page and line in txt's and place the record
    if not os.path.isdir(f"files/{type_name}"):
        # print("Type does not exist")
        return False
    with open(f"files/{type_name}/metadata.txt", "r") as file:
        number_of_fields = int(file.readline().strip())
        primary_key_order = int(file.readline().strip())
    if len(values) != number_of_fields:
        # print("Invalid number of fields")
        return False
    records_in_page = 0
    first_empty_page = 0
    page_begin_position = 0
    lines = []
    # find the correct position to insert
    with open(f"files/{type_name}/file.txt", "r") as file:
        page_begin_position = file.tell()
        line = file.readline()
        records_in_page = int(line.strip('\n '))
        while records_in_page == 10:
            first_empty_page += 1
            for i in range(RECORDS_PER_PAGE):
                line = file.readline()
                if line.split()[primary_key_order - 1] == values[primary_key_order - 1]:
                    # print("Primary key already exists")
                    return False
            page_begin_position = file.tell()
            line = file.readline()
            records_in_page = int(line.strip('\n '))
        lines.append(f"{records_in_page + 1}\n")
        if first_empty_page >= PAGES_PER_FILE:
            # file is full cannot add more pages
            return False
        for i in range(records_in_page):
            line = file.readline()
            lines.append(line)
            # print(line.split(), primary_key_order-1)
            if line.split()[primary_key_order - 1] == values[primary_key_order - 1]:
                # print("Primary key already exists")
                return False
        records_in_page += 1
    # insert the record to the correct position
    if records_in_page == 10:
        with open(f"files/{type_name}/file.txt", "r+") as file:
            file.seek(page_begin_position)
            for i in lines:
                file.write(i)
            file.write(" ".join(values) + "\n")
            file.write("0\n")
            return True
    else:
        with open(f"files/{type_name}/file.txt", "r+") as file:
            file.seek(page_begin_position)
            for i in lines:
                file.write(i)
            file.write(" ".join(values) + "\n")
            return True


def delete(type_name: str, primary_key: str):
    search_tup = search(type_name, primary_key, False)
    if not search_tup:
        return False
    # find the folder under files (file), find the correct space in txt's (page) and delete the record
    if not os.path.isdir(f"files/{type_name}"):
        # print("Type does not exist")
        return False
    last_record = ""
    with open(f"files/{type_name}/metadata.txt", "r") as file2:
        file2.readline()
        primary_key_order = int(file2.readline().strip())
        with open(f"files/{type_name}/file.txt", "r+") as file:
            last_page_begin = file.tell()
            page_last_rec = file.tell()
            prev_page = file.tell()
            line = file.readline()
            records_in_page = int(line.strip('\n '))
            if records_in_page == 0:
                return False
            while records_in_page == 10:
                for i in range(RECORDS_PER_PAGE):
                    page_last_rec = file.tell()
                    file.readline()
                prev_page = last_page_begin
                last_page_begin = file.tell()
                line = file.readline()
                records_in_page = int(line.strip('\n '))
            if records_in_page == 0:
                lines = []
                file.seek(prev_page)
                file.readline()
                lines.append(f"9\n")
                for i in range(9):
                    line = file.readline()
                    lines.append(line)
                last_record = file.readline()
                file.seek(prev_page)
                lines.append(f"0\n")
                for i in lines:
                    file.write(i)
                file.truncate()
            else:
                lines = []
                lines.append(f"{records_in_page - 1}\n")
                for i in range(records_in_page - 1):
                    line = file.readline()
                    lines.append(line)
                last_record = file.readline()
                file.seek(last_page_begin)
                lines.append(f"0\n")
                for i in lines:
                    file.write(i)
                file.truncate()
                file.flush()
            file2.flush()
    if last_record.split()[primary_key_order - 1] == primary_key:
        return True
    line_no = search_tup[1] * 11 + search_tup[0] + 1
    replace_line(f"files/{type_name}/file.txt", line_no, last_record.strip('\n'))
    return True


def search(type_name: str, primary_key: str, flag: bool):
    # find the folder under files with the correct type
    # then check all pages one by one to find the requested record
    if not os.path.isdir(f"files/{type_name}"):
        # print("Type does not exist")
        return False
    # open file header
    with open(f"files/{type_name}/metadata.txt", "r") as file2:
        file2.readline()
        primary_key_order = int(file2.readline().strip())
        with open(f"files/{type_name}/file.txt", "r") as file:
            line = file.readline()
            records_in_page = int(line.strip('\n '))
            page_no = 0
            # check full pages one by one
            while records_in_page == 10:
                for i in range(RECORDS_PER_PAGE):
                    line = file.readline()
                    if line.split()[primary_key_order - 1] == primary_key:
                        if flag:
                            with open(OUTPUT_FILE, "a") as output:
                                # record found return True and output the record
                                output.write(line)
                            return True
                        else:
                            # this is used for delete function
                            # record to be deleted found
                            return i + 1, page_no
                line = file.readline()
                records_in_page = int(line.strip('\n '))
                page_no = page_no + 1
            # check the last page
            for i in range(records_in_page):
                line = file.readline()
                if line.split()[primary_key_order - 1] == primary_key:
                    if flag:
                        # record found return True and output the record
                        with open(OUTPUT_FILE, "a") as output:
                            output.write(line)
                        return True
                    else:
                        # this is used for delete function
                        # record to be deleted found
                        return i + 1, page_no
    # record not found
    return False
