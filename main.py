from guardianpy.gui import run_gui
from guardianpy.database import initialize_database


if __name__ == "__main__":
    initialize_database()
    run_gui()
