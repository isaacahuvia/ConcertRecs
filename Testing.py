"""
Testing
"""

from BuildLists import find_local_concerts
from BuildLists import find_related_artists
from SendEmails import send_email

# print('TEST CASE 1: find_related_artists("Ty Dolla $ign", 20) - should give single list of artist objects')
# print(find_related_artists("Ty Dolla $ign", 20))

# print('TEST CASE 2: find_related_artists(["50 Cent", "The Game", "Ja Rule"], 10) - should give list with artist objects of various weights')
# print(find_related_artists(["50 Cent", "The Game", "Ja Rule"], 10))

# print('TEST CASE 3: find_related_artists(100, 10) - should be error')
# print(find_related_artists(100, 10))

# print('TEST CASE 4: find_local_concerts("Noname", "Chicago", related = True, n_related_artists = 15)')
# output = find_local_concerts("Noname", "Chicago", related = True, n_related_artists = 15)
# for show in output.values():
#     print(show.artist.name)
#     print(show.lineup)
#     print(show.date)
#     print(show.address)

# print('TEST CASE 5: find_local_concerts(artist_list = ["Noname", "Chance", "Isaiah Rashad", "Rapsody"], city = "Chicago")')
# output = find_local_concerts(artist_list = ["Noname", "Chance", "Isaiah Rashad", "Rapsody"], city = "Chicago")
# for show in output:
#     print(show.artist.name)
#     print(show.artist.n_ref)
#     print(show.lineup)
#     print(show.venue)
#     print(show.cost)
#     print(show.date)
#     print(show.address)

#output = find_local_concerts(artist_list = ["Noname", "Kanye West", "The Roots", "Isaiah Rashad", "Rapsody", "A Tribe Called Quest"], city = "Chicago")

#send_email(output, "isaacahuvia@gmail.com")

# send_email(find_local_concerts(artist_list = ['Francis and the Lights', 'Solange', 'Neon Indian', 'MGMT'], city = 'Chicago'), "timikoyejo@uchicago.edu")

output1 = find_local_concerts(artist_list = ['Cage the Elephant', 'Saint Motel', 'Pain Impala', 'Alt J', 'Capital Cities'], city = "Detroit")
output2 = find_local_concerts(artist_list = ['Tipper', 'Griz', 'Big Gigantic', 'Clozee', 'Carivan Palace', 'Overwerk', 'The M Machine', 'Tennyson'], city = "Detroit")
send_email(output1, "ahuviaii@gmail.com")
send_email(output2, "ahuviaii@gmail.com")