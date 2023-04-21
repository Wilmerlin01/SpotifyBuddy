import tkinter as tk
from tkinter import ttk
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import sys
import pickle
import threading
import requests
from base64 import b64encode
import json
from urllib.parse import urlencode

def authenticate():
    try:
        if(len(var_dict["CLIENT_ID"]) == 0 or len(var_dict["CLIENT_SECRET"]) == 0):
            pass
        else:
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=var_dict["CLIENT_ID"], client_secret=var_dict["CLIENT_SECRET"], redirect_uri=REDIRECT_URI, scope=scope))
            user = sp.current_user()
            display_name = user['display_name']
            console_log.config(state='normal')
            console_log.insert('end', "Authentication successful: Welcome " + display_name + "\n")
            console_log.config(state='disabled')
            with open("saved_variables.pkl", "wb") as f:
                pickle.dump(var_dict, f)
    except spotipy.oauth2.SpotifyOauthError as error:
        print(error)
        console_log.config(state='normal')
        console_log.insert('end', str(error) + "\n")
        console_log.config(state='disabled')

def authenticate_in_thread():
    t = threading.Thread(target=authenticate)
    t.start()

#Variables
REDIRECT_URI = "http://localhost:8888/callback"
var_dict = {
    "CLIENT_SECRET": "",
    "CLIENT_ID": "",
    "CURRENT_PLAYLIST": "",
    "BINDING_ADD_SONG": "",
    "BINDING_REMOVE_LAST_ADDED": ""
}
root = tk.Tk()

#Loading variables from pickle file
if os.path.exists("saved_variables.pkl"):
    with open("saved_variables.pkl", "rb") as f:
        loaded_vars = pickle.load(f)
        var_dict = loaded_vars

# Create the widgets
label_client_secret = tk.Label(root, text="Client Secret")
entry_enter_client_secret = tk.Entry(root)
label_client_id = tk.Label(root, text="Client ID")
entry_enter_client_id = tk.Entry(root)
label_current_playlist = tk.Label(root, text="Current Playlist")
dropdown_playlists = ttk.Combobox(root)
label_action = tk.Label(root, text="Action")
label_binding = tk.Label(root, text="Binding")
label_add_song = tk.Label(root, text="Add Song")
entry_add_song_binding = tk.Entry(root)
label_remove_last_added = tk.Label(root, text="Remove Last Added")
entry_remove_last_added_binding = tk.Entry(root)
console_log = tk.Text(root, height=10, state='disabled')

#Authenticating with Spotify
scope = "user-library-read user-library-modify user-read-playback-state playlist-modify-public playlist-modify-private"
#cache_path = os.path.join(os.getcwd(), ".spotifycache")
try:
    if(len(var_dict["CLIENT_ID"]) == 0 or len(var_dict["CLIENT_SECRET"]) == 0):
        pass
    else:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=var_dict["CLIENT_ID"], client_secret=var_dict["CLIENT_SECRET"], redirect_uri=REDIRECT_URI, scope=scope))
        user = sp.current_user()
        display_name = user['display_name']
        console_log.config(state='normal')
        console_log.insert('end', "Authentication successful: Welcome " + display_name + "\n")
        console_log.config(state='disabled')
except spotipy.oauth2.SpotifyOauthError as error:
    print(error)
    console_log.config(state='normal')
    console_log.insert('end', str(error) + '\n')
    console_log.config(state='disabled')



#Load widget states
if len(var_dict["CLIENT_SECRET"]) != 0:
    entry_enter_client_secret.insert(0, var_dict["CLIENT_SECRET"])
    entry_enter_client_secret.config(state='disabled')
if len(var_dict["CLIENT_ID"]) != 0:
    entry_enter_client_id.insert(0, var_dict["CLIENT_ID"])
    entry_enter_client_id.config(state='disabled')
if len(var_dict["BINDING_ADD_SONG"]) != 0:
    entry_add_song_binding.insert(0, var_dict["BINDING_ADD_SONG"])
    entry_add_song_binding.config(state='disabled')
if len(var_dict["BINDING_REMOVE_LAST_ADDED"]) != 0:
    entry_remove_last_added_binding.insert(0, var_dict["BINDING_REMOVE_LAST_ADDED"])
    entry_remove_last_added_binding.config(state='disabled')

playlists = sp.current_user_playlists()
playlist_names = [playlist['name'] for playlist in playlists['items']]
dropdown_playlists['values'] = playlist_names
if len(var_dict["CURRENT_PLAYLIST"]) != 0:
    dropdown_playlists.set(var_dict["CURRENT_PLAYLIST"])
else:
    dropdown_playlists.set('')

#functions
def save_client_secret():
    var_dict["CLIENT_SECRET"] = entry_enter_client_secret.get()
    print("Client Secret: ", var_dict["CLIENT_SECRET"])
    entry_enter_client_secret.config(state='disabled')
    try:
        if(len(var_dict["CLIENT_ID"]) == 0 or len(var_dict["CLIENT_SECRET"]) == 0):
            pass
        else:
            authenticate_in_thread()
    except spotipy.oauth2.SpotifyOauthError as error:
        print(error)
        console_log.config(state='normal')
        console_log.insert('end', str(error) + "\n")
        console_log.config(state='disabled')

def save_client_id():
    var_dict["CLIENT_ID"] = entry_enter_client_id.get()
    print("Client ID:", var_dict["CLIENT_ID"])
    entry_enter_client_id.config(state='disabled')
    try:
        if(len(var_dict["CLIENT_ID"]) == 0 or len(var_dict["CLIENT_SECRET"]) == 0):
            pass
        else:
           authenticate_in_thread()
    except spotipy.oauth2.SpotifyOauthError as error:
        print(error)
        console_log.config(state='normal')
        console_log.insert('end', error + "\n")
        console_log.config(state='disabled')

def save_add_song_binding():
    var_dict["BINDING_ADD_SONG"] = entry_add_song_binding.get()
    print("Add Song Binding: ", var_dict["BINDING_ADD_SONG"])
    entry_add_song_binding.config(state='disabled')
    with open("saved_variables.pkl", "wb") as f:
        pickle.dump(var_dict, f)

def save_remove_last_added_binding():
    var_dict["BINDING_REMOVE_LAST_ADDED"] = entry_remove_last_added_binding.get()
    print("Remove Last Added Binding: ", var_dict["BINDING_REMOVE_LAST_ADDED"])
    entry_remove_last_added_binding.config(state='disabled')
    with open("saved_variables.pkl", "wb") as f:
        pickle.dump(var_dict, f)

# Bind the Entry widgets to functions
entry_enter_client_secret.bind("<Button-1>", lambda event: entry_enter_client_secret.config(state='normal'))
entry_enter_client_id.bind("<Button-1>", lambda event: entry_enter_client_id.config(state='normal'))

button_save_client_secret = tk.Button(root, text="Save", command=save_client_secret)
button_save_client_id = tk.Button(root, text="Save", command=save_client_id)

entry_add_song_binding.bind("<Button-1>", lambda event: entry_add_song_binding.config(state='normal'))
entry_remove_last_added_binding.bind("<Button-1>", lambda event: entry_remove_last_added_binding.config(state='normal'))

button_apply_add_song_binding = tk.Button(root, text="Apply", command=save_add_song_binding)
button_apply_remove_last_added_binding = tk.Button(root, text="Apply", command=save_remove_last_added_binding)

# Place the widgets in the grid layout
label_client_secret.grid(row=1, column=1)
entry_enter_client_secret.grid(row=1, column=2)
button_save_client_secret.grid(row=1, column=3)

label_client_id.grid(row=2, column=1)
entry_enter_client_id.grid(row=2, column=2)
button_save_client_id.grid(row=2, column=3)

label_current_playlist.grid(row=3, column=1)
dropdown_playlists.grid(row=3, column=2)

tk.Label(root, text="").grid(row=4, column=1, columnspan=2)

label_action.grid(row=5, column=1)
label_binding.grid(row=5, column=2)

label_add_song.grid(row=6, column=1)
entry_add_song_binding.grid(row=6, column=2)
button_apply_add_song_binding.grid(row=6, column=3)

label_remove_last_added.grid(row=7, column=1)
entry_remove_last_added_binding.grid(row=7, column=2)
button_apply_remove_last_added_binding.grid(row=7, column=3)

console_log.grid(row=8, column=1, columnspan=3)

root.mainloop()
