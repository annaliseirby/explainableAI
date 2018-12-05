import cozmo
import sys
import time

"""
Annalise Irby and Divya Srivastava
15 November 2018
Explainable AI Project

Code modified from example:
https://github.com/anki/cozmo-python-sdk/blob/master/src/cozmo/faces.py

"""



def react():

	state = "init"
	while True:

		print(state)

		# check for face
		# if face has changed

		# check for emotion

		if state is "init":

			# something

		elif state is "alert":

			# state = comforting

			# state = cowering

			# state = celebrating

		elif state is "comforting":  # if Cozmo sees a sad face

			cozmo.animate()

		elif state is "cowering":  # if Cozmo sees an angry face


		elif state is "celebrating":  # if Cozmo sees a happy face


if __name__ == '__main__':
	react()
