


from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtChart import * 
from PyQt5.QtGui import *
import math
import numpy as np
import copy
import sys


####################################
#                                  #
####################################
class Main_Window(QMainWindow) :
	def __init__(self, parent = None):
		QMainWindow.__init__(self, parent)
		self.resize(400, 1000)
		self.x = []
		self.y = []
		self.cursor_x = 0
		self.reference = 0
		self.delta = 4
		self.visu_vec = []

		container = QWidget()
		container_layout = QVBoxLayout(container)


		############
		controler = QWidget()
		controler_layout = QVBoxLayout(controler)
		reference_layout = QHBoxLayout()
		self.reference_lab = QLabel( "Reference: " + str(self.reference) )
		self.reference_slider = QSlider(Qt.Horizontal)
		self.reference_slider.valueChanged.connect( self.set_reference )
		reference_layout.addWidget( self.reference_lab )
		reference_layout.addWidget( self.reference_slider )
		controler_layout.addLayout(reference_layout)

		delta_layout = QHBoxLayout()
		self.delta_lab = QLabel( "Delta: " + str(self.delta) )
		self.delta_slider = QSlider(Qt.Horizontal)
		self.delta_slider.setRange(0.1, 20)
		self.delta_slider.valueChanged.connect( self.set_delta )
		delta_layout.addWidget( self.delta_lab )
		delta_layout.addWidget( self.delta_slider )
		controler_layout.addLayout( delta_layout)


		#############
		visu_container = QWidget()
		self.visu_layout = QVBoxLayout( visu_container )


		container_layout.addWidget( visu_container )
		container_layout.addWidget( controler )
		self.setCentralWidget(container)


	def set_data(self,x,y):
		self.x = x
		self.y = y
		self.reference_slider.setRange( np.min(y), np.max(y) )
		self.delta_slider.setRange( 1, 10*np.max( np.max(y) - reference) + 1)
		self.delta_slider.setValue( (10*np.max( np.max(y) - reference) + 1 ) /2. )
		self.update_visus()


	def update_visus(self):
		for visu in self.visu_vec :
			visu.set_data(self.x, self.y, self.cursor_x, self.reference, self.delta)


	def add_visu(self, visu):
		self.visu_layout.addWidget(visu)
		self.visu_vec.append( visu )
		visu.cursor_moved.connect( self.set_cursor_line )
		self.update_visus()


	def set_reference(self, v):
		self.reference = round(float(v),2)
		self.reference_lab.setText( "Reference: " + str(v) )
		self.update_visus()


	def set_delta(self, v):
		self.delta = round(float(v) / 10.,2)
		self.delta_lab.setText( "Delta: " + str(self.delta) )
		self.update_visus()

	def set_cursor_line(self, x) :
		self.cursor_x = x
		self.update_visus()



####################################
#                                  #
####################################
class TimeSerieVisu( QChartView ) :
	cursor_moved = pyqtSignal( float )

	def __init__(self, parent = None):
		QChartView.__init__(self, parent)
		self.setChart( QChart() )
		self.cursor_x = 0
		self.cursor_y_min = -10
		self.cursor_y_max = 10
		self.cusor_x_min = 0
		self.cursor_x_max = 0

	def reference(self, new_reference) :
		return 0


	def add_cursor_line(self) :
		self.cursor_x = max(self.cursor_x, self.cursor_x_min)
		self.cursor_x = min(self.cursor_x, self.cursor_x_max)

		self.cursor_line = QLineSeries()
		self.cursor_line << QPointF(self.cursor_x, self.cursor_y_min ) << QPointF(self.cursor_x, self.cursor_y_max)
		self.cursor_line.setPen(Qt.black)
		self.chart().addSeries( self.cursor_line )


	def set_data(self, x, y, cursor_x, reference = 0, delta = 0 ):
		self.cursor_x = cursor_x
		new_reference = self.reference( reference )
		transformed_data = self.transform_data(copy.copy(x), copy.copy(y), new_reference, delta)
		self.chart().removeAllSeries()
		self.update_cursor_area( transformed_data ) # this is a patch
		self.update_chart(transformed_data, new_reference)
		self.add_cursor_line()
		self.chart().createDefaultAxes()
		self.chart().legend().setVisible(False)


	def update_cursor_area(self, data) :
		self.cursor_x_min = np.min( data[0] )
		self.cursor_x_max = np.max( data[0] )
		y_min = 100
		y_max = -100
		for k in data.keys() :
			if k!=0 :
				min_ = np.min( data[k] )
				max_ = np.max( data[k] )
				y_min = min_ if min_ < y_min else y_min
				y_max = max_ if max_ > y_max else y_max
		self.cursor_y_min = y_min
		self.cursor_y_max = y_max


	def transform_data(self, x,y, reference, delta):
		res = dict()
		res[0] = x
		res[1] = y
		return res


	def update_chart(self, data, reference =0) :

		self.line = QLineSeries()

		for x,y in zip(data[0],data[1]):

			self.line.append(QPointF(x,y))

		self.chart().addSeries(self.line)

	#caputre mouse move event to show the vertical cursor line
	def mouseMoveEvent(self, e) :
		scene_pos = self.mapToScene( e.pos() )
		chartItemPos = self.chart().mapFromScene( scene_pos )
		value = self.chart().mapToValue( chartItemPos )
		self.cursor_moved.emit( value.x() )



####################################
#                                  #
####################################
class AreaTimeSerieVisu( TimeSerieVisu ) :
	def __init__(self, parent = None):
		TimeSerieVisu.__init__(self, parent)

	def reference(self, new_reference) :
		return new_reference

	def same_sign(self, a,b, reference) :

		if a <= reference and b <= reference:
			return True
		elif a >= reference and b >= reference:
			return True
		else:
			return False

	#################
	# find the intersection of the segment P1-P2 with the horizontal line y_reference
	#################
	def x_intersection(self, y_intersection, x1, y1, x2, y2):

		line1 = QLineF(x1,y1,x2,y2)
		line2 = QLineF(0,y_intersection,9999999,y_intersection)
		intersection_point = QPointF()
		line1.intersect(line2,intersection_point)

		return intersection_point.x()


	def transform_data(self,x,y, reference, delta):
		res = dict()
		x_mod = x.copy()
		y_mod = y.copy()
		neg = []
		pos = []
		for i in range(len(x)-1):

			if not self.same_sign(y[i],y[i+1],reference):
				x_inter = self.x_intersection(reference,x[i],y[i],x[i+1],y[i+1])
				if x_inter > 0 and x_inter < x[-1] :
					index = len(np.where(x_mod < x_inter)[0])
					x_mod = np.insert(x_mod,index,x_inter)
					y_mod = np.insert(y_mod,index,reference)

		res[0] = x_mod

		for v in y_mod:

			if v <= reference :
				neg.append(v)
				pos.append(reference)
			elif v > reference:
				pos.append(v)
				neg.append(reference)

		res[1] = np.array(pos)
		res[ -1 ] = np.array(neg)

		return res

	def positive_brush(self):
		return QColor(255,0,0,50)

	def positive_pen(self):
		return QColor(255,0,0,50)

	def negative_brush(self) :
		return QColor(0,0,255,50)

	def negative_pen(self) :
		return QColor(0,0,255,50)


	def update_chart(self, data, reference = 0) :
		self.pos_series = QLineSeries() # Données brutes
		self.neg_series = QLineSeries()
		self.zero_series = QLineSeries()

		for i in range(len(data[0])):
			self.pos_series.append(QPointF(data[0][i],data[1][i]))
			self.neg_series.append(QPointF(data[0][i], data[-1][i]))
			self.zero_series.append(QPointF(data[0][i], reference))

		pos_area = QAreaSeries(self.zero_series,self.pos_series)
		pos_area.setBrush(self.positive_brush())
		pos_area.setPen(self.positive_pen())

		neg_area = QAreaSeries(self.zero_series, self.neg_series)
		neg_area.setBrush(self.negative_brush())
		neg_area.setPen(self.negative_pen())

		self.chart().addSeries(pos_area)
		self.chart().addSeries(neg_area)

####################################
#                                  #
####################################
class MirroredAreaTimeSerieVisu( AreaTimeSerieVisu ) :
	def __init__(self, parent = None):
		AreaTimeSerieVisu.__init__(self, parent)

	def transform_data(self, x, y, reference, delta):
		res = dict()
		x_mod = x.copy()
		y_mod = y.copy()
		neg = []
		pos = []
		for i in range(len(x) - 1):

			if not self.same_sign(y[i], y[i + 1], reference):
				x_inter = self.x_intersection(reference, x[i], y[i], x[i + 1], y[i + 1])
				if x_inter > 0 and x_inter < x[-1]:
					index = len(np.where(x_mod < x_inter)[0])
					x_mod = np.insert(x_mod, index, x_inter)
					y_mod = np.insert(y_mod, index, reference)

		res[0] = x_mod

		for v in y_mod:

			if v <= reference:
				neg.append(-v+reference*2)
				pos.append(reference)
			elif v > reference:
				pos.append(v)
				neg.append(reference)

		res[1] = np.array(pos)
		res[-1] = np.array(neg)

		return res


class StackedMirroredAreaTimeSerieVisu( MirroredAreaTimeSerieVisu ) :
	def __init__(self, parent = None):
		MirroredAreaTimeSerieVisu.__init__(self, parent)

	def  band_from(self,y,ref,delta):

		margin = 0.0001

		if y < 0:
			#print("y",y)
			#print(math.floor((y+margin+ref)/delta))
			return math.floor((y+margin+ref)/delta)
		else:
			return math.ceil((y+margin-ref)/delta)

	def modulo_value(self,y, ref, delta):

		if y < 0:
			return round(abs(abs(y)-ref) % delta,1)
		else:
			return round(abs(y - ref ) % delta, 1)

	def crossed_bands(self,y1,y2, ref, delta):

		b1 = self.band_from(y1,ref,delta)
		b2 = self.band_from(y2,ref,delta)

		bands = []
		if 0<b1<b2:
			bands = np.arange(b1,b2+1)
		elif 0<b2<b1:
			bands = np.arange(b2,b1+1)[::-1]
		if 0>b1>b2:
			bands = np.arange(b1,b2-1,-1)
		elif 0>b2>b1:
			bands = np.arange(b2,b1-1,-1)
			bands = np.sort(bands)

		return bands

	def y_interstected_line(self,prev_band, cur_band, ref, delta):

		if 0 < prev_band < cur_band:
			return ref + prev_band * delta +0.01
		elif 0 < cur_band < prev_band:
			return ref + prev_band * delta - cur_band*delta +0.01
		elif 0 > cur_band > prev_band:
			return ref + prev_band * delta - cur_band*delta +0.01
		elif 0 > prev_band > cur_band:
			return ref + prev_band * delta +0.01
		else :
			return ref

	def estimate_value_for_given_band(self,y, given_band, ref, delta):

		if 0 < given_band < self.band_from(y, ref, delta):
			return ref + delta
		elif 0 > given_band > self.band_from(y, ref, delta):
			return ref + delta
		elif given_band == self.band_from(y,ref,delta):
			return ref + abs(self.modulo_value(y,ref,delta))
		else:
			return ref

	def transform_data(self, x, y, reference, delta):
		res = dict()
		x_mod = x.copy()
		y_mod = y.copy()
		for i in range(len(x) - 1):

			if not self.same_sign(y[i], y[i + 1], reference):
				x_inter = self.x_intersection(reference, x[i], y[i], x[i + 1], y[i + 1])
				if x_inter > 0 and x_inter < x[-1]:
					index = len(np.where(x_mod < x_inter)[0])
					x_mod = np.insert(x_mod, index, x_inter)
					y_mod = np.insert(y_mod, index, reference)
			else:
				cb = self.crossed_bands(y[i],y[i+1],reference,delta)
				if len(cb)>1:
					for ib in range(len(cb)-1):
						y_inter = round(self.y_interstected_line(cb[ib],cb[ib+1],reference,delta),2)
						x_inter = round(self.x_intersection(y_inter, x[i], y[i], x[i + 1], y[i + 1]),2)
						print(y_inter,x_inter)
						if x_inter > 0 and x_inter < x[-1]:
							index = len(np.where(x_mod < x_inter)[0])
							x_mod = np.insert(x_mod, index, x_inter)
							y_mod = np.insert(y_mod, index, y_inter)


		band = max(self.band_from(max(y),reference,delta),abs(self.band_from(min(y),reference,delta)))

		for b in range(-band,band+1):
			serie = []
			for v in y_mod:
				serie.append(self.estimate_value_for_given_band(v,b,reference,delta))
			res[b] = serie

		res[0] = x_mod

		return res

	def update_chart(self, data, reference = 0) :

		self.series = dict()

		for k in data.keys():
			self.series[k] = QLineSeries()
		self.zero_series = QLineSeries()

		for i in range(len(data[0])):
			self.zero_series.append(QPointF(data[0][i], reference))
			for k in data.keys():
				self.series[k].append(QPointF(data[0][i],data[k][i]))

		for k in data.keys():
			if k != 0:
				area = QAreaSeries(self.zero_series, self.series[k])
				if k < 0:
					area.setBrush(self.negative_brush())
					area.setPen(self.negative_pen())
				else:
					area.setBrush(self.positive_brush())
					area.setPen(self.positive_pen())
			self.chart().addSeries(area)

if __name__=="__main__":
	n = 50
	reference = 0.5
	x = np.arange(n, dtype = float)
	y =  5 * np.sin( x /2. ) + 6* np.random.rand(n) - 3
	y = np.round(y,1)
	#y = np.array( [ 2.2,  6.8,  7.1,  9.8,  6.4,  6.8,  1.3, -5.8, -4.6, -9.5] )
	#y = y[0:8]
	app = QApplication(sys.argv)
	win = Main_Window()
	win.set_data(x,y)
	win.add_visu( TimeSerieVisu() )
	win.add_visu( AreaTimeSerieVisu() )
	win.add_visu( MirroredAreaTimeSerieVisu()  )
	win.add_visu( StackedMirroredAreaTimeSerieVisu()  )


	win.show()

	app.exec_()


