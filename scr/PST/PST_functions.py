#!/usr/bin/python
# Requires Python 3.8.10
from math import floor
import os
from math import floor
import numpy as np
import pandas as pd
from psychopy import core, data, event, gui, misc, sound, visual
import serial
import pdb 

def present_stims(fix,left_stim, right_stim, win, left_key,right_key,quit_key, RT, task_clock, scheduled_outcome):
    from psychopy import event
    left_stim.draw()
    right_stim.draw()
    win.flip()
    # wait for key press
    key_press = event.waitKeys(keyList = [left_key,right_key,quit_key], timeStamped=RT)
    # allKeys=event.getKeys(keyList = [left_key,right_key,quit_key], timeStamped=RT)
    print(key_press)
    fix.draw()
    win.flip()
    return(key_press)

def response_update(key_pressed, win, left_stim, right_stim, left_choice, right_choice, task_clock): 
    print(key_pressed)   
    resp_onset = task_clock.getTime()
    if key_pressed == '1':
        left_choice.draw()
        left_stim.draw()
        right_stim.draw()
        win.flip()
        # trial_response = show_resp(key_pressed[0][0],left_choice, right_choice, task_clock)
       
        # isi = show_fix(isi_dur,fMRI_clock.getTime(),refresh, fix, win)
        # object_dur = isi[0] - object_onset
        # feedback = show_fdbk(trial_response[0],scheduled_outcome,task_clock.getTime(), no_resp, zero, win, reward, info['test?'])
        
    #            act_trial_dur = object_dur + isi[1] + feedback[2]
    #            iti_dur = iti_dur + int(round(((targ_trial_dur - act_trial_dur)*1000)/refresh))
    #            iti = show_fix(iti_dur,fMRI_clock.getTime(),refresh, fix, win)
    #            stim_frameN = int(floor(3000/refresh))

    elif key_pressed == '4':
        right_choice.draw()
        left_stim.draw()
        right_stim.draw()
        win.flip()
        # trial_response = show_resp(key_pressed[0][0],left_stim_number,right_stim_number,stim_frameN,refresh,task_clock.getTime(), left_stim, right_stim, fix, win, left_choice, right_choice)
        # isi = show_fix(isi_dur,fMRI_clock.getTime(),refresh, fix, win)
        # object_dur = isi[0] - object_onset
        # feedback = show_fdbk(trial_response[0],scheduled_outcome,task_clock.getTime(),refresh, no_resp, zero,win, reward, info['test?'])
    #            act_trial_dur = object_dur + isi[1] + feedback[2]
    #            iti_dur = iti_dur + int(round(((targ_trial_dur - act_trial_dur)*1000)/refresh))
    #            iti = show_fix(iti_dur,fMRI_clock.getTime(),refresh, fix, win)
    #            stim_frameN = int(floor(3000/refresh))




def drawing(left_stim, right_stim, fix, left_choice, right_choice, win):
    left_stim.draw()
    right_stim.draw()
    fix.draw()
    win.flip()

def accuracy(l_stim_num , r_stim_num):
    if l_stim_num < r_stim_num: 
            accuracy = 1
            
    else: 
        accuracy = 0
    if l_stim_num > r_stim_num: 
            accuracy = 1        
    else: 
        accuracy = 0
    return (accuracy)

def show_resp(key_pressed, left_choice, right_choice, task_clock):
    resp_onset = task_clock.getTime()
    if key_pressed == '1':
        left_choice.draw()
        # win.flip()
    if key_pressed == '4':
        right_choice.draw()
        # win.flip()
    return(resp_onset)
    

def show_fdbk(accuracy,sched_out,start_time, no_resp, zero, win, reward, test, task_clock, fdbk_dur):

    # refresh = measured_refresh
    # fdbk_clock = task_clock.Clock()
    # fdbk_clock.reset()
    # fdbk_onset = start_time
    fdbk_onset = task_clock.getTime()

    if accuracy == 1 and sched_out == 1:
        reward.draw()
        core.wait(fdbk_dur)
        if test == false:
            ser.write(52)
        else:
            print('dispensing candy')

        # for frames in range(stupid_math(refresh)):
        #     reward.draw()
        #     if test == False:
        #         ser.write(52)
        #     else:
        #         print('neat')
            cc=str(ser.readline())
            ser.write(52)
            win.flip()
        
        # fdbk_dur = fdbk_clock.getTime()

        return ('reward')

    elif accuracy == 1 and sched_out == 0:

        zero.draw()
        win.flip()
        core.wait(fdbk_dur)
        
        return ('zero')

    elif accuracy == 0 and sched_out == 1:
        zero.draw()
        win.flip()

        #incorr_sound.play()
        # for frames in range(stupid_math(refresh)):
        #     zero.draw()
        #     win.flip()

        # fdbk_dur = fdbk_clock.getTime()

        return ('zero',fdbk_onset,fdbk_dur)

    elif accuracy == 0 and sched_out == 0:
        reward.draw()
        win.flip()
        #corr_sound.play()
        # for frames in range(stupid_math(refresh)):
        #     reward.draw()
        #     win.flip()

        # fdbk_dur = fdbk_clock.getTime()

        return ('reward')

    elif accuracy == 999:
        no_resp.draw()
        win.flip()

        # for frames in range(stupid_math(refresh)):
        #     no_resp.draw()
        #     win.flip()

        # fdbk_dur = fdbk_clock.getTime()

        return ('no_response')



 

def starter(small_blocks, stim_rand, win):
    from psychopy import visual
    for i in range(len(small_blocks)): #Randomize each small block (scramble AB,CD,EF trios).
        np.random.shuffle(small_blocks[i])
    AllTrials = np.asarray(small_blocks) #Make AllTrials array of small blocks.
    while not check_rand(AllTrials,20,3): #Check no more than 6 consecutive rewards scheduled, otherwise shuffle.
        np.random.shuffle(AllTrials)
    #Generate lists for leftStims, rightStims, and sch_outcome.
    #sch_outcome different from reward/zero fdbk, which depends on accuracy. 
    leftStims = []
    left_stim_numbers = []
    rightStims = []
    right_stim_numbers = []
    sch_outcome = []
    for x in range(20):
        for y in range(3):
            leftStims.append(AllTrials[x,y,0])
            rightStims.append(AllTrials[x,y,1])
            sch_outcome.append(AllTrials[x,y,2])
    left_stim_numbers = leftStims
    right_stim_numbers = rightStims
    
    leftStims2 = [stim_rand['stim_A'] if x==1 else stim_rand['stim_C'] if x==2 else stim_rand['stim_E'] if x==3 else stim_rand['stim_F'] if x==4 else stim_rand['stim_D'] if x==5 else stim_rand['stim_B'] if x==6 else x for x in leftStims]
    rightStims2 = [stim_rand['stim_A'] if x==1 else stim_rand['stim_C'] if x==2 else stim_rand['stim_E'] if x==3 else stim_rand['stim_F'] if x==4 else stim_rand['stim_D'] if x==5 else stim_rand['stim_B']if x==6 else x for x in rightStims]
    
    #Load the stims in a matrix to improve timing/efficiency.
    stim_matrix = {}
    for i in range(len(leftStims2)): 
        # print(leftStims)
        # print(leftStims2)
        # print(leftStims[i])
        left_stim = visual.ImageStim(win, units = 'norm', size = [0.5,0.5], pos = [-0.4,0], image=leftStims2[i])
        # print('hi1')
        left_stim_name = leftStims2[i]
        # print('hi2')
        left_stim_number = left_stim_numbers[i]
        # print('hi3')
        right_stim = visual.ImageStim(win, units = 'norm', size = [0.5,0.5], pos = [0.4,0], image=rightStims2[i])
        # print('hi4')
        right_stim_name = rightStims2[i]
        # print('hi5')
        right_stim_number = right_stim_numbers[i]
        # print('hi6')
        scheduled_outcome = sch_outcome[i] 
        # print('hi7')
        stim_matrix[i] = (left_stim,left_stim_name,left_stim_number,right_stim,right_stim_name,right_stim_number,scheduled_outcome)
    return(stim_matrix)


def intro(inst_text, instruct, win, allKeys, left_key, quit_key):
    for i in range(len(inst_text)):
        advance = 'false'

        while advance == 'false':
            instruct.setText(text = inst_text[i]) 
            instruct.draw()
            win.flip()
            allKeys = event.waitKeys(keyList = [left_key, quit_key])#wait for left key or quit key
            resp = allKeys[0][0]

            if resp == left_key:
                advance = 'true'
                allKeys = []

            elif resp == quit_key:
                core.quit()



def stim_mapping(pic_list, datapath, participantID):
    np.random.shuffle(pic_list)
    stim_rand = {'stim_A':pic_list[0], 'stim_C':pic_list[1], 'stim_E':pic_list[2], 'stim_F':pic_list[3], 'stim_D':pic_list[4], 'stim_B':pic_list[5]}
#    df = pd.DataFrame(stim_rand.items())
#    df.to_csv(os.path.join(datapath,'%s_PST_stim_rand.csv'%(participantID)), header=False, index=False)
    return(stim_rand)


def block_it(AB_trialList, CD_trialList, EF_trialList):
    small_blocks = [[i] for i in range(20)]
    for i in range(20):
        small_blocks[i] = np.vstack([AB_trialList[i],CD_trialList[i],EF_trialList[i]])
    return(small_blocks)


def stimulating(num_stims, trials_per_stim):
    letters = ['A','C','E','F','D','B']
    stim_list = [1 for x in range(num_stims)]
    for count,x in enumerate(range(num_stims)):
        count = count+1
        stim_list[x] = [count for y in range(trials_per_stim)]
    print(stim_list)
    stim_names = {}
    for i,x in enumerate(stim_list):
        stim_names[letters[i]] = x
    return(stim_names)

def make_it(stim_names):
    #Make the reward probability vectors.
    n80 = [1,1,1,1,1,1,1,1,0,0]
    n70 = [1,1,1,1,1,1,1,0,0,0]
    n60 = [1,1,1,1,1,1,0,0,0,0]
    #Concatenate stim lists and reward probability vectors.
    AB = np.column_stack([stim_names['A'],stim_names['B'],n80])
    BA = np.column_stack([stim_names['B'],stim_names['A'],n80])
    CD = np.column_stack([stim_names['C'],stim_names['D'],n70])
    DC = np.column_stack([stim_names['D'],stim_names['C'],n70])
    EF = np.column_stack([stim_names['E'],stim_names['F'],n60])
    FE = np.column_stack([stim_names['F'],stim_names['E'],n60])
    AB_trialList = np.vstack([AB,BA])
    CD_trialList = np.vstack([CD,DC])
    EF_trialList = np.vstack([EF,FE])
    trialList = [AB_trialList, CD_trialList, EF_trialList]
    for item in trialList:
        np.random.shuffle(item)
    return(trialList)


def set_visuals(size, monitor, color, wintype,text, align, ht, wWidth, textcolor, radius):
    from psychopy import visual
    win = visual.Window([600,400], fullscr= False, allowGUI = False, monitor = monitor, color = color, winType=wintype) #check window here
    instruct = visual.TextStim(win, text=text, alignHoriz = align, height = ht, wrapWidth = wWidth, color = textcolor)
    fix = visual.TextStim(win, text = '+')
    left_choice = visual.Circle(win, radius = radius, lineColor = textcolor, lineWidth = 2.0, pos = [-0.4,0])
    right_choice = visual.Circle(win, radius = radius, lineColor = textcolor, lineWidth = 2.0, pos = [0.4,0])
    parameters = {'win':win, 'instruct':instruct, 'fix':fix, 'left_choice':left_choice, 'right_choice':right_choice}
    return(parameters)


def stupid_math(refresh):
    return(int(floor(1000/refresh)))

def check_rand (in_array,num_array,num_row): #Cannot have more than 6 consecutive reward outcomes scheduled.
    counter = 0
    for x in range(num_array):
        for y in range(num_row):
            if in_array[x,y,2] == 1:
                counter += 1
                if counter == 6:
                    return False
            else:
                counter = 0
    return True

   

def show_fdbk(accuracy,sched_out,start_time,measured_refresh, no_resp, zero, win, reward, test):

    refresh = measured_refresh
    fdbk_clock = core.Clock()
    fdbk_clock.reset()
    fdbk_onset = start_time

    if accuracy == 1 and sched_out == 1:
        for frames in range(stupid_math(refresh)):
            reward.draw()
            if test == False:
                ser.write(52)
            else:
                print('neat')
            cc=str(ser.readline())
            ser.write(52)
            win.flip()
        
        fdbk_dur = fdbk_clock.getTime()

        return ('reward',fdbk_onset,fdbk_dur)

    elif accuracy == 1 and sched_out == 0:

        #incorr_sound.play()
        for frames in range(stupid_math(refresh)):
            zero.draw()
            win.flip()

        fdbk_dur = fdbk_clock.getTime()

        return ('zero',fdbk_onset,fdbk_dur)

    elif accuracy == 0 and sched_out == 1:

        #incorr_sound.play()
        for frames in range(stupid_math(refresh)):
            zero.draw()
            win.flip()

        fdbk_dur = fdbk_clock.getTime()

        return ('zero',fdbk_onset,fdbk_dur)

    elif accuracy == 0 and sched_out == 0:
        
        #corr_sound.play()
        for frames in range(stupid_math(refresh)):
            reward.draw()
            win.flip()

        fdbk_dur = fdbk_clock.getTime()

        return ('reward',fdbk_onset,fdbk_dur)

    elif accuracy == 999:

        for frames in range(stupid_math(refresh)):
            no_resp.draw()
            win.flip()

        fdbk_dur = fdbk_clock.getTime()

        return ('no_response',fdbk_onset,fdbk_dur)

def show_fix(duration,start_time,measured_refresh, fix, win):

    refresh = measured_refresh
    fix_onset = start_time
    fix_clock = core.Clock()
    fix_clock.reset()
    
    for i in range(duration):
        fix.draw()
        win.flip()

    fix_dur = fix_clock.getTime()

    return (fix_onset,fix_dur)