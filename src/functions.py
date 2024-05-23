import os

PAGE_SIZE = 10
FILE_SIZE = 10
RECORDS_PER_PAGE = 10
PAGES_PER_FILE = 10
OUTPUT_FILE = "output.txt"

def replace_line(file_path, line_number, new_line):
    # Create a temporary file
    temp_file_path = file_path + '.tmp'

    with open(file_path, 'r') as input_file, open(temp_file_path, 'w') as output_file:
        current_line = 1
        for line in input_file:
            if current_line == line_number:
                output_file.write(new_line + '\n')
            else:
                output_file.write(line)
            current_line += 1

    # Replace the original file with the temporary file
    os.replace(temp_file_path, file_path)


def create_type(type_name: str, number_of_fields: str, primary_key_order: str, fields: dict):
    # create a folder under files (file), create its page
    if (os.path.isdir(f"files/{type_name}")):
        #print("Type already exists")
        return False
    os.mkdir(f"files/{type_name}")
    with open(f"files/{type_name}/metadata.txt", "w") as file:
        file.write(f"{number_of_fields}\n")
        file.write(f"{primary_key_order}\n")
#        for field, field_type in fields.items():
#            file.write(f"{field} {field_type}\n")
    with open(f"files/{type_name}/file.txt", "w") as file:
        file.write("0\n")
        pass
    return True



def create_record(type_name: str, values: list[str]):
    # find the folder under files (file), find the correct space in txt's (page) and place the record
    if not os.path.isdir(f"files/{type_name}"):
        #print("Type does not exist")
        return False
    with open(f"files/{type_name}/metadata.txt", "r") as file:
        number_of_fields = int(file.readline().strip())
        primary_key_order = int(file.readline().strip())
    if len(values) != number_of_fields:
        #print("Invalid number of fields")
        return False
    records_in_page = 0
    first_empty_page = 0
    page_begin_position = 0
    lines = []
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
        lines.append(f"{records_in_page+1}\n")
        for i in range(records_in_page):
            line = file.readline()
            lines.append(line)
            #print(line.split(), primary_key_order-1)
            if line.split()[primary_key_order - 1] == values[primary_key_order - 1]:
                # print("Primary key already exists")
                return False
        records_in_page += 1
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


# DELETEDEN SONRA SON FILEIN SON ÖGESİNİ BURAYA TAŞI
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
                lines.append(f"{records_in_page-1}\n")
                for i in range(records_in_page-1):
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
    line_no = search_tup[1]*11+search_tup[0]+1
    replace_line(f"files/{type_name}/file.txt",line_no,last_record.strip('\n'))
    return True


def search(type_name: str, primary_key: str, flag: bool):
    # find the folder under files (file), find the correct space in txt's (page) and return the record
    if not os.path.isdir(f"files/{type_name}"):
        # print("Type does not exist")
        return False
    with open(f"files/{type_name}/metadata.txt", "r") as file2:
        file2.readline()
        primary_key_order = int(file2.readline().strip())
        with open(f"files/{type_name}/file.txt", "r") as file:
            line = file.readline()
            records_in_page = int(line.strip('\n '))
            page_no = 0
            while records_in_page == 10:
                for i in range(RECORDS_PER_PAGE):
                    line = file.readline()
                    if line.split()[primary_key_order - 1] == primary_key:
                        if flag:
                            with open(OUTPUT_FILE, "a") as output:
                                output.write(line)
                            return True
                        else:
                            return i+1, page_no
                line = file.readline()
                records_in_page = int(line.strip('\n '))
                page_no = page_no + 1
            for i in range(records_in_page):
                line = file.readline()
                if line.split()[primary_key_order - 1] == primary_key:
                    if flag:
                        with open(OUTPUT_FILE, "a") as output:
                            output.write(line)
                        return True
                    else:
                        return i+1, page_no
    return False
