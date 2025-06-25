# main.py

from recording.runner import run_and_record
from editing.edit import edit

def main():
    run_and_record()
    if input("Will you this footage be uploaded? (y/n) ") == "y":
        edit()

if __name__ == "__main__":
    main()
