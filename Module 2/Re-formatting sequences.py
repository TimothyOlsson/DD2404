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

#Removes all lines with hashes, // and empty lines
for i in file_contents:
    if ("#" in i) or ('//' in i) or (i == '\n'):
        pass
    else:
        #Append to content list if it does not have it
        contents.append(i)

#Create a new list
fixed_contents = []

#Opens and writes to a new file
with open(filename + '_fixed.sthlm','w') as f:
    for i in contents:
        i = i.split() #Creates a splitted list
        for ii in range(0,2):
            if ii == 0:
                f.write('>' + i[ii] + '\n')
            else:
                while (len(i[ii])) > 60:
                    f.write(i[ii][:60] + '\n')
                    i[ii] = i[ii][60:]
                f.write(i[ii] + '\n')
        


