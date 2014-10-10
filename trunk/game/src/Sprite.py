class Sprite:
	def __init__(self, type, x, y):
		self.type = type
		self.x = x
		self.y = y
		self.dx = 0
		self.dy = 0
		self.waypoints = []
		self.v = 2.0
		self.last_direction = 's'
		self.dead = False
		self.half = False
		self.renderer = None
		self.lifetime = 0
		self.ghost = type == 'ball' # can pass through things
	
	def specific_update(self, type, area, counter):
		if type == 'mothercar1' or type == 'mothercar2':
			self.dx = $math_sin(self.lifetime * 2 * 3.14159 / 100)
		elif type == 'hippochoke':
			rate = 30
			c = counter % rate
			if c == 0:
				self.dx = -2
			elif c == $int(rate / 2):
				self.dx = 2
			
	
	def update(self, area):
		self.specific_update(self.type, area, self.lifetime)
		self.lifetime += 1
		if $list_length(self.waypoints) > 0:
			wp = self.waypoints[0]
			dx = wp[0] - self.x
			dy = wp[1] - self.y
			dist = (dx ** 2 + dy ** 2) ** .5
			if dist <= self.v:
				self.dx = wp[0] - self.x
				self.dy = wp[1] - self.y
				$list_remove(self.waypoints, 0)
			else:
				self.dx = 1.0 * dx * self.v / dist
				self.dy = 1.0 * dy * self.v / dist
		if self.dx != 0 or self.dy != 0:
			dx = self.dx
			dy = self.dy
			self.last_direction = self.convert_vector_to_direction(dx, dy)
			newx = self.x + dx
			newy = self.y + dy
			if area.is_passable(newx, newy) or self.ghost:
				self.x = newx
				self.y = newy
			self.dx = 0
			self.dy = 0
	
	def set_waypoint(self, tx, ty):
		self.waypoints = [(tx, ty)]
	
	def queue_waypoint(self, tx, ty):
		$list_add(self.waypoints, (tx, ty))
	
	def convert_vector_to_direction(self, dx, dy):
		if dx == 0:
			if dy < 0:
				return 'n'
			else:
				return 's'
		elif dy == 0:
			if dx < 0:
				return 'w'
			else:
				return 'e'
				
			
	def render(self, screen, images, rc):
		if self.renderer == None:
			if self.type == 'player':
				if self.scale == 'half': self.renderer = sr_player_half
				elif self.scale == 'double': self.renderer = sr_player_double
				else: self.renderer = sr_player_full
			else:
				if self.type[0] == 'b':
					if self.type == 'ball': self.renderer = sr_ball
					elif self.type == 'battleship': self.renderer = sr_battleship
					elif self.type == 'bballplayer1': self.renderer = sr_bballplayer1
					elif self.type == 'bballplayer2': self.renderer = sr_bballplayer2
					elif self.type == 'bballplayer3': self.renderer = sr_bballplayer3
					elif self.type == 'bluepin': self.renderer = sr_bluepin
					elif self.type == 'boot': self.renderer = sr_boot
					elif self.type == 'bow': self.renderer = sr_bow
				else:
					if self.type == 'hippochoke': self.renderer = sr_hippochoke
					elif self.type == 'hipposafe': self.renderer = sr_hipposafe
					elif self.type == 'racecar': self.renderer = sr_racecar
					elif self.type == 'knight1': self.renderer = sr_knight1
					elif self.type == 'knight2': self.renderer = sr_knight2
					elif self.type == 'legopog': self.renderer = sr_legopog
					elif self.type == 'mothercar1': self.renderer = sr_mothercar1
					elif self.type == 'mothercar2': self.renderer = sr_mothercar2
					elif self.type == 'rubberband': self.renderer = sr_rubberband
					elif self.type == 'teleporter': self.renderer = sr_teleporter
					elif self.type == 'thimble': self.renderer = sr_thimble
					elif self.type == 'wizard': self.renderer = sr_wizard
					
				
		self.renderer(self, screen, images, rc)

def draw_image_centered(screen, sprite, img):
	w = $image_width(img)
	h = $image_height(img)
	x = sprite.x - $int(w / 2)
	y = sprite.y - h
	$image_blit(screen, img, x, y)
	sprite.last_width = w
	sprite.last_height = h

def draw_image_centered_directional(screen, sprite, images, key):
	img = images[key + '_' + sprite.last_direction]
	draw_image_centered(screen, sprite, img)



def sr_ball(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['simple/ball'])
def sr_battleship(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/battleship'])
def sr_bballplayer1(sprite, screen, images, rc): draw_image_centered_directional(screen, sprite, images, 'sprites/cards/red')
def sr_bballplayer2(sprite, screen, images, rc): draw_image_centered_directional(screen, sprite, images, 'sprites/cards/red')
def sr_bballplayer3(sprite, screen, images, rc): draw_image_centered_directional(screen, sprite, images, 'sprites/cards/red')
def sr_bluepin(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['simple/bluepin'])
def sr_boot(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/boot'])
def sr_bow(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/bow'])
def sr_hippochoke(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/hippo/choking'])
def sr_hipposafe(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/hippo/hippo'])
def sr_knight1(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/guard0'])
def sr_knight2(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/guard1'])
def sr_legopog(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/pog'])
def sr_racecar(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/racecar'])
def sr_rubberband(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['simple/rubberband_ground'])
def sr_thimble(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/thimble'])
def sr_wizard(sprite, screen, images, rc): draw_image_centered_directional(screen, sprite, images, 'sprites/cards/wizard')

def sr_mothercar1(sprite, screen, images, rc):
	key = 'sprites/mothercar/left1'
	if sprite.last_direction == 'e':
		key = 'sprites/mothercar/right1'
	draw_image_centered(screen, sprite, images[key])

def sr_mothercar2(sprite, screen, images, rc):
	key = 'sprites/mothercar/left2'
	if sprite.last_direction == 'e':
		key = 'sprites/mothercar/right2'
	draw_image_centered(screen, sprite, images[key])

def sr_player_double(sprite, screen, images, rc):
	draw_image_centered(screen, sprite, images['sprites/mc_double/s0_alt'])

def sr_player_full(sprite, screen, images, rc):
	draw_image_centered(screen, sprite, images['sprites/mc/s0_alt'])

def sr_player_half(sprite, screen, images, rc):
	draw_image_centered(screen, sprite, images['sprites/mc_half/s0_alt'])

def sr_teleporter(sprite, screen, images, rc):
	key = 'teleporter/frame' + $str($int(rc / 5) % 3 + 1)
	draw_image_centered(screen, sprite, images[key])
