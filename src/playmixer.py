import sys
import glob
import os
import time
import csv
import webbrowser
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth
from tkinter import *
from random import *
from PIL import ImageTk, Image
from tkinter.ttk import *
from pprint import *
import tkinter.messagebox


class AuthWindow:

    def __init__(self):
        self.authWindow = Tk()
        self.authWindow.wm_title("Spotify Authentication")
        self.username = StringVar()
        img = ImageTk.PhotoImage(Image.open("logo.png"))
        self.L1 = Label(self.authWindow, image=img)
        self.L2 = Label(self.authWindow, text="Spotify User Name:")
        self.L3 = Label(self.authWindow, text="Redirected URL:")
        self.E1 = Entry(self.authWindow, textvariable=self.username)
        self.E2 = Entry(self.authWindow)
        self.B1 = Button(self.authWindow, command=lambda: self.authcmd(), width=10, text="LOGIN")
        self.B2 = Button(self.authWindow, command=lambda: self.grabresponse(), width=10, text="RESPONSE")
        self.L1.grid(columnspan=3, row=0)
        self.L2.grid(column=0, row=1)
        self.E1.grid(column=1, row=1)
        self.B1.grid(column=2, row=1)
        self.authWindow.mainloop()

    def grabresponse(self):
        response = self.E2.get()
        username = self.username.get()
        code = self.sp_auth.parse_response_code(response)
        token_info = self.sp_auth.get_access_token(code)
        token = token_info['access_token']
        if code:
            spotify = spotipy.Spotify(auth=token)
            self.L2.configure(text="Login Successful")
            self.authWindow.destroy()
            MenuWindow(spotify, username)
        else:
            self.L2.configure(text=("Error Logging Into", self.username, "Make sure the correct details were entered."))

    def authcmd(self):
        username = self.username.get()
        scope = 'playlist-modify-private playlist-modify-public playlist-read-private playlist-read-collaborative '
        self.sp_auth = oauth.SpotifyOAuth('1cf3b8418ecb47a49c0f7d1310747802', '83783723564748dea00ec41f61c493cf',
                                     'http://localhost/', scope=scope, cache_path=".cache-" + username)
        token_info = self.sp_auth.get_cached_token()
        if not token_info:
            auth_url = self.sp_auth.get_authorize_url()
            webbrowser.open(auth_url, 2, autoraise=True)
            self.E2.grid(column=1, row=2)
            self.B2.grid(column=2, row=2)
            self.L3.grid(column=0, row=2)
            tkinter.messagebox.showinfo("Enter URL",
                                        "Please copy / paste the URL you were redirected to into the"
                                        " Redirect Bar (URL will begin with localhost)")
        if token_info:
            token = token_info['access_token']
            spotify = spotipy.Spotify(auth=token)
            self.L2.configure(text="Login Successful")
            self.authWindow.destroy()
            MenuWindow(spotify, username)


class Question:
    def __init__(self, q, a1, a2, a3, a4, question_type):
        self.q = q
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.question_type = question_type


class QuizWindow:

    def __init__(self):
        self.questionWindow = Tk()
        self.questionWindow.wm_title("PlayMixer Quiz")
        self.qq = StringVar()
        self.qa1 = StringVar()
        self.qa2 = StringVar()
        self.qa3 = StringVar()
        self.qa4 = StringVar()
        self.randomList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.l1 = Label(self.questionWindow, text="", width=40)
        self.b1 = Button(self.questionWindow, command=lambda: self.scoring(1, self.question), text="", width=20)
        self.b2 = Button(self.questionWindow, command=lambda: self.scoring(2, self.question), text="", width=20)
        self.b3 = Button(self.questionWindow, command=lambda: self.scoring(3, self.question), text="", width=20)
        self.b4 = Button(self.questionWindow, command=lambda: self.scoring(4, self.question), text="", width=20)
        self.csv_entry = Entry(self.questionWindow)
        self.csv_label = Label(self.questionWindow, text="Enter Desired Filename:")
        self.exit_button = Button(self.questionWindow, command=lambda: self.finish(), text="Finish Quiz",
                                  width=12)
        self.l1.grid(column=0, row=0)
        self.b1.grid(column=0, row=1)
        self.b2.grid(column=1, row=1)
        self.b3.grid(column=0, row=2)
        self.b4.grid(column=1, row=2)
        self.rock = self.pop = self.rap = self.electronic = self.short = self.med = self.long = 0
        self.acoustic = self.val = self.dance = self.live = self.energy = 0.5
        self.question = Question("How much do you like acoustic music?", "I love it", "I like it", "It's alright",
                                 "I hate it", "acoustic")
        self.l1.configure(text=self.question.q)
        self.b1.configure(text=self.question.a1)
        self.b2.configure(text=self.question.a2)
        self.b3.configure(text=self.question.a3)
        self.b4.configure(text=self.question.a4)
        self.questionWindow.mainloop()

    def generation(self):
        if not self.randomList:
            self.question = Question("All questions answered", "", "", "", "", "")
            self.b1.grid_remove()
            self.b2.grid_remove()
            self.b3.grid_remove()
            self.b4.grid_remove()
            self.csv_label.grid(column=0, row=1)
            self.csv_entry.grid(column=1, row=1)
            self.exit_button.grid(column=2, row=1)
        else:
            rand_choice = choice(self.randomList)
            if rand_choice == 1:
                self.question = Question("What's your favorite music genre?", "Rock", "Pop", "Rap", "Electronic",
                                         "genre")
            elif rand_choice == 2:
                self.question = Question("What is the most important aspect of a song?", "Guitar Solos",
                                         "Melody", "Beat", "Harmonies", "genre")
            elif rand_choice == 3:
                self.question = Question("What's your favourite musical instrument?", "Electric Guitar", "Drum Machine",
                                         "Piano", "Synthesiser", "genre")
            elif rand_choice == 4:
                self.question = Question("Who's the best Beatle?", "George", "Paul", "John", "Ringo", "genre")
            elif rand_choice == 5:
                self.question = Question("Do you like positive songs?", "I love them", "I like them",
                                         "I prefer sad songs", "Happy songs are the worst!", "val")
            elif rand_choice == 6:
                self.question = Question("Do happy endings exist?", "Of course they do!", "They do sometimes", "Rarely",
                                         "Happiness is a lie", "val")
            elif rand_choice == 7:
                self.question = Question("How heavy do you like your songs?", "I LIKE THEM LOUD!", "Fun and lively",
                                         "I prefer slower songs", "Quiet and gentle", "energy")
            elif rand_choice == 8:
                self.question = Question("Why do you listen to music?", "To party!", "To liven up my mood",
                                         "To wind down", "To sleep to", "energy")
            elif rand_choice == 9:
                self.question = Question("What's your preferred song length?", "Short", "Medium",
                                         "Long", "N/A", "length")
            elif rand_choice == 10:
                self.question = Question("Pink Floyd or the Sex Pistols?", "The Sex Pistols", "They're both good",
                                         "Pink Floyd", "I don't know either", "length")
            elif rand_choice == 11:
                self.question = Question("Do you dance to music", "I love dancing!",
                                         "At Parties", "Rarely", "never", "dance")
            elif rand_choice == 12:
                self.question = Question("How important is the beat / groove?", "Very Important", "Quite Important",
                                         "Somewhat important", "Not important", "dance")
            elif rand_choice == 13:
                self.question = Question("Do you like live recordings?", "Yes!", "Sometimes", "Not really",
                                         "Studio Only","live")
            elif rand_choice == 14:
                self.question = Question("Do you go to gigs?", "Of course!", "I want to", "Rarely", "Never", "live")
            elif rand_choice == 15:
                self.question = Question("Which genre do you prefer?", "Folk Music", "Soft Pop",
                                         "Metal", "Dance Music", "acoustic")
            self.randomList.remove(rand_choice)
        self.l1.configure(text=self.question.q)
        self.b1.configure(text=self.question.a1)
        self.b2.configure(text=self.question.a2)
        self.b3.configure(text=self.question.a3)
        self.b4.configure(text=self.question.a4)

    def scoring(self, button, question):
        if question.question_type == "genre":
            if button == 1:
                self.rock += 10
            elif button == 2:
                self.pop += 10
            elif button == 3:
                self.rap += 10
            elif button == 4:
                self.electronic += 10
        elif question.question_type == "length":
            if button == 1:
                self.short += 10
            elif button == 2:
                self.med += 10
            elif button == 3:
                self.long += 10
        elif question.question_type == "val":
            if button == 1:
                self.val += 0.2
            elif button == 2:
                self.val += 0.1
            elif button == 3:
                self.val -= 0.1
            elif button == 4:
                self.val -= 0.2
        elif question.question_type == "acoustic":
            if button == 1:
                self.acoustic += 0.2
            elif button == 2:
                self.acoustic += 0.1
            elif button == 3:
                self.acoustic -= 0.1
            elif button == 4:
                self.acoustic -= 0.2
        elif question.question_type == "energy":
            if button == 1:
                self.energy += 0.2
            elif button == 2:
                self.energy += 0.1
            elif button == 3:
                self.energy -= 0.1
            elif button == 4:
                self.energy -= 0.2
        elif question.question_type == "dance":
            if button == 1:
                self.dance += 0.2
            elif button == 2:
                self.dance += 0.1
            elif button == 3:
                self.dance -= 0.1
            elif button == 4:
                self.dance -= 0.2
        elif question.question_type == "live":
            if button == 1:
                self.live += 0.2
            elif button == 2:
                self.live += 0.1
            elif button == 3:
                self.live -= 0.1
            elif button == 4:
                self.live -= 0.2
        self.generation()

    def finish(self):
        desname = self.csv_entry.get()
        filename = (desname + ".csv")
        export = open(filename, mode='w')
        if self.rock > max(self.pop, self.rap, self.electronic):
            genre = "rock"
        elif self.pop > max(self.rock, self.rap, self.electronic):
            genre = "pop"
        elif self.rap > max(self.pop, self.rock, self.electronic):
            genre = "hip-hop"
        elif self.electronic > max(self.pop, self.rap, self.rock):
            genre = "electronic"
        else:
            genre = "pop"
        if self.long > self.med:
            length = "360000"
        elif self.med > self.short:
            length = "240000"
        else:
            length = "150000"
        val = str(round(self.val, 1))
        acoustic = str(round(self.acoustic, 1))
        energy = str(round(self.energy, 1))
        dance = str(round(self.dance, 1))
        live = str(round(self.live, 1))
        export_list = [genre, length, val, acoustic, energy, dance, live]
        writer = csv.writer(export)
        writer.writerow(export_list)
        self.questionWindow.destroy()


class ResultsWindow:
    def __init__(self):
        self.resultsWindow = Tk()
        self.resultsWindow.wm_title("Previous Quiz Results")
        homepath = os.getcwd()
        os.chdir(homepath)
        path = glob.glob("*.csv")
        self.c1 = Combobox(self.resultsWindow, values=path)
        self.b1 = Button(self.resultsWindow, text="Select", command=lambda: self.retrieve())
        self.b2 = Button(self.resultsWindow, text="Exit", command=lambda: self.exitResults())
        self.c1.grid(column=0, row=0)
        self.b1.grid(column=1, row=0)
        self.b2.grid(column=1, row=1)
        self.resultsWindow.mainloop()

    def exitResults(self):
        self.resultsWindow.destroy()

    def retrieve(self):
        try:
            desfile = self.c1.get()
            file = open(desfile, mode="r")
            data = file.read()
            data = str(data)
            datalist = []
            datalist.append(data)
            for entry in datalist:
                entry1 = entry.split(",")
            tkinter.messagebox.showinfo("Results", entry1)
        except FileNotFoundError:
            tkinter.messagebox.showinfo("File Not Found", "No results detected, please take the quiz first.")
            self.resultsWindow.destroy()


class GenerateWindow:

    def __init__(self, spotify, username):
        self.username = username
        self.spotify = spotify
        self.generateWindow = Tk()
        self.generateWindow.wm_title("Create A Playlist")
        playlist_length = ["5", "10", "15"]
        homepath = os.getcwd()
        os.chdir(homepath)
        path = glob.glob("*.csv")
        l1 = Label(self.generateWindow, text="Playlist Name:")
        l2 = Label(self.generateWindow, text="Results to Use")
        l3 = Label(self.generateWindow, text="Length of Playlist")
        self.e1 = Entry(self.generateWindow)
        b1 = Button(self.generateWindow, text="Generate Playlist", command=lambda: self.generate())
        self.b2 = Button(self.generateWindow, text="Exit", command=lambda: self.exitGenerate())
        self.c1 = Combobox(self.generateWindow, values=playlist_length)
        self.c2 = Combobox(self.generateWindow, values=path)
        l1.grid(column=0, row=0)
        l2.grid(column=0, row=1)
        l3.grid(column=0, row=2)
        self.e1.grid(column=1, row=0)
        self.c1.grid(column=1, row=2)
        self.c2.grid(column=1, row=1)
        b1.grid(column=1, row=3)
        self.b2.grid(column=0, row=3)
    
    def exitGenerate(self):
        self.generateWindow.destroy()
    
    def generate(self):
        des_name = self.e1.get()
        playlist = self.spotify.user_playlist_create(self.username, des_name)
        playlist_id = playlist['id']
        try:
            desfile = self.c2.get()
            file = open(desfile, mode="r")
            data = file.read()
            datalist = []
            datalist.append(data)
            playlist_len = int(self.c1.get())
            for entry in datalist:
                entry1 = entry.split(",")
            genre = entry1[0]
            length = entry1[1]
            val = entry1[2]
            acoustic = entry1[3]
            energy = entry1[4]
            dance = entry1[5]
            live = entry1[6]
            id_list = []
            import_dict = self.spotify.recommendations(seed_genres=genre, targert_duration_ms=length,
                                                       target_valence=val, target_acousticness=acoustic,
                                                       target_energy=energy, target_danceability=dance,
                                                       target_live=live, limit=playlist_len)
            track_list = import_dict['tracks']
            for i in range(0, playlist_len):
                track_info = dict(track_list[i])
                track_id = track_info['id']
                id_list.append(track_id)
            self.spotify.user_playlist_add_tracks(self.username, playlist_id, id_list)
        except FileNotFoundError:
            tkinter.messagebox.showinfo("File Not Found", "No results detected, please take the quiz first.")


class MenuWindow:
    def __init__(self, spotify, username):
        self.username = username
        self.spotify = spotify
        self.menuWindow = Tk()
        self.menuWindow.wm_title("PlayMixer Menu")
        img = ImageTk.PhotoImage(Image.open("logo.png"))
        l1 = Label(self.menuWindow, image=img)
        b1 = Button(self.menuWindow, command=self.quiz, text="Start Quiz")
        b2 = Button(self.menuWindow, command=self.results, text="View Previous Quiz Results")
        b3 = Button(self.menuWindow, command=self.generate, text="Generate a Playlist")
        l1.grid(columnspan=3, row=0)
        b1.grid(column=0, row=1)
        b2.grid(column=1, row=1)
        b3.grid(column=2, row=1)
        self.menuWindow.mainloop()

    def quiz(self):
        QuizWindow()

    def results(self):
        ResultsWindow()

    def generate(self):
        GenerateWindow(self.spotify, self.username)
AuthWindow()
