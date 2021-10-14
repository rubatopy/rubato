import pygame
import random
pygame.init()

# technique hard
# SoundChannels = {
#     'background': 0,
#     'ambient': 1,
#     'game music': 2,
#     'game sound': 3,
# }
# music = pygame.mixer.Sound('sunset.mp3')
# pygame.mixer.Channel(SoundChannels['background']).play(music, -1)


# technique 1
# poof_sound = pygame.mixer.Sound('Alexa/Sounds/poof.wav')
# music = pygame.mixer.Sound('sunset.mp3')
# music.set_volume(0.5)
# music.play(-1)
# music2 = pygame.mixer.Sound('statwind.wav')
# music2.set_volume(0.15)
# music2.play(-1)
# music.stop()
# music2.stop()


# technique 2
# sounds = {}
# sound_list = ['crash', 'bang', 'ouch', 'meow the cat']
# for sound in sound_list:
#     sounds[sound] = pygame.mixer.Sound('Alexa/Sounds/' + sound + '.wav')
#
# sounds[random.choice(['crash', 'bang'])].play()  # ['crash', 'bang'] is a subset
