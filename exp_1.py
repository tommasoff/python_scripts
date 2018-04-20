###  Sham protocol study  ###
#========================================
# To be performed during sham stimulation.
#
# Four stimuli in four fixed positions.
# Random opacity set in each trial
# Audio feedbacks

# Ptc has to press a key when stimulus
# is shown. Responses are collected in
# a -csv file. 

### Tommaso Viola - 20 / 04 / 2018
### CUBRIC



##SETUP VARIABLES
size_monitor = 1300, 850

#stimuli
dots_radius = 0.21
n_blocks = 1
n_trials = 1 #for each block

#experiment flow
fixation_time = 3
fixation_end_time = 3
block_time = 3
breack_time = 3

#inter-stimulus-interval 
isi = 2




#import stuff
from psychopy import visual, event, sound, core, gui
import random
import numpy
import os
import time


#input participant data w/ graphic interface
#collect id and session n
gui = gui.Dlg()
gui.addField("Subject ID:")
gui.addField("Session:")
gui.show()

#set input data as variables to write on csv file
sub_id = gui.data[0]
session = gui.data[1]


#create file for data output
timestamp = time.strftime('%Y%m%d%H%M')
basename = ("{}_{}".format(timestamp,sub_id))


filename = os.path.join('data_output/', basename)

# create csv file
datafile = open(filename+'.csv', 'w')

datafile.write('participant,trial,response,rt\n')


#set display
win = visual.Window(
    size = (size_monitor), fullscr = False,
    monitor = "testMonitor", color = [0,0,0],
    units = "deg"
)

#set text stimuli
text = visual.TextStim(
    win = win,
    text = "GET READY \n\n\n\n\n Press any key to start",
    color = "red",
    height = 2
)

fixation = visual.ShapeStim(win,
    vertices = ((0,-0.3), (0,0.3), (0,0), (-0.3,0), (0.3,0)),
    lineWidth = 2,
    closeShape = False,
    lineColor = "white"
)

text_break = visual.TextStim(
    win = win,
    text = "BREAK"
)

#set sound feedback
sound_feed = sound.Sound(
    "C",
    secs = 0.1,
    octave = 6
)


#set dots stimuli
dots = []

dot_1 = visual.Circle(
    win = win,
    radius = dots_radius,
    pos = (-5, 5),
    fillColor = [1,1,1],
    fillColorSpace = 'rgb',
    opacity = (0.5),
    units = "deg"
)

dot_2 = visual.Circle(
    win = win,
    radius = dots_radius,
    pos = (-2, 2),
    fillColor = [1,1,1],
    fillColorSpace = 'rgb',
    opacity = (0.5),
    units = "deg"
)

dot_3 = visual.Circle(
    win = win,
    radius = dots_radius,
    pos = (-2, -2),
    fillColor = [1,1,1],
    fillColorSpace = 'rgb',
    opacity = (0.5),
    units = "deg"
)

dot_4 = visual.Circle(
    win = win,
    radius = dots_radius,
    pos = (-2, -2),
    fillColor = [1,1,1],
    fillColorSpace = 'rgb',
    opacity = (0.5),
    units = "deg"
)

dots = [dot_1, dot_2, dot_3, dot_4]
clock = core.Clock()


#==============================
###experiment routine

#start of the experiment
text.draw()
win.flip()
event.waitKeys()

#fixation before main blocks
fixation.draw()
win.flip()
core.wait(fixation_time)


#stimuli presentation
counter = 1
#loops through blocks and trials
for i in range(n_blocks): 
    for c in range(n_trials):
        key = None #empty keypresses list

        #I used rand_n to present stimuli just in 50% of the trials (since
        #it takes a random choice between 1-2). 
        #If you prefer to show stimuli every trial, just delete this and the
        #if-conditional below. In this case though, you also have to check 
        #how to write responses on the output file (since I have four different
        #outcomes conditional on the presence/assence of the stimulus)
        rand_n = random.choice([1,2])
        if rand_n == 1: #the stimulus is presented half of the trials
            clock.reset()
            dot = random.choice(dots)
            dot.setOpacity(random.random()) #set random luminance between 0-1
            								#(1=max in psychopy, 0=min)
            dot.draw()
            fixation.draw()
            win.flip()
            core.wait(0.2)    #dot life = .200 sec
            fixation.draw()
            win.flip()
            key = event.waitKeys(isi, timeStamped = clock) #wait for a response for a max time = isi 
            											   #(set as variable at the start)
            if key: 
            	#task can be stopped by pressing esc during trials
                if key[0][0] == "escape":
                    core.quit()  # abort experiment
                else: #play feedback and wait for remaining time
                      #max waiting time = isi
                      #if ptc pressed key, waiting time is found 
                    resp = 1   #write response in output file
                    rt = key[0][1]
                    datafile.write('{},{},{},{},{}\n'.format(sub_id, session, counter, resp, rt))
                    isi_2 = isi - rt #corrected waiting time
                    sound_feed.play()
                    core.wait(isi_2)
            else: 
                resp = "na"  #data output
                rt = "na"
                datafile.write('{},{},{},{},{}\n'.format(sub_id, session, counter, resp, rt))
                fixation.draw()
                core.wait(isi)
                win.flip()
            counter += 1 #update counter 
        else:
            fixation.draw()
            win.flip()
            clock.reset()
            key = event.waitKeys(isi, timeStamped = clock)
            if key:
                if key[0][0] == "escape":
                    core.quit()  # abort experiment
                else: #play feedback and wait for remaining time
                    n_trial = c
                    resp = 0   #data output
                    rt = key[0][1]
                    datafile.write('{},{},{},{},{}\n'.format(sub_id, session, counter, resp, rt))
                    isi_2 = isi - rt
                    sound_feed.play()
                    core.wait(isi_2)
                counter += 1
            else:
                n_trial = c
                resp = 1  #data output
                rt = "na"
                datafile.write('{},{},{},{},{}\n'.format(sub_id, session, counter, resp, rt))
                core.wait(isi)
            counter += 1


###between 1st and 4rd block display BREAK
    if i < range(n_blocks):
        text_break.draw() #show BREAK between blocks
        win.flip()
        core.wait(block_time)
###after last block show fixation and end experiment
    elif i == range(n_blocks):  #experiments ends with fixation
        fixation.draw()
        win.flip()
        core.wait(fixation_end_time)


#===========================================
#end of experiment

datafile.close()

#quit display and exp
win.close()
core.quit()

