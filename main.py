import csv
import os

USERS_FILE = "users.csv"

ROLE_PERMISSIONS = {
    "Employee": ["view_profile"],
    "HR": ["view_profile", "view_hr_records"],
    "IT_Admin": ["view_profile", "manage_accounts"],
    "Manager": ["view_profile", "view_team"],
}


def load_users():
    with open(USERS_FILE, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def list_users():
    for user in load_users():
        print(
            user["user_id"], "|", user["name"], "|",
            user["department"], "|", user["role"], "|",
            user["status"]
        )


def check_access():
    user_id = input("Enter user ID (example U002): ").strip()
    permission = input("Permission (example manage_accounts): ").strip()

    for user in load_users():
        if user["user_id"] == user_id:
            allowed = (
                user["status"] == "Active"
                and permission in ROLE_PERMISSIONS.get(user["role"], [])
            )
            print("ACCESS GRANTED" if allowed else "ACCESS DENIED")
            return

    print("User not found.")


def deactivate_user():
    users = load_users()
    user_id = input("Enter user ID to deactivate: ").strip()

    for user in users:
        if user["user_id"] == user_id:
            user["status"] = "Inactive"

            with open(USERS_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=users[0].keys())
                writer.writeheader()
                writer.writerows(users)

            print("Account deactivated.")
            return

    print("User not found.")


def access_review():
    print("\n--- Access Review ---")
    for user in load_users():
        if user["status"] != "Active":
            print(user["user_id"], user["name"], "- Inactive account")
        elif user["role"] == "IT_Admin":
            print(user["user_id"], user["name"], "- Review privileged access")


def main():
    while True:
        print("\n=== IAM User Access Management ===")
        print("1. List users")
        print("2. Check access")
        print("3. Deactivate account")
        print("4. Run access review")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_users()
        elif choice == "2":
            check_access()
        elif choice == "3":
            deactivate_user()
        elif choice == "4":
            access_review()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()