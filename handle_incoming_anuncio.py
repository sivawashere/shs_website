import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

def anuncio_key():
	return ndb.Key('Anuncio', "2014-2015") # Change every new school year

class Anuncio(ndb.Model):
	title = ndb.StringProperty(indexed=False)
	content = ndb.TextProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class ReceiveAnuncio(InboundMailHandler):
	def receive(self, msg):
		anuncio = Anuncio(parent=anuncio_key())
		anuncio.title = msg.subject
		content, texts = "", msg.bodies(content_type='text/html')
		for _, text in texts:
			content += text.decode()
		anuncio.content = content
		anuncio.put()

app = webapp2.WSGIApplication([ReceiveAnuncio.mapping()], debug=True)