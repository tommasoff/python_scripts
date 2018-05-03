###          Sham protocol study             ###
###				Pracise run					 ###
#===============================================
# 
# One dot
# Random position set in each trial
# Random opacity set in each trial
# Audio feedbacks
#
# One block of n trials
# 

# Ptc has to press a key when stimulus
# is shown. Responses are not collected 

### Tommaso Viola - 03 / 05 / 2018
### CUBRIC

#===============================================

##SETUP VARIABLES
size_monitor = 1300, 850 # This is overridden by correct values if full screen is used.

allowgui = True # change to False for real testing
fullscreen = True # change to True for real testing

#stimuli
dots_radius = 0.21
n_trials = 20 #for each block

#experiment flow
fixation_time = 3
fixation_end_time = 3

#inter-stimulus-interval length in seconds
isi = 1


#import stuff
from psychopy import visual, event, sound, core, gui
import random
import numpy
import os
import time


#input participant data w/ graphic interface
gui = gui.Dlg()
gui.addField("Subject ID:")
gui.addField("Session nr:")
gui.show()



#===========================================================

### SET DISP AND STIMULI

win = visual.Window(
    size = (size_monitor), fullscr = False, #change this for the experiment to True
    monitor = "testMonitor", color = [0,0,0],
    units = "deg",
    screen = 0, # 0 is participant monitor, 1 is experimenter monitor
    allowGUI = True
)

#set text stimuli
text = visual.TextStim(
    win = win,
    text = "Pracice run \n\n GET READY \n\n Press any key to start",
    units = 'norm'
)

fixation = visual.ShapeStim(win,
    vertices = ((0,-0.5), (0,0.5), (0,0), (-0.5,0), (0.5,0)),
    lineWidth = 1,
    closeShape = False,
    lineColor = "white"
)


#create and display end screen
text_end = visual.TextStim(
    win = win,
    text = "Well done",
    units = 'norm'
)

#set sound feedback
sound_feed = sound.Sound(
    "C",
    secs = 0.1,
    octave = 6
)

block_sound = sound.Sound(
    "C",
    secs = 0.1,
    octave = 7
)

end_sound = sound.Sound(
    "C",
    secs = 0.1,
    octave = 5
)


# 4 deg - top left
dot = visual.Circle(
    win = win,
    radius = dots_radius,
    fillColor = [1,1,1],
    fillColorSpace = 'rgb',
    opacity = (0.5),
    units = "deg"
)

# list of 4 fixed dot positions in degrees
pos_list = [(-4, 4), (-20, 20), (4, -4), (20, -20)]

clock = core.Clock()


#=========================================================
### EXPERIMENT ROUTINE

#start of the experiment
text.draw()
win.flip()
event.waitKeys()

#fixation before main blocks
fixation.draw()
win.flip()
core.wait(fixation_time)
block_sound.play()
core.wait(2)


#stimuli presentation

#loops through blocks and trials
for c in range(n_trials):
    key = None #empty keypresses list
    # choose random luminance between 0-0.75
    lum = random.uniform(0, 0.75)
    # choose random dot position from list
    dotpos = random.choice(pos_list)
    # set luminance
    dot.setOpacity(lum) 
    # set position 
    dot.setPos(dotpos)
    dot.draw()
    fixation.draw()
    clock.reset()
    win.flip()
    core.wait(0.2)    #dot life = .200 sec
    fixation.draw()
    win.flip()
    key = event.waitKeys(isi, keyList = ['down', 'escape'], timeStamped = clock) #wait for a response for a max time = isi (set as variable at the start)
    if key:
        #task can be stopped by pressing esc during trials
        if key[0][0] == "escape":
            core.quit()  # abort experiment
        else: #play feedback and wait for remaining time
            #max waiting time = isi
            rt = key[0][1]
            sound_feed.play()
            isi_2 = isi - rt #corrected waiting time
            core.wait(isi_2)
    else:
        fixation.draw()
        core.wait(isi)
        win.flip()

#===========================================
### END OF EXP


text_end.draw()
win.flip()

# play end sound
end_sound.play()
core.wait(0.1)
sound_feed.play()
core.wait(0.1)
block_sound.play()

core.wait(2)


#quit display and exp
win.close()
core.quit()


