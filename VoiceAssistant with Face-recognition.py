"""
Aim         :   To design a Voice assistant application with face-recogntion technology which 
                the interacts with the users, give response to all the queries which user asks 
                and also recognizes and remembers the user face and wish him/her when they 
                appear in front of the camera.

Description :
                This project is to give senses to a machine/system. This application is 
                designed to be natural and conversational, making them more accessible 
                and user-friendly. As the technology is advancing, use of robots are also
                increasing, to reduce the man power. This application can be injected in 
                modern robots to give vision to the machine and ability to communicate with
                the user and answer all the queries which the user asks.
                Speech-recognition technology is used to make the system communicate and 
                computer vision technology is used to analyze and identify human faces.
                
Scope       :   The scope of the project is, this technology  can be implemented in robots and these
                robots can be used in various public places which requires human guidance.
                As an example, it can be used in hospitals to guide the patients (if this
                application is trained to medical related queries) and also acts as 
                a security to moniter patient. This technology can also be used at 
                restaurants, when the customer visits the restaurant, it takes the order
                and remember the customer face and servers the customer based on the 
                face-recognition. It is used in homes to control the devices (similar to alexa)
                and identifies the owner's face, and acts as security for home.
                And also can be used in attendance monitoring system in institutes/offices, etc.
"""


""" pyttsx3 module is used to convert text-to-speech """
import pyttsx3   

""" speech_recognition module is used to recognize and convert speech-to-text """             
import speech_recognition as sr   
      
""" time module is used to display time in Application  """
import time as tt    
            
""" webbrowser module is used to search the queries which requires the use of web brower """   
import webbrowser as wb

""" wikipedia module is used search the information from wikipedia """
import wikipedia as wk

""" WolFram Alpha is API (answer engine) used to answer factual queries """
import wolframalpha as wfa

""" os module is used here to get control of files """
import os

""" random module is used to select the random songs from the application database when user wants to listen music """
import random

""" pygame module is used to give sound effects for the application """
import pygame

""" tkinter module is used to provide a Graphical User Interface """
import tkinter

""" threading module is used to run the various parts of application parallely """
import threading

""" cv2 module (OpenCV library) is used for face-recognition """
import cv2

""" numpy module is used to provide a key for each human face for recognition"""
import numpy as np

""" pillow module is used to put the camera frames in GUI """
from PIL import Image,ImageTk

""" This is a developer written module which contains a single function KNN algorithm """
import ML

""" pickle module is used to stores the unique IDs of songs """
import pickle


"""
Set the directory to where all the project files are saved
"""
os.chdir("Voice assistant(Mini project)")


"""
For security purpose, complete chats are stored in database
"""
chatStartTime = tt.ctime()      # start time of the application for chat...
chatPerson=[chatStartTime]      # Who are persons involved in chat/communication with application...
chats = ""                      # Complete chat data...
chatHistory={}                  # Stored in a dictionary to store in database...

"""
Wolfram Alpha is an AI & NLP based answer engine,which answers the factual queries,
                                                                   science related queries, 
                                                                   math related queries, 
                                                                   general knowledge etc.

All the queries are answered via an WolFram Alpha account which each account has unique AppID.
"""


"""
Declaring global variables
"""

# Here, ID is your unique API key of wolfram alpha... (Create a account in wolfram alpha and request API key)...  
client = wfa.Client(ID)      # Setting the AppID to use wolfram alpha service...

current_voice = 1   # The global variable to change the voice of assistant... 

present  = None     # The global variables to make the voice assistant remember the face recoginzed...
previous = None


################### Initializing the pyttsx3 & pygames module for setting up the properties ##################


engine = pyttsx3.init()
pygame.init()

speech_voices = engine.getProperty('voices')          # default Male voice...
engine.setProperty('voice', speech_voices[1].id)
# speech_rate = engine.getProperty('rate')            # default speech rate is 200wpm...
engine.setProperty('rate', 175)
# speech_volume = engine.getProperty('volume')        #default volume 1.0 (max. volume)...
# engine.setProperty('volume',1.0)



############################# Initializing the database which contains the list of songs ###################################

class initializingDB:
    """
        This class is used to load the list of songs to a variable from the database
        to access songs fast...
    """                                                
    def __init__(self):
        songsDatabase = open("songsDatabase.pickle", "rb")   # Opening the pickle file which contains the unique ID's of songs...
        self.data = pickle.load(songsDatabase)               # Load the whole data into a variable...
        songsDatabase.close()                                # Close the file...

############################################################################################################################


############################# Speaker class contains all the functions required for VoiceA #################################

class speaker:
    """
        This class contains all the functions which uses the system speaker and microphone 
        to communicate with user and also produce sound effects.
    """
       
    ########################################## SOUND EFFECTS ###################################################
    
    def sound_effect(self,se):                 # 'sound_effect' function is used for microphone ON/OFF sound effects...
        
        """ 
            This function uses 'for' loop to produce sound effect.
            The loop should run to some extent so that the sound packets/frames 
            produce the sound sequencially.
        """
        for _ in range(1000):                                  # for-loop is used for continues flow of sound packets...
            pygame.mixer.music.load(se)                        # Loading the sound-effect in mixer...
            pygame.mixer.music.play()                          # Playing the sound-effect...
            # pygame.mixer.Sound.play(pygame.mixer.Sound(se))
        tt.sleep(1)  # waiting for 1 sec to setup...
        
    #############################################################################################################
    

    ############################################ SPEAK OUT ######################################################
    
    def speak(self,audio):                     # 'speak' function is used for replying the user by speaking out...
        
        """
            The function uses the system speaker to speak-out/respond to the user query.
            The 'say()' function from pyttsx3 module takes the text as argument and speak the text out.
        """
        
        try:
            global chats
            print(audio)
            VoiceA = tkinter.LabelFrame(Frame2,text="VoiceA",bg="yellow",
                                        font=("Times New Roman", 13))
            VoiceA.pack(pady=10)

            msg = tkinter.Label(VoiceA,wraplength=220,
                                width=40,text=audio,bg="white")
            msg.pack()
            chats+="( VoiceA : "+audio+" ) "     # Communicated data of VoiceA to be stored...
            engine.say(audio)                    # This function uses the speaker of the system to speak out...
            engine.runAndWait()                  # This function makes the speech audible in the system...
        except:
            pass
    
    #############################################################################################################
    
    
    ######################################### LISTENING FROM USER ###############################################
    
    def listen_from_user(self):                # 'listen_from_user' function is used to listen the query from user...
         
        """
            This function uses the system microphone to take the input/query from the user,
            And using Google Speech recognition, the query is recognized and converted to text.
        """
        
        r = sr.Recognizer()                                # Initializing the Recognizer class to adjust the speech parameters...
        with sr.Microphone() as source:                    # Initializing the Microphone class to setup the microphone...
            try:
                print("Listening...")
                microphone.configure(image=mic_bg)
                self.sound_effect('listening_effect.wav')
                r.pause_threshold = 0.8          # Seconds of non-speaking audio before a phrase is considered complete...
                r.non_speaking_duration = 0.5    # Setting the non_speaking_duration parameter...
                r.energy_threshold = 800         # Minimum audio energy to consider for recording, below this level considered as silent...
                audio = r.listen(source)         # Records the phrase from source which the user said...
                
                # Recognizing the phrase using Google speech recognition by using default google API key...
                query = r.recognize_google(audio, language="en-in") 

            except:
                # self.speak("Sorry, Unable to recognize...")
                query = None
            self.sound_effect('listenover_effect.wav')
            microphone.configure(image=mic_rm)
        return query
    
    #############################################################################################################

############################################################################################################################


####################################### Face-recognition based on the available data #######################################

class FACE_RECOGNITION(speaker):     # Inherits the properties from 'speaker' class...
    
    """
        This class contains all the functions required for face-recognition.
        All the trained data which contains the human faces is loaded to a variable and 
        All the recorded face data is loaded into a variable for identifying the face from live camera.
    """
    
    def __init__(self):
        # Setting the path for face-recognition files to access...
        self.default_path = "OpenCV"
        
        # Loading the classifier into a variable which contains the trained data of human faces...
        self.face_classifier = cv2.CascadeClassifier(os.path.join(self.default_path,"data\haarcascades\haarcascade_frontalface_alt.xml"))
        
        # Path for recorded faces...
        self.path = os.path.join(self.default_path,"faces_detected")

        self.names = {}             # Loading the names of the persons which are available in database...
        self.face_data = []         # Loading the numpy data of each person...
        self.label_data = []        # Making some labels to identify easily...
        self.count = 0              # Initializing the count to 0 & used as key for names...

        for file in os.listdir(self.path):                         # Searching the face data files in the given path..
            if file.endswith('.npy'):                              # Extension of face data file is .npy (numpy array data)
                self.names[self.count] = file[1:-4]                # File name is saved as Mr.<name_of_person>...
                data = np.load(self.path + "\\" + file)            # Loading the person's face data..
                target = self.count * np.ones((data.shape[0], 1))  # Creating the nx1 array, all values in array are key of the name...
                self.face_data.append(data)                        # Storing the face data in list...
                self.label_data.append(target)                     # Storing the nx1 array data in a list... 
                self.count += 1                                    # Incrementing the count...
    
        self.face_data = np.concatenate(self.face_data, axis=0)    # Merging the arrays by row (columns should be same)
        self.label_data = np.concatenate(self.label_data, axis=0).reshape((-1, 1)) # Merging the arrays by row (columns should be same)
        self.trained_data = np.concatenate((self.face_data, self.label_data), axis=1) # Merging the arrays by column (rows should be same)
        self.pad = 5        # Add padding around the frame...

    
    def showCap(self,showf):
        """
            This function displays the frames in GUI.
        """
        img = cv2.cvtColor(showf, cv2.COLOR_BGR2RGB)            # Converting the color from BGR ro RGB...
        img = ImageTk.PhotoImage(image=Image.fromarray(img))    # Convert NumPy array to image... 
        capL.config(image=img)                                  # Place the image in label...
        capL.image = img
    
    def startFR(self):
        
        """
            This function uses the system camera for reading frames and recognizing the face 
            of the user who is in front of the camera.
            The recognition of face is done by using KNN algorithm.
            This algorithm finds the nearest match of faces which are available in the database of recorded faces.
        """
        
        cap = cv2.VideoCapture(0)           # Turning ON the camera...
        while cap.isOpened():               
            try:
                global present         # Global variable to make assistant remember the user face...
                global previous        # Global variable to make assistant remember the user face...
                global capview         # Global variable to show/hide the OpenCV window...
                
                _, frame = cap.read()                                  # reading the frames from the camera... 
                frame = cv2.flip(frame, 1)                             # Mirror flip the frame...
                frame = cv2.resize(frame, (280, 300))                  # Resizing the frame...
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   # Converting the frames to gray scale image...
                self.faces = self.face_classifier.detectMultiScale(gray_frame, 1.05, 5)     # Detecting the faces in the frame...
                
                ######################### Placing the frames in GUI #############################
                
                self.showCap(frame)
                
                #################################################################################
                
                if len(self.faces) == 0:  # If no faces found in the frame, clear the assistant memory...
                    present = None
                    previous = None

                for (x, y, w, h) in self.faces:
                    self.face_detected = frame[y - self.pad:y + self.pad + h, x + self.pad:x - self.pad + w] # Padding detected faces...
                    self.face_detected = cv2.resize(self.face_detected, (100, 100))         # Resizing the face frames...
                    
                    ################### Sending the face frame to recognize the person using KNN algorithm ##################
                    self.result = ML.knn(self.trained_data, self.face_detected.flatten())   # Returns the person's name key... 
                    self.person = self.names[self.result]                           # Identifying the person's name using the key...
                    cv2.putText(frame, self.person, (x-(w//2), y - (h//2)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2) # Adding Text...
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 225, 0), 3)            # Drawing the rectangular box to the face...
                    present = self.person       # Storing the person name who is infront of the camera...

                    if self.person not in chatPerson:          # Store the person face which is captured by application...
                        chatPerson.append(self.person)
                    
                    if present != previous:     # If person is different from the memory, wish the person...
                        audio = "Hello " + str(self.person)   # Wishing the user...
                        threading.Thread(target=super().speak, args=(audio,)).start()    # Using the system speaker to wish...
                        previous = present      # Remembering the person's face who is infront of the camera...
                
                cv2.waitKey(1) & 0xFF       # Waiting the window to update the frames...        
                if capview:
                    cv2.imshow("FACE_RECOGNITION", frame)   # Displaying the OpenCV window...
                else:
                    cv2.destroyWindow("FACE_RECOGNITION")   # Destroying the OpenCV window...
            except:
                pass

        cap.release()            # Releasing the camera when application is closed...
        cv2.destroyAllWindows()  # Destroying all the frames whan application is closed...

############################################################################################################################



######################################## Voice-assistant to interact with the user #########################################

class VOICE_ASSISTANT(speaker,initializingDB):    # Inherits the properties from 'speaker' class & 'initializingDB' class...
    
    """
        This class contains all the responses which are required to answer the queries 
        of the user...
    """
    
    def __init__(self):
        self.filesFound=[]                        # To search the files in file explorer...
        initializingDB.__init__(self)             # Initializing database for music...
        super().speak("Waking the assistant")     # Waking the assistant...
        
    def find_file(self,filename, fs):                 # 'find_file' function searches the file in File Manager asked by the user... 
        
        """
            This function is used to search a file in the file manager which 
            is asked by the user.
            This function search the asked file in each and every directory and 
            give user all the paths in which that file exists.
        """
        
        for file in os.listdir(filename):           
            try:
                path = os.path.join(filename, file)
                if os.path.isdir(path):
                    self.find_file(path, fs)
                else:
                    if file == fs:
                        self.filesFound.append(path)   # If file found, append to to the list...
            except:
                pass

    def startVA(self):
        
        """
            This function contains all the responses based on the user query.
            WolFram Alpha is also used to respond the user on some factual questions.
            The assistant voice can also be changed through query by simply saying "change voice", which 
            converts the male voice to female voice and vice versa.
            All the commands/queries which the user asks must be direct,
            there should not be any 'hey' or 'hii' etc. like commmands in the query.
                Ex: 'Hey assistant, what is the time?' ---- Is invalid command.
                    'what is the time? ' ------------------ Is valid command. 
            If the assistant doesn't recognize any commands/queries from the user, 
            it tries to listen atmost 2 times, even after 2 times it doesn't recognized it shuts down,
            else it continues chat with user until the user stops.
        """
        
        cont = 0
        while True:           # Running the infinite loop to continue the conversion in good flow...
            try:
                global chats
                query = super().listen_from_user().lower()                  # Listening the query from user...
                Me = tkinter.LabelFrame(Frame2,text="Me",bg="yellow",
                                        font=("Times New Roman", 13),
                                        labelanchor="ne")
                Me.pack(pady=10)

                msg = tkinter.Label(Me,wraplength=220,width=40,
                                    text=query,bg="white")
                msg.pack()
                chats+="(  Person : "+query+" )  "                          # Communicated data of person to be stored...
                
                ###################### Some general queries #############################
                if ("hello" in query) or ("hii" in query) or ("hey" in query):
                    if ("how are you" in query):
                        super().speak("Hii, I'm fine. How are you?")
                    else:
                        super().speak("Hello, how may I help you?")

                elif ("welcome" in query):
                    super().speak("Thank you.")

                elif ("how are you" in query) or ("are you okay" in query):
                    super().speak("I am fine. How are you?")

                elif ("i am fine " in query) or ("i am good" in query) or ("all good" in query) or (
                        "i'm good" in query) or ("i'm fine" in query):
                    super().speak("Good to hear, how may I assist you?")

                elif ("what is the time" in query) or ("time now" in query) or ("current time" in query):
                    t = tt.strftime("%I:%M %p")
                    super().speak("It's " + t)

                elif ("your name" in query):
                    super().speak("I haven't named yet, for now you can simply call me as VoiceA.")

                elif ("thank you" in query) or ("thanks" in query):
                    super().speak("You're most Welcome...")

                elif ("open youtube" in query):
                    super().speak("Opening youtube")
                    wb.open("https://www.youtube.com/")        # Opening the Youtube in your default browser...

                elif ("wikipedia" in query):
                    super().speak("Searching wikipedia")
                    output = wk.summary(query.replace("wikipedia", ""), sentences=3)  # Searching the query in wikipedia...
                    VoiceA = tkinter.LabelFrame(Frame2,text="VoiceA",bg="yellow",
                                                font=("Times New Roman", 13))
                    VoiceA.pack(pady=10)
                    msg = tkinter.Label(VoiceA, wraplength=220, width=40, text=output, bg="white")
                    msg.pack()
                    super().speak("You can read the answer for your query in the chat box...")

                elif (("change" in query) and ("voice" in query)):          # Change the voice of assistant...
                    global current_voice
                    if current_voice == 1:
                        engine.setProperty('voice', speech_voices[0].id)
                        current_voice = 0
                    else:
                        engine.setProperty('voice', speech_voices[1].id)
                        current_voice = 1
                    super().speak("I have changed my voice")

                elif (("play" in query) and (("songs" in query) or ("song" in query) or ("music" in query))):
                    super().speak("Playing Music...")
                    key = random.choice(range(1, 101))              # Choosing some random index...
                    wb.open("https://music.youtube.com/watch?v=" + self.data[key])   # Playing music from YTmusic...

                elif ("search" in query):
                    if ("file" in query):                           # Searching files in the system...
                        self.filesFound.clear()
                        opening_path = os.path.join(r"C:", "\\")    # Setting the base path...
                        super().speak("Could you repeat the file name with its extension?")
                        search = str(super().listen_from_user())    
                        if search!=None:
                            search = search.replace("dot", ".")
                            search = search.replace(" ", "")
                            super().speak("Searching " + str(search) + " file")
                            self.find_file(opening_path, search)       # Calling the function to search a file...
                            fileList = len(self.filesFound)
                            if fileList == 0:
                                super().speak("Not files found!!")
                            else:
                                if fileList == 1:
                                    super().speak("According to the search, below file is found : ")
                                else:
                                    super().speak("According to the search, below file are found : ")

                                FF = tkinter.LabelFrame(Frame2, text="Me", bg="yellow")
                                FF.pack(pady=10)
                                files_found=""
                                for f in self.filesFound:
                                    files_found+=f+"\n"
                                    print(f)
                                msg = tkinter.Label(FF, wraplength=220, width=40, text=files_found)
                                msg.pack()
                        else:
                            super().speak("Sorry, I haven't understood the filename...\nExiting the search command")
                    else:
                        super().speak("Opening google search...")
                        if query == "open google search":
                            wb.open("https://www.google.com/")                          # Opening google.com
                        else:
                            wb.open("https://www.google.com/search?q="+query.replace("search", "")) 
                            super().speak("Here are some results found...")
                            
                elif ("open email" in query) or ("open gmail" in query):
                    super().speak("Opening E-mail...")
                    wb.open("https://mail.google.com")                                  # Opening Gmail...
                
                elif (("compose" in query) or ("write" in query)) and ("email" in query):
                    super().speak("Opening E-mail...")
                    wb.open("https://mail.google.com/mail/u/0/#inbox?compose=new")      # Composing a new e-mail...

                elif ("note down" in query) or (("take" in query) and ("note" in query)) or ("open notepad" in query):  # Taking a note...
                    super().speak("Started taking note...")
                    note = super().listen_from_user()
                    NOTED = tkinter.LabelFrame(Frame2, text="Me", bg="yellow")
                    NOTED.pack(pady=10)
                    msg = tkinter.Label(NOTED, wraplength=220, width=40, text=note)
                    msg.pack()
                    print("\n\n", str(note))
                    filename = str(tt.strftime("%x_%I%M%S"))
                    filename = filename.replace("/", "") + ".txt"     # Filename is of date_time.txt... 
                    # print(filename)
                    fpNew = open(filename, "w")                       # Creating the new file...
                    fpNew.write(note)                                 # Writing the note which user said...
                    fpNew.close()                                     # Close the file...
                    super().speak("Note completed...")

                elif ("open calculator" in query):                    # Opening calculator...
                    super().speak("Opening calculator...")
                    wb.open("simple_calculator.exe")

                elif ("activate sleep mode" in query) or ("go to sleep mode" in query):     # Activating sleep mode...
                    super().speak("Sleep mode activated!")
                    tt.sleep(3 * 60)

                else:                       
                    try:
                        result = client.query(query)             # Searching the query in Wolfram alpha...
                        output = next(result.results).text
                        super().speak(output)
                    except StopIteration:
                        super().speak("Data not available right now!!")     
                    except:
                        super().speak("Sorry, I haven't understood what you said. Could you repeat?")

            except:
                cont += 1               # Incrementing the count if no query is heared from user...
                if cont % 2 == 0:       # The assistant listens atmost two times, after no query from user...
                    break               # If no query got from user at second time, exit the loop...
                pass

############################################################################################################################



############################################### Starting the Application ###################################################

class startProgram(FACE_RECOGNITION,VOICE_ASSISTANT):   # Inherits the properties from face_recognition class & voice_assistant class...
    
    """
        This class contains the functions which is required to start the application,
        initializes all the required methods, and running the functions parallely.
    """
    
    def __init__(self):
        FACE_RECOGNITION.__init__(self)
        VOICE_ASSISTANT.__init__(self)

    def startThreadFR(self):                                       # Starting the face-recognition in a new thread...
        
        """
            This function starts the face-recognition function in a new thread and 
            recognizes the user face.
        """
        
        task1 = threading.Thread(target=FACE_RECOGNITION.startFR,
                                 args=(self,),daemon=True)
        task1.start()
        
    def startThreadVA(self):                                        # Starting the voice-assistant in a new thread...
        
        """
            This function starts the voice assistant function in a new thread and
            interacts with the user.
        """
        
        task2 = threading.Thread(target=VOICE_ASSISTANT.startVA,
                                 args=(self,),daemon=True)
        task2.start()

    def WISH(self):
        
        """
            This function is used to wish the user when the assistant wakes up.
        """
        
        timeNow = tt.strftime("%I:%p")
        timeNow = timeNow.split(":")
        timeNow[0] = int(timeNow[0])
        wish = ""
        if timeNow[1] == "AM":
            wish = "Good Morning, "
        elif (timeNow[0] == 12 or 1 <= timeNow[0] < 4) and timeNow[1] == "PM":
            wish = "Good Afternoon, "
        elif (4 <= timeNow[0] < 8) and timeNow[1] == "PM":
            wish = "Good Evening, "
        super().speak(wish + "This is VoiceA")
        
############################################################################################################################



########################################### GRAPHICAL USER INTERFACE (GUI) ###########################################

"""
    The tkinter module is used to create user interfaces, which contains
    labels, frames, buttons, etc.
"""

root = tkinter.Tk()                                      # Creating a root window...
root.title("Voice Assistant")                            # Giving title for the window...

sw = root.winfo_screenwidth()                            # Fetching the screen-width
sh = root.winfo_screenheight()                           # Fetching the screen-height
ww = 650                                                 # Initializing the window width
wh = 650                                                 # Initializing the window height

posX=(sw-ww)//2                                          # Positioning the window
posY=(sh-wh)//2                                          # Positioning the window

root.geometry(f"{680}x{670}+{posX}+{posY}")              # Setting the window parameters...
root.resizable(width="0",height="0")                     # Window cannot be resized
root.configure(bg="#262050",padx=12,pady=12)             # Initializing the background...
root.iconbitmap("va_icon.ico")                           # Giving the icon for the Application...


################################### Displaying the TIME ###################################

timeL = tkinter.Label(root,bg="#262050",font=("Times New Roman",22),foreground="white")
timeL.place(x=posX,y=posY-98)

def Tstart():
    """ This function displays the time interface. """
    timeL["text"] = tt.strftime("%I:%M:%S %p")
    timeL.after(1,Tstart)
Tstart()

############################################################################################

###########################################  CHAT BOX ######################################

chat_bg = tkinter.PhotoImage(file="chatBG.png")
chat_bckgd = tkinter.Label(root,image=chat_bg,width="345",height="620",border="5")
chat_bckgd.place(x=posX-435,y=posY-98)

LabelH = tkinter.Label(root,text="Chat Box",
                       fg="black",bg="white",
                       width="31",height="2",
                       font=("Times of Roman",15))

LabelH.place(x=posX-431,y=posY-86)

Frame1 = tkinter.Frame(root,width=445,height=555)
Frame1.place(x=posX-429,y=posY-26)

# Setting the scrollbar...
sb=tkinter.Scrollbar(Frame1,orient="vertical")
sb.pack(side="right",fill="y")

# creating the canvas frame for displaying all chats...
canvasFrame = tkinter.Canvas(Frame1,bg="#3e1c5c",
                             width=321,height=540,borderwidth=0,
                             yscrollcommand=sb.set)

canvasFrame.pack(side="left")
sb.config(command=canvasFrame.yview)


Frame2 = tkinter.Frame(canvasFrame,bg="#3e1c5c",bd=0)
Frame2.bind("<Configure>",
            lambda e: canvasFrame.configure(scrollregion=canvasFrame.bbox("all")))

canvasFrame.create_window((0,0),window=Frame2,anchor="nw")

# Indication to "swipe up" for latest chats...
tkinter.Label(Frame2,bg="#3e1c5c",fg="white",
              width=35,font=("Times New Roman",12),
              text="Swipe up \u2191 for latest chats").pack()

############################################################################################


################################ Displaying the camera frames in GUI #######################

capL = tkinter.Label(root,bg="#262050",width=280,height=300)
capL.place(x=posX-70,y=posY-50)

############################################################################################


############################ Microphone ON/OFF identification in GUI #######################

mic_bg = tkinter.PhotoImage(file="microphone.png")
mic_rm = tkinter.PhotoImage(file="rm_mic.png")

microphone = tkinter.Label(root,bg="#262050",width=22,height=28)
microphone.place(x=posX+190,y=posY+505)

############################################################################################


################################### Sound Waves Animation in GUI ###########################

listenAnimateL = tkinter.Label(root,bg="#262050",padx=0,pady=0,
                               font=("Times New Roman",43),
                               foreground="white")

listenAnimateL.place(x=posX-65,y=posY+415)

listenAnimateR = tkinter.Label(root,bg="#262050",padx=0,pady=0,
                               font=("Times New Roman",43),
                               foreground="white")

listenAnimateR.place(x=posX+125,y=posY+415)

# Declaring the Global varaible dots for animation...
dots = 1
# Calling the listenAnimation function, to put the animation live in GUI...
def listenAnimation():
    """
        This function creates the animation of sound wave.
    """ 
    global dots
    showDot = "~|" * (dots % 3)                 # Wave pattern for animation...
    listenAnimateL["text"] = showDot
    listenAnimateR["text"] = showDot
    dots += 1
    if dots > 3:
        dots = 1
    root.after(180, listenAnimation)
listenAnimation()

############################################################################################


####################################### Camera Frames in GUI ###############################

capview = None
def capShow():                 # Button to show actual Opencv Face-recognition window...
    """ This function is used to show the OpenCV window. """
    global capview
    capview = True
def capStop():                 # Button to destroy actual Opencv Face-recognition window...
    """ This function is used to stop the OpenCV window. """
    global capview             
    capview = False

startCV = tkinter.Button(root,bg="white",bd=5,
                         text="Start OpenCV window",
                         font=("Times New Roman",15),
                         padx=4,foreground="black",
                         command=capShow)

startCV.place(x=posX-31,y=posY+270)

stopCV = tkinter.Button(root,bg="white",bd=4,
                        text="Stop OpenCV window",
                        font=("Times New Roman",15),
                        padx=5,foreground="black",
                        command=capStop)

stopCV.place(x=posX-31,y=posY+330)

############################################################################################


################################## Microphone Button #######################################

voice_assist=tkinter.PhotoImage(file="voice_assist.png")
clickVA = tkinter.Button(root,image=voice_assist,borderwidth=0,border=0)
clickVA.place(x=f"{ww-185}",y=f"{wh-140}",width="100",height="98")

############################################################################################

startP = startProgram()   # Creating the object & invoking the constructor of 'startProgram' class...
startP.startThreadFR()    # Invoking the face-recognition function...
startP.startThreadVA()    # Invoking the voice-assistant...
threading.Thread(target=startP.WISH).start()

clickVA.configure(command=startP.startThreadVA)     # Button to activate microphone for speech recognition...

# Running the tkinter window in the infinite loop...
root.mainloop()

"""
Storing the complete chat after closing the application.
"""

chatHistory[chats] = chatPerson                       # Created a dictionary with key = chats and value = persons involved... 
with open("chatHistory.pickle","ab") as historyDB:
    pickle.dump(chatHistory,historyDB)                # Dumping the data in a pickle file...
historyDB.close()
