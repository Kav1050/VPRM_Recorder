# VPRM_Recorder
Used to record daily weekly or monthly mining revenue for VPRM. Can be use for other coins if modified. Exports and loads data from excel
Currently has 3 seperate areas so 3 seperate wallets can be tracked but can be easily changed to add more or less
Uses Excel as the data base.
On first use you must press the export to ecel button to be able to start using
each time the program starts it loads the excel file with the previous exported data
Can be easily changed to suit other coins with different block values
Created with the help of Chat GPT

To run this file in Python the following python packages installed:
- tkinter = python -m tkinter
- pandas = pip install pandas
- xlsxwriter = pip install XlsxWriter

To compile into a windows exe file you need Pyinstaller installed = pip install pyinstaller
then in a CMD prompt window, navigate to the folder where the VPRM_Recorder file is and and run = pyinstaller --onefile --noconsole your_script.py


