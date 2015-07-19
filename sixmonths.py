'''===============
   ===TOM WALLIS
   ===PLATFORMER ENGINE V0.2
   ===
   ===MUCH OF MY PYGAME KNOWLEDGE HAS BEEN LEARNED 
   ===THROUGH http://www.nandnor.net/code/platformer/platform.txt
   ===AS A RESULT THIS PROGRAM RESEMBELED THE ORIGINAL AT FIRST. 
   ===IT HAS SINCE GROWN TO SUPPORT MULTIPLE LEVELS, BETTER COLLISIONS, &c. 
   ===
   ===
   ===  
   ===
   ===
   ===TODO: Find other things to fix.
   ===	Beta test?
   ==============='''

import pygame, os, sys
from entities import *
from levels import *

DISPLAY = (800, 640)
FLAGS = 0
DEPTH = 32

## As the original at http://www.nandnor.net/code/platformer/platform.txt says, 
## The screen fits nicely into 25x20 blocks.
blocks_long, blocks_high = 25, 20


pygame.font.init()
gameFont = pygame.font.SysFont(pygame.font.get_default_font()+",ariel,helvetica,times new roman,monospace", 16)

background_colour = "#202030" # IF THIS IS UPDATED, ALSO UPDATE THE VALUE IN ENTITIES.PY
textColour = (180, 150, 200)


		
def gameLoop():
	
	pygame.init()
	screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
	pygame.display.set_caption("Six Months")

	timer = pygame.time.Clock()
	up = down = left = right = False

	bg = pygame.Surface((32, 32))
	bg.convert()
	bg.fill(pygame.Color(background_colour))

	entities = pygame.sprite.Group()

	lastLevel = False

	
	
	for level in LEVELS[:len(LEVELS)-1]:
		try:
			player = Player(level.playerx, level.playery, '#DFDFDF', 25, 25)
			blocks = []
			
			x = y = 0
			
			for row in level.blocksList:
				for item in row:
					
					block = getBlock(item, x, y)

					if block != 'noblock':
						blocks.append(block)
						entities.add(block)
					x += 32
				y += 32
				x = 0

			entities.add(player)
			
			while True:
				timer.tick(60)
				for event in pygame.event.get():
					if event.type == pygame.QUIT: raise SystemExit, "QUIT"
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_UP:
							up = True
						if event.key == pygame.K_DOWN:
							down = True
						if event.key == pygame.K_LEFT:
							left = True
						if event.key == pygame.K_RIGHT:
							right = True
					elif event.type == pygame.KEYUP:
						if event.key == pygame.K_UP:
							up = False
						if event.key == pygame.K_DOWN:
							down = False
						if event.key == pygame.K_LEFT:
							left = False
						if event.key == pygame.K_RIGHT:
							right = False

				#Draw background
				for y in range(blocks_high):
					for x in range(blocks_long):
						screen.blit(bg, (x*32, y*32))
			
				for textDetails in level.textDetails:
					# Write each message in the textdetails in the appropriate places.
					screen.blit(gameFont.render(textDetails[0], 1, textColour), textDetails[1])
			
			
				#Update player, draw everything else.
				entities.draw(screen)
				player.update(up, down, left, right, blocks)

				pygame.display.flip()
				
			
			

			
		except LevelComplete:
			if lastLevel: raise GameComplete
			x = y = 0
			#Draw background
			for y in range(blocks_high):
				for x in range(blocks_long):
					screen.blit(bg, (x*32, y*32))
			x = y = 0
			entities.empty()

		except GameComplete:
			print "\n\n\n\n\n\t\tI love you.\n\n\n\n\n"
			quit()
			
		except SystemExit:
			print 'Exiting...'
			quit()

		except KeyboardInterrupt:
			print 'Exiting...'
			quit()

		except:
			print "\n\nSomething went wrong...raising error..\n\n"
			print sys.exc_info()
			quit()

	lastLevel = True
	
	try:
		level = LEVELS[-1]
		# os.system('mpg123 *.mp3 &') ### OMIT FOR WINDOWS MACHINES.
		
		player = Player(level.playerx, level.playery, '#DFDFDF', 25, 25)
		blocks = []
				
		x = y = 0
				
		for row in level.blocksList:
			for item in row:
				block = getBlock(item, x, y)			

				if block != 'noblock':
					blocks.append(block)
					entities.add(block)
				x += 32
			y += 32
			x = 0

		entities.add(player)
			
		while True:	
			timer.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.QUIT: raise SystemExit, "QUIT"
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						up = True
					if event.key == pygame.K_DOWN:
						down = True
					if event.key == pygame.K_LEFT:
						left = True
					if event.key == pygame.K_RIGHT:
						right = True
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_UP:
						up = False
					if event.key == pygame.K_DOWN:
						down = False
					if event.key == pygame.K_LEFT:
						left = False
					if event.key == pygame.K_RIGHT:
						right = False

			#Draw background
			for y in range(blocks_high):
				for x in range(blocks_long):
					screen.blit(bg, (x*32, y*32))
				
			for textDetails in level.textDetails:
				# Write each message in the textdetails in the appropriate places.
				screen.blit(gameFont.render(textDetails[0], 1, textColour), textDetails[1])
			
			
			#Update player, draw everything else.
			entities.draw(screen)
			player.update(up, down, left, right, blocks)
	
			pygame.display.flip()

	except LevelComplete:
		if lastLevel: raise GameComplete("Game Complete")
		x = y = 0
		#Draw background
		for y in range(blocks_high):
			for x in range(blocks_long):
				screen.blit(bg, (x*32, y*32))
		x = y = 0
		entities.empty()

	except GameComplete:
		print "\n\n\n\n\n\t\tI love you.\n\n\n\n\n"
		quit()
			
	except SystemExit:
		print 'Exiting...'
		quit()

	except KeyboardInterrupt:
		print 'Exiting...'
		quit()

	except:
		print "\n\nSomething went wrong...raising error..\n\n"
		print sys.exc_info()
		quit()


if (__name__ == '__main__'):
	gameLoop()
	print '\n\n\n\n\nI LOVE YOU.\n\n\n\n\n'
