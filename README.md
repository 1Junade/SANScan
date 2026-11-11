# SANScan

This is a Python script that pulls Windows forensic artifacts from the registry.
Info from the SANS Windows Forensic Analysis poster.

## What it reads

Right now it reads RunMRU, which shows the history of commands typed into the Windows Run Box.
It shows from newest to oldest.
If a letter is in the list but its command is gone, it will flag it as missing, which can mean it was deleted.

Reads TypedPaths, which is the list of folder paths someone typed in the File Explorer search bar. It also shows the newest first, starting at url1, if a number is skipped it flags as missing.

## How to run

Open a terminal in the SANScan folder and run the command below, no admin needed since it is your own registry.

python SANScan.py

When it starts a menu will pop up, type the menu number you want to run. Type 1 for RunMRU, 2 for TypedPaths, 0 to quit, etc.

## Requirements

Windows, Python 3.12 or newer.

## Why

Building my own forensics tool to understand how it works, instead of someone elses tool.
Planning to add more artifacts.