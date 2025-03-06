import streamlit as st
import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# Initialize text-to-speech engine globally
engine = None

# Function to initialize the pyttsx3 engine
def init_engine():
    global engine
    if engine is None:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Optional: Adjust speech rate

# Function to convert text to speech
def speak(text):
    init_engine()  # Ensure the engine is initialized
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Stop the engine after speaking

# Function to capture voice input using sounddevice
def get_audio_input():
    fs = 44100  # Sample rate
    duration = 5  # Duration in seconds
    st.write("Listening... Speak now!")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype=np.int16)
    sd.wait()  # Wait until the recording is finished
    write("output.wav", fs, recording)  # Save as WAV file

    # Use speech_recognition to process the saved audio file
    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            st.write("Sorry, there was an issue with the speech recognition service.")
            return None

# Unit mapping for normalization
unit_mapping = {
    "kilometre": "Kilometers",
    "kilometer": "Kilometers",
    "metre": "Meters",
    "meter": "Meters",
    "foot": "Feet",
    "mile": "Miles",
    "kg": "Kilograms",
    "gram": "Grams",
    "pound": "Pounds",
    "ounce": "Ounces",
    "celsius": "Celsius",
    "fahrenheit": "Fahrenheit",
    "kelvin": "Kelvin",
    "hectare": "Hectares",
    "acre": "Acres",
    "liter": "Liters",
    "litre": "Liters",
    "milliliter": "Milliliters",
    "gallon": "Gallons"
}

def normalize_unit(unit_name):
    return unit_mapping.get(unit_name.lower(), unit_name.title())

# Title of the app
st.title("Smart & Quick Voice-Controlled Converter")

# Sidebar configuration
st.sidebar.title("SQ Converter")  # Sidebar name
st.sidebar.markdown("### About")
st.sidebar.write(
    """
    **SQ Converter** is a voice-enabled unit conversion tool that allows you to convert between different units of measurement. 
    You can use voice commands to select units, input values, and get results. 
    Supported categories include Length, Weight, Temperature, Area, and Volume.
    """
)

# Sidebar for enabling voice
voice_enabled = st.sidebar.checkbox("Enable Voice")

# Sidebar for unit categories
unit_category = st.sidebar.selectbox(
    "Select Unit Category",
    ["Length", "Weight", "Temperature", "Area", "Volume"]
)

# If voice is enabled, use voice input
if voice_enabled:
    speak("Which converter do you want to use?")
    st.write("Which converter do you want to use?")
    voice_input = get_audio_input()
    if voice_input:
        unit_category = voice_input.title()  # Normalize to match expected category names
        speak(f"You selected {unit_category}.")
        st.write(f"You selected {unit_category}.")

# Conversion logic based on selected category
if unit_category in ["Length", "Weight", "Temperature", "Area", "Volume"]:  # Validate category
    st.header(f"{unit_category} Converter")  # Dynamic header based on selected category
    if unit_category == "Length":
        units = ["Meters", "Kilometers", "Feet", "Miles"]
    elif unit_category == "Weight":
        units = ["Kilograms", "Grams", "Pounds", "Ounces"]
    elif unit_category == "Temperature":
        units = ["Celsius", "Fahrenheit", "Kelvin"]
    elif unit_category == "Area":
        units = ["Square Meters", "Hectares", "Acres"]
    elif unit_category == "Volume":
        units = ["Liters", "Milliliters", "Cubic Meters", "Gallons"]
    else:
        units = []  # Default to empty if category is not recognized
    
    # Initialize from_unit and to_unit
    from_unit = None
    to_unit = None
    
    if voice_enabled:
        speak("Which unit do you want to convert from?")
        st.write("Which unit do you want to convert from?")
        from_unit_voice = get_audio_input()
        if from_unit_voice:
            from_unit = normalize_unit(from_unit_voice)  # Normalize the unit name
            if from_unit in units:  # Check if the unit is valid
                speak(f"You selected {from_unit}.")
                st.write(f"You selected {from_unit}.")
            else:
                st.write("Invalid unit. Please try again.")
                from_unit = None
        else:
            st.write("Voice input failed. Please select the unit manually.")
            from_unit = st.selectbox("From", units)

        speak("Which unit do you want to convert to?")
        st.write("Which unit do you want to convert to?")
        to_unit_voice = get_audio_input()
        if to_unit_voice:
            to_unit = normalize_unit(to_unit_voice)  # Normalize the unit name
            if to_unit in units:  # Check if the unit is valid
                speak(f"You selected {to_unit}.")
                st.write(f"You selected {to_unit}.")
            else:
                st.write("Invalid unit. Please try again.")
                to_unit = None
        else:
            st.write("Voice input failed. Please select the unit manually.")
            to_unit = st.selectbox("To", units)
    else:
        from_unit = st.selectbox("From", units)
        to_unit = st.selectbox("To", units)

    if voice_enabled:
        speak("Please say the value you want to convert.")
        st.write("Please say the value you want to convert.")
        value_voice = get_audio_input()
        if value_voice:
            try:
                value = float(value_voice)  # Convert the voice input to a float
            except ValueError:
                st.write("Invalid value. Please enter a number.")
                value = st.number_input("Enter value for conversion", value=1.0)  # Fallback to manual input
        else:
            value = st.number_input("Enter value for conversion", value=1.0)  # Fallback to manual input
    else:
        value = st.number_input("Enter value for conversion", value=1.0)  # Manual input if voice is not enabled

    result = None  # Initialize result
    # Conversion logic based on selected category
    if unit_category == "Length":
        # Conversion logic for length
        if from_unit == "Meters":
            if to_unit == "Kilometers":
                result = value / 1000
            elif to_unit == "Feet":
                result = value * 3.28084
            elif to_unit == "Miles":
                result = value * 0.000621371
            else:
                result = value
        elif from_unit == "Kilometers":
            if to_unit == "Meters":
                result = value * 1000
            elif to_unit == "Feet":
                result = value * 3280.84
            elif to_unit == "Miles":
                result = value * 0.621371
            else:
                result = value
        elif from_unit == "Feet":
            if to_unit == "Meters":
                result = value / 3.28084
            elif to_unit == "Kilometers":
                result = value / 3280.84
            elif to_unit == "Miles":
                result = value * 0.000189394
            else:
                result = value
        elif from_unit == "Miles":
            if to_unit == "Meters":
                result = value * 1609.34
            elif to_unit == "Kilometers":
                result = value * 1.60934
            elif to_unit == "Feet":
                result = value * 5280
            else:
                result = value
    elif unit_category == "Weight":
        # Conversion logic for weight
        if from_unit == "Kilograms":
            if to_unit == "Grams":
                result = value * 1000
            elif to_unit == "Pounds":
                result = value * 2.20462
            elif to_unit == "Ounces":
                result = value * 35.274
            else:
                result = value
        elif from_unit == "Grams":
            if to_unit == "Kilograms":
                result = value / 1000
            elif to_unit == "Pounds":
                result = value * 0.00220462
            elif to_unit == "Ounces":
                result = value * 0.035274
            else:
                result = value
        elif from_unit == "Pounds":
            if to_unit == "Kilograms":
                result = value * 0.453592
            elif to_unit == "Grams":
                result = value * 453.592
            elif to_unit == "Ounces":
                result = value * 16
            else:
                result = value
        elif from_unit == "Ounces":
            if to_unit == "Kilograms":
                result = value * 0.0283495
            elif to_unit == "Grams":
                result = value * 28.3495
            elif to_unit == "Pounds":
                result = value * 0.0625
            else:
                result = value
    elif unit_category == "Temperature":
        # Conversion logic for temperature
        if from_unit == "Celsius":
            if to_unit == "Fahrenheit":
                result = (value * 9/5) + 32
            elif to_unit == "Kelvin":
                result = value + 273.15
            else:
                result = value
        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                result = (value - 32) * 5/9
            elif to_unit == "Kelvin":
                result = (value - 32) * 5/9 + 273.15
            else:
                result = value
        elif from_unit == "Kelvin":
            if to_unit == "Celsius":
                result = value - 273.15
            elif to_unit == "Fahrenheit":
                result = (value - 273.15) * 9/5 + 32
            else:
                result = value
    elif unit_category == "Area":
        # Conversion logic for area (example)
        if from_unit == "Square Meters":
            if to_unit == "Hectares":
                result = value / 10000
            elif to_unit == "Acres":
                result = value * 0.000247105
            else:
                result = value
        elif from_unit == "Hectares":
            if to_unit == "Square Meters":
                result = value * 10000
            elif to_unit == "Acres":
                result = value * 2.47105
            else:
                result = value
        elif from_unit == "Acres":
            if to_unit == "Square Meters":
                result = value / 0.000247105
            elif to_unit == "Hectares":
                result = value / 2.47105
            else:
                result = value
    elif unit_category == "Volume":
        # Conversion logic for volume (example)
        if from_unit == "Liters":
            if to_unit == "Milliliters":
                result = value * 1000
            elif to_unit == "Cubic Meters":
                result = value / 1000
            elif to_unit == "Gallons":
                result = value * 0.264172
            else:
                result = value
        elif from_unit == "Milliliters":
            if to_unit == "Liters":
                result = value / 1000
            elif to_unit == "Cubic Meters":
                result = value / 1000000
            elif to_unit == "Gallons":
                result = value * 0.000264172
            else:
                result = value
        elif from_unit == "Cubic Meters":
            if to_unit == "Liters":
                result = value * 1000
            elif to_unit == "Milliliters":
                result = value * 1000000
            elif to_unit == "Gallons":
                result = value * 264.172
            else:
                result = value
        elif from_unit == "Gallons":
            if to_unit == "Liters":
                result = value / 0.264172
            elif to_unit == "Milliliters":
                result = value / 0.000264172
            elif to_unit == "Cubic Meters":
                result = value / 264.172
            else:
                result = value

    if result is not None and value > 0:  # Check if result is valid and value is positive
        st.success(f"Result: {result} {to_unit}")
        if voice_enabled:
            speak(f"The result is {result} {to_unit}")
    else:
        st.error("Conversion failed. Please check your inputs.")

else:
    st.write("Select a unit category to start converting.")













# import streamlit as st
# import speech_recognition as sr
# import pyttsx3
# import sounddevice as sd
# import numpy as np
# from scipy.io.wavfile import write

# # Initialize text-to-speech engine globally
# engine = None

# # Function to initialize the pyttsx3 engine
# def init_engine():
#     global engine
#     if engine is None:
#         engine = pyttsx3.init()
#         engine.setProperty('rate', 150)  # Optional: Adjust speech rate

# # Function to convert text to speech
# def speak(text):
#     init_engine()  # Ensure the engine is initialized
#     engine.say(text)
#     engine.runAndWait()
#     engine.stop()  # Stop the engine after speaking

# # Function to capture voice input using sounddevice
# def get_audio_input():
#     fs = 44100  # Sample rate
#     duration = 5  # Duration in seconds
#     st.write("Listening... Speak now!")
#     recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype=np.int16)
#     sd.wait()  # Wait until the recording is finished
#     write("output.wav", fs, recording)  # Save as WAV file

#     # Use speech_recognition to process the saved audio file
#     recognizer = sr.Recognizer()
#     with sr.AudioFile("output.wav") as source:
#         audio = recognizer.record(source)
#         try:
#             text = recognizer.recognize_google(audio)
#             st.write(f"You said: {text}")
#             return text
#         except sr.UnknownValueError:
#             st.write("Sorry, I could not understand the audio.")
#             return None
#         except sr.RequestError:
#             st.write("Sorry, there was an issue with the speech recognition service.")
#             return None

# # Unit mapping for normalization
# unit_mapping = {
#     "kilometre": "Kilometers",
#     "kilometer": "Kilometers",
#     "metre": "Meters",
#     "meter": "Meters",
#     "foot": "Feet",
#     "mile": "Miles",
#     "kg": "Kilograms",
#     "gram": "Grams",
#     "pound": "Pounds",
#     "ounce": "Ounces",
#     "celsius": "Celsius",
#     "fahrenheit": "Fahrenheit",
#     "kelvin": "Kelvin",
#     "hectare": "Hectares",
#     "acre": "Acres",
#     "liter": "Liters",
#     "litre": "Liters",
#     "milliliter": "Milliliters",
#     "gallon": "Gallons"
# }

# def normalize_unit(unit_name):
#     return unit_mapping.get(unit_name.lower(), unit_name.title())

# # Title of the app
# st.title("Smart & Quick Voice-Controlled Converter")

# # Sidebar for enabling voice
# voice_enabled = st.sidebar.checkbox("Enable Voice")

# # Sidebar for unit categories
# unit_category = st.sidebar.selectbox(
#     "Select Unit Category",
#     ["Length", "Weight", "Temperature", "Area", "Volume"]
# )

# # If voice is enabled, use voice input
# if voice_enabled:
#     speak("Which converter do you want to use?")
#     st.write("Which converter do you want to use?")
#     voice_input = get_audio_input()
#     if voice_input:
#         unit_category = voice_input.title()  # Normalize to match expected category names
#         speak(f"You selected {unit_category}.")
#         st.write(f"You selected {unit_category}.")

# # Conversion logic based on selected category
# if unit_category in ["Length", "Weight", "Temperature", "Area", "Volume"]:  # Validate category
#     st.header(f"{unit_category} Converter")  # Dynamic header based on selected category
#     if unit_category == "Length":
#         units = ["Meters", "Kilometers", "Feet", "Miles"]
#     elif unit_category == "Weight":
#         units = ["Kilograms", "Grams", "Pounds", "Ounces"]
#     elif unit_category == "Temperature":
#         units = ["Celsius", "Fahrenheit", "Kelvin"]
#     elif unit_category == "Area":
#         units = ["Square Meters", "Hectares", "Acres"]
#     elif unit_category == "Volume":
#         units = ["Liters", "Milliliters", "Cubic Meters", "Gallons"]
#     else:
#         units = []  # Default to empty if category is not recognized
    
#     # Initialize from_unit and to_unit
#     from_unit = None
#     to_unit = None
    
#     if voice_enabled:
#         speak("Which unit do you want to convert from?")
#         st.write("Which unit do you want to convert from?")
#         from_unit_voice = get_audio_input()
#         if from_unit_voice:
#             from_unit = normalize_unit(from_unit_voice)  # Normalize the unit name
#             if from_unit in units:  # Check if the unit is valid
#                 speak(f"You selected {from_unit}.")
#                 st.write(f"You selected {from_unit}.")
#             else:
#                 st.write("Invalid unit. Please try again.")
#                 from_unit = None
#         else:
#             st.write("Voice input failed. Please select the unit manually.")
#             from_unit = st.selectbox("From", units)

#         speak("Which unit do you want to convert to?")
#         st.write("Which unit do you want to convert to?")
#         to_unit_voice = get_audio_input()
#         if to_unit_voice:
#             to_unit = normalize_unit(to_unit_voice)  # Normalize the unit name
#             if to_unit in units:  # Check if the unit is valid
#                 speak(f"You selected {to_unit}.")
#                 st.write(f"You selected {to_unit}.")
#             else:
#                 st.write("Invalid unit. Please try again.")
#                 to_unit = None
#         else:
#             st.write("Voice input failed. Please select the unit manually.")
#             to_unit = st.selectbox("To", units)
#     else:
#         from_unit = st.selectbox("From", units)
#         to_unit = st.selectbox("To", units)

#     if voice_enabled:
#         speak("Please say the value you want to convert.")
#         st.write("Please say the value you want to convert.")
#         value_voice = get_audio_input()
#         if value_voice:
#             try:
#                 value = float(value_voice)  # Convert the voice input to a float
#             except ValueError:
#                 st.write("Invalid value. Please enter a number.")
#                 value = st.number_input("Enter value for conversion", value=1.0)  # Fallback to manual input
#         else:
#             value = st.number_input("Enter value for conversion", value=1.0)  # Fallback to manual input
#     else:
#         value = st.number_input("Enter value for conversion", value=1.0)  # Manual input if voice is not enabled

#     result = None  # Initialize result
#     # Conversion logic based on selected category
#     if unit_category == "Length":
#         # Conversion logic for length
#         if from_unit == "Meters":
#             if to_unit == "Kilometers":
#                 result = value / 1000
#             elif to_unit == "Feet":
#                 result = value * 3.28084
#             elif to_unit == "Miles":
#                 result = value * 0.000621371
#             else:
#                 result = value
#         elif from_unit == "Kilometers":
#             if to_unit == "Meters":
#                 result = value * 1000
#             elif to_unit == "Feet":
#                 result = value * 3280.84
#             elif to_unit == "Miles":
#                 result = value * 0.621371
#             else:
#                 result = value
#         elif from_unit == "Feet":
#             if to_unit == "Meters":
#                 result = value / 3.28084
#             elif to_unit == "Kilometers":
#                 result = value / 3280.84
#             elif to_unit == "Miles":
#                 result = value * 0.000189394
#             else:
#                 result = value
#         elif from_unit == "Miles":
#             if to_unit == "Meters":
#                 result = value * 1609.34
#             elif to_unit == "Kilometers":
#                 result = value * 1.60934
#             elif to_unit == "Feet":
#                 result = value * 5280
#             else:
#                 result = value
#     elif unit_category == "Weight":
#         # Conversion logic for weight
#         if from_unit == "Kilograms":
#             if to_unit == "Grams":
#                 result = value * 1000
#             elif to_unit == "Pounds":
#                 result = value * 2.20462
#             elif to_unit == "Ounces":
#                 result = value * 35.274
#             else:
#                 result = value
#         elif from_unit == "Grams":
#             if to_unit == "Kilograms":
#                 result = value / 1000
#             elif to_unit == "Pounds":
#                 result = value * 0.00220462
#             elif to_unit == "Ounces":
#                 result = value * 0.035274
#             else:
#                 result = value
#         elif from_unit == "Pounds":
#             if to_unit == "Kilograms":
#                 result = value * 0.453592
#             elif to_unit == "Grams":
#                 result = value * 453.592
#             elif to_unit == "Ounces":
#                 result = value * 16
#             else:
#                 result = value
#         elif from_unit == "Ounces":
#             if to_unit == "Kilograms":
#                 result = value * 0.0283495
#             elif to_unit == "Grams":
#                 result = value * 28.3495
#             elif to_unit == "Pounds":
#                 result = value * 0.0625
#             else:
#                 result = value
#     elif unit_category == "Temperature":
#         # Conversion logic for temperature
#         if from_unit == "Celsius":
#             if to_unit == "Fahrenheit":
#                 result = (value * 9/5) + 32
#             elif to_unit == "Kelvin":
#                 result = value + 273.15
#             else:
#                 result = value
#         elif from_unit == "Fahrenheit":
#             if to_unit == "Celsius":
#                 result = (value - 32) * 5/9
#             elif to_unit == "Kelvin":
#                 result = (value - 32) * 5/9 + 273.15
#             else:
#                 result = value
#         elif from_unit == "Kelvin":
#             if to_unit == "Celsius":
#                 result = value - 273.15
#             elif to_unit == "Fahrenheit":
#                 result = (value - 273.15) * 9/5 + 32
#             else:
#                 result = value
#     elif unit_category == "Area":
#         # Conversion logic for area (example)
#         if from_unit == "Square Meters":
#             if to_unit == "Hectares":
#                 result = value / 10000
#             elif to_unit == "Acres":
#                 result = value * 0.000247105
#             else:
#                 result = value
#         elif from_unit == "Hectares":
#             if to_unit == "Square Meters":
#                 result = value * 10000
#             elif to_unit == "Acres":
#                 result = value * 2.47105
#             else:
#                 result = value
#         elif from_unit == "Acres":
#             if to_unit == "Square Meters":
#                 result = value / 0.000247105
#             elif to_unit == "Hectares":
#                 result = value / 2.47105
#             else:
#                 result = value
#     elif unit_category == "Volume":
#         # Conversion logic for volume (example)
#         if from_unit == "Liters":
#             if to_unit == "Milliliters":
#                 result = value * 1000
#             elif to_unit == "Cubic Meters":
#                 result = value / 1000
#             elif to_unit == "Gallons":
#                 result = value * 0.264172
#             else:
#                 result = value
#         elif from_unit == "Milliliters":
#             if to_unit == "Liters":
#                 result = value / 1000
#             elif to_unit == "Cubic Meters":
#                 result = value / 1000000
#             elif to_unit == "Gallons":
#                 result = value * 0.000264172
#             else:
#                 result = value
#         elif from_unit == "Cubic Meters":
#             if to_unit == "Liters":
#                 result = value * 1000
#             elif to_unit == "Milliliters":
#                 result = value * 1000000
#             elif to_unit == "Gallons":
#                 result = value * 264.172
#             else:
#                 result = value
#         elif from_unit == "Gallons":
#             if to_unit == "Liters":
#                 result = value / 0.264172
#             elif to_unit == "Milliliters":
#                 result = value / 0.000264172
#             elif to_unit == "Cubic Meters":
#                 result = value / 264.172
#             else:
#                 result = value

#     if result is not None and value > 0:  # Check if result is valid and value is positive
#         st.success(f"Result: {result} {to_unit}")
#         if voice_enabled:
#             speak(f"The result is {result} {to_unit}")
#     else:
#         st.error("Conversion failed. Please check your inputs.")

# else:
#     st.write("Select a unit category to start converting.")