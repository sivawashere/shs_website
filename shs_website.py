import os, webapp2, jinja2, csv
from handle_incoming_anuncio import Anuncio, anuncio_key

env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def ausencias(nombre):
	ausencias = []
	for fname in os.listdir('asistencia'):
		fecha, ext = os.path.splitext(fname)
		if ext == '.csv':
			with open('asistencia/' + fname, 'rb') as f:
				for row in csv.reader(f):
					if row[0] == nombre and row[1] == "No":
						ausencias.append([fecha, row[2]])
	return ausencias

def get(nombre, folder):
	data, fname = [], folder + '/' + nombre + '.csv'
	if os.path.exists(fname):
		with open(fname, 'rb') as f:
			for row in csv.reader(f):
				data.append(row[:3])
		return data[1:]

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write(env.get_template('index.html').render({
			'anuncios': Anuncio.query(ancestor=anuncio_key()).order(-Anuncio.date).fetch()}))

class HorarioPage(webapp2.RequestHandler):
	def get(self):
		self.response.write(env.get_template('horario.html').render())

class ContactenosPage(webapp2.RequestHandler):
	def get(self):
		self.response.write(env.get_template('contactenos.html').render())

class SocioPage(webapp2.RequestHandler):
	def post(self):
		nombre = self.request.get('nombre')
		aus, horas, cositas = ausencias(nombre), get(nombre, 'horas'), get(nombre, 'cositas')
		if not aus:
			aus = []
		if not horas:
			horas = []
		if not cositas:
			cositas = []
		minutos = 0
		aus = [[fecha, ''.join(['' if ord(c) < 32 or ord(c) > 126 else c for c in s])] for fecha, s in aus]
		horas = [[''.join(['' if ord(c) < 32 or ord(c) > 126 else c for c in s]) for s in l] for l in horas]
		cositas = [''.join(['' if ord(c) < 32 or ord(c) > 126 else c for c in s]) for l in cositas for s in l]
		for _, hora, _, in horas:
			minutos += int(hora)
		print(minutos)
		self.response.write(env.get_template('socio.html').render({
			'nombre': nombre,
			'ausencias': aus,
			'horas': horas,
			'minutos': minutos % 60,
			'horas_total': minutos // 60,
			'cositas': cositas
		}))

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/horario', HorarioPage),
	('/contactenos', ContactenosPage),
	('/socio', SocioPage)
], debug=True)