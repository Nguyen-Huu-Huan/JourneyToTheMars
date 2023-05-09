from tkinter import *
from tkinter import messagebox
from tkinter import font
from datetime import datetime as dt
from PIL import Image, ImageTk
import tkinter.ttk as ttk
import pygame
import json

# create the main window for GUI and set the main window's title, geometry
window = Tk()
window.title("What will the astronauts need?")
window.geometry("1000x668")
# create an empty list (astronaut_status) to store current status of the spaceship
astronaut_status = []
# create an empty dictionary to store
database = {}
# create the main window's background image and a canvas with size (1000,668). Then, add the background to canvas
main_background = ImageTk.PhotoImage(Image.open("background_image.png"))
canvas = Canvas(window, width=1000, height=668)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=main_background, anchor="nw")
# create the rocket image for spaceship illustration
rocket = ImageTk.PhotoImage(Image.open("new_rocket.png"))
item = canvas.create_image(750, 305, image=rocket, anchor="nw", tags="rocket")
# create an image on the left of the Start button
circle = Image.open("circle-removebg-preview.png")
circle = circle.resize((25, 25), Image.ANTIALIAS)
circle_image = ImageTk.PhotoImage(circle)
# create a list of 6 empty lines of text which are later used for displaying the spaceship's current status
spaceship_status_list = [canvas.create_text(50, 480+25*i, text="", fill="white", anchor="nw", font=("Times", "16", "bold")) for i in range(6) ]
canvas.move(spaceship_status_list[3], 0, 25)
canvas.move(spaceship_status_list[4], 0, 25)
canvas.move(spaceship_status_list[5], 0, 25)
# create an empty notification. The notification will later show whether the spaceship completes the journey to Mars
notification = canvas.create_text(40, 500, text="", fill="yellow", anchor="nw", font=("Ariel", 24, "bold"))
# The variable save_move_distance is used for calculating the distance the spaceship is supposed to move since previous click on the Start button
save_move_distance = 0
# sign_of_error variable used to detect conditions that the spaceship may fail to continue on its journey to Mars. Ex: out of fuel, negative spaceship or crew member health, etc.
sign_of_error = 0
# initialize pygame to play music
pygame.init()
pygame.mixer.music.load("ez.mp3")
pygame.mixer.music.play(-1)
medium_font = font.Font(family='Time New Roman', size=15)
# create a combobox for choosing things easier
diary = ttk.Combobox(window, width=18, height=1, font=medium_font)
diary.place(x=732, y=534)


# create clear_spaceship_status_list def to clear the spaceship_status_list. It is cleared by setting the text attribute to an empty string ""
def clear_spaceship_status_list():
    for i in range(len(spaceship_status_list)):
        canvas.itemconfig(spaceship_status_list[i], text="")


def save_status(data):
    # Save status into file.txt
    with open("save_status.txt", "a") as save_data:
        save_data.write(json.dumps(data))
        save_data.write("\n")


def read_status():
    global astronaut_status
    # get the data from file
    with open("save_status.txt", "r") as read_data:
        data = read_data.readlines()
        astronaut_status = json.loads(data[-1])


# This help to save position of the ship which uses for moving
def save_pos(parameter):
    with open("save_pos.txt", "a") as save_position:
        save_position.write(str(parameter))
        save_position.write("\n")


# This help to move the ship to the previous position when you closed the program
def move_ship():
    global save_move_distance
    with open("save_pos.txt", "r") as read_position:
        position = read_position.readlines()
        if len(position) != 0:
            position = float(position[-1])
            canvas.move(item, position, 0)
            save_move_distance += position


move_ship()


# as its name :))) convert to the format from seconds
def time_convert(seconds):
    # create a list to store months,days,hours,minutes and seconds
    display_time = [0, 0, 0, 0, 0]
    intervals = ["months", "days", "hours\n", "minutes", "seconds"]
    out_put = ""
    while seconds > 2629800:
        display_time[0] += 1
        seconds -= 2629800
    while seconds > 86400:
        display_time[1] += 1
        seconds -= 86400
    while seconds > 3600:
        display_time[2] += 1
        seconds -= 3600
    while seconds > 60:
        display_time[3] += 1
        seconds -= 60
    display_time[4] = seconds
    for i in range(5):
        if display_time[i] != 0:
            out_put += str(display_time[i]) + " " + intervals[i] + " "
    return out_put


# create input_data def for the functionality of the Add the current status button. The button's functionality is to get the spaceship's status input from users
def input_data():
    # create a window and set the its title, geometry
    status = Tk()
    status.geometry("650x500")
    status.title("Just input database")
    label_list = ["Current Velocity (m/s)", "Distance from Earth (m)", "Distance from Mars (m)",
              "Estimated time arrival (s)", "Current fuel level (number)", "Current fuel burn rate (speed/s)",
              "Current spaceship health (number)", "Current members health (number)"]
    # create 8 labels to display the name of input data
    for i in range(len(label_list)):
        label = Label(status, text=label_list[i], anchor="center", font=("Times", "16", "bold"))
        label.grid(column=0, row=i, pady=8)
    # create 8 entries to get the info of the spaceship from users.
    # creates a blue border for each entry
    entry_frame = [Frame(status, highlightcolor="blue", highlightthickness=2) for i in range(8)]
    # create entries
    entry_list = [Entry(entry_frame[i], relief=FLAT, width=50) for i in range(8)]
    # position each entry and its border on the grid
    for i in range(len(entry_list)):
        entry_frame[i].grid(column=1, row=i)
        entry_list[i].grid(column=1, row=i)
    # when the window is active, the border of the first entry is brightened
    entry_list[0].focus_set()
    # create two notices for wrong input from users and set their positions
    notice1 = Label(status, text="Distance from Earth and Distance from Mars must be positive, ", fg="red", anchor="center", font=("Times", "16", "bold"))
    notice2 = Label(status, text="other inputs must be greater or equal to 0", fg="red", anchor="center", font=("Times", "16", "bold"))
    notice1.grid(column=0, row=9, columnspan=2)
    notice2.grid(column=0, row=10, columnspan=2)

    # create save_button def for the Save button's functionality. When the button is clicked upon, all inputs are saved for further processes.
    def save_button():
        global save_move_distance, sign_of_error

        sign_of_error = 0
        with open("current_status.txt", "r+") as file:
            file.truncate(0)
            file.close()
        with open("save_status.txt", "r+") as file:
            file.truncate(0)
            file.close()
        with open("save_pos.txt", "r+") as file:
            file.truncate(0)
            file.close()
        astronaut_status.clear()
        # update the status with the current input
        astronaut_status.extend([items.get() for items in entry_list])
        # iterate through all items of the status, check and display errors
        for i in range(len(astronaut_status)):
            try:
                # if all input can be converted to float, then the input is correct. (only number under str type are acceptable)
                float(astronaut_status[i])
                if i + 1 == len(astronaut_status):
                    status.destroy()
                astronaut_status[i] = float(astronaut_status[i])
                if (i == 1) | (i == 2):
                    assert astronaut_status[i] >= 0
                else:
                    assert astronaut_status[i] > 0
            except ValueError:
                if astronaut_status[i] == "":
                    messagebox.showerror("Type Error", label_list[i] + " is a blank\n" + "You must fill all the blanks")
                else:
                    messagebox.showerror("Type Error", label_list[i] + " must be a integer or float not a string \n" +
                                         "\t\t        Try again")
                astronaut_status.clear()
                return
            except AssertionError:
                if (i == 1) | (i == 2):
                    messagebox.showerror("Value Error", label_list[i] + " must be greater than 0 \n" +
                                         "\t\t        Try again")
                else:
                    messagebox.showerror("Value Error", label_list[i] + " must be greater or equal to 0 \n" +
                                         "\t\t        Try again")
                astronaut_status.clear()
                return

        # the full distance between Earth and Mars is 650 pixel
        full_distance = 650
        # get distance from Mars and Mars from the austronaut_status
        Mar_distance = astronaut_status[2]
        Earth_distance = astronaut_status[1]
        # save_move_distance help to save the distance which the ship have moved and return it to the start point (fix bug)
        if save_move_distance != 0:
            canvas.move(item, -save_move_distance, 0)
            save_move_distance = 0
        #move the spaceship to the current distance when you fill in input data
        canvas.move(item, -full_distance / (Mar_distance + Earth_distance) * Earth_distance, 0)
        save_move_distance += -full_distance / (Mar_distance + Earth_distance) * Earth_distance
        #clear notification and content in blackboard
        canvas.itemconfig(notification, text="")
        clear_spaceship_status_list()
        # save data to file
        save_status(astronaut_status)
    #create Save button to run function save_button()
    save_input = Button(status, text="Save", command=save_button, width=25)
    save_input.grid(column=1, row=8)


def record_time():
    # Append the record to the file
    append_file = open('current_status.txt', 'a')
    append_file.write(dt.now().strftime('%Y/%m/%d - %H:%M:%S'))
    append_file.write('\n')
    append_file.close()
    return dt.now().strftime('%Y/%m/%d - %H:%M:%S')


def format_txt():
    # Save the existing file
    with open('current_status.txt', 'r') as time_record:
        lines = time_record.readlines()
        time_record.close()
    # Format the file (delete all lines and keep 2 chronologically earliest record)
    if len(lines) > 1:
        return lines[0].rstrip(), lines[-1].rstrip(), lines[-2].rstrip()


class current_status:
    # assign all the input data to variable to keep and use for calculating
    def __init__(self, current_velocity, distance_from_Earth, distance_from_Mars, estimated_time_arrival,
                 current_fuel_level, current_fuel_burn_rate, current_spaceship_health, current_members_health):
        self.current_velocity = current_velocity
        self.distance_from_Earth = distance_from_Earth
        self.distance_from_Mars = distance_from_Mars
        self.estimated_time_arrival = estimated_time_arrival
        self.current_fuel_level = current_fuel_level
        self.current_fuel_burn_rate = current_fuel_burn_rate
        self.current_spaceship_health = current_spaceship_health
        self.current_members_health = current_members_health

    def status_calculation(self, interval, stop):
        global sign_of_error
        # calculate next distance when press start
        stop.distance_from_Earth = self.current_velocity * interval + self.distance_from_Earth
        stop.distance_from_Mars = self.distance_from_Mars - self.current_velocity * interval
        # To check the ship has reached the Mars or not and stop the program
        if stop.distance_from_Mars <= 0:
            clear_spaceship_status_list()
            canvas.itemconfig(notification, text="MISSION COMPLETE!!!", font=("Ariel", 36), justify=CENTER, fill="red")
        # If the ship has not reached the Mars, the program continue to calculate the next figures and assign it to the variable
        else:
            stop.estimated_time_arrival = stop.distance_from_Mars / stop.current_velocity
            stop.current_fuel_level = self.current_fuel_level - (self.current_fuel_burn_rate * interval)
            stop.current_spaceship_health = self.current_spaceship_health - 0.04 * interval
            stop.current_members_health = self.current_members_health - 0.002 * interval
            # To check if fuel run out and stop program
            if stop.current_fuel_level < 0:
                clear_spaceship_status_list()
                canvas.itemconfig(notification, text="MISSION FAILED!!!\n Not enough fuel", font=("Ariel", 20),
                                  justify=CENTER, fill="red")
                sign_of_error += 1
                return
            # To check members health below 0 and stop program
            elif stop.current_members_health < 0:
                clear_spaceship_status_list()
                canvas.itemconfig(notification, text="MISSION FAILED!!!\n All people died", font=("Ariel", 20),
                                  justify=CENTER, fill="red")
                sign_of_error += 1
                return
            # to check spaceship health blow 0 and stop program
            elif stop.current_spaceship_health < 0:
                clear_spaceship_status_list()
                canvas.itemconfig(notification, text="MISSION FAILED!!!\n Spaceship was destroyed", font=("Ariel", 20),
                                  justify=CENTER, fill="red")
                sign_of_error += 1
                return
            # show the info in blackboard to illustrate the current status
            else:
                spaceship_status_list_label = ["Current_distance_from_Earth", "Current_distance_from_Mars", "Estimated_time_arrival",
                             "Current_fuel_level", "Current_spaceship_health", "Current_members_health"]
                details = [stop.distance_from_Earth, stop.distance_from_Mars, time_convert(stop.estimated_time_arrival),
                           stop.current_fuel_level, stop.current_spaceship_health, stop.current_members_health]
                print('', end='\n\n\n')
                print('**************************************')
                print('********* MOST RECENT STATUS *********')
                print('**************************************')
                for i in range(len(spaceship_status_list_label)):
                    canvas.itemconfig(spaceship_status_list[i], text=spaceship_status_list_label[i] + " is : " + str(details[i]))
                    print(spaceship_status_list_label[i] + " is : " + str(details[i]))

    def __str__(self):
        return 'This is the spaceship\'s current status'


# This function help to save all the data to file by import json library
def save_mess_file():
    global database
    with open("save_name_content.txt", "a") as add_content:
        add_content.write(json.dumps(database))
        add_content.write("\n")


# This function help to load the data and convert it into dict for using in program (also use json library)
def load_mess_file():
    global database
    with open("save_name_content.txt", "r") as read_content:
        content = read_content.readlines()
        # Get the newest content that has been saved
        if len(content) != 0:
            database = json.loads(content[-1])
            diary['value'] = (tuple(database.keys()))


load_mess_file()


def run():
    global save_move_distance, sign_of_error
    # if sign_of_error is 0 ,the program continue working, else, it stops the program (to check error)
    if sign_of_error != 0:
        return
    read_status()
    record = record_time()
    # save_interval help to calculate the time between the first and second when you press Start button
    save_interval = 0
    # if you press Start at first time, pass, else run the code below
    if format_txt() is not None:
        # save the time to two parameters
        # start : start time
        # end : end time
        start, end, end_ship = format_txt()
        # create two parameters to store data
        start_status = current_status(astronaut_status[0], astronaut_status[1], astronaut_status[2], astronaut_status[3], astronaut_status[4],
                                      astronaut_status[5], astronaut_status[6], astronaut_status[7])
        end_status = current_status(astronaut_status[0], astronaut_status[1], astronaut_status[2], astronaut_status[3], astronaut_status[4],
                                    astronaut_status[5], astronaut_status[6], astronaut_status[7])
        # convert to 'Year/Month/Day - Hour/Minute/Second' format
        start = dt.strptime(start, '%Y/%m/%d - %H:%M:%S')
        end = dt.strptime(end, '%Y/%m/%d - %H:%M:%S')
        end_ship = dt.strptime(end_ship, '%Y/%m/%d - %H:%M:%S')
        # calculate the interval between two press times
        interval = end - start
        interval_ship = end - end_ship
        # convert save_interval to seconds
        save_interval = interval_ship.seconds
        # clear notification that appear in blackboard
        canvas.itemconfig(notification, text="")
        # run the function and calculate the next status
        current_status.status_calculation(start_status, interval.seconds, end_status)
    # when you press Start at first time, it will show notification
    else:
        canvas.itemconfig(notification,
                          text="Start at " + record + "\nTry to run the second \ntime to get the end time",
                          fill="yellow", anchor="nw", font=("Ariel", 24, "bold"))
    # play music whenever click the Start button
    pygame.init()
    click_music = pygame.mixer.Sound('click.wav')
    pygame.mixer.Sound.play(click_music)
    # Earth_position: 530
    # Mars_position: 100
    Mar_distance = astronaut_status[2]
    Earth_distance = astronaut_status[1]
    full_distance = 650
    pos = canvas.coords(item)
    """
    :parameter time_interval          : save the time and use to calculate spaceship_x_coordinate
    :parameter spaceship_x_coordinate : the distance which the ship need to move 
    :parameter pos                    : get position of the ship and assign it to pos variable (a list)
    note : canvas.coords() help to get (x, y) and return it to a list 
    """
    spaceship_x_coordinate = -full_distance / (Mar_distance + Earth_distance) * save_interval * astronaut_status[0]
    # the ship will continue to move if it has not reached the Mars
    if pos[0] + spaceship_x_coordinate > 100:
        canvas.move(item, spaceship_x_coordinate, 0)
        save_move_distance += spaceship_x_coordinate
    # this help to fix bug when the spaceship_x_coordinate was over the Mars_distance.This code will instantly move the ship to the Mars
    else:
        canvas.move(item, -(pos[0] - 100), 0)
        save_move_distance += -(pos[0] - 100)
    save_pos(save_move_distance)


big_font = font.Font(family='Time New Roman', size=20)
small_font = font.Font(family='Time New Roman', size=17)

binary_clock = Button(window, text="Project 35", fg='black', width=15, height=2, bg='yellow', font=big_font
                      )
binary_clock_button = canvas.create_window(600, 570, anchor="nw", window=binary_clock)
status = Button(window, text="Add new current status", font=small_font, command=input_data)
status_button = canvas.create_window(600, 450, anchor="nw", window=status)
start = Button(window, text="Start", font=("Time New Roman", 16, "bold"), command=run, bg="#6F00FF", fg="white",
               image=circle_image, compound=LEFT, width=100, height=40)
start_button = canvas.create_window(846, 449, anchor="nw", window=start)


def add_message():
    # create window for add_message
    add_mes_win = Tk()
    add_mes_win.title("Astronaut's messages :D")
    save_time = (dt.now().strftime('%Y/%m/%d - %H:%M:%S'))

    # add input from user to database (a dict) and combobox for checking message
    def message():
        database[title.get()] = [note.get("1.0", END), save_time]
        diary['value'] = (tuple(database.keys()))
        save_mess_file()
        add_mes_win.destroy()
    # display labels which is known as GUI for program
    content_label = Label(add_mes_win, text="Content", font=("Ariel", 16))
    name_label = Label(add_mes_win, text="Name", font=("Ariel", 16))
    current_time = Message(add_mes_win, text=dt.now().strftime('%Y/%m/%d - %H:%M:%S'), fg="red",
                           font=("Ariel", 10, "bold"), width=1000)
    title = Entry(add_mes_win, width=106)
    note = Text(add_mes_win)
    button = Button(add_mes_win, text="Save", command=message)
    current_time.grid(column=0, row=0)
    name_label.grid(column=0, row=1)
    title.grid(column=0, row=2)
    content_label.grid(column=0, row=3)
    note.grid(column=0, row=4)
    button.grid(column=0, row=5)
    # store the content in file
    load_mess_file()


new_message = Button(canvas, text="Add message", font=("Time New Roman", 10, "bold"), command=add_message, fg="red",
                     width=43, height=1)
add_message_button = canvas.create_window(600, 500, anchor="nw", window=new_message)


# Check message


def check():
    check_win = Tk()
    check_win.geometry("900x700")
    check_win.title("Checking for sureeeee")
    check_win.configure(bg="grey")
    key = diary.get()
    if key not in database.keys():
        check_win.destroy()
        messagebox.showerror("Type Error", "Could not find related content")
        return
    content_label = Label(check_win, text="Content", font=("Ariel", 16, "bold"), anchor="nw", fg="red", bg="grey")
    name_label = Label(check_win, text="Name", font=("Ariel", 16, "bold"), anchor="nw", fg="red", bg="grey")
    name = Label(check_win, text=key, borderwidth=1, font=("Helvetica", "16"), relief="solid", width=50,
                 bg="cyan", fg="purple")
    content = Text(check_win, font=("Helvetica", "16"), borderwidth=1, relief="solid", width=50,
                   bg="cyan", fg="purple")
    content.insert(INSERT, database[key][0])
    content.configure(state=DISABLED)
    time_label = Label(check_win, text=database[key][1], font=("Helvetica", 32, "bold"), fg="red", anchor="nw",
                       bg="grey")
    name_label.grid(column=0, row=0)
    name.grid(column=1, row=0)
    content_label.grid(column=0, row=3)
    content.grid(column=1, row=3)
    time_label.grid(column=1, row=5)


check_message = Button(window, text="Check message", width=14, height=1, font=("Time New Roman", 10), command=check)
check_message_button = canvas.create_window(600, 535, anchor="nw", window=check_message)


def music_section():
    global music_background_image, start_music_image, stop_music_image
    music_window = Toplevel()
    music_window.geometry("500x500")
    music_window.title("Space Music")
    music_canvas = Canvas(music_window, width=500, height=500)
    music_canvas.pack(fill="both", expand=True)

    def start_play(song):
        pygame.init()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(-1)

    def stop_play():
        pygame.init()
        pygame.mixer.music.stop()

    music_background_image = ImageTk.PhotoImage(Image.open("background_music.jpg").resize((200, 200), Image.ANTIALIAS))
    music_canvas.create_image(50, 150, anchor="nw", image=music_background_image)

    start_music_image = ImageTk.PhotoImage(Image.open("start_music.png").resize((20, 20), Image.ANTIALIAS))
    stop_music_image = ImageTk.PhotoImage(Image.open("stop_music.png").resize((100, 100), Image.ANTIALIAS))

    music_list = ['Angel.mp3', 'Solo.mp3', 'background.wav', 'call_me_by_your_name.mp3', 'special_music.mp3', 'Lost_control.mp3', 'Phoenix.mp3']
    play_button_1 = Button(music_canvas, image=start_music_image, relief=FLAT, command=lambda: start_play(music_list[0]))
    play_button_2 = Button(music_canvas, image=start_music_image, relief=FLAT, command=lambda: start_play(music_list[1]))
    play_button_3 = Button(music_canvas, image=start_music_image, relief=FLAT, command=lambda: start_play(music_list[2]))
    play_button_4 = Button(music_canvas, image=start_music_image, relief=FLAT, command=lambda: start_play(music_list[3]))
    play_button_5 = Button(music_canvas, image=start_music_image, relief=FLAT, command=lambda: start_play(music_list[4]))
    play_button_6 = Button(music_canvas, image=start_music_image, relief=FLAT, command=lambda: start_play(music_list[5]))
    play_button_7 = Button(music_canvas, image=start_music_image, relief=FLAT, command=lambda: start_play(music_list[6]))

    songs_name = ['Angel With Shotgun', 'Solo', 'Signature Music', 'Call Me By Your Name', 'Special Music', 'Lost Control', 'Phoenix']
    play_buttons = [play_button_1, play_button_2, play_button_3, play_button_4, play_button_5, play_button_6, play_button_7]
    for i in range(7):
        song_label = Label(music_canvas, text=songs_name[i], anchor="w")
        music_canvas.create_window(275, 160+30*i, window=song_label, anchor="w")
        music_canvas.create_window(420, 160+30*i, window=play_buttons[i])

    stop_music = Button(music_canvas, image=stop_music_image, relief=FLAT, command=stop_play)
    music_canvas.create_window(150, 425, window=stop_music)


music_image = ImageTk.PhotoImage(Image.open("123.png").resize((81, 81), Image.ANTIALIAS))
music_playlist = Button(canvas, image=music_image, bg='blue', command=music_section)
music_playlist_button = canvas.create_window(865, 570, anchor="nw", window=music_playlist)
# binary_clock with tkinter-----------------------------------------------------------
canvas.create_rectangle(5, 70, 200, 130, fill="yellow")
time = canvas.create_text(100, 100, text="", font=("Ariel", 36), fill="red")
dot_x_coordinates = [163, 137, 96, 70, 29, 3]
dot_locations = [(coords, 140+20*i) for coords in dot_x_coordinates for i in range(4)]
dot_list = [canvas.create_oval(10, 10, 25, 25, fill="white") for i in range(24)]
for i in range(len(dot_list)):
    canvas.move(dot_list[i], dot_locations[i][0], dot_locations[i][1])
binary_numbers = [8, 4, 2, 1]
for j in range(4):
    canvas.create_text(205, 158+20*j, text=binary_numbers[j], fill="light green", font=("Ariel", 16))


def clear_color():
    for items in dot_list:
        canvas.itemconfig(items, fill="white")


def run_clock():
    canvas.itemconfig(time, text=dt.now().strftime('%H:%M:%S'))
    # run the clock after 1000 miliseconds (i.e. 1 second)
    window.after(1000, lambda: run_clock())
    # clear the color every second
    clear_color()
    # get the datetime and divide it into hour, minute, and second records. Each record has two components, the left digit and the right digit
    # left digit is calculated by floor division (i.e. // operator)
    # right digit is calculated by taking the record and record modular 10
    sec1 = dt.now().second % 10
    sec2 = dt.now().second // 10
    mn1 = dt.now().minute % 10
    mn2 = dt.now().minute // 10
    hr1 = dt.now().hour % 10
    hr2 = dt.now().hour // 10
    # turtles 1->4 are

    def clock_logic(col_str):
        i = 'temporary variable'
        # if col_str
        if col_str == 'sec1':
            i = 3
            col = sec1
        elif col_str == 'sec2':
            i = 7
            col = sec2
        elif col_str == 'mn1':
            i = 11
            col = mn1
        elif col_str == 'mn2':
            i = 15
            col = mn2
        elif col_str == 'hr1':
            i = 19
            col = hr1
        elif col_str == 'hr2':
            i = 23
            col = hr2
        if col == 1:
            canvas.itemconfig(dot_list[i], fill="orange")
        elif col == 2:
            canvas.itemconfig(dot_list[i-1], fill="orange")
        elif col == 3:
            canvas.itemconfig(dot_list[i], fill="orange")
            canvas.itemconfig(dot_list[i-1], fill="orange")
        elif col == 4:
            canvas.itemconfig(dot_list[i-2], fill="orange")
        elif col == 5:
            canvas.itemconfig(dot_list[i], fill="orange")
            canvas.itemconfig(dot_list[i-2], fill="orange")
        elif col == 6:
            canvas.itemconfig(dot_list[i-2], fill="orange")
            canvas.itemconfig(dot_list[i-1], fill="orange")
        elif col == 7:
            canvas.itemconfig(dot_list[i-2], fill="orange")
            canvas.itemconfig(dot_list[i-1], fill="orange")
            canvas.itemconfig(dot_list[i], fill="orange")
        elif col == 8:
            canvas.itemconfig(dot_list[i-3], fill="orange")
        elif col == 9:
            canvas.itemconfig(dot_list[i-3], fill="orange")
            canvas.itemconfig(dot_list[i], fill="orange")
    clock_logic('sec1')
    clock_logic('sec2')
    clock_logic('mn1')
    clock_logic('mn2')
    clock_logic('hr1')
    clock_logic('hr2')


run_clock()
window.mainloop()
