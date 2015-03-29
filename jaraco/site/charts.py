#!python

"""
Example charts from svg.charts
"""

import cherrypy
from svg.charts.plot import Plot
from jaraco.site import output, render
from genshi import XML
import itertools
import random

from more_itertools.recipes import flatten


def get_random_data_pairs():
	range = (0, 20)
	while True:
		yield random.randint(*range), random.randint(*range)

def get_data_set():
	"get 10-15 datapoints"
	return itertools.islice(get_random_data_pairs(), random.randint(1, 10) + 5)

class Charts(object):
	@cherrypy.expose
	@output('chart example', method='xhtml', content_type='text/xml')
	def plot(self):
		g = Plot(dict(
			width = 640,
			height = 480,
			graph_title = "Plot",
			show_graph_title = True,
			no_css = True,
			key = True,
			scale_x_integers = True,
			scale_y_integers = True,
			min_x_value = 0,
			min_y_value = 0,
			show_data_labels = True,
			show_x_guidelines = True,
			show_x_title = True,
			x_title = "Time",
			show_y_title = True,
			y_title = "Ice Cream Cones",
			y_title_text_direction = 'bt',
		))
		# add a few random datasets
		for n in range(1, 4):
			g.add_data(dict(
				data = flatten(get_data_set()),
				title = 'series %d' % n,
				))
		res = XML(g.burn())
		return render(chart=res)
