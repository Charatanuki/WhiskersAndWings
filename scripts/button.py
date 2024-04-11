class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
			self.image = image
			self.x_pos = pos[0]
			self.y_pos = pos[1]
			self.font = font
			self.base_color, self.hovering_color = base_color, hovering_color
			self.text_input = text_input
			self.text = self.font.render(self.text_input, True, self.base_color)
			if self.image is None:
				self.image = self.text
			self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

			# Ajuster le rectangle pour correspondre exactement aux dimensions du texte
			self.rect_padding_x = self.text_rect.width // 2
			self.rect_padding_y = self.text_rect.height // 2

			if self.image is not None:
				self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
				self.rect.inflate_ip(self.rect_padding_x, self.rect_padding_y)  # Agrandir le rectangle
			else:
				self.rect = self.text_rect.inflate(self.rect_padding_x, self.rect_padding_y)  # Agrandir le rectangle

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)