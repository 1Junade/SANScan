import winreg
import textwrap
import shutil

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
    MRUorder = "" # backup incase MRUList doesnt exist
    while True:
        try:
            # grab paper number paperNum from folder, typed = what was typed, valType = (1,2,etc)
            letter, typed, valType =  winreg.EnumValue(folder , paperNum)
            if letter == "MRUList":
                MRUorder = typed # get data, the order of MRUList
            else:
                if typed.endswith(r"\1"):
                    MRUdict[letter] = typed[:-2] # slice last two chars \1 only if its there
                else:
                    MRUdict[letter] = typed # no \1 is saved noramlly 
            paperNum+=1 # next page
        except OSError:
            winreg.CloseKey(folder) # done reading, put the folder back
            return MRUdict, MRUorder # stop when no papers r left, hand back MRUdict and MRUorder

# reads TypedPaths from the registry, hands back TypedPath_dict
def RunTypedPaths():
    # check if TypedPaths exist
    try:
        folder = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths")
    except FileNotFoundError:
        return {}  # return empty dict, incase TypedPaths doesnt exist
    paperNum = 0 # paper number starts at 0
    TypedPath_dict = {} 
    while True:
        try:
            # grab paper number paperNum, Name = url1, url2, etc, Path = what was typed in the adress bar
            Name, Path, valType = winreg.EnumValue(folder, paperNum)
            TypedPath_dict[Name] = Path
            paperNum +=1
        except OSError:
            winreg.CloseKey(folder) # done reading the TypedPaths folder, put folder back
            return TypedPath_dict   # hand back the new dict 
def RunKeys():
    # check if Run exists
    try:
        folder = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
    except FileNotFoundError:
        return {} # return and leave function with empty dict, incase Run doesnt exist
    paperNum = 0 # paper number starts at 0
    RunPath_dict = {}
    while True:
        try:
            # grabs Paper num from folder, Name = Spotify, Discord, Mozilla, etc, Path, full path of startup apps
            Name, fullPath, valType = winreg.EnumValue(folder, paperNum)
            RunPath_dict[Name] = fullPath
            paperNum +=1
        except OSError:
            winreg.CloseKey(folder) # done reading the Run folder, put folder back
            return RunPath_dict # hand back new dict
           
# menu, pick an artifact to run
print(f"{"":-^40}")
print(f"{"Menu":^40}")
print(f"{"":-^40}")
print(f"1. {"Run MRU":^34}")
print(f"2. {"Run TypedPaths":^40}")
print(f"3. {"Run RunKeys":^38}")
print(f"0. {"Quit":^30}")
print(f"{"":-^40}")
while True:
    try:
        # take user input from the menu
        UserInput = int (input("\nEnter a menu number: "))
        print()
    except ValueError:
        print(f"{"":-^40}")
        print("Enter a valid menu number.")
        print(f"{"":-^40}")
        continue
    except KeyboardInterrupt: # Ctrl+C quits program without an error
        break 
    if UserInput == 0:
        # user quits and leaves program
        print(f"{"":-^40}")
        print(f"{"Goodbye!"}")
        print(f"{"":-^40}")
        break
    elif UserInput == 1:
        MRUdict, MRUorder = RunMRU() 
        # check if there was no dict found
        if MRUdict == {}:
            print()
            print(f"{"":-^40}")
            print(f"{"RunMRU not found.":^40}")
            print(f"{"":-^40}")
        else:
            print(f"{"":-^40}")
            print(f"ORDER: {MRUorder:^25}")
            print(f"{"":-^40}")
            # Loops for each letter in the MRUorder, newest first
            for nextLetter in MRUorder:
                # checks whether a letter is really in the dict, or been deleted / missing
                if nextLetter in MRUdict:
                    print(f"{MRUdict[nextLetter]:^40}")
                else:
                    print(f"Letter: {nextLetter} is Missing")
            print(f"{"":-^40}")
            print(f"{" Run MRU Done":^40}")
            print(f"{"":-^40}")
            print()
    elif UserInput == 2:
        # catch RunTypedPaths
        TypedPaths_dict = RunTypedPaths()
        if TypedPaths_dict == {}: # check if TypedPaths_dict is empty
            print(f"{"":-^40}")
            print(f"{"TypedPaths not found.":^40}")
            print(f"{"":-^40}")
        else:
            print(f"{"":-^40}")
            highest = 0  # finds biggest url number, so missing ones dont get skipped
            for name in TypedPaths_dict:
                urlNum = int(name[3:])
                if urlNum > highest:
                    highest = urlNum
            for num in range(1, highest + 1):  # count url1 url2, etc in order, newest first
                urlName = f"url{num}"
                # checks whether a url is in the dict, or has been deleted / missing
                if urlName in TypedPaths_dict:
                    print(f"{TypedPaths_dict[urlName]:^40}")
                else:
                    print(f"{urlName} is missing.") 
            print(f"{"":-^40}")
    elif UserInput == 3:
        # catch RunPath_dict
        RunPath_dict = RunKeys()
        if RunPath_dict == {}: # check whether Run path dict is empty
            print(f"{"":-^40}")
            print(f"{"No Run keys found.":^40}")
            print(f"{"":-^40}")
        else:
            # loop through each startup app and its path
            for appName in RunPath_dict:
                print(f"{"":-^40}")
                print(f"{appName:^40}") # print app name
                width = shutil.get_terminal_size().columns # get how wide the terminal is
                print(textwrap.fill(str(RunPath_dict[appName]), width=width)) # print app name path
            print(f"{"":-^40}")
    else:
        # user enters invalid number value
        print(f"{"":-^40}")
        print("Number must be 0-3")
        print(f"{"":-^40}")