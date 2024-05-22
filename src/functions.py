import os

PAGE_SIZE = 10
FILE_SIZE = 10
OUTPUT_FILE = "output.txt"


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
    for i in range(FILE_SIZE):
        with open(f"files/{type_name}/page{i}.txt", "w") as file:
            pass
    return True



# FILE DA DOLDUYSA NE YAPILACAK BİLMİYORUM
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
    for i in range(FILE_SIZE):
        with open(f"files/{type_name}/page{i}.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.split()[primary_key_order-1] == values[primary_key_order-1]:
                    #print("Primary key already exists")
                    return False
            if len(lines) < PAGE_SIZE:
                with open(f"files/{type_name}/page{i}.txt", "a") as file:
                    file.write(" ".join(values) + "\n")
                    return True
    return False
        

# DELETEDEN SONRA SON FILEIN SON ÖGESİNİ BURAYA TAŞI
def delete(type_name: str, primary_key: str):
    # find the folder under files (file), find the correct space in txt's (page) and delete the record
    if not os.path.isdir(f"files/{type_name}"):
        #print("Type does not exist")
        return False
    with open(f"files/{type_name}/metadata.txt", "r") as file:
        file.readline()
        primary_key_order = int(file.readline().strip())
    for i in range(FILE_SIZE):
        with open(f"files/{type_name}/page{i}.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.split()[primary_key_order-1] == primary_key:
                    lines.remove(line)
                    with open(f"files/{type_name}/page{i}.txt", "w") as file:
                        file.writelines(lines)
                    return True
    return False


def search(type_name: str, primary_key: str):
    # find the folder under files (file), find the correct space in txt's (page) and return the record
    if not os.path.isdir(f"files/{type_name}"):
        #print("Type does not exist")
        return False
    with open(f"files/{type_name}/metadata.txt", "r") as file:
        file.readline()
        primary_key_order = int(file.readline().strip())
    for i in range(FILE_SIZE):
        with open(f"files/{type_name}/page{i}.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.split()[primary_key_order-1] == primary_key:
                    with open(OUTPUT_FILE, "a") as output:
                        output.write(line)
                    return True
    return False
