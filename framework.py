#Program to perform CRUD operation on MySQL database.
import mysql.connector
connection = mysql.connector.connect(host = "165.22.14.77", database = "db_Venkatesh" ,user = "Venkatesh", password = "Venkatesh");
my_cursor = connection.cursor(buffered=True,dictionary=True)
file_not_found_message = "File may not exist or error opening the file"

try:
	with open("menu.cfg") as f_menu:
		menu = f_menu.read()
	f_menu.close()

except FileNotFoundError:
	print(file_not_found_message)

try:
	with open("promt_messages.cfg") as f_promt_messages:
		promt_messages = eval(f_promt_messages.read())
	f_promt_messages.close()

except FileNotFoundError:
	print(file_not_found_message)


my_cursor.execute("select * from my_table limit 0")


column_names =  my_cursor.column_names

max_length_column_name = column_names[0]

for column_name in column_names:
	if(len(max_length_column_name) < len(column_name)):
		max_length_column_name = column_name

def get_no_of_fields():
	count_of_field = 0
	for column_name in column_names:
		count_of_field = count_of_field + 1
	return count_of_field

count_of_fields = get_no_of_fields()

def print_pipe():
	print("-" + "-" * (len(max_length_column_name) + 9) * (count_of_fields - 1))

def print_column_names():
	print_pipe()
	print("|", end = "")
	for index in range(1, count_of_fields):
		print(column_names[index], end = "")
		print(" " * (len(max_length_column_name) - len(column_names[index]) + 8), end = "")
		print("|", end = "")
	print("\t")
	print_pipe()

def show_records():
    my_cursor.execute("SELECT * from my_table WHERE STATUS = 'a'")
    records = my_cursor.fetchall()
    print_column_names()
    for record in records:
        print_record(record)

def print_record(record):
    print("|", end ="")
    for counter in range(1,len(record)):
        print(record[column_names[counter]], end= "")
        print(" " * (len(max_length_column_name) - int(len(str(record[column_names[counter]]))) + 8), end = "")
        print("|", end="")
    print("\t")
    print_pipe()

def show_record():
    user_input_id = int(input("Enter ID: "))
    my_cursor.execute("SELECT * from my_table WHERE STATUS = 'a' AND ID = " + str(user_input_id))
    records = my_cursor.fetchall()
    if not records:
        print(promt_messages[0])
    else:
        print_column_names()
        for record in records:
            print_record(record)

def insert_record():
    field_values = []
    status = 'A'
    field_values.append(status)
    for index in range(1, count_of_fields):
        field_value = input("Enter " + column_names[index] + ": ")
        field_values.append(field_value)
    record = tuple(field_values)
    my_cursor.execute('INSERT INTO my_table VALUES ' + str(record))
    is_record_saved = my_cursor.rowcount
    connection.commit()
    print(is_record_saved)
    if is_record_saved > 0:
        print(promt_messages[1])
    else:
       print(promt_messages[2])

def delete_record():
    user_input_id =int(input("Enter ID: "))
    my_cursor.execute("UPDATE my_table set STATUS = 'i' where ID ="  + str(user_input_id))
    is_record_deleted = my_cursor.rowcount
    if is_record_deleted != 0:
        print(promt_messages[3])
    else:
        print(promt_messages[0])
    connection.commit()

def check_record_present_or_not(id):
    my_cursor.execute('SELECT * FROM my_table WHERE Status = "a" AND ' + column_names[1] + ' = ' + str(id))
    records = my_cursor.fetchall()
    is_record_found = False
    for record in records:
        if int(records[0]['id']) == int(id):
            is_record_found = True
            break
    return is_record_found

def update_record():
    user_input_id = int(input("Enter ID: "))
    is_record_found = check_record_present_or_not(user_input_id)
    print(is_record_found)
    if is_record_found:
        with open('updatable_fields.cfg') as f_updatable_fields:
            updatable_fields = eval(f_updatable_fields.read())
        f_updatable_fields.close()
        counter = 1
        for index in updatable_fields:
            print(str(counter) + ". Update " + column_names[index])
            counter = counter + 1
        try:
            user_update_choice = int(input("Enter choice: "))
        except ValueError:
            print("INVALID CHOICE.")
            return
        new_field_values = input("Enter new " + column_names[updatable_fields[user_update_choice - 1]] + ": ")
        my_cursor.execute('UPDATE my_table SET ' + column_names[updatable_fields[user_update_choice - 1]] + ' = ' + "\"" + new_field_values + "\"" + ' WHERE ' + column_names[1] + ' = ' + str(user_input_id))
        is_record_updated = my_cursor.rowcount
        print(is_record_updated)
        if is_record_updated != 0:
            print(promt_messages[4])
        else:
            print(promt_messages[5])
    else:
        print(promt_messages[0])
    connection.commit()

functions_list = [insert_record, show_records, show_record, update_record, delete_record, exit]

while True:
    print(menu)
    try:
        user_option = int(input("Enter option: "))
    except ValueError:
        print("INVALID INPUT")
        continue
    if user_option >= 1 and user_option <= 5:
        functions_list[user_option - 1]()
    elif user_option == 6:
        print("Press Y to exit.")
        quit_option = input("Enter option: ")
        if quit_option.upper() == 'Y':
            functions_list[user_option - 1]()
    else:
        print("INVALID INPUT")
connection.close()
