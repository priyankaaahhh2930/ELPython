# Hospital Management System

patients = []
doctors = []
appointments = []
records = []
bills = []
medicines = []


# 1. Patient Registration
def register_patient():
    print("\n--- Patient Registration ---")

    name = input("Enter patient name: ")
    age = input("Enter age: ")
    phone = input("Enter phone number: ")

    patients.append([name, age, phone])

    print("Patient registered successfully!")


def view_patients():
    print("\n--- Patient List ---")

    if len(patients) == 0:
        print("No patients found.")
    else:
        for p in patients:
            print("Name:", p[0], "Age:", p[1], "Phone:", p[2])


# 2. Doctor Management
def manage_doctor():
    print("\n--- Doctor Management ---")
    print("1. Add Doctor")
    print("2. View Doctors")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Enter doctor name: ")
        specialization = input("Enter specialization: ")

        doctors.append([name, specialization])

        print("Doctor added successfully!")

    elif choice == "2":
        if len(doctors) == 0:
            print("No doctors found.")
        else:
            for d in doctors:
                print("Doctor:", d[0], "| Specialization:", d[1])


# 3. Appointment Management
def manage_appointment():
    print("\n--- Appointment Management ---")
    print("1. Book Appointment")
    print("2. View Appointments")

    choice = input("Enter choice: ")

    if choice == "1":
        patient = input("Enter patient name: ")
        doctor = input("Enter doctor name: ")
        date = input("Enter appointment date: ")

        appointments.append([patient, doctor, date])

        print("Appointment booked successfully!")

    elif choice == "2":
        if len(appointments) == 0:
            print("No appointments found.")
        else:
            for a in appointments:
                print("Patient:", a[0],
                      "| Doctor:", a[1],
                      "| Date:", a[2])


# 4. Medical Records
def medical_records():
    print("\n--- Medical Records ---")
    print("1. Add Record")
    print("2. View Records")

    choice = input("Enter choice: ")

    if choice == "1":
        patient = input("Enter patient name: ")
        disease = input("Enter disease: ")
        medicine = input("Enter medicine: ")

        records.append([patient, disease, medicine])

        print("Medical record added!")

    elif choice == "2":
        if len(records) == 0:
            print("No records found.")
        else:
            for r in records:
                print("Patient:", r[0],
                      "| Disease:", r[1],
                      "| Medicine:", r[2])


# 5. Billing
def billing():
    print("\n--- Billing ---")

    patient = input("Enter patient name: ")
    doctor_fee = float(input("Enter doctor fee: "))
    medicine_fee = float(input("Enter medicine fee: "))

    total = doctor_fee + medicine_fee

    bills.append([patient, total])

    print("Total Bill:", total)
    print("Bill generated successfully!")


# 6. Pharmacy Management
def pharmacy_management():
    print("\n--- Pharmacy Management ---")
    print("1. Add Medicine")
    print("2. View Medicines")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Enter medicine name: ")
        quantity = int(input("Enter quantity: "))

        medicines.append([name, quantity])

        print("Medicine added successfully!")

    elif choice == "2":
        if len(medicines) == 0:
            print("No medicines found.")
        else:
            for m in medicines:
                print("Medicine:", m[0],
                      "| Quantity:", m[1])


# 7. Reports
def generate_report():
    print("\n--- Hospital Report ---")

    print("Total Patients:", len(patients))
    print("Total Doctors:", len(doctors))
    print("Total Appointments:", len(appointments))
    print("Total Medical Records:", len(records))
    print("Total Bills:", len(bills))
    print("Total Medicines:", len(medicines))


# Main Menu
while True:

    print("\n===== HOSPITAL MANAGEMENT SYSTEM =====")
    print("1. Patient Registration")
    print("2. Doctor Management")
    print("3. Appointment Management")
    print("4. Medical Records")
    print("5. Billing")
    print("6. Pharmacy Management")
    print("7. Generate Report")
    print("8. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        register_patient()

    elif choice == "2":
        manage_doctor()

    elif choice == "3":
        manage_appointment()

    elif choice == "4":
        medical_records()

    elif choice == "5":
        billing()

    elif choice == "6":
        pharmacy_management()

    elif choice == "7":
        generate_report()

    elif choice == "8":
        print("Thank you!")
        break

    else:
        print("Invalid choice!")