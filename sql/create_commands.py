import os
import shutil

# split synonyms file into seperate lines
# store each word in the line as a key in the dictionary with value as the remaining words in the line
# store those in the db accordingly

dict = {}

# list of commands for load_data.sql
load_commands = []

# one line is one word and its synonyms
lines = open('synonyms.txt', 'r').read().split("\n")

# for each synonym group (each line)
for line in lines:
    words = line.split()
    for word in words:
        if not(word in dict):
            synList = [''] * 4
            for i in range(len(words)):
                    synList[i] = words[i]
            dict[word] = synList
            
for word in dict:
    sugg1 = dict[word][0]
    sugg2 = dict[word][1]
    sugg3 = dict[word][2]
    sugg4 = dict[word][3]

    command = "INSERT INTO Synonyms (word, one, two, three, four) VALUES (" + (str(word) + ", " + str(sugg1) + ", " + str(sugg2) + ", " + str(sugg3) + ", " + str(sugg4) + ");")
    load_commands.append(command)

write_file = open("load_data.sql", "w+")
for command in load_commands:
    write_file.write(command)
    write_file.write("\n")