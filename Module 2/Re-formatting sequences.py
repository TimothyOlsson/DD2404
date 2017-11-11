#Imports os, used to change folder in this case
import os

#Change directory
os.chdir(r'files')

#input filename
filename = input('Filename: ')

#Opens and reads the file. Gets all the lines
with open(filename + '.sthlm','r') as f:
    file_contents = f.readlines()

#Create a list
contents = []

#Removes all lines that starts with hash, // and empty lines
for i in file_contents:
    if i.startswith('#'): #Starts with # = comment
        pass
    elif i == '\n': #Ignore empty line
        pass
    elif i.startswith('//'): #End of file
        break
    else: #Append to content list
        contents.append(i)

#Create a new list
fixed_contents = []

#Opens and writes to a new file
for i in contents:
    i = i.split() #Creates a splitted list, with name and sequences

    #first line with name, add > and \n
    fixed_contents.append('>' + i[0] + '\n')

    #Add \n for every 60 characters in sequence
    fixed_contents.append(('\n'.join(i[1][j:j+60] for j in range(0, len(i[1]), 60))) + '\n')


with open(filename + '_fixed.sthlm', 'w') as f:
    for i in fixed_contents:
        f.write(i)
