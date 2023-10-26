from tkcalendar import Calendar
from tkinter import *
import mysql.connector

# Opening MySQL
mydb = mysql.connector.connect(host='localhost', user='root', password='root', database='bush')
c = mydb.cursor()

# Primary window (Part-1)
win = Tk()
win.config(bg="#FFE6D3")
win.title("CS PROJECT")
title = Label(win, text="PERIOD MAP", bd=10, relief=SUNKEN, fg="#FE0303", bg="#EBFFD7",
              font=("Lucida Calligraphy", 30, "underline", "bold"), pady=3)
title.pack(fill=X)
w = Label(win, text="Welcome user! Please enter the required details to know about your upcoming period dates",
          bd=8, relief=GROOVE, fg="dark blue", bg="#FFFBD7", font=("Comic Sans MS", 16, "bold"), pady=1)
w.pack(fill=X)

info = Label(win, text="KINDLY READ THIS INFORMATION!!\n"
                      "A menstrual cycle is measured from the first day\n"
                      "of your period to the first day of your next\n"
                      "period. The average length of a menstrual cycle\n"
                      "is 28 to 29 days, but every woman's cycle is\n"
                      "different. For example, teenagers might have\n"
                      "cycles that last 45 days, whereas women\n"
                      "in their 20s to 30s have cycles that\n"
                      "last 21 to 38 days.\n"
                      "Menstruation is commonly known as a period.\n"
                      "When you menstruate, your uterus lining sheds\n"
                      "and flows out of your vagina. Your period\n"
                      "contains blood, mucus and some cells from the\n"
                      "lining of your uterus. The average length of a\n"
                      "period is 3 to 7 days.\n\n"
                      "Ovulation is when an egg is released from the\n"
                      "ovary, and is critical to the whole process. For\n"
                      "people with regular cycles, ovulation likely\n"
                      "occurs 10-16 days before the next period.\n"
                      "The eggs released during ovulation can only be\n"
                      "fertilized for 12 to 24 hours.",
             font=("MV Boli", 14, "bold"), bd=8, relief=SUNKEN, fg="#FF0000", bg="#A5FF95")
info.place(x=1032, y=130, relheight=0.82, relwidth=0.33)


def hoho():
    # Connecting to MySQL
    y = "insert into t1 values(" + "'" + e1.get() + "'" + "," + e2.get() + "," + e3.get() + "," + e4.get() + "," + e5.get() + "," + e6.get() + ")"
    c.execute(y)
    mydb.commit()


    # Calendar window (Event design)
    class Agenda(Calendar):
        def __init__(self, master=None, **kw):
            Calendar.__init__(self, master, **kw)
            for i, row in enumerate(self._calendar):
                for j, label in enumerate(row):
                    self._cal_frame.rowconfigure(i + 1, uniform=1)
                    self._cal_frame.columnconfigure(j + 1, uniform=1)
                    label.configure(justify="center", anchor="n", padding=(1, 4))

        def _display_days_without_othermonthdays(self):
            year, month = self._date.year, self._date.month
            cal = self._cal.monthdays2calendar(year, month)
            while len(cal) < 6:
                cal.append([(0, i) for i in range(7)])

            week_days = {i: 'normal.%s.TLabel' % self._style_prefixe for i in range(7)}
            week_days[self['weekenddays'][0] - 1] = 'we.%s.TLabel' % self._style_prefixe
            week_days[self['weekenddays'][1] - 1] = 'we.%s.TLabel' % self._style_prefixe
            _, week_nb, d = self._date.isocalendar()
            if d == 7 and self['firstweekday'] == 'sunday':
                week_nb += 1
            modulo = max(week_nb, 52)
            for i_week in range(6):
                if i_week == 0 or cal[i_week][0][0]:
                    self._week_nbs[i_week].configure(text=str((week_nb + i_week - 1) % modulo + 1))
                else:
                    self._week_nbs[i_week].configure(text='')
                for i_day in range(7):
                    day_number, week_day = cal[i_week][i_day]
                    style = week_days[i_day]
                    label = self._calendar[i_week][i_day]
                    label.state(['!disabled'])
                    if day_number:
                        txt = str(day_number)
                        label.configure(text=txt, style=style)
                        date = self.date(year, month, day_number)
                        if date in self._calevent_dates:
                            ev_ids = self._calevent_dates[date]
                            i = len(ev_ids) - 1
                            while i >= 0 and not self.calevents[ev_ids[i]]['tags']:
                                i -= 1
                            if i >= 0:
                                tag = self.calevents[ev_ids[i]]['tags'][-1]
                                label.configure(style='tag_%s.%s.TLabel' % (tag, self._style_prefixe))

                            text = '%s\n' % day_number + '\n'.join([self.calevents[ev]['text'] for ev in ev_ids])
                            label.configure(text=text)
                    else:
                        label.configure(text='', style=style)

        def _display_days_with_othermonthdays(self):
            year, month = self._date.year, self._date.month

            cal = self._cal.monthdatescalendar(year, month)

            next_m = month + 1
            y = year
            if next_m == 13:
                next_m = 1
                y += 1
            if len(cal) < 6:
                if cal[-1][-1].month == month:
                    i = 0
                else:
                    i = 1
                cal.append(self._cal.monthdatescalendar(y, next_m)[i])
                if len(cal) < 6:
                    cal.append(self._cal.monthdatescalendar(y, next_m)[i + 1])

            week_days = {i: 'normal' for i in range(7)}
            week_days[self['weekenddays'][0] - 1] = 'we'
            week_days[self['weekenddays'][1] - 1] = 'we'
            prev_m = (month - 2) % 12 + 1
            months = {month: '.%s.TLabel' % self._style_prefixe,
                      next_m: '_om.%s.TLabel' % self._style_prefixe,
                      prev_m: '_om.%s.TLabel' % self._style_prefixe}

            week_nb = cal[0][1].isocalendar()[1]
            modulo = max(week_nb, 52)
            for i_week in range(6):
                self._week_nbs[i_week].configure(text=str((week_nb + i_week - 1) % modulo + 1))
                for i_day in range(7):
                    style = week_days[i_day] + months[cal[i_week][i_day].month]
                    label = self._calendar[i_week][i_day]
                    label.state(['!disabled'])
                    txt = str(cal[i_week][i_day].day)
                    label.configure(text=txt, style=style)
                    if cal[i_week][i_day] in self._calevent_dates:
                        date = cal[i_week][i_day]
                        ev_ids = self._calevent_dates[date]
                        i = len(ev_ids) - 1
                        if i >= 0:
                            tag = self.calevents[ev_ids[i]]['tags'][-1]
                            label.configure(style='tag_%s.%s.TLabel' % (tag, self._style_prefixe))

                        text = '%s\n' % date.day + '\n'.join([self.calevents[ev]['text'] for ev in ev_ids])
                        label.configure(text=text)


    # Calendar window (Event Configuration)
    if __name__ == '__main__':
        import tkinter as tk
        root = tk.Tk()
        root.geometry("800x500")
        agenda = Agenda(root, selectmode='none')
        yy = int(e5.get())
        mm = int(e4.get())
        dd = int(e3.get())
        for i in range(0, int(e2.get())):
            agenda.calevent_create(agenda.datetime(yy, mm, dd) + agenda.timedelta(days=int(e6.get()) + i), 'Periods', 'message')
            agenda.tag_config('message', background='red', foreground='yellow')

        for j in range(0, 7):
            agenda.calevent_create(agenda.datetime(yy, mm, dd) + agenda.timedelta(days=int(e6.get()) + int(e6.get()) - 13 - j),
                                   'High pregnancy Chances', 'message2')
            agenda.tag_config('message2', background='yellow', foreground='red')

        agenda.calevent_create(agenda.datetime(yy, mm, dd) + agenda.timedelta(days=int(e6.get()) + int(e6.get()) - 14),
                               'Ovulation day', 'message2')

        agenda.pack(fill="both", expand=True)
        root.mainloop()

# Primary window (Part-2)
win.geometry("1300x800")
n = Label(win, text="Name:", font=("Comic Sans MS", 14, "bold"), bd=6, relief=RAISED, fg="#3C0978", bg="#C8FFE9")
n.place(x=30, y=130, relheight=0.1, relwidth=0.135)
p = Label(win, text="Period duration:", font=("Comic Sans MS", 14, "bold"), bd=6, relief=RAISED, fg="#3C0978", bg="#C8FFE9")
p.place(x=30, y=230, relheight=0.1, relwidth=0.135)
m = Label(win, text="Date of last\nperiod:", font=("Comic Sans MS", 14, "bold"), bd=6, relief=RAISED, fg="#3C0978",
          bg="#C8FFE9")
m.place(x=30, y=330, relheight=0.1, relwidth=0.135)
r = Label(win, text="Month of last\nperiod:", font=("Comic Sans MS", 14, "bold"), bd=6, relief=RAISED, fg="#3C0978",
          bg="#C8FFE9")
r.place(x=30, y=430, relheight=0.1, relwidth=0.135)
g = Label(win, text="Year:", font=("Comic Sans MS", 14, "bold"), bd=6, relief=RAISED, fg="#3C0978", bg="#C8FFE9")
g.place(x=30, y=530, relheight=0.1, relwidth=0.135)
o = Label(win, text="Duration of\nrepetition:", font=("Comic Sans MS", 14, "bold"), bd=6, relief=RAISED, fg="#3C0978",
          bg="#C8FFE9")
o.place(x=30, y=630, relheight=0.1, relwidth=0.135)
cap1 = Label(win, text="(Enter the month's number)", font=("Comic Sans MS", 14, "bold"), bd=8, relief=GROOVE,
             fg="#E00056", bg="#FFCFCF")
cap1.place(x=480, y=430, relheight=0.1, relwidth=0.35)
cap2 = Label(win, text="(Enter the beginning date of bleeding\nin numericals)", font=("Comic Sans MS", 14, "bold"),
             bd=8, relief=GROOVE, fg="#E00056", bg="#FFCFCF")
cap2.place(x=480, y=330, relheight=0.1, relwidth=0.35)

cap3=Label(win, text="(Enter the total no. of days of your"+"\n"+" last bleeding)", font = ("Comic Sans MS",14,"bold"), bd=8, relief=GROOVE,
           fg="#E00056", bg="#FFCFCF")
cap3.place(x=480, y=230, relheight=0.1, relwidth=0.35)
cap4=Label(win, text="(Enter the current year)", font = ("Comic Sans MS",14,"bold"), bd=8, relief=GROOVE, fg="#E00056", bg="#FFCFCF")
cap4.place(x=480, y=530, relheight=0.1, relwidth=0.35)
cap5=Label(win, text="(Enter the duration of repetion of"+"\n"+" your menstrual cycle)", font = ("Comic Sans MS",14,"bold"), bd=8, relief=GROOVE,
           fg="#E00056", bg="#FFCFCF")
cap5.place(x=480, y=630, relheight=0.1, relwidth=0.35)
cap6=Label(win, text="(Enter your full name)", font = ("Comic Sans MS",14,"bold"), bd=8, relief=GROOVE, fg="#E00056", bg="#FFCFCF")
cap6.place(x=480, y=130, relheight=0.1, relwidth=0.35)

e1=Entry(win, relief=SUNKEN, bd=6, font = ("Comic Sans MS",14,"bold"), fg="#207816", bg="#FFB892")
e1.place(x=250, y=130, relheight=0.1, relwidth=0.13)
e2=Entry(win, relief=SUNKEN, bd=6, font = ("Comic Sans MS",14,"bold"), fg="#207816", bg="#FFB892")
e2.place(x=250, y=230, relheight=0.1, relwidth=0.13)
e3=Entry(win, relief=SUNKEN, bd=6, font = ("Comic Sans MS",14,"bold"), fg="#207816", bg="#FFB892")
e3.place(x=250, y=330, relheight=0.1, relwidth=0.13)
e4=Entry(win, relief=SUNKEN, bd=6, font = ("Comic Sans MS",14,"bold"), fg="#207816", bg="#FFB892")
e4.place(x=250, y=430, relheight=0.1, relwidth=0.13)
e5=Entry(win, relief=SUNKEN, bd=6, font = ("Comic Sans MS",14,"bold"), fg="#207816", bg="#FFB892")
e5.place(x=250, y=530, relheight=0.1, relwidth=0.13)
e6=Entry(win, relief=SUNKEN, bd=6, font = ("Comic Sans MS",14,"bold"), fg="#207816", bg="#FFB892")
e6.place(x=250, y=630, relheight=0.1, relwidth=0.13)

btn=Button(win, text="Launch", width=10, command=lambda:hoho(), relief=RAISED, bd=5, font = ("Comic Sans MS",14,"bold"),
           activeforeground="#0043AA", activebackground="cyan", fg="red", bg="#FDFF4C")
btn.place(x=30, y=730)

win.mainloop()



    
              
