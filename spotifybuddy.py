import tkinter as tk
from tkinter import ttk
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import sys

#Variables
CLIENT_SECRET = "test"
CLIENT_ID = ""
REDIRECT_URI = "http://localhost:8000/callback"
scope = "user-library-read user-library-modify user-read-playback-state playlist-modify-public playlist-modify-private"
cache_path = os.path.join(os.getcwd(), ".spotifycache")

root = tk.Tk()

# Create the widgets
label_client_secret = tk.Label(root, text="Client Secret")
entry_enter_client_secret = tk.Entry(root)
if len(CLIENT_SECRET) != 0:
    entry_enter_client_secret.insert(0, CLIENT_SECRET)
    entry_enter_client_secret.config(state='disabled')


label_client_id = tk.Label(root, text="Client ID")
entry_enter_client_id = tk.Entry(root)
if len(CLIENT_ID) != 0:
    entry_enter_client_id.insert(0, CLIENT_ID)
    entry_enter_client_secret.config(state='disabled')


label_current_playlist = tk.Label(root, text="Current Playlist")
dropdown_playlists = ttk.Combobox(root, values=["Playlist 1", "Playlist 2", "Playlist 3"])

label_action = tk.Label(root, text="Action")
label_binding = tk.Label(root, text="Binding")

label_add_song = tk.Label(root, text="Add Song")
entry_add_song_binding = tk.Entry(root)

label_remove_last_added = tk.Label(root, text="Remove Last Added")
entry_remove_last_added_binding = tk.Entry(root)

console_log = tk.Text(root, height=10, state="disabled")

#functions

def save_client_secret():
    CLIENT_SECRET = entry_enter_client_secret.get()
    print("Client Secret:", CLIENT_SECRET)
    entry_enter_client_secret.config(state='disabled')

def save_client_id():
    CLIENT_ID = entry_enter_client_id.get()
    print("Client ID:", CLIENT_ID)
    entry_enter_client_id.config(state='disabled')

# Bind the Entry widgets to functions
entry_enter_client_secret.bind("<Button-1>", lambda event: entry_enter_client_secret.config(state='normal'))
entry_enter_client_id.bind("<Button-1>", lambda event: entry_enter_client_id.config(state='normal'))

button_save_client_secret = tk.Button(root, text="Save", command=save_client_secret)
button_save_client_id = tk.Button(root, text="Save", command=save_client_id)





# Place the widgets in the grid layout

label_client_secret.grid(row=1, column=1)
entry_enter_client_secret.grid(row=1, column=2)

label_client_id.grid(row=2, column=1)
entry_enter_client_id.grid(row=2, column=2)

button_save_client_secret.grid(row=1, column=3)
button_save_client_id.grid(row=2, column=3)

label_current_playlist.grid(row=3, column=1)
dropdown_playlists.grid(row=3, column=2)

tk.Label(root, text="").grid(row=4, column=1, columnspan=2)

label_action.grid(row=5, column=1)
label_binding.grid(row=5, column=2)

label_add_song.grid(row=6, column=1)
entry_add_song_binding.grid(row=6, column=2)
label_remove_last_added.grid(row=7, column=1)
entry_remove_last_added_binding.grid(row=7, column=2)

console_log.grid(row=8, column=1, columnspan=3)

root.mainloop()
