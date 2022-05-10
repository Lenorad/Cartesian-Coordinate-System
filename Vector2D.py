from graphics import *

#Before you use this, you may need to know about graphics.py(which is wrapper around tkinker) > https://www.youtube.com/watch?v=R39vTAj1u_8
#NOTE :I'm neither the creator of graphics.py nor the above video. I'm just using his module to make a ploting graph 

def Rn(number):
	if number >= 0:
		return number
	else:
		if isinstance(number, float):
			index = str(number).index('.')
			number = str(number).replace('.', '')
			return int(str(number[1:index]))
		return int(str(number)[1:])

def ceil(jumper):
	if isinstance(jumper,float):
		string_float = str(jumper)[str(jumper).index('.') + 1]
		if int(string_float) < 5:
			jumper
		else:
			jumper += 1
		return int(jumper) 
	else:
		return jumper

def draw_Point(self, x, y, color = None):
		p = Point(x, y)
		if color is not None:
			p.setFill(color)
		else:
			p.setFill(self.color[2])
		p.draw(self.window)

def draw_Line(self, x1, y1, x2, y2, color = None):
		l = Line(Point(x1, y1), Point(x2, y2))
		if color is not None:
			l.setFill(color)
		else:
			l.setFill(self.color[1])
		l.draw(self.window)

class Vector2D:
	def __init__(self, var = 801, hor = 801, squares=(4, 4), minimize = (1,1), color=(color_rgb(44, 45, 46), 'black', 'yellow')):
		sqe = squares[0]
		lagx = 0 
		lagy = 0
		if squares[0] < squares[1]:
			sqe = squares[0]
			lagy = squares[1] - squares[0]
		else:
			sqe = squares[1]
			lagx = squares[0] - squares[1]

		avg_value = int((var-1) / (sqe))
		pluse = avg_value

		if avg_value * sqe != var - 1:
			var -=  var - (avg_value * sqe)
		if avg_value * sqe != hor - 1:
			hor -=  hor - (avg_value * sqe)

		if lagx != 0:
			hor += (avg_value * lagx)
		elif lagy != 0:
			var += (avg_value * lagy)

		window = GraphWin('Vector2D', hor, var)
		window.setBackground(color[0])
		self.window = window
		self.color = color
		self.sqe = sqe
		self.lagx = lagx
		self.lagy = lagy
		self.avg_value = avg_value
		self.hor = hor
		self.var = var
		self.minimize = minimize
		zero = (0, 0)
		self.zero = zero
		master = [0, 0, 0, 0]
		self.master = master

	def Grid(self):
		sqe = self.sqe
		lagx = self.lagx 
		lagy = self.lagy
		avg_value = self.avg_value
		hor = self.hor
		var = self.var

		pluse = avg_value
		for _ in range(sqe):
			draw_Line(self, avg_value, 0, avg_value, var)
			draw_Line(self, 0, avg_value, hor, avg_value)
			avg_value += pluse

		if lagx != 0:
			for _ in range(lagx):
				draw_Line(self, avg_value, 0, avg_value, hor)
				avg_value += pluse
		if lagy != 0:
			for _ in range(lagy):
				draw_Line(self, 0, avg_value, var, avg_value)
				avg_value += pluse
		
	def Origin(self, x=0 , y=0):
		avg_value = self.avg_value
		if x != 0 or y != 0:
			X, Y = ((ceil((self.hor / 2) / avg_value) * avg_value), ceil((self.var / 2) / avg_value) * avg_value)
			X, Y = X + (x * avg_value), Y - (y * avg_value)
			self.zero = (X, Y)
		else:
			X, Y = (ceil((self.hor / 2 )/ avg_value) * avg_value, ceil((self.var / 2 )/ avg_value) * avg_value)
			self.zero = (X, Y)
		draw_Line(self, X, 0, X, self.var, 'white')
		draw_Line(self, 0, Y, self.hor, Y, 'white')
		X1 = (self.zero[0] / avg_value)
		Y1 = (self.zero[1] / avg_value)
		self.master[0] = X1 
		self.master[1] = Y1 
		self.master[2] = (ceil((self.hor) / avg_value) + 0.0) - X1
		self.master[3] = (ceil((self.var) / avg_value) + 0.0) - Y1

	def Points(self, *xy):
		points = []
		m = self.master
		modx = 0 
		mody = 0
		for x, y in xy:
			x /= self.minimize[0] 
			y /= self.minimize[1]
			if self.minimize[0] != 1:
				modx = x
			if self.minimize[1] != 1:
				mody = y 
			if x != 0 and y != 0:
				if x > 0 and y > 0:
					X = m[0] + x
					Y = m[1] - y
				elif x < 0 and y < 0:
					X = m[0] - Rn(x) + modx 
					Y = m[1] + Rn(y) - mody
				elif x > 0 and y < 0:
					X = m[0] + x
					Y = m[1] + Rn(y) - mody
				else:
					X = m[0] - Rn(x) + modx
					Y = m[1] - y
				draw_Point(self, X * self.avg_value, Y * self.avg_value)
				points.append((X, Y))
			else:
				if x == 0:
					X = self.zero[0]
					if y < 0:
						Y = (self.master[1] - y) * self.avg_value
					else:
						Y = (self.master[1] - Rn(y)) * self.avg_value				
					draw_Point(self, X, Y)
				elif y == 0:
					Y = self.zero[1]
					if x > 0:
						X = (self.master[0] + x) * self.avg_value
					else:
						if self.minimize[0] != 1:
							X = (self.master[0] + modx) * self.avg_value
						else:
							X = (self.master[0] - Rn(x)) * self.avg_value
					draw_Point(self, X, Y)
				else:
					X = self.zero[0]
					Y = self.zero[1]
					draw_Point(self, X, Y)
				points.append((X / self.avg_value, Y / self.avg_value))
		return points

	def Connect_points(self, points, color = None):
		avg_value = self.avg_value
		if color is not None:
			color = color
		else:
			color = self.color[2]
		#x, y = (ceil((self.hor / 2 )/ avg_value) * avg_value, ceil((self.var / 2 )/ avg_value) * avg_value)
		x, y = self.zero[0], self.zero[1]
		if len(points) == 1:
			draw_Line(self, x, y, points[0][0] * avg_value, points[0][1] * avg_value, color)
		else:
			for index in range(len(points) - 1):
				origin = points[index]
				end = points[index + 1]
				draw_Line(self, origin[0] * avg_value, origin[1] * avg_value, end[0] * avg_value, end[1] * avg_value, color)
			draw_Line(self, points[len(points) - 1][0] * avg_value, points[len(points) - 1][1] * avg_value, points[0][0] * avg_value, points[0][1] * avg_value, color)

	def getmouse(self):
		print(f'X label: -{str(self.master[0] - 1)[:-2]} to {str(self.master[2] - 1)[:-2]}, {self.minimize[0]} unit per horizontal row.')
		print(f'Y label: -{str(self.master[3] - 1)[:-2]} to {str(self.master[1] - 1)[:-2]}, {self.minimize[1]} unit per vartical row.')
		self.window.getMouse()

	def close(self):
		self.window.close()