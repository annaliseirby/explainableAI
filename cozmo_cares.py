import cozmo
import sys
import time

from cozmo import faces

"""
Annalise Irby and Divya Srivastava
15 November 2018
Explainable AI Project

Code modified from example:
https://github.com/anki/cozmo-python-sdk/blob/master/src/cozmo/faces.py

"""

async def react(robot: cozmo.robot.Robot):
	"""
	Cozmo will react to the facial expressions of the first face it sees.

	Rules:
	1. If Cozmo sees a sad face, she will try to cheer you up.
	2. If Cozmo sees an angry face, she will run away.
	3. If Cozmo sees a happy face, she will celebrate with you.
	4. At any point, you can ask Cozmo why she did something. She will stop what
	   she's doing, explain, and then go back to her alert "watching" state.
	"""

	robot.enable_facial_expression_estimation(enable=True)

	state = "finding face"
	face_visible = False
	explanation = "I'm trying to find a face."
	any_face = None

	while True:

		########## INITIAL CHECKS ##########

		# if key:  # check for voice input (from computer microphone)
		# 	state = "explaining"

		if not face_visible:
			state = "finding face"

		########## STATE MACHINE ##########

		print(state)

		if state is "init":

			explanation = "I'm just getting started."
			robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
			robot.move_lift(-3)

		if state is "finding face":

			explanation = "I'm trying to find a face."
			any_face = None
			print("Looking for a face!")
			look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)

			try:
				any_face = await(robot.world.wait_for_observed_face(timeout=30))

			except asyncio.TimeoutError:
				print("Didn't find anyone :-(")

			finally:
				# whether we find it or not, we want to stop the behavior
				look_around.stop()

			if any_face is None:
				print("no faces found :(")
				face_visible = False
			else:
				print("FOUND A FACE")
				face_visible = True
				state = "watching face"

		elif state is "watching face":

			explanation = "I'm just staying alert."

			print("face is ", any_face)

			robot.stop_all_motors()
			expression = any_face.expression
			print("expression is ", expression)

			if expression is "sad":
				state = "reacting to sad face"
			elif expression is "angry":
				state = "reacting to angry face"
			elif expression is "happy":
				state = "reacting to happy face"
			else:
				state = "finding face"

		elif state is "reacting to sad face":

			explanation = "You seemed sad, so I'm trying to cheer you up."

			reaction = robot.play_anim_trigger(triggers.DanceMambo)
			await(reaction.wait_for_completed())

			time.sleep(500)
			state = "watching face"

		elif state is "reacting to angry face":

			explanation = "You seemed angry, so I'm giving you some space."

			reaction = robot.play_anim_trigger(triggers.CodeLabScaredCozmo)
			await(reaction.wait_for_completed())

			time.sleep(500)
			state = "watching face"

		elif state is "reacting to happy face":

			explanation = "You seemed happy, so I'm celebrating!"

			reaction = robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabPartyTime)
			await(reaction.wait_for_completed())

			break

			time.sleep(500)
			state = "watching face"

		elif state is "explaining":

			robot.abort_all_actions()
			explain = cozmo.say_text(explanation)
			await(explain.wait_for_completed())
			state = "watching face"


# def say(self, robot:cozmo.robot.Robot = None, cmd_args = None):
#
#     entire_message = None
#     if len(cmd_args) > 0:
#         try:
#             entire_message = ""
#             for s in cmd_args:
#                 entire_message = entire_message + " " + str(s)
#             entire_message = entire_message.strip()
#         except:
#             pass
#
#     if (entire_message is not None) and (len(entire_message) > 0):
#         robot.say_text(entire_message).wait_for_completed()
#         return 'I said "' + entire_message + '"!'
#
#     return "Error: no message!"

# async def look(robot:cozmo.robot.Robot):
# def look(self, cmd_args = None):

	# any_face = None
	# print("Looking for a face...")
	# robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
	# robot.move_lift(-3)
	# look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)
	#
	# try:
	#     any_face = robot.world.wait_for_observed_face(timeout=30)
	#
	# except asyncio.TimeoutError:
	#     print("Didn't find anyone :-(")
	#
	# finally:
	#     # whether we find it or not, we want to stop the behavior
	#     look_around.stop()
	#
	# if any_face is None:
	#     robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail).wait_for_completed()
	#     return any_face, False
	#
	# print("Yay, found someone!")
	#
	# anim = robot.play_anim_trigger(cozmo.anim.Triggers.LookInPlaceForFacesBodyPause)
	# anim.wait_for_completed()
	# return any_face, True


cozmo.run_program(react, use_viewer=True, force_viewer_on_top=True)
