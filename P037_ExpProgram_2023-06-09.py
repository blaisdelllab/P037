#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 13:35:04 2023

@author: cyruskirkman and Marco Vasconcelos

This is the main code for Dr. Marco Vasconcelos's P037 suboptimal choice task 
with a reject-key option that was run in the spring of 2023 when he was on 
sabbatical at UCLA. The experiment had two main session types:
    
    1)  Instrumental pre-training: one of the seven stimuli were randomly
        activated at the beginning of each trial. After a peck on the filled
        stimulus (FR1),a reinforcer was immediately provided. Fill colors were
        varied based on their position on the screen
        
    2)  Match to sample: The next phase was the main experimental condition in
        this experiment. Sessions consisted of 100 trials (which were split into
        two blocks of 50 trials). Each block was split into the following trial
        types, which were semi-randomly dispersed within each block such that
        no more than three trials of the same tye occured consecutively:
            
            a) 20 forced-choice trials - 10 trials with the informative option
                only and 10 with the non-informative option only
            b) 20 rejection trials - 10 with the informative option and the
                rejection key and 10 with the non-informative option and the
                rejection key
            c) 10 free-choice trials (with both the informative and non-
                informative options available). 
                                      
       Within each of these trial types, pigeons had one (ForcedC) or two
       (rejection, FreeC) choices available. The informative and the non-
       informative options were always presented on the same side, but side
       allocation was counterbalanced across pigeons. During the FreeC trials,
       both the two side keys were lit in white, starting the initial links. If
       the pigeon pecked the Informative key, the Non-informative key was
       turned off and vice versa.
       
           a) Informative choice - the S- is turned on 80% of the occasions.
               Ten seconds after, the S- is turned off and a 10-s ITI follows.
               Pecks during the terminal links are recorded but have no
               programmed consequence. On the remaining 20% of these trials,
               the S+ is turned on for 10 s, food is delivered immediately
               after, and the ITI follows.
           b) Non-informative choice - on 20% of the trials one terminal
               stimulus (e.g., yellow) is turned on; on the remaining 80% of
               the trials, the other terminal stimulus (e.g., blue) is turned
               on. In both non-informative terminal links, the key remains lit
               for 10 s, food is delivered on a randomly selected half of the
               trials, and the 10-s ITI follows. The terminal-link hues are
               counterbalanced across pigeons, with the restriction that red
               and green are always associated with one option and yellow and
               blue are always associated with the other option. The reinforcer
               duration varies from bird to bird in order to avoid feeding
               outside the experimental chamber. Figure 1 shows the
               contingencies for each option.
           c) Rejection choice - rejection trials structurally similar to free-
               choice trials except that they involve a choice between one of
               the aforementioned options and the rejection key. If the pigeon
               chooses the available (optimal or suboptimal) option, the
               rejection key is turned off and the contingencies follow as
               usual. If the pigeon chooses the rejection key, both keys are
               turned off and the alternative option is lit on the other side
               of the screen (i.e., if the trial started with the informative
               option, it switches into the non-informative and vice-versa).
               The change to the other option on the other side of the screen
               occurs immediately (note that the options are not counterbalanced
               for side, one appears always on the left and the other on the
               right). If the experiment works, we may implement an FI on the
               rejection key. It starts as a FR1 but we can program immediately
               the possibility of an increasing FI.
               
       Training continued for at least 12 sessions depending on performance. If
       rejection develops for one of the options, we may increase the travel
       time (the work requirement in the rejection key) using a FI schedule.

"""

# The first variable declared is whether the program is the operant box version
# for pigeons, or the test version for humans to view. The variable below is 
# a T/F boolean that will be referenced many times throughout the program 
# when the two options differ (for example, when the Hopper is accessed or
# for onscreen text, etc.). It needs to be changed manually based on whether
# the program is running in operant boxes (True) or not (False).
operant_box_version = True

# Prior to running any code, its conventional to first import relevant 
# libraries for the entire script. These can range from python libraries (sys)
# or sublibraries (setrecursionlimit) that are downloaded to every computer
# along with python, or other files within this folder (like control_panel or 
# maestro).
from tkinter import Toplevel, Canvas, BOTH, TclError, Tk, Label, Button, \
    StringVar, OptionMenu, IntVar, Radiobutton, Entry
from datetime import datetime, timedelta, date
from time import time
from csv import writer, DictReader, QUOTE_MINIMAL
from os import getcwd, mkdir, path as os_path
from random import shuffle, uniform, choice
from sys import setrecursionlimit, path as sys_path

# Import hopper/other specific libraries from files on operant box computers
try:
    if operant_box_version:
        cwd = getcwd()
        sys_path.insert(0, str(os_path.expanduser('~')+"/OneDrive/Desktop/Hopper_Software"))
        import polygon_fill
        from hopper import HopperObject
except ModuleNotFoundError:
    print("ERROR :-( \n Cannot find the hopper software folder. \n Maybe a bird moved it? \n Check the trash and desktop folders and drag it to the desktop <3")
    input()

# Below  is just a safety measure to prevent too many recursive loops). It
# doesn't need to be changed.
setrecursionlimit(5000)

"""
The code below jumpstarts the loop by first building the hopper object and 
making sure everything is turned off, then passes that object to the
control_panel. The program is largely recursive and self-contained within each
object, and a macro-level overview is:
    
    ControlPanel -----------> MainScreen ------------> PaintProgram
         |                        |                         |
    Collects main           Runs the actual         Gets passed subject
    variables, passes      experiment, saves        name, but operates
    to Mainscreen          data when exited          independently
    

"""

# The first of two objects we declare is the ExperimentalControlPanel (CP). It
# exists "behind the scenes" throughout the entire session, and if it is exited,
# the session will terminate. The purpose of the control panel is to input 
# relevant information (like pigeon name) and select any variations to occur 
# within the upcoming session (sub/phase, FR, etc.)
class ExperimenterControlPanel(object):
    # The init function declares the inherent variables within that object
    # (meaning that they don't require any input).
    def __init__(self):
        # First, setup the data directory in "Documents"
        self.doc_directory = str(os_path.expanduser('~'))+"/Documents/"
        # Next up, we need to do a couple things that will be different based
        # on whether the program is being run in the operant boxes or on a 
        # personal computer. These include setting up the hopper object so it 
        # can be referenced in the future, or the location where data files
        # should be stored.
        if operant_box_version:
            # Setup the data directory in "Documents"
            self.doc_directory = str(os_path.expanduser('~'))+"/Documents/"
            self.data_folder = "P037_data" # The folder within Documents where subject data is kept
            self.data_folder_directory = str(os_path.expanduser('~'))+"/OneDrive/Desktop/Data/" + self.data_folder
        # Set hopper object to be a variable of self, so it can be referenced...
            self.Hopper = HopperObject()
        else: # If not, just save in the current directory the program us being run in 
            self.data_folder_directory = getcwd() + "/Data/"
            self.Hopper = None
        
        # setup the root Tkinter window
        self.control_window = Tk()
        self.control_window.title("P037 Control Panel")
        ##  Next, setup variables within the control panel:
        # Subject ID list (need to build/alphabetize) - TBD
        self.pigeon_name_list = ["Zappa", "Joplin", "Sting",
                                 "Jagger", "Iggy", "Evaristo",
                                 "Ozzy", "Kurt"]
        self.pigeon_name_list.sort() # This alphabetizes the list
        self.pigeon_name_list.insert(0, "TEST")
        # Subject ID menu and label
        Label(self.control_window, text="Pigeon Name:").pack()
        self.subject_ID_variable = StringVar(self.control_window)
        self.subject_ID_variable.set("Select")
        self.subject_ID_menu = OptionMenu(self.control_window,
                                          self.subject_ID_variable,
                                          *self.pigeon_name_list,
                                          command=self.set_pigeon_ID).pack()
        
        # Training phases
        Label(self.control_window, text = "Select experimental phase:").pack()
        self.training_phase_variable = StringVar() # This is the literal text of the phase, e.g., "0: Autoshaping"
        self.training_phase_variable.set("Select") # Default
        self.training_phase_name_list = ["0: Pre-Training",
                                         "1: Sub-Optimal Choice Training"
                                    ]
        self.training_phase_menu = OptionMenu(self.control_window,
                                          self.training_phase_variable,
                                          *self.training_phase_name_list)
        self.training_phase_menu.pack()
        self.training_phase_menu.config(width = 20)
        # If we want, we can set it to a specific training phase
        # self.training_phase_variable.set("1: Sub-Optimal Choice Training") # Default set to the main training phase
        
        # Pre-training key FR selection. This is default 1, but can be varied
        # to alternative values (e.g., FR 4 and 8) dependent upon the
        # requirements and progression in pre-training
        # If it is a non-numerical value, it will not he ahle to run.
        Label(self.control_window,
              text = "Pre-Training FR:").pack()
        self.preTraining_FR_stringvar = StringVar()
        self.preTraining_FR_variable = Entry(self.control_window, 
                                     textvariable = self.preTraining_FR_stringvar).pack()
        self.preTraining_FR_stringvar.set(1)
        
        # Forced choice variable? Y/N binary radio button
# =============================================================================
#         Label(self.control_window,
#               text = "Forced Choice").pack()
#         self.forced_choice_variable = IntVar()
#         self.forced_choice_rad_button1 =  Radiobutton(self.control_window,
#                                    variable = self.forced_choice_variable,
#                                    text = "Yes",
#                                    value = True).pack()
#         self.forced_choice_rad_button2 = Radiobutton(self.control_window,
#                                   variable = self.forced_choice_variable,
#                                   text = "No",
#                                   value = False).pack()
#         self.forced_choice_variable.set(False) # Default set to True
#         
# =============================================================================
        # Record data variable? Y/N binary radio button
        Label(self.control_window,
              text = "Record data in seperate data sheet?").pack()
        self.record_data_variable = IntVar()
        self.record_data_rad_button1 =  Radiobutton(self.control_window,
                                   variable = self.record_data_variable,
                                   text = "Yes",
                                   value = True).pack()
        self.record_data_rad_button2 = Radiobutton(self.control_window,
                                  variable = self.record_data_variable,
                                  text = "No",
                                  value = False).pack()
        self.record_data_variable.set(True) # Default set to True
        
        
        # Start button
        self.start_button = Button(self.control_window,
                                   text = 'Start program',
                                   bg = "green2",
                                   command = self.build_chamber_screen).pack()
        
        # This makes sure that the control panel remains onscreen until exited
        self.control_window.mainloop() # This loops around the CP object
        
        
    def set_pigeon_ID(self, pigeon_name):
        # This function checks to see if a pigeon's data folder currently 
        # exists in the respective "data" folder within the Documents
        # folder and, if not, creates one.
        if operant_box_version:
            try:
                if not os_path.isdir(self.data_folder_directory + pigeon_name):
                    mkdir(os_path.join(self.data_folder_directory, pigeon_name))
                    print("\n ** NEW DATA FOLDER FOR %s CREATED **" % pigeon_name.upper())
            except FileExistsError:
                print("Data folder for %s exists." % pigeon_name)       
        else:
            parent_directory = getcwd() + "/data/"
            if not os_path.isdir(parent_directory + pigeon_name):
                mkdir(os_path.join(parent_directory, pigeon_name))
                print("\n ** NEW DATA FOLDER FOR %s CREATED **" % pigeon_name.upper())
                
    def build_chamber_screen(self):
        # Once the green "start program" button is pressed, then the mainscreen
        # object is created and pops up in a new window. It gets passed the
        # important inputs from the control panel. Importantly, it won't
        # run unless all the informative fields are filled in.
        if self.subject_ID_variable.get() in self.pigeon_name_list:
            if self.training_phase_variable.get() in self.training_phase_name_list:
                list_of_variables_to_pass = [self.Hopper,
                                             self.subject_ID_variable.get(),
                                             self.record_data_variable.get(), # Boolean for recording data (or not)
                                             self.data_folder_directory, # directory for data folder
                                             self.training_phase_variable.get(), # Which training phase
                                             self.training_phase_name_list, # list of training phases
                                             self.preTraining_FR_stringvar.get() # Manual FR
                                             # self.forced_choice_variable.get(), # Forced choice Boolean
                                             ]
                print(f"{'SESSION STARTED': ^15}") 
                self.MS = MainScreen(*list_of_variables_to_pass)
            else:
                print("\nERROR: Input Experimental Phase Before Starting Session")
        else:
            print("\nERROR: Input Correct Pigeon ID Before Starting Session")
            

# Next, setup the MainScreen object
class MainScreen(object):
    # We need to declare several functions that are 
    # called within the initial __init__() function that is 
    # run when the object is first built:
    
    def __init__(self, Hopper, subject_ID, record_data, data_folder_directory,
                 training_phase, training_phase_name_list, preTraining_FR #, forced_choice_session
                 ):
        ## Firstly, we need to set up all the variables passed from within
        # the control panel object to this MainScreen object. We do this 
        # by setting each argument as "self." objects to make them global
        # within this object.
        
        # Setup training phase
        self.training_phase = training_phase_name_list.index(training_phase) # Starts at 0 **
        self.training_phase_name_list = training_phase_name_list
        
        
        # Setup data directory
        self.data_folder_directory = data_folder_directory
        
        ## Set the other pertanent variables given in the command window
        self.subject_ID = subject_ID
        self.record_data = record_data
        if self.training_phase == 0: # If pre-training, we can modulate FR
            try:
                self.preTraining_FR = int(preTraining_FR) # Number of times the oberving key should be pressed for the target to appear 
            except ValueError:
                print("\nERROR: Incorrect Manual FR Input")
        else:
            self.preTraining_FR = 1
# =============================================================================
#         # Including forced choice variables
#         self.forced_choice_session = forced_choice_session
#         self.forced_choice_stim_list = forced_choice_stim_list
# =============================================================================
        
        ## Set up the visual Canvas
        self.root = Toplevel()
        self.root.title("P037: - " + self.training_phase_name_list[self.training_phase][3:]) # this is the title of the windows
        self.mainscreen_height = 600 # height of the experimental canvas screen
        self.mainscreen_width = 800 # width of the experimental canvas screen
        self.root.bind("<Escape>", self.exit_program) # bind exit program to the "esc" key
        
        # If the version is the one running in the boxes...
        if operant_box_version: 
            # Keybind relevant keys
            self.cursor_visible = True # Cursor starts on...
            self.change_cursor_state() # turn off cursor UNCOMMENT
            self.root.bind("<c>", # bind cursor on/off state to "c" key
                           lambda event: self.change_cursor_state()) 
            
            # Then fullscreen (on a 800x600p screen)
            self.root.attributes('-fullscreen', True)
            self.mastercanvas = Canvas(self.root,
                                   bg="black")
            self.mastercanvas.pack(fill = BOTH,
                                   expand = True)
        # If we want to run a "human-friendly" version outide the box
        else: 
            # No keybinds and  800x600p fixed window
            self.mastercanvas = Canvas(self.root,
                                   bg="black",
                                   height=self.mainscreen_height,
                                   width = self.mainscreen_width)
            self.mastercanvas.pack()
            
        # Function to provide manual reinforcer (not active)
        #self.root.bind("<m>",lambda event: self.manual_reinforcer())
            
        # Setup hopper (passed from the control panel)
        self.Hopper = Hopper
        
        # Timing variables
        self.start_time = None # This will be reset once the session actually starts
        self.trial_start = None # Duration into each trial as a second count, resets each trial
        self.session_duration = datetime.now() + timedelta(minutes = 90) # Max session time is 90 min
        self.ITI_duration = 10 * 1000 # duration of inter-trial interval (ms)
        if self.subject_ID == "TEST":
            self.feedback_duration = 5 * 1000 # duration of post-choice feedback (ms)
        else:
            self.feedback_duration = 15 * 1000 # duration of post-choice feedback (ms)
        # Hopper duration per bird refereneced a settings sheet
        
        self.current_trial_counter = 0 # counter for current trial in session
        self.reinforcers_provided = 0 # number of trials where a reinforcer was provided
        self.rejected_trial = False # Marks a rejected trial
        self.informative_prob = 0.2
        self.noninformative_prob = 0.5
        self.rejection_FI_duration = 1 # Duration of rejection key FI (ms)
        # Max number of trials within a session differ by phase and was set 
        # later in the first-ITI function
        
        # Here are variables for data structuring 
        self.session_data_frame = [] #This where trial-by-trial data is stored
        header_list = ["SessionTime", "Xcord","Ycord", "LocationEvent",
                       "ExperimentalEvent", "TrialStage", "TrialTime", 
                       "TrialFR", "TrialNum", "ReinforcersProvided", "TrialType",
                       "RejectedTrial", "RejectionFIDuration", 
                       "InformativeProbability", "NoninformativeProbability",
                       "Subject", "TrainingPhase", "Date"] # Column headers
        
        self.session_data_frame.append(header_list) # First row of matrix is the column headers
        self.date = date.today().strftime("%y-%m-%d") # Today's date

        ## Finally, start the recursive loop that runs the program:
        self.place_birds_in_box()

    def place_birds_in_box(self):
        # This is the default screen run until the birds are placed into the
        # box and the space bar is pressed. It then proceedes to the ITI. It only
        # runs in the operant box version. After the space bar is pressed, the
        # "first_ITI" function is called for the only time prior to the first trial
        
        def first_ITI(event):
            # Is initial delay before first trial starts. It first deletes all the
            # objects off the mainscreen (making it blank), unbinds the spacebar to 
            # the first_ITI link, followed by a 30s pause before the first trial to 
            # let birds settle in and acclimate.
            self.mastercanvas.delete("all")
            self.root.unbind("<space>")
            self.start_time = datetime.now() # Set start time
            
            # Then we can read the settings .csv to set up subject-specific 
            # parameters for this session.
            if operant_box_version:
                settings_csv_directory = str(os_path.expanduser('~')+"/OneDrive/Desktop/P037/P037_Settings-Assignments.csv")
            else:
                settings_csv_directory = "P037_Settings-Assignments.csv"
            
            # Next, check if the csv file exists.
            settings_list = []
            if os_path.isfile(settings_csv_directory):
                # Read the content of the csv as a dictionary
                with open(settings_csv_directory, 'r', encoding='utf-8-sig') as data:
                    for line in DictReader(data):
                        settings_list.append(line)
            else:
                print("Error: cannot find settings csv file!")
                input()
            # After we have a list off the settings for all subjects converted 
            # into a Python-friendly data form (list of dictionaries), we can 
            # narrow it down to a single subject-specific dictionary
            settings_dict = "NA"
            try:
                for entry in settings_list:
                    if entry["Subject"] == self.subject_ID:
                        settings_dict = entry
            except KeyError:
                print("Error reading settings .csv.\n Make sure it is in comma-dilimeted form.")
                    
            # And we can then update subject-specific settings...
            print(settings_dict)
            try:
                self.hopper_duration = int(settings_dict["Hopper Duration (ms)"])
                self.rejection_FI_duration = int(settings_dict["Rejection FI Duration (ms)"])
                self.informative_side = settings_dict["Informative Side"]
                self.informative_Splus_color = settings_dict["Informative S+"]
                self.informative_Sminus_color = settings_dict["Informative S-"]
                self.noninformative_side = settings_dict["Non-Informative Side"]
                self.noninformative_Splus_color = settings_dict["Non-Informative S+"]
                self.noninformative_Sminus_color = settings_dict["Non-Informative S-"]
            except TypeError:
                print("Error: Unable to import Settings Sheet for {self.subject_ID}")
            # And create a dictionary with key color assignments:
            if self.informative_side == "Left":
                self.key_color_dict = {"left_choice_key": "white",
                                      "right_choice_key": "white",
                                      "ll_feedback_key": self.informative_Splus_color,
                                      "lr_feedback_key": self.informative_Sminus_color,
                                      "rl_feedback_key": self.noninformative_Splus_color,
                                      "rr_feedback_key": self.noninformative_Sminus_color,
                                      "rejection_key": "darkslategrey"
                                      }
            elif self.informative_side == "Right":
                self.key_color_dict = {"left_choice_key": "white",
                                      "right_choice_key": "white",
                                      "ll_feedback_key": self.noninformative_Splus_color,
                                      "lr_feedback_key": self.noninformative_Sminus_color,
                                      "rl_feedback_key": self.informative_Splus_color,
                                      "rr_feedback_key": self.informative_Sminus_color,
                                      "rejection_key": "white"
                                      }                                 
            # Next, we can set up the order of each trial within the session.
            # The total number of trials per session differs based on whether
            # the session is a pre-training (100% reinforced) or training 
            # (variably reinforced) session type.
            
            if self.training_phase == 0: # pre-training
                self.trials_per_session = 56 # 7 trial types * 8 iterations
                trial_option_list = [
                    "rejection_key",
                    "left_choice_key",
                    "right_choice_key",
                    "ll_feedback_key",
                    "lr_feedback_key",
                    "rl_feedback_key",
                    "rr_feedback_key"
                    ] * 8
                
            
            elif self.training_phase == 1: # rejection training
                self.trials_per_session = 100
                trial_option_list = [
                    "forced_choice-informative",
                    "forced_choice-noninformative"
                    ]  * 10 + [
                        "rejection-informative",
                        "rejection-noninformative"
                        ] * 10 + [
                            "free_choice"] *10
                            
                # Next step is setting up the sampling without replacement for 
                # the forced choice trials. To do this, we need to seperate out
                # the forced choice non/informative trials each session and 
                # designate a certain number are wins vs losses, all dependent
                # upon the initial win probability, such that by the end of 
                # the session, the probabilities are balanced.
                
                # We assume that there are 20 of each (10 * 2) forced choice 
                # trials per session, here.
                self.forced_I_choice_outcome_list = ["win"] * (int(self.informative_prob * 20)) + ["loss"] * (int((1 - self.informative_prob) * 20))
                self.forced_NI_choice_outcome_list = ["win"] * (int(self.noninformative_prob * 20)) + ["loss"] * (int((1 - self.noninformative_prob) * 20))
                self.forced_NI_choice_feedback_list = [self.noninformative_Splus_color] * (int(self.informative_prob * 20)) + [self.noninformative_Sminus_color] * (int((1 - self.informative_prob) * 20))
                
                
            # Once we have the number of trials per session (and what type of
            # trials they will be), we can semi-randomly determine the order.
            # The key here will be that we're avoiding repeats of four or more
            # of the same trial type.
            self.trial_order_list = []
            
            while len(self.trial_order_list) != self.trials_per_session:
                shuffle(trial_option_list) # shuffle
                approved = True
                c = 0  # counter
                while c < len(trial_option_list) and approved:
                    if c > 3:
                        a = trial_option_list[c]
                        if a == trial_option_list[c-1] and a == trial_option_list[c-2] and a == trial_option_list[c-3]:
                            approved = False
                    c += 1
                if approved:
                    for i in trial_option_list:
                        self.trial_order_list.append(i)
  
            # Now we have the type of every sequential trial within the session
            # and we can get started!
                
# =============================================================================
#                 # Importantly, we need to change the trial type if its a forced
#                 # choice trial (easier to do this after the fact):
#                 if c in fc_trial_index:
#                     self.stimulus_order_dict[c]["trial_type"] = "FC_trial"
# =============================================================================

            
            # After we ~finally~ set up the stimulus order, we need to set up 
            # a timer and move on to the ITI
            
            if self.subject_ID == "TEST": # If test, don't worry about first ITI delay
                self.ITI_duration = 1 * 1000
                self.root.after(1, lambda: self.ITI())
            else:
                self.root.after(30000, lambda: self.ITI())

        self.root.bind("<space>", first_ITI) # bind cursor state to "space" key
        self.mastercanvas.create_text(350,300,
                                      fill="white",
                                      font="Times 20 italic bold",
                                      text=f"P037 \n Place bird in box, then press space \n Subject: {self.subject_ID} \n Training Phase {self.training_phase_name_list[self.training_phase]}")
        
                
## %% ITI

    # Every trial (including the first) "starts" with an ITI. The ITI function
    # does several different things:
    #   1) Checks to see if any session constraints have been reached
    #   2) Resets the hopper and any trial-by-trial variables
    #   3) Increases the trial counter by one
    #   4) Moves on to the next trial after a delay (ITI)
    # 
    def ITI (self):
        # This function just clear the screen. It will be used a lot in the future, too.
        self.clear_canvas()
        
        # Make sure pecks during ITI are saved...
        self.mastercanvas.create_rectangle(0,0,
                                           self.mainscreen_width,
                                           self.mainscreen_height,
                                           fill = "black",
                                           outline = "black",
                                           tag = "bkgrd")
        self.mastercanvas.tag_bind("bkgrd",
                                   "<Button-1>",
                                   lambda event, 
                                   event_type = "ITI_peck": 
                                       self.write_data(event, event_type))
        
        # First, check to see if any session limits have been reached (e.g.,
        # if the max time or reinforcers earned limits are reached).
        if self.current_trial_counter  == self.trials_per_session:
            print("&&& Trial max reached &&&")
            self.exit_program("event")
            
# =============================================================================
#         elif datetime.now() >= (self.session_duration):
#             print("Time max reached")
#             self.exit_program("event")
# =============================================================================
        
        # Else, after a timer move on to the next trial. Note that,
        # although the after() function is given here, the rest of the code 
        # within this function is still executed before moving on.
        else: 
            # Print text on screen if a test (should be black if an experimental trial)
            if not operant_box_version or self.subject_ID == "TEST":
                self.mastercanvas.create_text(400,300,
                                              fill="white",
                                              font="Times 20 italic bold",
                                              text=f"ITI ({int(self.ITI_duration/1000)} sec.)")
                
            # This calls the Hopper function to turn it off, and resets other
            # variables. The hopper should be turned off in the previous function,
            # but this is an additional safeguard just to be safe.
            if operant_box_version:
                self.Hopper.change_hopper_state("Off")
                
            # Reset other variables for the following trial.
            self.trial_start = time() # Set trial start time (note that it includes the ITI, which is subtracted later)
            self.choice = None # Reset the choice tracker
            self.rejected_trial = False # Resets a rejected trial
            self.write_comp_data(False) # update data .csv with trial data from the previous trial
            
            # Next up, set the sample key FR for this upcoming
            if self.training_phase == 0:
                self.choice_key_FR = self.preTraining_FR
            else:
                self.choice_key_FR = 1
                
            # Next up, set the string that tracks the trial type
            self.trial_type = self.trial_order_list[self.current_trial_counter]

            # Increase trial counter by one
            self.current_trial_counter += 1
            
            # Next, set a delay timer to proceed to the next trial
            self.root.after(self.ITI_duration,
                            lambda: self.initial_links_stage())
            
            # Finally, print terminal feedback "headers" for each event within the next trial
            print(f"\n{'*'*40} Trial {self.current_trial_counter} begins {'*'*40}") # Terminal feedback...
            print(f"{'Event Type':>30} | Xcord. Ycord. | Stage |  Session Time  | Trial Type")
        
#    #%%  Pre-choice loop 
    """
    Each trial is built of x- number of distinct subtrial phases. 
        
        0) Initial links - At the beginning of each trial, the white choice
            key(s) is lit, depending on the trial type. If a rejection trial,
            the rejection key (a cross) is also illuminated alongside the
            choice key. If rejection key is picked, it immediately results in
            presentation of the alternative key (same "trial" and "trial 
            stage", though).
            
        1) Feedback stage - After a choice is made, either informative
            or uniformative feedback is provided (dependenent upon choice and
            counterbalancing) for 10 s.
            
        2) Reward - If the trial is rewarded (20% of informative conditions but
            always with the S+ and in and 50% of non-informative conditions
            but not dependent upon feedback stimulus), then the subject is
            rewarded once the the feedback stage concludes. If not, the trial
            proceeds directly to the ITI.
    """
    

    def initial_links_stage(self):
        # This is the first part of the trial in which initial links (or choice
        # keys are presented)
        self.clear_canvas()
        self.trial_stage = 0
        self.build_keys()

    def feedback_stage(self):
        self.clear_canvas()
        self.trial_stage = 1
        # If an informative choice...
        if self.choice.split("_")[0] == self.informative_side.lower():
            # For not forced choice trials
            if "forced" not in self.trial_type:
                random_choice = uniform(0,1)
                if random_choice <= self.informative_prob:
                    reinforced = True
                    feedback_color = self.informative_Splus_color
                else:
                    reinforced = False
                    feedback_color = self.informative_Sminus_color
            # For forced choice...
            else:
                outcome = choice(self.forced_I_choice_outcome_list) # Sample...
                self.forced_I_choice_outcome_list.remove(outcome) # ...without replacement
                if outcome == "win":
                    reinforced = True
                    feedback_color = self.informative_Splus_color
                else:
                    reinforced = False
                    feedback_color = self.informative_Sminus_color
                    
        # If non-informative choice
        else:
            if "forced" not in self.trial_type:
                # 50% chance of reinforcement, equal chance of S+ or S- as informative
                # First outcome...
                random_choice = uniform(0,1)
                if random_choice <= self.noninformative_prob:
                    reinforced = True
                else:
                    reinforced = False
                # Then feedback color
                random_choice = uniform(0,1)
                if random_choice <= self.informative_prob:
                    feedback_color = self.noninformative_Splus_color
                else:
                    feedback_color = self.noninformative_Sminus_color
            # If forced non-informative
            else:
                outcome = choice(self.forced_NI_choice_outcome_list) # Sample...
                self.forced_NI_choice_outcome_list.remove(outcome) # ...without replacement
                if outcome == "win":
                    reinforced = True
                else:
                    reinforced = False
                    
                feedback_color = choice(self.forced_NI_choice_feedback_list) # Sample...
                self.forced_NI_choice_feedback_list.remove(feedback_color) # ...without replacement
                
            
        # Then we need to set the feedback stimulus string (using the color dict)
        self.feedback_stimulus = list(self.key_color_dict.keys())[list(self.key_color_dict.values()).index(feedback_color)]
        
        # Then build the feedback key!
        self.build_keys()
        # Lastly, set the timer for the feedback duration (leading to either
        # reinforcement or just directly to the ITI)
        if reinforced:
            self.feedback_timer = self.root.after(self.feedback_duration,
                                                  self.provide_food)
        else:
            self.feedback_timer = self.root.after(self.feedback_duration,
                                                  self.ITI)
        
    def build_keys(self):
        # This is a function that builds the all the buttons on the Tkinter
        # Canvas. The Tkinter code (and geometry) may appear a little dense
        # here, but it follows many of the same rules. Al keys will be built
        # during non-ITI intervals, but they will only be filled in and active
        # during specific times. However, pecks to keys will be differentiated
        # regardless of activity.
        
        # First, build the background. This basically builds a button the size of 
        # screen to track any pecks; buttons built on top of this button will
        # NOT count as background pecks but as key pecks, because the object is
        # covering that part of the background. Once a peck is made, an event line
        # is appended to the data matrix.
        self.mastercanvas.create_rectangle(0,0,
                                           self.mainscreen_width,
                                           self.mainscreen_height,
                                           fill = "black",
                                           outline = "black",
                                           tag = "bkgrd")
        self.mastercanvas.tag_bind("bkgrd",
                                   "<Button-1>",
                                   lambda event, 
                                   event_type = "background_peck": 
                                       self.write_data(event, event_type))
        
        # Nest, we update all the colors needed for this stage of the trial
        
        # Coordinate dictionary for the shapes around a key. The keys are 
        # given in [x1, y1, x2, y2] coordinates
        key_coord_dict = {"left_choice_key": [150, 250, 250, 350],
                          "right_choice_key": [550, 250, 650, 350],
                          "rejection_key": [350, 250, 450, 350],
                          "ll_feedback_key": [150, 250, 250, 350],
                          "lr_feedback_key": [150, 250, 250, 350],
                          "rl_feedback_key": [550, 250, 650, 350],
                          "rr_feedback_key": [550, 250, 650, 350]
                          }

        # Now we need to select the keys to build for this specific trial...
        key_str_list_to_build = []
        if self.training_phase == 0: # If pre-training
            key_str_list_to_build.append(self.trial_type)
        elif self.training_phase == 1: # If pre-training
            # For choice stage...
            if self.trial_stage == 0:
                if not self.rejected_trial:
                    if self.trial_type in ["forced_choice-informative",
                                           "rejection-informative",
                                           "free_choice"]:
                        key_str_list_to_build.append(f"{self.informative_side.lower()}_choice_key")
                    if self.trial_type in ["rejection-noninformative",
                                             "forced_choice-noninformative",
                                             "free_choice"]:
                        key_str_list_to_build.append(f"{self.noninformative_side.lower()}_choice_key")
                    # For rejection trials, build rejection key...
                    if self.trial_type in ["rejection-noninformative",
                                           "rejection-informative"]:
                        key_str_list_to_build.append("rejection_key")
                else: # If rejectED trial
                    if self.trial_type == "rejection-noninformative":
                        key_str_list_to_build.append(f"{self.informative_side.lower()}_choice_key")
                    elif self.trial_type == "rejection-informative":
                        key_str_list_to_build.append(f"{self.noninformative_side.lower()}_choice_key")
                    
                            
            # For feedback stage...
            elif self.trial_stage == 1:
                key_str_list_to_build.append(self.feedback_stimulus)
                    
        # Now that we have all the coordinates linked to each specific key,
        # we can use a for loop to build each one.
        for key_string in key_str_list_to_build:
            # First up, build the actual circle that is the key and will
            # contain the stimulus. Order is important here, as shapes built
            # on top of each other will overlap/cover each other.
                
            self.mastercanvas.create_oval(
                key_coord_dict[key_string][0] - 25,
                key_coord_dict[key_string][1] - 25,
                key_coord_dict[key_string][2] + 25,
                key_coord_dict[key_string][3] + 25,
                fill = "",
                outline = "",
                tag = key_string)

            self.mastercanvas.create_oval(
                *key_coord_dict[key_string],
                fill = self.key_color_dict[key_string],
                outline = "",
                tag = key_string)
            
            # We'll have to identify rejection trials/keys and treat them 
            # differently and build a cross on top of the 
            if "rejection_key" in key_string:
                x1 = key_coord_dict[key_string][0]
                x2 = key_coord_dict[key_string][2]
                y1 = key_coord_dict[key_string][1]
                y2 = key_coord_dict[key_string][3]
                rect1_cords = [
                    x1 + (x2-x1)/2 - (x2-x1)/10, # x1
                    y1 + (y2-y1)/10, # y1
                    x1 + (x2-x1)/2 + (x2-x1)/10, # x2
                    y2 - (y2-y1)/10 # y2
                    ]
                rect2_cords = [
                    x1 + (x2-x1)/10, # x1
                    y1 + (y2-y1)/2 - (y2-y1)/10, # y1
                    x2 - (x2-x1)/10, # x2
                    y1 + (y2-y1)/2 + (y2-y1)/10 # y2
                    ] 
                self.mastercanvas.create_rectangle(
                    *rect1_cords,
                    fill = "purple",
                    outline = "purple",
                    tag = key_string)
                self.mastercanvas.create_rectangle(
                    *rect2_cords,
                    fill = "purple",
                    outline = "purple",
                    tag = key_string)
                
                
                
            self.mastercanvas.tag_bind(
                key_string,
                "<Button-1>",
                lambda event, key_string = key_string: self.key_press(event,
                                                                    key_string))
            
# =============================================================================
#         # If we're in a forced choice trial, we need to cover up the incorrect 
#         # foil such that only the sample and correct comparison are visible 
#         # (and active) on the screen.
#         if self.stimulus_order_dict[self.current_trial_counter]["trial_type"] == "FC_trial":
#             # To do this, we need to first figure out if the foil is on the 
#             # left or the right side. If the correct comparison is on the left,
#             # foil should be on the right:
#             if self.stimulus_order_dict[self.current_trial_counter]["correct_comparison_key"] == self.stimulus_order_dict[self.current_trial_counter]["left_comparison_key"]:
#                 cover_cords = key_coord_dict["right_comparison_key"]
#                 # foil should be on the right:
#             elif self.stimulus_order_dict[self.current_trial_counter]["correct_comparison_key"] == self.stimulus_order_dict[self.current_trial_counter]["right_comparison_key"]:
#                 cover_cords = key_coord_dict["left_comparison_key"]
#             # Then we can build the cover on top of the foil:
#             self.mastercanvas.create_rectangle(cover_cords,
#                                                fill = "black",
#                                                outline = "black",
#                                                tag = "bkgrd")
#             # This cover should be just like the background and write data
#             # events accordingly...
#             self.mastercanvas.tag_bind("bkgrd",
#                                        "<Button-1>",
#                                        lambda event, 
#                                        event_type = "background_peck": 
#                                            self.write_data(event, event_type))
# =============================================================================
            
    
    """ 
    The three functions below represent the outcomes of choices made under the 
    two different cotnigencies (simple or choice). In the simple task (with
    only one "choice" key and target color), any response on the green "choice" 
    key within time contraints is correct and will be reinforced and logged as
    such. In the true choice task, only a choice of the "correct" target-color
    matching key will be reinforced; the opposite key leads to a TO.
    
    Note that, in this setup, the left and right choice keys are fixed to a 
    specific color (left is always blue). We'll need to counterbalance color
    across subjects later on.
    """
    
    def key_press(self, event, keytag):
        # First, we always write data for the peck
        if "rejection" not in keytag:
            self.write_data(event, (f"{keytag}_peck"))
        else:
            if self.trial_type == "rejection-informative":
                self.write_data(event, ("rejection-informative_peck"))
            elif self.trial_type == "rejection-noninformative":
                self.write_data(event, ("rejection-noninformative_peck"))
            else:
                print("ERROR")
        # We need two different processes for different phase...
        # For pretraining
        if self.training_phase == 0:
            self.choice_key_FR -= 1 
            if self.choice_key_FR == 0:
                self.provide_food()
            else:
                self.initial_links_stage()
        # For experimental task
        elif self.training_phase == 1:
            if self.trial_stage == 0:
                if "rejection" in keytag:
                    # If it'sthe first rejection key choice of a trial (else
                    # pass all this)
                    if not self.rejected_trial:
                        self.rejected_trial = True
                        # Cover up the choice keys
                        choice_key_coord_matrix = [[100, 200, 300, 400],
                                                  [500, 200, 700, 400]]
                        for c_list in choice_key_coord_matrix:
                            self.mastercanvas.create_rectangle(*c_list,
                                                               fill = "black",
                                                               outline = "black",
                                                               tag = "bkgrd")
                        # Tag as background
                        self.mastercanvas.tag_bind("bkgrd",
                                                   "<Button-1>",
                                                   lambda event, 
                                                   event_type = "background_peck": 
                                                       self.write_data(event, event_type))
                        # Go back to initial links after the timer
                        self.root.after(self.rejection_FI_duration,
                                        self.initial_links_stage)
                        
                else:
                    self.choice = keytag
                    self.feedback_stage()
            
    
    # %% Post-choice contingencies: always either reinforcement (provide_food)
    # or time-out (time_out_func). Both lead back to the next trial's ITI,
    # thereby completing the loop.
    
    def provide_food(self):
        # This function is contingent upon correct and timely choice key
        # response. It opens the hopper and then leads to ITI after a preset
        # reinforcement interval (i.e., hopper down duration)
        self.clear_canvas()
        self.write_data(None, "reinforcer_provided")
        
        # We first need to add one to the reinforcement counter
        self.reinforcers_provided += 1
        
        # If key is operantly reinforced
        if not operant_box_version or self.subject_ID == "TEST":
            self.mastercanvas.create_text(400,300,
                                          fill="white",
                                          font="Times 20 italic bold", 
                                          text=f"Food accessible ({int(self.hopper_duration/1000)} s)") # just onscreen feedback

        if operant_box_version:
            self.Hopper.change_hopper_state("On") # turn on hopper
        self.root.after(self.hopper_duration,
                        lambda: self.ITI())
        

    # %% Outside of the main loop functions, there are several additional
    # repeated functions that are called either outside of the loop or 
    # multiple times across phases.
    
    def change_cursor_state(self):
        # This function toggles the cursor state on/off. 
        # May need to update accessibility settings on your machince.
        if self.cursor_visible: # If cursor currently on...
            self.root.config(cursor="none") # Turn off cursor
            print("### Cursor turned off ###")
            self.cursor_visible = False
        else: # If cursor currently off...
            self.root.config(cursor="") # Turn on cursor
            print("### Cursor turned on ###")
            self.cursor_visible = True
# =============================================================================
#                                                          
#     def manual_reinforcer(self):
#         # This function provides a manual reinforcer to the bird but keeps
#         # everything the same. The trial doesn't end, there's just a 3s 
#         # food access.
#         def delete_text(m, t):
#             self.mastercanvas.destroy(t)
#         
#         self.write_data(None, "manual_reinforcer_provided")
#         if operant_box_version:
#             self.Hopper.change_hopper_state("On") # turn on hopper
#             self.root.after(self.hopper_duration,
#                             lambda: self.Hopper.change_hopper_state("Off"))
#         else:
#             text = self.mastercanvas.create_text(400,100,
#                                             fill="white",
#                                             font="Times 20 italic bold", 
#                                             text=f"Manual reinforcer provided \nFood accessible ({int(self.hopper_duration/1000)} s)")
#             self.root.after(self.hopper_duration,
#                             delete_text(text)) # then remove the text after a delay
#         
# =============================================================================
    
    def clear_canvas(self):
         # This is by far the most called function across the program. It
         # deletes all the objects currently on the Canvas. A finer point to 
         # note here is that objects still exist onscreen if they are covered
         # up (rendering them invisible and inaccessible); if too many objects
         # are stacked upon each other, it can may be too difficult to track/
         # project at once (especially if many of the objects have functions 
         # tied to them. Therefore, its important to frequently clean up the 
         # Canvas by literally deleting every element.
        try:
            self.mastercanvas.delete("all")
        except TclError:
            print("No screen to exit")
        
    def exit_program(self, event): 
        # This function can be called two different ways: automatically (when
        # time/reinforcer session constraints are reached) or manually (via the
        # "End Program" button in the control panel or bound "esc" key).
            
        # The program does a few different things:
        #   1) Return hopper to down state, in case session was manually ended
        #       during reinforcement (it shouldn't be)
        #   2) Turn cursor back on
        #   3) Writes compiled data matrix to a .csv file 
        #   4) Destroys the Canvas object 
        #   5) Calls the Paint object, which creates an onscreen Paint Canvas.
        #       In the future, if we aren't using the paint object, we'll need 
        #       to 
        def other_exit_funcs():
            if operant_box_version:
                self.Hopper.change_hopper_state("Off")
                # root.after_cancel(AFTER)
                if not self.cursor_visible:
                	self.change_cursor_state() # turn cursor back on, if applicable
            self.write_comp_data(True) # write data for end of session
            self.root.destroy() # destroy Canvas
            print("\n GUI window exited")
            
        self.clear_canvas()
        other_exit_funcs()
        print("\n You may now exit the terminal and operater windows now.")
        if operant_box_version:
            polygon_fill.main(self.subject_ID) # call paint object
        
    
    def write_data(self, event, outcome):
        # This function writes a new data line after EVERY peck. Data is
        # organized into a matrix (just a list/vector with two dimensions,
        # similar to a table). This matrix is appended to throughout the 
        # session, then written to a .csv once at the end of the session.
        if event != None: 
            x, y = event.x, event.y
        else: # There are certain data events that are not pecks.
            x, y = "NA", "NA"
            
        # Next, we should translate the locational information from "outcome"
        # into experimental data
        if outcome in ["left_choice_key_peck", "right_choice_key_peck"]:
            if self.informative_side.lower() in outcome:
                exp_outcome = "informative_key_peck"
            elif self.noninformative_side.lower() in outcome:
                exp_outcome = "uninformative_key_peck"
            else:
                print("ERROR")
        elif outcome in ["ll_feedback_key_peck", "lr_feedback_key_peck",
                       "rl_feedback_key_peck", "rr_feedback_key_peck"]:
            if self.key_color_dict[outcome[:-5]] == self.informative_Splus_color:
                exp_outcome = "informative_Splus_peck"
            elif self.key_color_dict[outcome[:-5]] == self.informative_Sminus_color:
                exp_outcome = "informative_Sminus_peck"
            elif self.key_color_dict[outcome[:-5]] == self.noninformative_Splus_color:
                exp_outcome = "noninformative_Splus_peck"
            elif self.key_color_dict[outcome[:-5]] == self.noninformative_Sminus_color:
                exp_outcome = "noninformative_Sminus_peck"
        elif "rejection" in outcome:
            exp_outcome = "rejection_key_peck"
        else:
            exp_outcome = outcome
            
            
        print(f"{outcome:>30} | x: {x: ^3} y: {y:^3} | {self.trial_stage:^5} | {str(datetime.now() - self.start_time)} | {self.trial_type}")
        # print(f"{outcome:>30} | x: {x: ^3} y: {y:^3} | Target: {self.current_target_location: ^2} | {str(datetime.now() - self.start_time)}")
        self.session_data_frame.append([
            str(datetime.now() - self.start_time), # SessionTime as datetime object
            x, # X coordinate of a peck
            y, # Y coordinate of a peck
            outcome, # Type of event (e.g., background peck, target presentation, session end, etc.)
            exp_outcome, # translated location-independent outcome
            self.trial_stage, # Substage within each trial (1 or 2)
            round((time() - self.trial_start - (self.ITI_duration/1000)), 5), # Time into this trial minus ITI (if session ends during ITI, will be negative)
            self.choice_key_FR, # FR of the current choice key (relevant later?)
            self.current_trial_counter, # Trial count within session (1 - max # trials)
            self.reinforcers_provided, # Reinforced trial counter
            self.trial_type, # Trial type (e.g., "training", "CBE.1", etc.)
            self.rejected_trial, # Whether the second half is a rejected trial
            self.rejection_FI_duration, # FI duration (fixed across session)
            self.informative_prob, # Probability of an informative win
            self.noninformative_prob, # Probability of a non-info win
            self.subject_ID, # Name of subject (same across datasheet)
            self.training_phase, # Phase of training as a number (0 - 7)
            date.today() # Today's date as "MM-DD-YYYY"
            ])
        
        
        header_list = ["SessionTime", "Xcord","Ycord", "LocationEvent",
                       "ExperimentalEvent", "TrialStage", "TrialTime", 
                       "TrialFR", "TrialNum", "ReinforcersProvided", "TrialType",
                       "RejectedTrial", "RejectionFIDuration", 
                       "InformativeProbability", "NoninformativeProbability",
                       "Subject", "TrainingPhase", "Date"] # Column headers


        
    def write_comp_data(self, SessionEnded):
        # The following function creates a .csv data document. It is either 
        # called after each trial during the ITI (SessionEnded ==False) or 
        # one the session finishes (SessionEnded). If the first time the 
        # function is called, it will produce a new .csv out of the
        # session_data_matrix variable, named after the subject, date, and
        # training phase. Consecutive iterations of the function will simply
        # write over the existing document.
        if SessionEnded:
            self.write_data(None, "SessionEnds") # Writes end of session to df
        if self.record_data : # If experimenter has choosen to automatically record data in seperate sheet:
            myFile_loc = f"{self.data_folder_directory}/{self.subject_ID}/{self.subject_ID}_{self.start_time.strftime('%Y-%m-%d_%H.%M.%S')}_P037_data-Phase{self.training_phase}.csv" # location of written .csv
            # This loop writes the data in the matrix to the .csv              
            edit_myFile = open(myFile_loc, 'w', newline='')
            with edit_myFile as myFile:
                w = writer(myFile, quoting=QUOTE_MINIMAL)
                w.writerows(self.session_data_frame) # Write all event/trial data 
            print(f"\n- Data file written to {myFile_loc}")
                
#%% Finally, this is the code that actually runs:
    
if __name__ == '__main__':
    cp = ExperimenterControlPanel()


    
