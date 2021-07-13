#!/bin/bash
#
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
#
# findwords.sh:
#	Find words that are candidates for the NYT Spelling Bee
#
#	Syntax:
#		findwords.sh [letters]
#	where [letters] is the set of letters allowed, with the first
#	letter in the string being the required (center) letter.
#
#	Bugs:
#		My word list includes way too many false positives.

# Location of the wordlist
wordlist="unigram"

musthave=`echo $1 | sed -e 's/^\(.\).*/\1/'`
exclude='[-0-9_.,^'
for i in a b c d e f g h i j k l m n o p q r s t u v w x y z
do
	if (echo $1 | grep -q -v $i)
	then
		exclude=$exclude$i
	fi
done
exclude=$exclude\]

# Find words with the required letter, get rid of all excluded letters,
# keep four-char or longer, get rid of capital letters as a proxy for
# proper nouns

grep -i $musthave $wordlist | grep -i -v $exclude | grep .... | grep -v '[A-Z]' | sort

exit 0
