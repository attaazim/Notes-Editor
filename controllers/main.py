from flask import *
from extensions import db
import os
import shutil


main = Blueprint('main', __name__, template_folder='templates', url_prefix='/noteseditor')

@main.route('/', methods=['GET', 'POST'])
def main_route():
    
    # dictionary of all suggested edits
    edits = {}

    # dictionary of all stopwords
    stopwords = {}

    read_stopwords = open('stopwords.txt', 'r')
    # save stopwords into memory
    for word in read_stopwords:
        # save all stopwords
        stopwords[word] = 1
    
    if request.method == 'POST':
        
        # ask editor to review the user's note'
        if request.form['op'] == 'review':
            # open file to insert user's note'
            write_file = open('usernote.txt', 'w+')
            # write the user's note to the file
            write_file.write(request.form['notetext'])

            # open the file to read the user's note
            # split into individual words
            words = open('usernote.txt', 'r').read().split()

            for term in range(len(words)):
                # make word case insensitive
                word = words[term].lower()
                # check if word is not a stopword
                if not(word in stopwords):
                    
                    # TODO: check if this is necessary
                    # remove garbage characters
                    word = re.sub(r'[^a-zA-Z0-9]+', '', word)

                    # ==================================================
                    # query sql db for word and save to edits dictionary
                    # ==================================================
                    cur = db.cursor()
                    cur.execute('SELECT * FROM Synonyms WHERE word = \"%s\";' %(word))
                    results = cur.fetchall()

                    edits[word] = results



            options = {
                "edit": True,
                "edits_dict": edits
            }
            return render_template('index.html', **options)

                    

                

    