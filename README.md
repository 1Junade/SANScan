# SANScan

This is a Python script that pulls Windows forensic artifacts from the registry.
Info from the SANS Windows Forensic Analysis poster.

## What it reads

Right now it reads RunMRU, which shows the history of commands typed into the Windows Run Box.
It shows from newest to oldest.
If a letter is in the list but its command is gone, it will flag it as missing, which can mean it was deleted.

## How to run

Open a terminal in the SANScan folder and run the command below, no admin needed since it is your own registry.

python SANScan.py

## Requirements

Windows, Python 3.12 or newer.

## Why

Building my own forensics tool to understand how it works, instead of someone elses tool.
Planning to add more artifacts.