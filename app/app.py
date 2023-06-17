import sys

from utils import validateLockedLinks, mineAdditionalIssues, gatherPostRawData, formatConvoKit

def main():
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '-v' or sys.argv[1] == '--validate':
            validate()
        elif sys.argv[1] == '-g' or sys.argv[1] == '--gather':
            gather()
    
        elif sys.argv[1] == '-f' or sys.argv[1] == '--format':
            format()
        elif sys.argv[1] == '-a' or sys.argv[1] == '--all':
            all()
        elif sys.argv[1] == '-t' or sys.argv[1] == '--test':
            mineAdditionalIssues('TextFiles', 2)
        elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print("Usage: python app.py [OPTION]")
            print("Options:")
            print("  -v, --validate\t\tValidate list of GitHub issue links")
            print("  -g, --gather\t\t\tGather raw post data from valid links")
            print("  -f, --format\t\t\tFormat data into alternative format (+++$+++)")
            print("  -a, --all\t\t\tRun all options (WITH JSON FORMATTING IN ONE LARGE CORPUS)")
            print("  -h, --help\t\t\tShow this help message")
        else:
            print("Please enter a valid command | Accepts 1 argument")

    else:
        print("Please enter a valid command | Accepts 1 argument")
        
        

def validate():
    
    print("Validating verified issues...")
    validateLockedLinks('TextFiles')
    print("Validation complete!")
    
    print("Mining additional issues...")
    locked, unlocked = mineAdditionalIssues('TextFiles', 3)
    print(f"Found {locked/2} Locked issues and {unlocked} Unlocked issues") #Bug, adds a duplicate of each locked issue. Doesn't effect the rest of the program or the final ourput
    
    
    
    
def gather():
    
    print("Gathering Raw Data of Locked Issues...")
    gatherPostRawData('TextFiles/validLinks.txt')
    
    gatherPostRawData('TextFiles/additionalLockedIssues.txt')
    
    print("Gathering Raw Data of Unlocked Issues...")
    gatherPostRawData('TextFiles/unlockedLinks.txt')
    print("Finished gathering raw data!")
    

    
    
    
def format():
    
    print("Formatting Raw Data...")
    formatConvoKit('FinalFormattedData')
    print("Finished formatting raw data!")
    
def all():
    
    print("Running full process...")
    validate()
    gather()
    format()
    print("Finished running full process!")
        


if __name__ == "__main__":
    main()
