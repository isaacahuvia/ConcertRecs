"""
Classes
"""

class Artist:
    def __init__(self, name, n_ref):
        self.name = name
        self.n_ref = n_ref
    
    def name(self):
        return self.name

    def n_ref(self):
        return self.n_references


class Show(object):
    def __init__(self, artist, lineup, venue, date, time, cost, cancelled_flag, address):
        self.artist = artist
        self.lineup = lineup
        self.venue = venue
        self.date = date
        self.time = time
        self.cost = cost
        self.cancelled_flag = cancelled_flag
        self.address = address
   
    def get_artist(self):
        return self.artist

    def get_lineup(self):
        return self.lineup

    def get_venue(self):
        return self.venue

    def get_date(self):
        return self.date

    def get_time(self):
        return self.time

    def get_cost(self):
        return self.cost

    def get_cancelled_flag(self):
        return self.cancelled_flag

    def get_address(self):
        return self.address