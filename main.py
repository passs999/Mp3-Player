from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
from mutagen.mp3 import MP3

import pygame
import os
import shutil
import time

root = Tk()
root.title("MP3 Player")
root.geometry("600x500")

pygame.mixer.init()

def play_time():
    user = os.getlogin()
    current_time = pygame.mixer.music.get_pos() / 1000

    current_song = song_box.curselection()
    song = song_box.get(current_song)
    song = f"C:/Users/{user}/AppData/Local/MP3_Music/{song}"
    song_name = MP3(song)
    song_len = song_name.info.length
    convert_song_len = time.strftime("%M:%S", time.gmtime(song_len))

    if int(slider.get()) == int(song_len):
        pass
    elif paused:
        pass
    elif int(slider.get()) == int(current_time):
        slider_position = int(song_len)
        slider.config(to=slider_position, value=int(current_time))
    else:
        slider_position = int(song_len)
        slider.config(to=slider_position, value=int(slider.get()))
        convert_time = time.strftime("%M:%S", time.gmtime(int(slider.get())))
        next_time = int(slider.get()) + 1
        slider.config(value=next_time)
        status_bar.config(text=f"Time elapsed:{convert_time} of {convert_song_len}")
    status_bar.after(1000, play_time)


def start_song():
    status_bar.config(text="")
    slider.config(value=0)
    user = os.getlogin()
    song = song_box.get(ACTIVE)
    song = f"C:/Users/{user}/AppData/Local/MP3_Music/{song}"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()



global paused
paused = False
def pause_song(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


def next_song():
    status_bar.config(text="")

    user = os.getlogin()
    next = song_box.curselection()
    next = next[0]+1
    song = song_box.get(next)

    song = f"C:/Users/{user}/AppData/Local/MP3_Music/{song}"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(next)
    song_box.selection_set(next)
    slider.config(value=0)

def stop_music():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

def previous_song():
    status_bar.config(text="")

    user = os.getlogin()

    next = song_box.curselection()
    next = next[0]-1
    song = song_box.get(next)

    song = f"C:/Users/{user}/AppData/Local/MP3_Music/{song}"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(next)
    song_box.selection_set(next, last=None)
    slider.config(value=0)
def add_song():
    user = os.getlogin()
    song = filedialog.askopenfilename(title="Choose a song", filetypes=(("mp3 Files", "*.mp3"), ))
    song_name = song.split("/")
    shutil.copyfile(song, f"C:/Users/{user}/AppData/Local/MP3_Music/{song_name[-1]}")
    song_box.insert(END, song_name[-1])

def add_many_songs():
    user = os.getlogin()
    songs = filedialog.askopenfilenames(title="Choose a song", filetypes=(("mp3 Files", "*.mp3"), ))
    for i in songs:
        song_name = i.split("/")
        shutil.copyfile(i, f"C:/Users/{user}/AppData/Local/MP3_Music/{song_name[-1]}")
        song_box.insert(END, song_name[-1])

def delete_song():
    status_bar.config(text="")
    slider.config(value=0)
    user = os.getlogin()
    selected = song_box.get(ACTIVE)
    os.remove(f"C:/Users/{user}/AppData/Local/MP3_Music/{selected}")
    song_box.delete(ANCHOR)

def delete_all_songs():
    status_bar.config(text="")
    slider.config(value=0)
    song_box.delete(0, END)
    pygame.mixer.music.stop()
    user = os.getlogin()
    path = f"C:/Users/{user}/AppData/Local/MP3_Music/"
    shutil.rmtree(path)
    os.mkdir(path)


def slider(x):
    user = os.getlogin()
    song = song_box.get(ACTIVE)
    song = f"C:/Users/{user}/AppData/Local/MP3_Music/{song}"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider.get()))

def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

def load_songs():
    user = os.getlogin()
    lst = os.listdir(f"C:/Users/{user}/AppData/Local/MP3_Music/")
    for i in lst:
        song_box.insert(END, i)

def saved_songs():
    user = os.getlogin()
    path = f"C:/Users/{user}/AppData/Local/MP3_Music/"
    os.startfile(path)

master_frame = Frame(root)
master_frame.pack(pady=20)

song_box = Listbox(master_frame, bg="white", fg="black", width=60)
song_box.grid(row=0, column=0)

volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1)

controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0)

load_songs()

pause_button_img = PhotoImage(data="iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAd+SURBVGhD3dnJUhVLEAbgOq0oIgo47Qwfypdhx9KtERjhzghcs4E9a55FHHBmUDm3vgyTW54LnOaEfRf8ERX0X105VGbW0IfRuKJUfPjwoXhcWVkpXdeVT58+lZ8/f5Y7d+6UGzdulG/fvpXDw8Ny+/btMj8/X46OjsrXr1/LzZs3y+LiYvn161f5+PFjuXbtWlleXqayvH//PnQ+ePAg+FA26OqCVZycnEQbjUbBGWw54C3w33GIcS0HvJVJPoSNUZ3R2ENGzYxFSdTMXERESdRExrO+W7duReSOj4/Lly9fyvXr18vS0lIo3d/fD6P37t0Lne/evYu/Q9rozK6dYfI2au17aPlklJJrifY9pM6/aWNU627shSjB3bt3o+ZEQE2KyNzcXPn+/XtERpREzbM+74wxlgxZOoBOxkXN36Fs8L/2dfFgkHQnN1vcswY4tJyDODmcXMrgrcxQNugd1Z2jjhvHrgAiYKCoqF/1arAIicyPHz9iN/GszztjjCVDlg5IneodhrLB/46QFBqkEcItLJwQbvY44IRxUcLJ4eRwenGNU/qS/20b+Kh2xAoyYxABCg1kQFQMJiSFyT2nIn2tM3RA6nQmwJA2OgM0UdOZnAI8lYhOCuGU4WlYw8m1/ODg4JQPZSMmV+s3MiI9QChTSlFy6dU865vkxpJJDqlTScCQNjozsnCkShM13JUBJ4BTmOnMxYpTjItK6sBlIrmrh77kQ9gY1Y4/T6IpEBURsXucBwYzYpO4SE7mlE3auAxOL42uER5dIyhy0FDqcqYWM6quERbv8+fPy9bWVkRDesmK0OPHj8vGxkYof/v2bfQ/evQoOHj3+vXryIYJizp5B96LFy/ioPMuL42fP3+OZ3aNdUk03vUG2JBJi2WsWStadSZ4dfwPLnM4rK2tmfy5rUY9xqVO8rC5uXnm+LZBncAfNvmC86XlWtqQifHe3l4ogHrVDl5LI3iNSPB0Bp48eXKmE21zGU28efMm9D19+vTMsW3b3d0NGTY5CDVzwetFMXjNTPCajeDQZRqVUW5rLbfQ8Do2OOROcRHoUQpkrAvp7yNHBthU4uStN5zO9AtX1sk7taf5yLEu1Cqu3nHCOGV56WNgGhYWFmK86zZ5EIxpsA6NIyOIuVZxAcGtV1zDraPOTsFJDstOctHDRQjnPN4X9BgvauT7gl22yJgQHbKJp05jcA3neycTPkF9sGi1LoOLKG5nwUUHh76RdaEjY6cREDqmQUUAmxwlz1mcTpxeXLbx+Cyg3AwZ4mDyjEjWtuc+E0jEllhBJiJWeR/5XCOZGTL6cL7hfMPTL+8754Q92QydJeoOV4e4aOCE85O1zxrJqNnnc89PJy+CiuAcGY6zqSpw2cJ9XOF8x2Xm9McHEWujxtnJKPaZQIJc6ky0uvqCzbRLvuWQvFO/ouZz9P79+7F74TKDO11xacwfD/o4JGoiRqbu+aflMQ3qnWNsWtzkbRg4nbh1gcsGzvf//PgA0/j/gcva7MzIXcjszFIUcXsz7uDBRUdkoU3teRBZa4QMeSVmnU2DijAJMjJIvt4qysOHD0Mn7uzAM9t8/7eAe6DPBC5CnyhP2ujDtS53K7MzSxHBrRHcGsFFB4c+DqlntZvZhj7niN2OY2RUAZvWiLVMJ55nE99xa3mmH+j6oJWx0LXJaJ6F3OVaeXLksy+5lujsx7JhL9bUIW4/x0UDFx0c+jgkstaZqF1mjbALbKoCNlUFTidOLy4TuDVT9V/+B7o+oMf4y8hARr61mTx1GpN+4XzvzM66kBk1LSK4uxbuVMXVNw5t2s+Dm4HxeTYBR6bB6c1BMhykw+0Cd9fCZQbXcGtmph/o+iDLiIzSyChOQ06WTQEjrw/nG843nO/JO2vC2WFH0EQE9z2Cu/DhHMP7wreDCJKRbc7k5C4Cu8AmJ8lzGKcTl21cJnBtph/oRHcayBjPMc/AxjSQYYuMDOICgKdOvrVcdqyJ+DauHdF82OM+9Fteo3v63b66umqRnNvqbSDGpU7ydfLjra2tM8e3LeVam3zB+dJyLW2M6sET/7HKw852phbjkKnlIG11YGzLtmLPri3Pnj0rOzs7kTERMTYPzZcvX4YOJQWuEaLr3fb2dllfXz8dr1+E6Xz16lXYZYNdG45S994WKwNKqs41DkyytmG4Mj/QdRRrFlBNVUQGV8+4qOGyhkO+z6s1eI/LqO3SGOO996yxYUw6Kco45yFtgvGyhpsgriJwGUuduE1lpL4IGgxKRURElMHkHNUmuWd9xpJJDqlTMGBIG50ZORTVomaXwWUm6xMXHRxwBnB1i4sSLkq4TOCag0tf8iFsjGpHZIRSkF4zVx4UMyIKlImCZ32e9SU3lgzZ3GZTJwdgSBsz/4hNkah41id6rtbKKHerXA8ujTCUDROc6Qc6nEMZUZwcTg7XcAs0+VA26J3pHNF3mT2+PUdgCBsz/UCHU4KTw8nh5PBWhgP4UDa8vzprJFhFkNp+zysMtRz0tcCzz7iWg2c6EkPZiHZl1ghFWsJLfDJqLVpuHG5cy9sxk/zv2yjlH/OknxeRrvjnAAAAAElFTkSuQmCC")
start_button_img = PhotoImage(data="iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAelSURBVGhD3drJihRPEMfx7HLfd+8e9B18Ar2LoAcXUFAUT76GouKG4lwEUcGzB4++gGe9eHXf963/+YmZaOrf40z3LK3gD5Kpb1ZmRGTkUtWlnW5VqXr16lVxuW7dutI0TXn79m358eNHWbVqVVm8eHH5+PFj+fLlS1mxYkVZunRp+fr1a/nw4UNZsmRJWblyZfn582d58+ZNWbBgQVm7di2T5eXLl2Fz48aNwaPywVYTVPXr168onU4nmMM2E24LT+Qh2rWZcLtP8ih8dOqIui4ya0YsS7Jm5DIiS7ImM67VLVu2LDL37du38v79+7Jw4cKyZs2aMPr69etwun79+rD54sWL+DtKH43RtUeY3M5a+z61uT9LyUqqfZ/S5nz66NR113VDlmj16tWx5mTAmpSRRYsWlU+fPkVmZEnWXKtzTxtt9dGXDWKTc1nzd1Q+xF/rmrjQyHQnGy12rRCmNgsQ64f1yz643WdUPtjt1JOjtuvGqUAyoKGsWL/Wq8YyJDPfv3+P08S1Ove00VYffdmgtGm906h8iL/RyRRqpOiEbSysEzZ6TFhnLEtYP6wfZhcrglKXPN8+cKdWxA4yYpIBBjXkQFY01olh9/01nWlIm3Yw2lDa9EygYXywmzwTH40GiqypTGYAp5Hly5cHP3nyJFhwOB0rWL82f/78uceDfEgQJixgPMhHDK6u35gR00M65ZQyhA3iyJEj5erVq9HGU/XmzZtl586dwZ7I2uqTs0Vp05Kg6XxgS0hJG/08nQ8Pq+6zZ8/qvXHV14jg2jC4ZrF7//59g51U6rHavXfvXrSrWYq/dfqj//Pnz4Pp6dOn0/p49+5dcM1ucJ3FYEmmmvHg+hAM/p2PTt39gppSTokLFy6UEydOTNRM1oYNG8qZM2fKvn37gk13tR3Xs5HMz7R/I1DF8nBMWvvYes5jMzfrVPLitn///pj269ev92zo7wE2yIflgW3m9IktK2xpYhscSxRWsKO4YUxRaS8kexvFlGt8kARy4MCBCODWrVtl06ZNZfPmzT2bU/mw3rF+6ROzhyUI29TYgNIGlpjGiOoajVcAxSmD3cSmWIeZSJ+9e/fGErlz5044FtRUPpxC2EAw4ezjdMJmAksINttYaWSFQcbyWGuzYHonwyy0e/fu6H/79u2JmhIz0fYh41gCMGG+sRnDYss+WIKSdQ45AZwENQvBTghM165d651Ucyk1sO7Y2FjYpPrCFz6cSlRXR7BTi5xiuGY/2CmHnXop7ORtrH8jNlqZSpZFTHg+VP2WQ4cORaYvXrwYvy3sI/V8qG/7VI8tOSw2LDasYLEPfI6YobNnz/42w/NRLl26FH5kv+7FuJ7Nc6SxPo3Qxqoc6zVHjGVJRkalY8eOhY86oN5sYDH4KwaxYbFhsWEl77sI/Yk9Mkw5ffp0+CQzJIah9kjtHJJ1pd4Lbs9E1v0JnTx5MnzbQ2bILGASh+tk6vHf3iPTlW3btkUMQ+2RWiZlvJ//lh49elQePnw4fioNUOMTjdeIOjOljjBe0bEnJzZt+RP1b6iukHizcEz74FBnIj44YLFjsY/uOJoHbd26tWzfvj3esVLt/UG9PeIDXXutWYe4Pnwmarrdc+fO/W/t/onSf3rZy94EyP7FYk/N6gPdKHX58uXwd/z48d6XErF4VmQcyUpPRucUcFopZgL7TJTndf2J28vUqEo9bsOXeDzlxeCvGOpbbnB9OQw2Mzjjtorqo2L6D3SUz5NR6NSpU5FpT3gz4EcazhUhhmRxYLFhBYvdp/0YYa2I4imKrUtM58+f/20W51Lae6D+cgyf3rH49Berx2YGmxnsuYIVbKYGfqCrfsZHPA9izy9HNu0Bf4l9PmVYG8LuYzOBxYbFhsWePPADnU/9V65cKUePHo37s5Vfirt27Yrr+CFUlT488ASk3qCSXWew6rTVR3zipIx74Ac6MuLZqr5wRmYNwvr3kGWv7SMD1S59YgHjHJyC9WtzDM47v44ZrE45pTlyr9iWwrDS1wAOHjwY7OsJTeUj2RJSXKvrZ231Saa02RiR00LAipnB3jyxTjIwjDjxBdJa3rNnz0Tt+ECm8yEoLGhM2FLC7GKZTxvYR4zkeflAJ4AbN270gudgLpJ5CZyRaoeQ1xKvxjULwe0fVg8ePGB1Uqm/ubt3796NNqR9PkQJ+1yamspHzXTwXD4+dDSuQcVyoP51i316OXz4cBkbG4s23pAdozt27AjO06e9jilt5jqezgdmQ+nntKntVD46RqOx12KqWYqbvudaMj6C2Ud5//Hjx2XLli1hlEH7pz6Y4gQxQPVeq93Lf8WtWQse5MNruvXuWp2viD6+DeOjY9pcyDrZiBraiJwwIguMqHPPRpMRde5po23eZ4PSpsBoGB/sps2Z+Oj9zwcjdGmERioDOssAY3nyeEDqzJAfX67VmVXPCcvIv5+TZwabfqjRqHwY4MAPdDpjjjFhAWVGsX5YP6xgSyV5VD7YHXqPzGX9/ok9MvADHUfYtUKYEawf1g/rh9t9BIBH5cP9f2ePBFUF1DIxrnDUZlLXFs467dpMrtlIjcpHlH9mjzCkpNzE/Vlrq83aYe3a3G7Tz/Pvo5T/APlxJ7YYZp12AAAAAElFTkSuQmCC")
forward_button_img = PhotoImage(data="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")
back_button_img = PhotoImage(data="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")
stop_button_img = PhotoImage(data="iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABHNCSVQICAgIfAhkiAAAAAFzUkdCAK7OHOkAAAAEZ0FNQQAAsY8L/GEFAAAACXBIWXMAABYlAAAWJQFJUiTwAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAATNJREFUaEPtmVuKhDAQRePrS/ega9PdCbom3YN+KdpeqBkYxiRtN623pQ4EEz/MPT4ipIJ1w9yAUI5fj4qwoSJsHFq1hmEwfd+bIAjkzGdApDzPTZZlcuYJIOKjbds1jmMIn9qiKFqbppEUbrwiZVnuTnJmQwYfThHcjb0LX9F8T8b5jSRJYuZ5ltG1bK+2maZJRv+xrlrjONJIAGRBJhtWka7rpMeDK5NVJAz5fjGuTHxpX0RF2FARNlSEDRVhQ0XYUBE2VIQNFWFDRdhQETZUhA2ryLIs0uPBlcm694vtyUP1iRNAfSZNUxn95f6b2KCua+ldjzcLnoiLqqp+axRXtbcLPT+g9La9ZruTfLKh9Ia5n+FQMRQLALb2zyiGFkVh/bD3OCTCjP7Z2VARNm4iYswDinhaQ5SZI9QAAAAASUVORK5CYII=")

pause_button = Button(controls_frame, image=pause_button_img, borderwidth=0, command=lambda: pause_song(paused))
start_button = Button(controls_frame, image=start_button_img, borderwidth=0, command=start_song)
forward_button = Button(controls_frame, image=forward_button_img, borderwidth=0, command=next_song)
back_button = Button(controls_frame, image=back_button_img, borderwidth=0, command=previous_song)
stop_button = Button(controls_frame, image=stop_button_img, borderwidth=0, command=stop_music)

pause_button.grid(row=0, column=2, padx=5)
start_button.grid(row=0, column=1, padx=5)
forward_button.grid(row=0, column=4, padx=5)
back_button.grid(row=0, column=0, padx=5)
stop_button.grid(row=0, column=3, padx=5)

menu = Menu(root)
root.config(menu=menu)


add_song_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song", command=add_song)
add_song_menu.add_command(label="Add Many Songs", command=add_many_songs)
add_song_menu.add_command(label="Saved Songs Location", command=saved_songs)

remove_song_menu = Menu(menu, tearoff = 0)
menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete One Song", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs", command=delete_all_songs)

status_bar = Label(root, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM)

slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=250, command=slider)
slider.grid(row=2, column=0, pady=30)

volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, length=125, command=volume)
volume_slider.pack()

root.mainloop()