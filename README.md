# SANScan

This is a Python script that pulls Windows forensic artifacts from the registry.
Info from the SANS Windows Forensic Analysis poster.

## What it reads

Right now it reads RunMRU, which shows the history of commands typed into the Windows Run Box.
It shows from newest to oldest.
If a letter is in the list but its command is gone, it will flag it as missing, which can mean it was deleted.

Reads TypedPaths, which is the list of folder paths someone typed in the File Explorer address bar. It also shows the newest first, starting at url1, if a number is skipped it flags as missing.

Run Keys reads the startup programs and their paths. These programs are set to start automatically when you log in.

Wifi reads the network profiles Windows saves for every network the PC has joined. Right now it shows each network's name. First and last connected dates are to come.

## How to run

Open a terminal in the SANScan folder and run the command below

python SANScan.py

When it starts a menu will pop up, type the menu number you want to run. Type 0 to quit.

Wifi reads the network profiles, which is a part of the registry that needs admin. So, when you start SANScan, it will ask to run as admin with a popup, click Yes, and it will open in a new elevated admin window.

## Requirements

Windows, Python 3.12 or newer.

## Why

Building my own forensics tool to understand how it works, instead of someone else's tool.
Planning to add more artifacts.