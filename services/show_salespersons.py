from database.MySQL.execute_command import execute_command


def show_salespersons() -> dict:
    _result = execute_command("SELECT person.*, employee.employee_dateOfHire, employee.employee_education, "
                              "employee.employee_workExperience, employee.employee_legalInformation FROM person "
                              "INNER JOIN employee ON person.person_id = employee.person_id "
                              "INNER JOIN salesperson ON employee.person_id = salesperson.employee_id", None)

    if not _result["execute"]:
        return {"show": False, "message": _result["message"]}

    if len(_result["data"]) == 0:
        return {"show": False, "message": "There is no salespersons to show"}

    for row in _result["data"]:
        print("----------------------------------------")
        print(f"Salespersons ID = {row[0]}\n"
              f"Salespersons first name              ->   {row[1]}\n"
              f"Salespersons last name               ->   {row[2]}\n"
              f"Salespersons region                  ->   {row[3]}\n"
              f"Salespersons phone number            ->   {row[4]}\n"
              f"Salespersons E-mail                  ->   {row[5]}\n"
              f"Salespersons date of birth           ->   {row[6]}\n"
              f"Salespersons gender                  ->   {row[7]}\n"
              f"Salespersons address                 ->   {row[8]}\n"
              f"Salespersons description             ->   {row[9]}\n"
              f"Salespersons date of hire            ->   {row[10]}\n"
              f"Salespersons education               ->   {row[11]}\n"
              f"Salespersons work experience "
              f"with this format [company name, job title, start date, end date, description]\n{row[12]}\n"
              f"Salespersons legal information       ->   {row[13]}\n")

    return {"show": True, "message": "All salespersons were displayed"}


def show_a_salesperson(salesperson_id: str) -> dict:
    _result = execute_command("SELECT person.*, employee.employee_dateOfHire, employee.employee_education, "
                              "employee.employee_workExperience, employee.employee_legalInformation FROM person "
                              "INNER JOIN employee ON person.person_id = employee.person_id "
                              "INNER JOIN salesperson ON employee.person_id = salesperson.employee_id "
                              "WHERE salesperson.employee_id = %s", (salesperson_id,))

    if not _result["execute"]:
        return {"show": False, "message": _result["message"]}

    print("----------------------------------------")
    print(f"Salespersons ID = {_result["data"][0][0]}\n"
          f"Salespersons first name              ->   {_result["data"][0][1]}\n"
          f"Salespersons last name               ->   {_result["data"][0][2]}\n"
          f"Salespersons region                  ->   {_result["data"][0][3]}\n"
          f"Salespersons phone number            ->   {_result["data"][0][4]}\n"
          f"Salespersons E-mail                  ->   {_result["data"][0][5]}\n"
          f"Salespersons date of birth           ->   {_result["data"][0][6]}\n"
          f"Salespersons gender                  ->   {_result["data"][0][7]}\n"
          f"Salespersons address                 ->   {_result["data"][0][8]}\n"
          f"Salespersons description             ->   {_result["data"][0][9]}\n"
          f"Salespersons date of hire            ->   {_result["data"][0][10]}\n"
          f"Salespersons education               ->   {_result["data"][0][11]}\n"
          f"Salespersons work experience "
          f"with this format [company name, job title, start date, end date, description]\n{_result["data"][0][12]}\n"
          f"Salespersons legal information       ->   {_result["data"][0][13]}\n")

    return {"show": True, "message": "salesperson was displayed"}
