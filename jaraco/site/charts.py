#!python

"""
Example charts from svg.charts
"""

import cherrypy
from svg.charts.plot import Plot
from jaraco.site import output, render

class Charts(object):
	@cherrypy.expose
	@output('chart example')
	def plot(self):
		g = Plot({
			'min_x_value': 0,
			'min_y_value': 0,
			'area_fill': True,
			'stagger_x_labels': True,
			'stagger_y_labels': True,
			'show_x_guidelines': True
		   })
		g.add_data({'data': [1, 25, 2, 30, 3, 45], 'title': 'series 1'})
		g.add_data({'data': [1,30, 2, 31, 3, 40], 'title': 'series 2'})
		g.add_data({'data': [.5,35, 1, 20, 3, 10.5], 'title': 'series 3'})
		res = g.burn()
		return render(chart=res)
