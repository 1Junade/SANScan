import winreg

# reads RunMRU from registry, hands back MRUdict and MRUorder
def RunMRU():
    # open RunMRU folder inside HKEY_CURRENT_USER, frolder is the handle for the folder
    # check if RunMRU exisit.
    try:
        folder = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU") 
    except FileNotFoundError:
        return {}, ""
    paperNum = 0   # paper number, starts at 0
    MRUdict = {}
    MRUorder = "" #backup incase MRUList doesnt exist
    while True:
        try:
            # grab paper number paperNum from folder, letter = letter, typed = what was typed, valType = (1,2,etc)
            letter, typed, valType =  winreg.EnumValue(folder , paperNum)
            if letter == "MRUList":
                MRUorder = typed # get data, the order of MRUList
            else:
                MRUdict[letter] = typed[:-2]# slice last two chars of data to cut out noise
            paperNum+=1 # next page
        except OSError:
            return MRUdict, MRUorder # stop when no papers r left, hand back MRUdict and MRUorder
# run RunMRU and print whats found
MRUdict, MRUorder = RunMRU() 
# check if there was no dict found
if MRUdict == {}:
    print(f"{"":-^40}")
    print(f"{"RunMRU not found.":^40}")
    print(f"{"":-^40}")
else:
    print(f"{"":-^40}")
    print(f"ORDER: {MRUorder:^25}")
    print(f"{"":-^40}")
    # Loops for each letter in the MRUorder, newest first
    for nextLetter in MRUorder:
        # checks whether a letter is really in the list, or been deleted / missing
        if nextLetter in MRUdict:
            print(f"{MRUdict[nextLetter]:^40}")
        else:
            print(f"Letter: {nextLetter} is Missing")
    print(f"{"":-^40}")
    print(f"{"Done":^40}")
    print(f"{"":-^40}")

