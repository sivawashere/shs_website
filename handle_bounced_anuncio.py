import logging, webapp2
from google.appengine.ext.webapp.mail_handlers import BounceNotificationHandler

class LogBounceHandler(BounceNotificationHandler):
	def receive(self, bounce_message):
		logging.info('Received bounce anuncio ... [%s]', str(self.request))
		logging.info('Bounce original: %s' + str(bounce_message.original))
		logging.info('Bounce notification: %s' + str(bounce_message.notification))

app = webapp2.WSGIApplication([LogBounceHandler.mapping()], debug=True)