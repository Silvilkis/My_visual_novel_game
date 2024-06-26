import pygame, sys
from pygame.locals import *

margins = 20
height = 300
label_background_color = (0, 0, 255, 128)
answer_background_color = (139, 222, 76, 200)
text_color = (0, 0, 0, 255)
txt_margins = 20
txt_size = 30
font = 'FeENrm28C.otf'

button_bg_color = (200, 200, 200)
choice1_bg_color = (255, 128, 128)
choice2_bg_color = (207, 159, 255)

class Button:
    def __init__(self, x, y, width, color_bg, color_txt, color_high, text=''):
        self.rectangle = pygame.Rect(x, y, width, 0)
        self.font = pygame.font.Font(font, 20)
        self.text = ''
        self.was_clicked = False
        self.color_background = color_bg
        self.color_text = color_txt
        self.color_highlight = color_high
        self.txt_margins = txt_margins
        self.new_line_position = 0
        self.line_rectangles = []
        self.line_surfaces = []
        self.change_button_text(text)

    def draw(self, screen):
        action = False
        mouse_position = pygame.mouse.get_pos()
        background = self.color_background
        if self.rectangle.collidepoint(mouse_position):
            background = self.color_highlight
            is_clicked = pygame.mouse.get_pressed()[0] == True
            if is_clicked and not self.was_clicked:
                action = True
                self.was_clicked = True

        if pygame.mouse.get_pressed()[0] == False:
            self.was_clicked = False

        pygame.draw.rect(screen, background, self.rectangle)
        if self.text != '':
            for line_index in range(len(self.line_rectangles)):
                screen.blit(self.line_surfaces[line_index], self.line_rectangles[line_index])

        return action

    def change_button_text(self, new_text):
        self.text = new_text
        lines = split_text_into_lines(self.text, self.font, self.rectangle.width, self.txt_margins)
        self.line_surfaces = [self.font.render(line, True, self.color_text) for line in lines]
        self.new_line_position = self.rectangle.y + self.txt_margins
        self.line_rectangles = []
        for line_surface in self.line_surfaces:
            line_rect = line_surface.get_rect()
            line_rect.x = self.rectangle.x + (self.rectangle.w / 2 - line_rect.w / 2)
            line_rect.y = self.new_line_position
            self.line_rectangles.append(line_rect)
            self.new_line_position += line_surface.get_height()
        self.rectangle.height = self.txt_margins * 2 + len(self.line_rectangles) * self.line_surfaces[0].get_height()


class BottomLabel:
    def __init__(self, screen, text=''):
        screen_width, screen_height = screen.get_size()
        x = margins
        y = screen_height - margins - height
        width = screen_width - margins * 2
        self.rectangle = pygame.Rect(x, y, width, height)
        self.text = ''
        self.text_size = txt_size
        self.color_text = text_color
        self.color_background = label_background_color
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill(self.color_background)
        self.txt_margins = txt_margins
        self.was_clicked = False
        self.new_line_position = 0
        self.font = pygame.font.Font(font, self.text_size)
        self.line_rectangles = []
        self.line_surfaces = []
        self.change_label_text(text)

    def bottom_label_draw(self, screen):
        screen.blit(self.surface, (self.rectangle.x, self.rectangle.y))
        action = False
        mouse_position = pygame.mouse.get_pos()
        if self.rectangle.collidepoint(mouse_position):
            is_clicked = pygame.mouse.get_pressed()[0] == True
            if is_clicked and not self.was_clicked:
                action = True
                self.was_clicked = True

        if pygame.mouse.get_pressed()[0] == False:
            self.was_clicked = False

        for line_index in range(len(self.line_rectangles)):
            screen.blit(self.line_surfaces[line_index], self.line_rectangles[line_index])

        return action

    def change_label_text(self, new_text):
        self.text = new_text
        lines = split_text_into_lines(self.text, self.font, self.rectangle.width, self.txt_margins)
        self.line_surfaces = [self.font.render(line, True, self.color_text) for line in lines]
        self.new_line_position = self.rectangle.y + self.txt_margins
        self.line_rectangles = []
        for line_surface in self.line_surfaces:
            line_rect = line_surface.get_rect()
            line_rect.x = self.rectangle.x + self.txt_margins
            line_rect.y = self.new_line_position
            self.line_rectangles.append(line_rect)
            self.new_line_position += line_surface.get_height()

    def change_background_color(self, color):
        self.color_background = color
        self.surface.fill(self.color_background)

class ChoiceWithButtons:
    def __init__(self, screen, label_text, choice1_text, choice2_text):
        self.screen = screen
        self.label_text = label_text
        self.choice1_text = choice1_text
        self.choice2_text = choice2_text
        self.bottom_label = BottomLabel(screen, label_text)

        button_x_coordinate = self.bottom_label.rectangle.x + self.bottom_label.txt_margins
        button_y_coordinate = self.bottom_label.new_line_position + 20
        button_width = self.bottom_label.rectangle.width - 2 * self.bottom_label.txt_margins
        self.choice1_button = Button(button_x_coordinate, button_y_coordinate, button_width, button_bg_color, text_color, choice1_bg_color, choice1_text)
        self.choice2_button = Button(button_x_coordinate, button_y_coordinate + self.choice1_button.rectangle.height + 15, button_width, button_bg_color, text_color, choice2_bg_color, choice2_text)

    def draw_choice(self):
        self.bottom_label.bottom_label_draw(self.screen)
        if self.choice1_button.draw(self.screen):
            return 0
        if self.choice2_button.draw(self.screen):
            return 1
        return -1

    def change_choice_texts(self, label_text, button1_text, button2_text):
        self.bottom_label.change_label_text(label_text)
        self.choice1_button.change_button_text(button1_text)
        self.choice2_button.change_button_text(button2_text)
        self.choice2_button.rectangle.y = self.choice1_button.rectangle.y + self.choice1_button.rectangle.height + 15

def split_text_into_lines(text, font, box_width, padding):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        line_surface = font.render(' '.join(current_line), True, (0, 0, 0))
        if line_surface.get_width() > box_width - 2 * padding:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    return lines

class CharacterImage:
    def __init__(self, mood, x, y, images):
        self.mood = mood
        self.x = x
        self.y = y
        self.images = images
        self.image = self.images[self.mood_to_index(mood)]

    def draw_image(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def mood_to_index(self, mood):
        if mood == "neutralus":
            return 0
        elif mood == "susimastes":
            return 1
        elif mood == "issigandes":
            return 2
        elif mood == "susirupines":
            return 3
        elif mood == "baubas":
            return 4
        else:
            return -1

    def change_mood(self, mood):
        self.image = self.images[self.mood_to_index(mood)]

