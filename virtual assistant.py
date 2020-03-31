import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import wikipedia
import calendar
import random


# ignore all the warnigs that come
warnings.filterwarnings('ignore')
# Record audio and return it as astring
def recordAudio():
    # Record the audio
    
    r = sr.Recognizer()#Creating a recognizer

    #open micrphone and start recording
    with sr.Microphone() as source:
        print('Say something?')
        audio = r.listen(source)

    # Use google speech recognition
    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: '+data)
    except sr.UnknownValueError:#Check unknown errors
        print('Google Speech Recognition could not understand the audio , unknown error')
    except sr.RequestError as e:
        print('Request result from google Speech Recognition service error '+e)
    
    return data

#recordAudio()

# A function to get the virtual assistant response
def assistantresponse(text):
    print(text)
    #convert text to speech
    myobj = gTTS(text= text, lang='en', slow=False)

    #Save the converted audio to a file
    myobj.save('assistant_response.mp3')

    #play the converted file
    os.system("parole assistant_response.mp3")

#text = input(str)
#assistantresponse(text)

# A function for the wake word or phrase
def wakeWord(text):
    WAKE_WORDS = ['smoke', 'root']# A list of wake words

    text = text.lower() # this is converting the text to all lower case words

    # Check to see if the users command/text contains a wake word/phrase
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    # If wake word is not found in the text from the loop so it returns false

    return False

# A function to get the current date

def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]# e.g friday
    monthNumber = now.month
    dayNumber =  now.day
    # A list of months
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # A list of ordinal numbers
    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']


    return 'Today is '+weekday+' '+ month_names[monthNumber - 1]+' the '+ ordinalNumbers[dayNumber - 1]+ '. '
 

# A function to return a random greeting response
def greeting(text):
    # greeting input
    GREETING_INPUTS = ['Hi', 'Hey', 'Holla', 'Greetings', 'wassup']

    # Greeting responses
    GREETING_RESPONSES = ['howdy', 'hello', 'hey there', 'whats good']

    #If the users input is a greeting, then return a randomy chosen greeting
    for word in text.split():
        if word.lower():
            return random.choice(GREETING_RESPONSES)+ '.'



    # If no greeting was detected then return an empty string
    return ''

# A function to get the person first and last name from the text
def getPerson(text):
    wordList = text.split()# splitting the text into a list of words

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and  wordList[1].lower() == 'who' and wordList[i+1].lower() == 'is':
            return wordList[i+2]+ ' '+ wordList[i+3]

while True:
    #record the audio
    text = recordAudio()
    response = ''
    # Ceck for the wake word/phrase
    if (wakeWord(text)) == True:
        # Check for the greetings from the user
        response = response + greeting(text)

        # Check if user said anything to do with time
        if('time' in text):
            now = datetime.datetime.now()
            midday = ''
            if now.hour >=12:
                midday = 'pm'# this is after midday
                hour = now.hour - 12
            else:
                midday = 'a.m' # after midnight
                hour = now.hour

            if now.minute< 10:
                  minute = '0'+str(now.minute)# this is to ensure that all the numbers below ten have the 0 infront of them
            else:
                minute = str(now.minute)
            response =  response +''+'It is'+str(hour)+ ':'+minute+ ' '+midday+'.'

        # check to see if the user daid anything to do with the date
        if('date' in text):
            get_date = getDate()
            response = response + ' '+ get_date 
        

        #Check if the user said 'who is'
        if('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)
            response = response +' '+ wiki

        # Have the assistant respond back using audio and text from response 
        assistantresponse(response)