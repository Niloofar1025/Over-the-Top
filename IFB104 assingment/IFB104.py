 
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: N10358790
#    Student name: Niloofar Gorjinejad
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Runners-Up
#
#  In this assignment you will combine your knowledge of HTMl
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application that allows the user to access online data.  See the
#  instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these functions
# only.  You can import other functions provided they are standard
# ones that come with the default Python/IDLE implementation and NOT
# functions from modules that need to be downloaded and installed
# separately.  Note that not all of the imported functions below are
# needed to successfully complete this assignment.

# The function for accessing a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# The function for displaying a web document in the host
# operating system's default web browser.  We have given
# the function a distinct name to distinguish it from the
# built-in "open" function for opening local files.
# (You WILL need to use this function in your solution.)
from webbrowser import open as urldisplay

# Import some standard Tkinter functions. (You WILL need to use
# some of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL, sub

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to download and save a web document. If the
# attempted download fails, an error message is written to
# the shell window and the special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * lying - If True the Python function will try to hide its
#      identity from the web server. This can sometimes be used
#      to prevent the server from blocking access to Python
#      programs. However we do NOT encourage using this option
#      as it is both unreliable and unethical!
# * got_the_message - Set this to True once you've absorbed the
#      message above about Internet ethics.
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             lying = False,
             got_the_message = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if lying:
            # Pretend to be something other than a Python
            # script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0')
            if not got_the_message:
                print("Warning - Request does not reveal client's true identity.")
                print("          This is both unreliable and unethical!")
                print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to open a local HTML file in your operating
# system's default web browser.  (Note that Python's "webbrowser"
# module does not guarantee to open local files, even if you use a
# 'file://..." address).  The file to be opened must be in the same
# folder as this module.
#
# Since this code is platform-dependent we do NOT guarantee that it
# will work on all systems.
#
def open_html_file(file_name):
    
    # Import operating system functions
    from os import system
    from os.path import isfile
    
    # Remove any platform-specific path prefixes from the
    # filename
    local_file = file_name[file_name.rfind('/') + 1:] # Unix
    local_file = local_file[local_file.rfind('\\') + 1:] # DOS
    
    # Confirm that the file name has an HTML extension
    if not local_file.endswith('.html'):
        raise Exception("Unable to open file " + local_file + \
                        " in web browser - Only '.html' files allowed")
    
    # Confirm that the file is in the same directory (folder) as
    # this program
    if not isfile(local_file):
        raise Exception("Cannot find file " + local_file + \
                        " in the same folder as this program")
    
    # Collect all the exit codes for each attempt
    exit_codes = []
    
    # Microsoft Windows: Attempt to "start" the web browser
    code = system('start ' + local_file)
    if code != 0:
        exit_codes.append(code)
    else:
        return 0
    
    # Apple macOS: Attempt to "open" the web browser
    code = system("open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Linux: Attempt to "xdg-open" the local file in the
    # web browser
    code = system("xdg-open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Give up!
    raise Exception('Unable to open file ' + local_file + \
                    ' in web browser - Exit codes: ' + \
                    str(exit_codes))

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

##### DEVELOP YOUR SOLUTION HERE #####
# create a window
the_TOP = Tk()

# title window name
the_TOP.title("Over the TOP")

#change the window's background colour
the_TOP.configure(bg = 'white')

# declare as a global python variables
selected_list = IntVar()

############################################################# ##<<Displaying data from online documents>>#############################################################################################
# choose option
def chosen():
    global selected_list
    global popularBooks
    global topSongs
    global topTvShows
    global name_movies
    global IMDB
    global years
    global name
    global Author
    global Average
    global Artist
    global SongStreams
    global RecordLabel
    global Title
    global AgeRate
    
    number = selected_list.get()
    popularMovies = [] # create an empty list for popular movies from IMDB charts
    popularBooks= [] # create an empty list for TOP Books
    topSongs=[] # create an empty list for TOP Muscis
    topTvShows=[] # create an empty list for TOP Tv Shows

    if number == 1: # Top Tv shows- TOP BOX OFFICE
        url_1= 'https://www.imdb.com/chart/moviemeter'
        html_code=urlopen(url_1).read().decode('UTF-8') #download the html code from a url in a string format
        #extract the data from the web sites
        #return the first match (name_movies)
        name_movies= findall('alt="(.*?)"',html_code) #title of movies (top box office)
        #return the second match (IMDB)
        IMDB= findall(r'<span name=\"ir\" data-value=\"([0-9]\.[0-9])\"></span>', html_code)
        #return the third match(years)
        years= findall('<span class="secondaryInfo">([0-9]*.+)</span>', html_code)
        for index in range(10): #first 10 results from finall
            #iterate all lists simultaneously to display the individual pair of elements from the lists
            popularMovies.append(str(index+1) + '. ' +name_movies[index]+ ' , '+ years[index]+ ' , '+IMDB[index])         
            # second options 
            secondpopularMovies = name_movies[1]+ ' , '+ years[1]+ ' , '+IMDB[1]
            #remove number 2 from the list
        popularMovies.pop(1)
        #change a property of frame others after its creation
        frameOthers['text'] = 'Other popular movies\n' + '\n'.join(popularMovies)
        #update the text property for second RunnerUp - \n new line character appearing in the string
        frameRunnerUP['text'] = 'RunnerUP\n'+ '2. '+ secondpopularMovies 
        
    elif number == 2: # popularBooks
        url_2 = 'https://www.goodreads.com/book/popular_by_date/2020'
        html_code=urlopen(url_2).read().decode() #download the html code from a url in a string format
        # extract the data from the web sites
        name = findall("<span itemprop='name' role='heading' aria-level='4'>([A-Za-z]*[A-Za-z ]*)", html_code)
        Author = findall('<span itemprop="name">([A-Z][A-Za-z \.-]*)', html_code) #Author of each books
        Average = findall('</span>\s*.([0-9]\.[0-9]*)', html_code)# average rating
        for index in range(10): #first 10 results from finall
         #iterate all lists simultaneously to display the individual pair of elements from the lists
         popularBooks.append(str(index+1) + '. ' +name[index]+ ' , '+Author[index]+' , '+Average[index])
         secondpopularBooks = name[1]+ ' , '+ Author[1]+' , '+Average[1]# second options
        popularBooks.pop(1) #remove number 2 from the lists
        frameOthers['text'] = 'Other popular books \n' + '\n'.join(popularBooks)
        frameRunnerUP['text'] = 'RunnerUP\n' +'2. '+ secondpopularBooks # update the text property to display the results
  
    elif number == 3: #TOP Songs- Live website
        url_3 = 'https://www.rollingstone.com/charts/songs/'#the top songs
        html_code = urlopen(url_3).read().decode() #download the html code from a url in a string format
        # extract the corresponding data from the web sites
        Artist = findall('<div class="c-chart__table--caption">([0-9]*[A-Za-z]+[a-z]*|[A-Z]+[a-z].*)</div>',html_code) # artist name
        SongStreams = findall('<span>([0-9]+\.[0-9]*[A-Z])', html_code)#shows the Song Streams
        RecordLabel = findall('<span class="c-chart__table--label-text">([A-Z]*.[A-Za-z ]*)</span>',html_code)
        for index in range(10): #first 10 results from finall
            Artist[index] = Artist[index].replace('&amp;','&')
            #iterate all lists simultaneously to display the individual pair of elements from the lists
            topSongs.append(str(index+1) + '. ' +Artist[index]+ ' , '+SongStreams[index]+' , '+RecordLabel[index]) 
            secondtopSongs =Artist[1]+ ' , '+ SongStreams[1]+' , '+RecordLabel[1] # second options
        topSongs.pop(1) # removes number 2 from the lists
        frameOthers['text'] = 'Other Top Songs\n' + '\n'.join(topSongs)
        frameRunnerUP['text'] = 'RunnerUP\n'+'2. '+ secondtopSongs #update the text property for RunnerUP
 
####################################################<<Displaying data from the previously-downloaded document>>#################################################################################################
        

    elif number == 4: #Top Tv shows - static website
        html_code = open('download.html', 'r', encoding = 'UTF-8').read()
        # extract the corresponding data from the web sites
        Title= findall('<img alt="(.*?)"',html_code) #show the title of Tv shows
        AgeRate= findall('<span class="certificate">([A-Z]*.[0-9]*[+]*)<',html_code) #shows the age rate of TVshowsprint(Duration)
        for index in range(10): #first 10 results from finall 
            topTvShows.append(str(index+1) + '. ' +Title[index] + ', '+ AgeRate[index])
            secondtopTvShows =Title[1]+ ', '+ AgeRate[1] # second options
        topTvShows.pop(1) #removes number 2 from the lists
        frameOthers['text'] = 'Other Top TV Shows\n' + '\n'.join(topTvShows)
        frameRunnerUP['text'] = 'RunnerUP\n'+'2. '+ secondtopTvShows
 
################################################################<<STARTING OF PART B>>########################################################################################################################
        
##Function to save information to SQL database when user presses Save button
def save_files():
    
    #Create a connection to the database
    connection = connect(database = 'runners_up.db')
    #Get a pointer into the database for others
    Others = connection.cursor()
    Others.execute("delete from others")
    Others.execute("delete from runner_up")
    #seperate each item- define the numbers
    number = selected_list.get()
    
    if number==1: #choosing the first option of the lists
        for sql in range(10): # first 10 results of the website 
            if sql !=1: #not equal to 1, show the rest
                #inserting values to 'others' table and extract the data in the database 
               popularMovies_others="INSERT INTO others VALUES (" + '"' + str(sql+1) + '",' + '"' + name_movies[sql]+'",' + '"' + years[sql] + ' ' + IMDB[sql] + '");'
               #execute the for others table 
               Others.execute(popularMovies_others)
            else:
                #inserting values to 'runners_up' table and extract the data in the database
                popularMovies_runnersup="INSERT INTO runner_up VALUES (" + '"'+ name_movies[sql] + '",' + '"' + years[sql] + ' , ' + IMDB[sql] + '");'
                #excute the data for runnerup table
                Others.execute(popularMovies_runnersup)
    elif number==2:
         for sql in range(10): 
            if sql !=1:
               popularBooks_others = "INSERT INTO others VALUES (" + '"'+str(sql+1) + '",' + '"' + name[sql] + ', ' + Author[sql] + '",' + '"' + Average[sql] +'");'
               Others.execute(popularBooks_others)
            else:
                popularBooks_runnersup = "INSERT INTO runner_up VALUES (" + '"'+name[sql] + ', '+Author[sql] + '",'+'"' + Average[sql]+'");'
                Others.execute(popularBooks_runnersup)

    elif number==3:
        for sql in range(10):
            if sql !=1:
               topSongs_others = "INSERT INTO others VALUES (" + '"'+str(sql+1) + '",'+'"' + Artist[sql] + ', '+ RecordLabel[sql] + '",' + '"' +SongStreams[sql]+'");'
               Others.execute(topSongs_others)
            else:
                topSongs_runnersup="INSERT INTO runner_up VALUES (" + '"'+ Artist[sql] + ', '+ RecordLabel[sql] + '",' + '"' + SongStreams[sql] + '");'
                Others.execute(topSongs_runnersup)

    elif number==4:
        for sql in range(10):
            if sql !=1:
               tvShows_others = "INSERT INTO others VALUES (" + '"' + str(sql+1) + '",' + '"' + Title[sql] + '",'+'"' + AgeRate[sql] + '");'
               Others.execute(tvShows_others)
            else:
                tvShows_runnersup ="INSERT INTO runner_up VALUES (" + '"' + Title[sql] + '",' + '"'+ AgeRate[sql] + '");'
                Others.execute(tvShows_runnersup)


    #Commit the changes to the database
    connection.commit()
    Others.close()
    connection.close()
        
############################################################<<CREATE LOGO, IMAGE>>###<<TITLE>>##############################################################################################


# create a logo
TOP_image = PhotoImage(file = "Top10.gif")
TOP_logo = Label(the_TOP, image = TOP_image)
TOP_logo.grid(row = 1, column = 0)

#A heading which identifies the application(Over the top)

title_name = Label(the_TOP, font = ('Arial', 18,'italic'),
                  text = "OVER THE TOP", bg = 'yellow', fg = 'black')
title_name.grid(row = 0,column = 0,columnspan=3)

#########################################<<CREATING FRAME>>##<<CURRENT,PREVIOUS>>###<<RUNNERUP,OTHERS>>##################################################################################


# creating frame to put all the options there
frameCurrent= LabelFrame(the_TOP,relief = 'ridge',
                  text = 'Current#2', bg = 'white', fg= 'red', font = ("Time News Roman",18,'bold','italic'))
frameCurrent.grid(row = 1,column = 1)

# creating frame to show the option for 'PREVIOUS'
framePrevious= LabelFrame(the_TOP, relief = 'ridge',bg = 'white',fg = 'Red',padx = 10,pady = 5,
                  text = 'Previous#2',font = ("Time News Roman",18,'bold', 'italic'))
framePrevious.grid(row = 1,column = 2)

# creating frame to show Nothing selected yet
frameRunnerUP= Label(the_TOP, relief = 'groove',bg = 'white',fg = 'black',
                     text = 'Nothing selected yet',font = ("Arial",14),
                     width = 50,height = 15,
                     anchor ='nw',justify = LEFT)
                     
frameRunnerUP.grid(row = 2,column = 1)

# creating frame to show Nothing selected
frameOthers= Label(the_TOP, relief = 'groove',bg = 'white',fg = 'black',
                   text = 'Nothing selected yet' ,font = ("Arial",14) ,
                   width = 60,height = 15,
                   anchor = 'nw',justify = LEFT)
                   
frameOthers.grid(row = 2,column = 2, padx = 10)

#############################################################################<<Opening the source web documents in a web browser>>#################################################################################################

#showing the resource of each url by clicking on show resource button

def open_website():
    #selected = int(selected_list.get())
    selected =selected_list.get()
    if selected==1: #choosing the first option
        urldisplay('https://www.imdb.com/chart/moviemeter') # display the url
    elif selected==2:
        urldisplay('https://www.goodreads.com/book/popular_by_date/2020')
    elif selected==3:
        urldisplay('https://www.rollingstone.com/charts/songs/')
    else:
        open_html_file('download.html')
        

######################################################################################<<BUTTON PART>>##############<<UPDATE,SHOW_RESOURCE,SAVE>>################################################################################
 
# updatebutton
update_button = Button(the_TOP, text = 'update', fg = 'red', font = ("Arial",18,'bold'),
                       justify = LEFT,command = chosen,
                       activeforeground= 'green')
update_button.grid(row = 3, column = 1)      
# show resource button    
show_resource_button = Button(the_TOP, text = 'show resource', fg = 'red',
                              font = ("Arial",18,'bold'),command = open_website,activeforeground = 'green')

show_resource_button.grid(row = 3, column = 2)

#Save Button
Save_button = Button(the_TOP, text = 'save', fg = 'red', font = ("Arial",18,'bold'),command = save_files,
                   activeforeground = 'green')

Save_button.grid(row = 3,column = 1, columnspan = 3)


#####################################################################################<<RADIOBUTTON PART>>##############################################################################################

# creating radio buttons for popular Movies
popularMovies = Radiobutton(frameCurrent,
                            text = 'Most popular movies from IMDB charts\n(Title,Years & IMDB)',
                            variable = selected_list, value = 1,
                            font = ('Times',15),
                            fg = 'midnight blue',justify = LEFT)
# show in the shell window
popularMovies.grid(row = 0, column = 0)

# creating radio buttons for popular books
popularBooks= Radiobutton(frameCurrent,
                          text ='Most popular books published in 2020\n(Title, Author & Average rating)',
                          font = ('Times',15),variable = selected_list, value = 2,
                          fg = 'green',justify = LEFT)
# show in the shell window
popularBooks.grid(row = 1, column = 0)

# creating radio buttons for top musics
top_musics = Radiobutton(frameCurrent,
                         text = 'Top 100 songs\n (Artists, Song streams & RecordLabel)',
                         font = ('Times',15),variable = selected_list, value = 3,
                         fg = 'red',justify = LEFT)
# show in the shell window
top_musics.grid(row = 2, column = 0)

# creating radio buttons for New Tv series
top_TVShows = Radiobutton(framePrevious,
                          text = 'New TV series\n (Title & Age rate)\n [6 months ago]',
                          font = ('Times',15),variable = selected_list, value = 4,
                          fg = 'purple',justify = LEFT)
# show in the shell window
top_TVShows.grid(row = 3, column = 0)



