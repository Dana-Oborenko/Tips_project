import sqlite3
import datetime

db = "database.db"

choice = "J"
while True:
    if choice in {"j", "J"}:
        print("")
        username = input("Lūdzu, ievadiet savu lietotājvārdu!\n")
        password = input("Lūdzu, ievadiet savu paroli!\n")
        with sqlite3.connect(db) as connection:
            c = connection.cursor()
            c.execute("SELECT POSITION FROM USERS WHERE USERNAME = ? AND PASSWORD = ?;", (username, password))
            user_position = c.fetchall()
            if len(user_position) == 1:
                user_position = user_position[0][0]
                if user_position == "W":
                    name = input("Lūdzu, ievadiet savu vārdu!\n")
                    surname = input("Lūdzu, ievadiet savu uzvārdu!\n")
                    c.execute("SELECT ID FROM WORKERS WHERE FIRST_NAME = ? AND LAST_NAME = ?;", (name, surname))
                    worker_id = c.fetchall()
                    if len(worker_id) == 1:
                        worker_id = worker_id[0][0]
                        print("Jūs esat darbinieks ar ID", worker_id)
                    else:
                        print("Šāds darbinieks nav atrasts! Lūdzu, ievadiet savus datus!")
                        title = input("Lūdzu, ievadiet savu amatu!\n")
                        c.execute("INSERT INTO WORKERS VALUES (NULL, ?, ?, ?);", (name, surname, title))
                        c.execute("SELECT last_insert_rowid();")
                        worker_id = c.fetchall()
                        worker_id = worker_id[0][0]
                        print("Jūs tagad esat darbinieks ar ID", worker_id)
                    date = datetime.datetime.now().strftime("%d.%m.%Y")
                    while True:
                        try:
                            summa = float(input("Lūdzu, ievadiet savu šodienas dzēramnaudu!\n"))
                            break
                        except ValueError:
                            print("Jūs ievadījāt nepieņemamo vērtību! Lūdzu, mēģiniet vēlreiz!")
                    c.execute("INSERT INTO TIPS VALUES (NULL, ?, ?, ?);", (summa, date, worker_id))
                    print("Dati ir veiksmīgi saglabāti!")
                elif user_position == "M":
                    while True:
                        print()
                        print("0 - Iziet no sistēmas")
                        print("1 - Apskatīt kopējo pārskatu")
                        print("2 - Aprēķināt datus par noteikto datumu")
                        menuChoice = input("Lūdzu, ievadiet saskarnes vērtību: ")
                        if len(menuChoice) != 1:
                            print("Jūs ievadījāt nepieņemamo vērtību! Lūdzu, mēģiniet vēlreiz!")
                            continue
                        menuChoice = menuChoice[0]
                        if menuChoice == "0":
                            break
                        elif menuChoice == "1":
                            c.execute("SELECT TIPS.ID, FIRST_NAME, LAST_NAME, SUMMA, DATE FROM WORKERS, TIPS WHERE WORKERS.ID = TIPS.WORKER;")
                            all_tips = c.fetchall()
                            print("\nVisa dzēramnauda:")
                            print("{:^4} | {:^20} | {:^20} | {:^11} | {:^10}".format("ID", "FIRST NAME", "LAST NAME", "SUMMA", "DATE"))
                            print("{:-^77}".format(""))
                            for tip in all_tips:
                                print("{:>4} | {:^20} | {:^20} | {:>7.2f} EUR | {:>10}".format(*tip))
                            c.execute("SELECT FIRST_NAME, LAST_NAME, SUM(SUMMA) FROM WORKERS, TIPS WHERE WORKERS.ID = TIPS.WORKER GROUP BY FIRST_NAME, LAST_NAME ORDER BY SUM(SUMMA) DESC;")
                            tips_by_worker = c.fetchall()
                            print("\nVisa dzēramnauda, sagrupētā pēc darbiniekiem:")
                            print("{:^20} | {:^20} | {:^11}".format("FIRST NAME", "LAST NAME", "SUMMA"))
                            print("{:-^58}".format(""))
                            for tip in tips_by_worker:
                                print("{:^20} | {:^20} | {:>7.2f} EUR".format(*tip))
                        elif menuChoice == "2":
                            while True:
                                try:
                                    date = datetime.datetime.strptime(input("Lūdzu, ievadiet datumu, par kuru tiks aprēķināti dati!\n"), "%d.%m.%Y")
                                    date = date.strftime("%d.%m.%Y")
                                    break
                                except ValueError:
                                    print("Jūs ievadījāt nepieņemamo vērtību! Lūdzu, mēģiniet vēlreiz!")
                            c.execute("SELECT SUM(SUMMA) FROM TIPS WHERE DATE = ?;", (date, ))
                            tips_sum = c.fetchall()
                            tips_sum = tips_sum[0][0]
                            if tips_sum is None:
                                tips_sum = 0
                            print("Dzēramnaudas kopsumma par {} - {:.2f} EUR".format(date, tips_sum))
                            if tips_sum > 0:
                                c.execute("SELECT COUNT(ID) FROM WORKERS;")
                                workers_count = c.fetchall()
                                workers_count = workers_count[0][0]
                                if workers_count is None:
                                    workers_count = 0
                                print("Darbinieku kopskaits -", workers_count)
                                if workers_count > 0:
                                    result = tips_sum / workers_count
                                else:
                                    result = 0
                            else:
                                result = 0
                            print("Katram darbiniekam par {} - {:.2f} EUR".format(date, result))
                        else:
                            print("Jūs ievadījāt nepieņemamo vērtību! Lūdzu, mēģiniet vēlreiz!")
                            continue
                else:
                    print("Jūsu amatam nav piekļuves šai sistēmai! Lūdzu, mēģiniet pieslēgties ar citu lietotājvārdu un paroli!")
                    continue
                print("\nVai gribat turpināt programmas darbību?")
                choiceStr = input("Ievadiet J (jā) vai N (nē): ")
                choice = choiceStr[0]
            else:
                print("Šāds lietotājs nav atrasts! Lūdzu, mēģiniet pieslēgties ar citu lietotājvārdu un paroli!")
    elif choice in {"n", "N"}:
        break
    else:
        print("Jūs ievadījāt nepieņemamo vērtību! Lūdzu, mēģiniet vēlreiz!")
print("Uz redzēšanos!")
