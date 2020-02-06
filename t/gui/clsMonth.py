from datetime import date as Date, timedelta as TimeDelta
import locale
import tkinter as tk

class number_color:
    def __init__(self, numb, col='grey'):
        self._number=numb
        self._color=col

    @property
    def number(self):
        return self._number

    @property
    def color(self):
        return self._color
    
class Month:
    def __init__(self, year, month):
        self._date = Date(year, month, 1)

    @property
    def year(self):
        return self._date.year
    
    @property
    def month(self):
        return self._date.month

    @property
    def name(self):
        return format(self._date, "%B")

    @property
    def calendardays(self):
        days=[]
        offset = self._date.weekday()
        for nr in range (offset-1,-1,-1):
            days.append(number_color(self.previous().days-nr))
            
        self.from_date(self.next())
        for nr in range(1,self.days+1):
            days.append(number_color(nr,'black'))
        nr = 1
        while len(days)%7:
            days.append(number_color(nr))
            nr+=1
        
        return days
        
    @property
    def days(self):
        return (self.next()._date - TimeDelta(days=1)).day
    
    def next(self):
        return self.from_date(self._date + TimeDelta(days=32))

    def previous(self):
        return self.from_date(self._date - TimeDelta(days=1))

    @classmethod
    def from_date(cls, date=None):
        if date is None:
            date = Date.today()
        return cls(date.year, date.month)
