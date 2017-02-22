"""
Build show lists
"""

import requests
import urllib.parse
import re
import lxml
import sys
from datetime import datetime
from bs4 import BeautifulSoup

from Classes import Artist
from Classes import Show


""" Find related artists """
def find_related_artists(artist_list, n):

    #this list will store the list of related artists, all of class Artist so we can track their occurences
    related_artists = []

    if type(artist_list) == str:
        artist = artist_list
        artist_encoded = urllib.parse.quote_plus(artist)
        url = "http://ws.audioscrobbler.com/2.0/?api_key=430711e29ad09c493dad2831eb0bbd08&format=json&artist=" + artist_encoded + "&method=artist.getSimilar"
        all_related = [artist['name'] for artist in requests.get(url).json()['similarartists']['artist']]
        related_artists_trimmed = all_related[0:n]
        related_artists_trimmed.append(artist_list)
        for related_artist in related_artists_trimmed:
            if related_artist not in related_artists:
                related_artist = Artist(related_artist, 1)
                related_artists.append(related_artist)
            else:
                related_artist = Artist(related_artist, related_artist.n_ref + 1)
                related_artists['related_artist'] = related_artist

    elif type(artist_list) == list and type(artist_list[0]) == str:
        related_artist_names = [] #to keep track of how many times a name has come up; another way to do this would be to write something like if related_artist not in x.name for x in related_artists_trimmed (i.e. going through the list of names and not the list of Artist objects, which is not searchable for strings), but I don't know how to do that. It also indexes identically to related_artists, allowing us to use related_artist_names.index('name') to get the index for an artist in related_artists.
        for i in range(len(artist_list)):
            artist = artist_list[i]
            artist_encoded = urllib.parse.quote_plus(artist)
            url = "http://ws.audioscrobbler.com/2.0/?api_key=430711e29ad09c493dad2831eb0bbd08&format=json&artist=" + artist_encoded + "&method=artist.getSimilar"
            try:
                all_related = [artist['name'] for artist in requests.get(url).json()['similarartists']['artist']]
            except:
                all_related = artist
            if type(all_related) == list:
                related_artists_trimmed = all_related[0:n]
                related_artists_trimmed.append(artist)
                for related_artist in related_artists_trimmed:
                    if related_artist not in related_artist_names:
                        related_artists.append(Artist(related_artist, 1))
                        related_artist_names.append(related_artist)
                    else:
                        related_artists[related_artist_names.index(related_artist)] = Artist(related_artist, related_artists[related_artist_names.index(related_artist)].n_ref + 1)
            else:
                related_artist = all_related
                if related_artist not in related_artist_names:
                    related_artists.append(Artist(related_artist, 1))
                    related_artist_names.append(related_artist)
                else:
                    related_artists[related_artist_names.index(related_artist)] = Artist(related_artist, related_artists[related_artist_names.index(related_artist)].n_ref + 1)



    else:
        sys.exit("Must supply either a single string or list of strings")

    return(related_artists)


""" Find local concerts """
def find_local_concerts(artist_list, city, related = True, days_ahead = 90, n_related_artists = 25, output_length = 10):
    city_url_friendly = city.replace(" ", "_")
    city_url = "http://acousti.co/feeds/metro_area/" + city_url_friendly + "?days=" + str(days_ahead)
    try:
        city_page = urllib.request.urlopen(city_url)
    except:
        city_url = "http://acousti.co/feeds/metro_area/" + city_url_friendly + "?days=" + str(days_ahead + 1)
        city_page = urllib.request.urlopen(city_url)

    city_soup = BeautifulSoup(city_page, "lxml")
    show_names_raw = city_soup.find_all("title")
    show_names_raw = show_names_raw[1:len(show_names_raw)] #Because show_names[0] is simply "Upcoming songkick events in Chicago"
    show_addresses_raw = city_soup.find_all("guid")
    
    show_names = []
    show_addresses = []
    
    if len(show_names_raw) == len(show_addresses_raw):
        for tag in show_names_raw:
            show_names.append(tag.text.strip())
        for tag in show_addresses_raw:
            show_addresses.append(tag.text.strip())
    elif len(show_names_raw) != len(show_addresses_raw):
        print("WARNING: Length of show names does not equal length of show addresses")
        
    show_dictionary = dict(zip(show_names, show_addresses))
    
    if related == True:
        related_artists = find_related_artists(artist_list, n_related_artists)
    elif related == False:
        related_artists = Artist(artist_list, 1)
        
    selected_show_names = []
    selected_show_addresses = []
    
    for artist_i in related_artists:
        if artist_i.name in str(show_names):
            artist_show_names = [name for name, address in show_dictionary.items() if artist_i.name in name]
            selected_show_names.append(artist_show_names)
            artist_show_addresses = [address for name, address in show_dictionary.items() if artist_i.name in name]
            selected_show_addresses.append(artist_show_addresses)
    
    #selected_show_names is a (perhaps nested) list of selected artists and their show names. An artist who appears twice will occupy one index of the list, but have a nested list of two show names. Likewise for selected_show_addresses
            
    selected_show_artist = []
    selected_show_lineup = []
    selected_show_venue = []
    selected_show_date = []
    selected_show_time = []
    selected_show_cost = []
    selected_show_cancelled_flag = []

    ## Get base show info from songkick
    for url_set in selected_show_addresses:
        for url in url_set:

            show_page = urllib.request.urlopen(url)
            show_soup = BeautifulSoup(show_page, "lxml")

            selected_show_artist_raw = show_soup.find("span", class_ = "artist-name")
            selected_show_artist_cleaned = selected_show_artist_raw.text.strip()
            #if artist found isn't actually in our list of artists, mark this entry None
            selected_show_artist.append(next((x for x in related_artists if x.name == selected_show_artist_cleaned), None))

            #use div class = "line-up", or find_all a data-analytics-label_ = "line_up_artist"
            selected_show_lineup_raw = show_soup.find("div", class_ = "line-up")
            if not selected_show_lineup_raw:
                selected_show_lineup.append([])
            else:
                selected_show_lineup_cleaned = selected_show_lineup_raw.text.strip()
                selected_show_lineup_cleaned = selected_show_lineup_cleaned.split(",")
                selected_show_lineup_cleaned = [re.sub(r".*\n", "", name) for name in selected_show_lineup_cleaned]
                selected_show_lineup.append(selected_show_lineup_cleaned)
           
            selected_show_venue_raw = show_soup.find("div", class_= "location")
            selected_show_venue_cleaned = selected_show_venue_raw.text.strip()
            selected_show_venue_cleaned = selected_show_venue_cleaned.replace("\n", " ")
            selected_show_venue_cleaned = selected_show_venue_cleaned.replace(" (map)", "")
            selected_show_venue.append(selected_show_venue_cleaned)
            
            selected_show_date_raw = show_soup.find("div", class_ = "date-and-name")
            selected_show_date_cleaned = selected_show_date_raw.text.strip()
            #Cancelled flag
            if "Cancel" in selected_show_date_cleaned:
                selected_show_cancelled_flag.append("Cancelled")
            else:
                selected_show_cancelled_flag.append([])
            selected_show_date_cleaned = re.sub(r".*\n", "", selected_show_date_cleaned)
            selected_show_date.append(selected_show_date_cleaned)
            
            selected_show_time_raw = show_soup.find("div", class_ = "additional-details-container")
            if not selected_show_time_raw:
                selected_show_time.append([])
            else:
                selected_show_time_cleaned = selected_show_time_raw.text.strip()
                try:
                    selected_show_time_cleaned = str(selected_show_time_cleaned)[0:selected_show_time_cleaned.index(": ") + 5] #trim to just time, defined as up to two spots after the first ': ' symbol (i.e. in Doors Open: 21:00)
                except:
                    selected_show_time_cleaned = selected_show_time_cleaned
                selected_show_time.append(selected_show_time_cleaned)            
            
            selected_show_cost_raw = show_soup.find_all("span", class_ = "price")
            if not selected_show_cost_raw: 
                selected_show_cost.append([])
            elif len(selected_show_cost_raw) > 0:
                cost_set = []
                for cost in selected_show_cost_raw:
                    cost = cost.text.strip()
                    starts = [i + 1 for i, string in enumerate(cost) if string == "$"]
                    decimals = [i for i, string in enumerate(cost) if string == "."]
                    ends = [i + 3 for i in decimals]
                    cost_minmax = []
                    for i in range(0, len(starts)):
                        cost_minmax.append(float(cost[starts[i]:ends[i]]))
                    cost_set.append(cost_minmax)
                selected_show_cost.append([min(min(cost_set)), max(max(cost_set))])

    #un-nest show address list (previously nested by artist), so that its index matches that of other concert info
    selected_show_addresses_unnested = []
    for obj in selected_show_addresses:
        if type(obj) == str:
            selected_show_addresses_unnested.append(obj)
        if type(obj) == list:
            for subobj in obj:
                selected_show_addresses_unnested.append(subobj)

    ## Metacritic artist page link
    #e.g. http://www.metacritic.com/person/aap-rocky?filter-options=music





    ## Youtube link 
    #by going to search page, finding link to top video, navigating to that page, getting video
    #e.g. https://www.youtube.com/results?search_query=a%24ap+rocky





    ## Artist portrait




    
    show_list = []
    for i in range(len(selected_show_addresses_unnested)):
        if selected_show_artist[i] != None: #i.e. if the show artist does match one on the list of related artists
            if not selected_show_addresses_unnested[i] in show_list:
                show_list.append(Show(selected_show_artist[i], selected_show_lineup[i], selected_show_venue[i], selected_show_date[i], selected_show_time[i], selected_show_cost[i], selected_show_cancelled_flag[i], selected_show_addresses_unnested[i]))

    #Keep 10 most relevant shows, sorted by recency
    show_list.sort(key = lambda x: x.artist.n_ref, reverse = True)
    show_list = show_list[:output_length - 1] 
    show_list.sort(key = lambda x: datetime.strptime(x.date[x.date.index(" ") + 1:], "%d %B %Y"))

    if show_list == []:
        sys.exit("No shows found")
    else:
        return(show_list)
    
    
"""
Add:
    >add 'related to' field to bottom of output
    >link to venue site for cost block
    >link to metacritic, popular youtube song (embed?), artist portrait (embed)
    >set up accounts, regular email dispatches
    >reformat email
"""