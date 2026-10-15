# Main menu
while True:
    print("1. Patient Registration")
    print("2. Doctor Management")
    print("3. Appointment Management")
    print("4. Medical Records")
    print("5. Billing")
    print("6. Pharmacy Management")
    choice = input("Enter choice: ")

    if choice == "1":
        register_patient()
    elif choice == "2":
        manage_doctor()
    elif choice == "3":
        manage_appointment()
    elif choice == "7":
        generate_report()
    elif choice == "8":
        break
