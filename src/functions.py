import os

def create_type(type_name: str, number_of_fields: int, primary_key_order: int, fields: list[str]):
    # create a folder under files (file), create its page
    if (os.path.isdir(f"files/{type_name}")):
        print("Type already exists")
        return
    os.mkdir(f"files/{type_name}")
    pass

def create_record(type_name: str, values: list[str]):
    # find the folder under files (file), find the correct space in txt's (page) and place the record
    pass

def delete(type_name: str, primary_key: str):
    # find the folder under files (file), find the correct space in txt's (page) and delete the record
    pass

def search(type_name: str, primary_key: str):
    # find the folder under files (file), find the correct space in txt's (page) and return the record
    pass
