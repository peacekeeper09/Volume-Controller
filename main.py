import tkinter as tk
import pygame
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume


class AudioControl:
    def __init__(self, master):
        self.master = master
        master.title("Audio Control")

        # Set up GUI elements
        self.mixer = pygame.mixer
        self.mixer.init()
        self.volume_scale = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL,
                                     label="Volume", command=self.set_volume, length=400,
                                     sliderlength=20, showvalue=False, highlightthickness=0)
        self.volume_scale.set(50)
        self.volume_scale.pack(side=tk.LEFT, padx=10)

        self.mute_button = tk.Button(master, text="Mute", command=self.toggle_mute, width=10,
                                     height=2, font=("Helvetica", 12))
        self.mute_button.pack(side=tk.RIGHT, padx=10)

        # Get audio sessions
        self.sessions = AudioUtilities.GetAllSessions()
        self.session_volumes = []
        for session in self.sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            self.session_volumes.append(volume)

    def set_volume(self, volume):
        volume_level = int(volume) / 100
        for volume in self.session_volumes:
            volume.SetMasterVolume(volume_level, None)

    def toggle_mute(self):
        for volume in self.session_volumes:
            if volume.GetMasterVolume() == 0:
                volume.SetMasterVolume(1, None)
                self.volume_scale.set(50)
                self.mute_button.config(text="Mute")
            else:
                volume.SetMasterVolume(0, None)
                self.volume_scale.set(0)
                self.mute_button.config(text="Unmute")


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioControl(root)
    root.geometry("500x100")
    root.mainloop()
