import pygame, sys
from pygame.locals import *
from utility import *
import json
import os

story_text_file = 'zaidimo_istorija.json'
male_characters_directory = 'veikejai/Male'

class GameLoop:
	def __init__(self, screen):
		self.screen = screen
		self.run = True
		self.images_male = []
		for root, dirs, file_names in os.walk(male_characters_directory):
			for file_name in file_names:
				image = pygame.image.load(os.path.join(root,file_name))
				self.images_male.append(image)
		with open(story_text_file, 'r', encoding="utf8") as file:
			self.story_data = json.load(file)

		self.character_portrait = CharacterImage("neutralus", 100, 35, self.images_male)

		pygame.display.update()
	def runLoop(self):
		texts = self.story_data["tekstai"]
		choices = self.story_data["pasirinkimai"]
		main_text_step = 0
		main_choice_step = 0

		first_choice_count = 0
		second_choice_count = 0

		current_text_level = 0
		show_choice = False
		show_buttons = True
		current_text = texts[main_text_step]
		current_choice = choices[main_choice_step]
		current_answer = []
		bottom_label = BottomLabel(self.screen, text=current_text["zodziai"][0])
		bottom_choice = ChoiceWithButtons(self.screen, current_choice["teiginys"], current_choice["mygtukai"][0], current_choice["mygtukai"][1])

		while self.run:
			self.screen.fill((255, 255, 255))
			self.character_portrait.draw_image(self.screen)
			if show_choice == False:
				bottom_label.change_background_color(label_background_color)
				self.character_portrait.change_mood(current_text["nuotaika"])
				if bottom_label.bottom_label_draw(self.screen):
					if current_text_level < len(current_text["zodziai"]) - 1:
						current_text_level += 1
						bottom_label.change_label_text(current_text["zodziai"][current_text_level])
					else:
						main_text_step += 1
						current_text_level = 0
						show_choice = True
						current_choice = choices[main_choice_step]
			else:
				if show_buttons == True:
					bottom_choice.change_choice_texts(current_choice["teiginys"], current_choice["mygtukai"][0], current_choice["mygtukai"][1])
					selection = bottom_choice.draw_choice()
					if selection != -1:
						show_buttons = False
						if selection == 0:
							first_choice_count += 1
						elif selection == 1:
							second_choice_count += 1
						current_answer = current_choice["atsakymai"][selection]
						bottom_label.change_label_text(current_answer[0])
				else:
					bottom_label.change_background_color(answer_background_color)
					if bottom_label.bottom_label_draw(self.screen):
						if current_text_level < len(current_answer) - 1:
							current_text_level += 1
							bottom_label.change_label_text(current_answer[current_text_level])
						else:
							show_buttons = True
							show_choice = False
							current_text_level = 0
							main_choice_step += 1
							if main_text_step < len(texts):
								current_text = texts[main_text_step]
								bottom_label.change_label_text(current_text["zodziai"][current_text_level])
							else:
								self.run = False

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			pygame.display.update()

		ending = True
		ending_data = self.story_data["pabaiga"]
		current_text_level = 0

		chosen_ending = []
		if first_choice_count > second_choice_count:
			chosen_ending = ending_data[0]
			bottom_label.change_background_color(choice1_bg_color)
		else:
			chosen_ending = ending_data[1]
			bottom_label.change_background_color(choice2_bg_color)

		bottom_label.change_label_text(chosen_ending["zodziai"][0])
		self.character_portrait.change_mood(chosen_ending["nuotaika"])

		while ending:
			self.screen.fill((255, 255, 255))
			self.character_portrait.draw_image(self.screen)
			if bottom_label.bottom_label_draw(self.screen):
				if current_text_level < len(chosen_ending["zodziai"]) - 1:
					current_text_level += 1
					bottom_label.change_label_text(chosen_ending["zodziai"][current_text_level])
				else:
					ending = False

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			pygame.display.update()
