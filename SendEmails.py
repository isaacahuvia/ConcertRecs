"""
Send emails
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from BuildLists import find_related_artists
from BuildLists import find_local_concerts


def send_email(related_shows, toaddr):
	fromaddr = "concertrecs@gmail.com"
	frompw = "ikeikeike1"
	toaddr = toaddr

	msg = MIMEMultipart('alternative')
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Test subject"

	#Create body text in HTML
	body = """\
	<html>
	  <head align='center'>Upcoming Concerts</head>
	  <body>
	"""

	for show in related_shows:
		artist_block = ", ".join(show.lineup) if show.lineup else show.artist.name
		venue_block = show.venue
		date_block = str(show.date) if show.date else "Date not available"
		time_block = str(show.time) if show.time else "Time not available"
		cost_block = "-".join(["$" + str(round(float(amt))) for amt in show.cost]) if show.cost else "Cost not available"
		link = show.address

		body = body + """
		<table border='0' cellpadding='5' cellspacing = '5' width='100%'>
		  <tr>
		    <td align='center'>
		    """ + "<a href='" + link + "'>" + artist_block + "<br>" + venue_block + "</a>" + """
		    </td>
		  </tr>
		  <tr>
		  	<td>
		  	""" + date_block + "<br>" + time_block + """
		  	</td>
		  	<td>
		  	""" + "Price range: " + cost_block + """
		  	</td>
		  </tr>
		</table>
		<br><br>
		"""

	body = body + """
	  </body>
	</html>
	"""

	# msg.attach(MIMEText(body_alt, "plain"))
	msg.attach(MIMEText(body, 'html')) #the second attachment is preferred

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, frompw)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()