from organizer.organizer import FileOrganizer

def main() -> None:
    print("=" * 40)
    print("   File Organizer — Portfolio v1")
    print("=" * 40)

    path = input("\nEnter the directory path to organize:\n> ").strip()
    try:
        organizer = FileOrganizer(path)
        organizer.organize()
    except (NotADirectoryError, PermissionError) as e:
        print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    main()