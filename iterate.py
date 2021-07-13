#!/usr/local/bin/python3

# Copyright (c) 2021 Michael Olson. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
#     + Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     + Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     + Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
	iterate.py: Iterate over the letters in the NYT Spelling Bee,
	generating candidate prefixes for the user to accept as possible
	or reject as impossible.

	The user is promted for the day's letters. This should be a seven-
	letter string, and the first letter should be the day's requiired
	letter. We generate all possible prefixes, so the required letter
	may not be in the generated prefix if a matching word is longer
	than the generated prefix, but this convention guarantees that we
	search for prefixes containing the required letter up to the
	maximum prefix length.

	The user is prompted for the longest prefix to search. Eight is a
	good number; gives you a reasonable set of strings to examine,
	and you can do it in a reasonable amount of time.

	The program displays possible prefixes in the bottom left corner
	of the window. For each one, you should answer:

		+ Is this an actual English word, or if it's a string of
		  max prefix length, do you recognize it as the prefix of
		  an actual English word? If so, type 's', and the word
		  will be saved in an answers list at the top of the
		  screen.

		+ Could this be the prefix of an English word? In this case,
		  you're not trying to recognize all (or even some) words
		  that start with it -- you're merely using your judgment of
		  English spelling to assess whether real words could start
		  with this combination of letters. If so, type '<space>'
		  and the program will further explore all possible prefixes
		  that build on this one.

		+ Are you sure that this could not be the prefix of a word
		  under the rules of English spelling as you understand them?
		  For example, a prefix that contains the string 'crk' is
		  pretty obviously no good. If so, type 'n' and the program
		  will cut off its exploration of thsi prefix.

		+ Are you tired of this? Type 'q' and you will quit the
		  program.

	When you quit, or when the program has completed its exploration
	of all prefixes with your guidance, you'll be prompted to type
	'q' one more time. This gives you a chance to type all the saved
	answers at the top of the screen into the day's Spelling Bee. Be
	careful! All the displayed words disappear when you confirm quit.
"""

import curses

"""
	We curses for user interaction.  Top part of the screen is the
	list of results the user has asked us to save.  Bottom part of
	the screen is for painting possible prefixes, collecting user input.
	I am lazy on error checking. In particular, I assume your window is
	big enough for a full list of answers.
"""

class UI:

	def __init__(self, parentwin):
		self.results = []	# list of users's saved results
		self.window = parentwin

		# don't want keystrokes echoed, don't buffer to <cr>
		curses.noecho()
		curses.cbreak()

		# hide the cursor
		curses.curs_set(0)

		parentwin.erase()

		termht, termwd = parentwin.getmaxyx()
		self.res_winht = termht - 3
		self.res_winwd = termwd

		self.res_colwd = 0	# we'll set this in our main()

		# UI clues
		parentwin.addstr(termht - 2, 0, "'<space>': continue / 'n': no / 's': save / 'q': quit")

	def getletters(self):
		self.window.move(self.res_winht + 2, 0)
		self.window.clrtoeol()
		self.window.addstr("Today's letters: ")
		hloc = 18
		s = ""
		while True:
			c = self.window.getkey()
			if c == "\n":
				break
			self.window.addstr(self.res_winht + 2, hloc, c)
			hloc += 1
			s = s + c
		self.window.move(0,0)
		self.window.clrtoeol()
		self.window.addstr(s)
		return s

	def getmaxlen(self):
		self.window.move(self.res_winht + 2, 0)
		self.window.clrtoeol()
		self.window.addstr("Max prefix length: ");
		hloc = 20
		s = ""
		while True:
			c = self.window.getkey()
			if c == "\n":
				break
			self.window.addstr(self.res_winht + 2, hloc, c)
			hloc += 1
			s = s + c
		self.window.move(0,0)
		self.window.clrtoeol()
		self.window.addstr(s)
		l = int(s)
		return l

	def saveres(self, word):
		resno = len(self.results)

		# We save these but don't do anything with them right now
		self.results.append(word)

		# Display the word in the list at the top of the screen
		col = self.res_colwd * int(resno / self.res_winht)
		row = resno % self.res_winht
		self.window.addstr(row, col, word)

	def score(self, word):
		self.window.move(self.res_winht + 2, 0)
		self.window.clrtoeol()
		self.window.addstr(self.res_winht + 2, 0, word)

		while True:
			answer = self.window.getkey()
			if answer == ' ' or answer == 's' or answer == 'n' or answer == 'q':
				break
			# bad char
			curses.flash()

		if answer == 's':
			self.saveres(word)	# this is a word
		if answer == 's' or answer == ' ':
			return True		# promising prefix
		elif answer == 'q':
			self.wrapup()		# i'm tired!
		else:
			return False		# not a promising prefix

	def wrapup(self):
		# confirm exit before we erase the screen and lose the words
		self.window.move(self.res_winht + 2, 0)
		self.window.clrtoeol()
		self.window.addstr(self.res_winht + 2, 0, "All done! Type q to confirm exit.")
		
		while True:
			answer = self.window.getkey()
			if answer == 'q':
				break

		exit()

# We call this recursively to explore prefixes of increasing length
def trystring(my_ui, prefix, letters, maxlen):

	if len(prefix) > maxlen:
		return

	# if the user likes this prefix, try all possible prefixes
	# based on it

	if (my_ui.score(prefix)):
		i = 0
		while i < len(letters):
			trystring(my_ui, prefix + letters[i], letters, maxlen)
			i += 1

def main(stdscr):

	my_ui = UI(stdscr)
	letters = my_ui.getletters()
	maxlen = my_ui.getmaxlen()
	my_ui.res_colwd = maxlen + 2

	i = 0
	while i < len(letters):
		trystring(my_ui, letters[i], letters, maxlen)
		i += 1

	my_ui.wrapup()

# Curses wrapper tries to leave the tty in a sane state on exit
curses.wrapper(main)
