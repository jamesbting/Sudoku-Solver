from tkinter import *
import time


class StopWatch(Frame):
    # Implements a stop watch frame widget.

    # constructor
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.e = 0
        self.m = 0
        self.makeWidgets(master)
        self.today = time.strftime("%d %b %Y %H-%M-%S", time.localtime())

    def makeWidgets(self,master):
        # Make the time label and appropriate widgest

        self.time_label = Label(master, textvariable=self.timestr,font = ("helvetica",30))
        self._setTime(self._elapsedtime)
        self.time_label.grid(row = 1, column = 0)

        self.start_button = Button(master, height=2, width=10,text='Start', command=self.start)
        self.start_button.grid(row = 2, column = 0)

        self.stop_button = Button(master, height=2, width=10,text='Stop', command=self.stop)
        self.stop_button.grid(row = 3, column = 0)

        self.reset_button = Button(master,height=2, width=10, text='Reset', command=self.reset)
        self.reset_button.grid(row = 4, column = 0)


    def _update(self):
        # Update the label with elapsed time.
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        # Set the time string to Minutes:Seconds:Hundreths
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        hseconds = int((elap - minutes * 60.0 - seconds) * 100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def _setLapTime(self, elap):
        # Set the time string to Minutes:Seconds:Hundreths
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        hseconds = int((elap - minutes * 60.0 - seconds) * 100)
        return '%02d:%02d:%02d' % (minutes, seconds, hseconds)

    def start(self):
        # Start the stopwatch, ignore if running.
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def stop(self):
        #Stop the stopwatch, ignore if stopped.
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def reset(self):
        #Reset the stopwatch
        self._start = time.time()
        self._elapsedtime = 0.0
        self.laps = []
        self.lapmod2 = self._elapsedtime
        self._setTime(self._elapsedtime)
