import winreg # read windows registry
import textwrap # text wrap long text to fit terminal
import shutil # get terminal width for textwrap
import ctypes # call windows functions, calling admin
import sys # python info used to relaunch as admin

# menu, pick an artifact to run
def ShowMenu():
    print(f"\n{"":-^40}")
    print(f"{"Menu":^40}")
    print(f"{"":-^40}")
    print("1. Run MRU")
    print("2. Run TypedPaths")
    print("3. Run Keys")
    print("4. Run Wifi")
    print("0. Quit")
    print(f"{"":-^40}")

# grabs one value from a network folder by its name, hands back None if its missing
def GetValue(netFolder, valueName):
    try: 
        data, valType = winreg.QueryValueEx(netFolder, valueName)
        return data  # hand back just the data
    except FileNotFoundError:
        return None # no file means value doesnt exist in this network folder
    
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
        
def RunWifi():

    # check is Network list profiles exist
    try:
        folder = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles")
    except FileNotFoundError:
        return [] # return empty list and leave funcation if it doesnt exist
    except PermissionError:
        return None # catches error and leaves function, key entry needs admin
    
    paperNum = 0 # starts at zero
    RunWifi_list = []

    while True:

        try:
            # grab network folders
            Network_GUID = winreg.EnumKey(folder, paperNum)
            netFolder = winreg.OpenKey(folder, Network_GUID) # open the networks GUID folder inside Profiles
            netName = GetValue(netFolder, "ProfileName") # send GetValue to grab ProfileName, catch what it hands back
            if netName is None: # GetValue hands back None when ProfileName is missing
                netName = "No Name Found" # placeholder so the network still shows up
            winreg.CloseKey(netFolder) # put key back with the network folder
            netInfo = {} # new empty dict for this one network, holds all its info
            netInfo["Name"] = netName # save the name in the box labeled Name
            RunWifi_list.append(netInfo) # put this networks dict in the list
            paperNum +=1 # next folder

        except OSError:
            winreg.CloseKey(folder) # close the key, and return list
            return RunWifi_list

if not ctypes.windll.shell32.IsUserAnAdmin():

    # check if user is running as admin, if not relaunch with admin popup
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}"', None, 1)
    sys.exit() # close the non admin copy

while True:    

    ShowMenu() # Show menu on each loop
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
                if name.startswith("url") and name[3:].isdigit():
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
            print(f"{"TypedPaths Done":^40}")
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
            print(f"{"Run Keys Done":^40}")
            print(f"{"":-^40}")

    elif UserInput == 4:
            # catch RunWifi list
        RunWifi_list = RunWifi()
        if RunWifi_list is None: # check if user is running as admin # Check if user is running as admin
            print(f"{"":-^40}")
            print(f"{"Run Program as Admin.":^40}")
        elif RunWifi_list == []: # check if user has any networks in the list == []: # check if user has any networks in the list
            print(f"{"":-^40}")
            print(f"{"No Networks Found.":^40}")
        else:
            for network in RunWifi_list: # loop through each network dict, one at a time
                print(f"{"":-^40}")
                print(network["Name"]) # open this networks Name box and print it
        print(f"{"":-^40}")
    else:
        # user enters invalid number value
        print(f"{"":-^40}")
        print("Number must be 0-4")
        print(f"{"":-^40}")