from database.MySQL.execute_command import execute_command


def show_drivers() -> dict:
    _result = execute_command("SELECT person.*, employee.employee_dateOfHire, employee.employee_education, "
                              "employee.employee_workExperience, employee.employee_legalInformation, "
                              "driver.driver_license, driver.driver_availableForFreight FROM person "
                              "INNER JOIN employee ON person.person_id = employee.person_id "
                              "INNER JOIN driver ON employee.person_id = driver.employee_id", None)

    if not _result["execute"]:
        return {"show": False, "message": _result["message"]}

    if len(_result["data"]) == 0:
        return {"show": False, "message": "There is no driver to show"}

    for row in _result["data"]:
        print("----------------------------------------")
        print(f"driver ID = {row[0]}\n"
              f"driver first name              ->   {row[1]}\n"
              f"driver last name               ->   {row[2]}\n"
              f"driver region                  ->   {row[3]}\n"
              f"driver phone number            ->   {row[4]}\n"
              f"driver E-mail                  ->   {row[5]}\n"
              f"driver date of birth           ->   {row[6]}\n"
              f"driver gender                  ->   {row[7]}\n"
              f"driver address                 ->   {row[8]}\n"
              f"driver description             ->   {row[9]}\n"
              f"driver date of hire            ->   {row[10]}\n"
              f"driver education               ->   {row[11]}\n"
              f"driver work experience "
              f"with this format [company name, job title, start date, end date, description]\n{row[12]}\n"
              f"driver legal information       ->   {row[13]}\n"
              f"driver license                 ->   {row[14]}\n"
              f"driver available for freight   ->   {row[15]}\n")

    return {"show": True, "message": "All salespersons were displayed"}


def show_a_driver(driver_id: str) -> dict:
    _result = execute_command("SELECT person.*, employee.employee_dateOfHire, employee.employee_education, "
                              "employee.employee_workExperience, employee.employee_legalInformation,"
                              "driver.driver_license, driver.driver_availableForFreight FROM person "
                              "INNER JOIN employee ON person.person_id = employee.person_id "
                              "INNER JOIN driver ON employee.person_id = driver.employee_id "
                              "WHERE driver.employee_id = %s", (driver_id,))

    if not _result["execute"]:
        return {"show": False, "message": _result["message"]}

    print("----------------------------------------")
    print(f"driver ID = {_result["data"][0][0]}\n"
          f"driver first name              ->   {_result["data"][0][1]}\n"
          f"driver last name               ->   {_result["data"][0][2]}\n"
          f"driver region                  ->   {_result["data"][0][3]}\n"
          f"driver phone number            ->   {_result["data"][0][4]}\n"
          f"driver E-mail                  ->   {_result["data"][0][5]}\n"
          f"driver date of birth           ->   {_result["data"][0][6]}\n"
          f"driver gender                  ->   {_result["data"][0][7]}\n"
          f"driver address                 ->   {_result["data"][0][8]}\n"
          f"driver description             ->   {_result["data"][0][9]}\n"
          f"driver date of hire            ->   {_result["data"][0][10]}\n"
          f"driver education               ->   {_result["data"][0][11]}\n"
          f"driver work experience "
          f"with this format [company name, job title, start date, end date, description]\n{_result["data"][0][12]}\n"
          f"driver legal information       ->   {_result["data"][0][13]}\n"
          f"driver license                 ->   {_result["data"][0][14]}\n"
          f"driver available for freight   ->   {_result["data"][0][15]}\n")

    return {"show": True, "message": "driver was displayed"}
