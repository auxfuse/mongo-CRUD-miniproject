import pymongo
import os
from dotenv import load_dotenv

# For all further projects use .env file and dotenv :D and store environmental variables in .env
# everything secret into .env stripe/secretkeys/environvariables/ EVERYTHING

load_dotenv()

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "myTestDB"
COLLECTION_NAME = "myFirstMDB"

def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")

def show_menu():
    print("")
    print("1. Add a record")
    print("2. Find a record by name")
    print("3. Edit a record")
    print("4. Delete a record")
    print("5. exit")

    option = input("Enter option: ")
    return option

def get_record():
    print("")
    first = input("Enter first name >")
    last = input("Enter last name >")

    try:
        doc = coll.find_one({'first': first.lower(), 'last': last.lower()})
    except:
        print("Error accessing the DB")

def find_record():
    doc = get_record()
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())


    if not doc:
        print("")
        print("Error no results found")

    return doc

def edit_record():
    doc = get_record()
    if doc:
        update_doc = {}
        print("")
        for k,v in doc.items():
            if k != "_id":
                update_doc[k] = input(k.capitalize() + " [" + v + "] >")

                if update_doc[k] == "":
                    update_doc[k] = v

        try:
            coll.update_one(doc, {'$set': update_doc})
            print("")
            print("Document updated")
        except:
            print("Error accessing database")

def add_record():
    print("")
    first = input("Enter first name >")
    last = input("Enter last name >")
    dob = input("Enter dob >")
    gender = input("Enter gender (f/m) >")
    hair_color = input("Enter hair color >")
    occupation = input("Enter occupation >")
    nationality = input("Enter nationality >")

    new_doc = {'first': first.lower(), 'last': last.lower(), 'dob': dob, 'gender': gender, 'hair_color': hair_color, 'occupation': occupation, 'nationality': nationality}

    try:
        coll.insert(new_doc)
        print("")
        print("Document inserted")
    except:
        print("Error in accessing database.")

def delete_record():

    doc = get_record()

    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())

        print("")
        confirmation = input("Is this the document you want to delete?\nY or N >")
        print("")

        if confirmation.lower() == "y":
            try:
                coll.remove(doc)
                print("Document deleted")
            except:
                print("Error accessing the database")
        else:
            print("Document not deleted")

def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            delete_record()
        elif option == "5":
            conn.close()
            break
        else:
            print("Invalid Option")
        print("")

conn = mongo_connect(MONGODB_URI)
coll = conn[DBS_NAME][COLLECTION_NAME]

main_loop()