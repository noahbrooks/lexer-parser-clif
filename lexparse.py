import ply.lex as lex
import ply.yacc as yacc

def main(CLIFfilePath, LexAndParse):
	
	if(LexAndParse):
		myFile = open(CLIFfilePath)
		lexer = ClifLexer()
		parser = ClifParser(lexer)
		parser.parse(myFile.read())
	else:
		myFile = open(CLIFfilePath)
		lexer = ClifLexer()
		lexer.lex(myFile.read())

## Lexer ##
class ClifLexer():

	# CONSTRUCTOR
	def __init__(self):
		print('Lexer constructor called.')
		self.lexer = lex.lex(module=self)
		# start in the (standard) initial state
		self.lexer.begin('INITIAL')

	# DESTRUCTOR
	def __del__(self):
		print('Lexer destructor called.')

	reserved_bool = {
		'and': 'AND',
		'or': 'OR',
		# Added
		'not' : 'NOT',
		'if' : 'IF',
		'iff' : 'IFF',
		'cl:comment': 'COMMENT'
	}


## ADDED 'DIGIT' ##
	tokens = ['OPEN', 'CLOSE', 'QUOTEDSTRING', 'RESERVEDELEMENT', 'NUMERAL']

	tokens += reserved_bool.values()

	t_ignore = ' \t\r\n\f\v'

	def t_NEWLINE(self,t):
		r'\n+'
		t.lexer.lineno += len(t.value)

	def t_error(self,t):
		print("Lexing error: Unknown character \"{}\" at line {}".format(t.value[0], t.lexer.lineno))
		t.lexer.skip(1)

	# token specification as a string (no regular expression)

	t_OPEN= '\('
	t_CLOSE= '\)'


	def t_RESERVEDELEMENT(self, t):
		# here we use a regular expression to say what matches this particular token:
		# any sequence of standard characters of length 1 or greater
		# but this does not yet cover all reservedelements
		r'[a-z|A-Z|\:]+'
		if t.value in self.reserved_bool:
			t.type = self.reserved_bool[t.value]
			#print("Boolean reserved word: " + t.value)
			return t
		else:
			pass

## Added ##
	#prints all numerals (digits 0-9 and numbers not in quotedstring)

	def t_NUMERAL(self, t):
		r'\d+'
		return t

### Added ###
	# change to quoted string, need r and the letter he wants in quoted string

	def t_QUOTEDSTRING(self, t):
		# This is not yet correct: you need to complete the lexing of quotedstring
		# we removed "_" from below because it's in \w we think?
		r'\'[\w|\~|\!|\#|\$|\%|\^|\&|\*|\+|\{|\}|\||\:|\<|\>|\?|\'|\-|\=|\[|\]|\;|\,|\.|\/ | " ]+\''
		return t

	def lex(self, input_string):
		self.lexer.input(input_string)
		while True:
			tok = self.lexer.token()
			if not tok:
				break
			print(tok)


## Parser ##
class ClifParser(object):

	tokens = ClifLexer.tokens

	# CONSTRUCTOR #
	def __init__(self,lexer):
		## Can remove asteriks when done, just added for output readability ##
		print('\n*Parser constructor called.*')
		self.lexer = ClifLexer()
		self.parser = yacc.yacc(module=self)
		## Can use for boolsent ops ##
		#self.ops = 0

	## Starts the parsing ##
	def p_starter(self, p):
		"""
		starter : multsentences
					| multsentences starter
		"""
		print("Starting the parsing process.\n")
		pass

	## Reads sentences until no more left ##
	def p_multsentences(self,p):
		"""
		multsentences : sentence multsentences
							| sentence
		"""
	
	## Decides whether the sentence is atomic or boolean ##
	def p_sentence(self, p):
		"""
		sentence : atomicsentence
					| booleansentence
		"""

		## Not 100% sure what this does but it isnt needed, can decide to keep or remove ##

		# print("Found a sentence: {} {} {} ".format(p[2], p[3], p[4]))
		# if p[3] == p[4]:
		# 	no_quotedstrings = 1
		# else:
		# 	no_quotedstrings = 2

		# print("Number of distinct quoted strings: " + str(no_quotedstrings))

	def p_interpretedname(self,p):
		"""
		interpretedname : NUMERAL
					| QUOTEDSTRING
		"""

	def p_predicate(self,p):
		"""
		predicate : interpretedname
		"""

## Could be any number of interpreted names from 0-infinity ##
	def p_termseq(self,p):
		"""
		termseq : emptyseq
					| interpretedname termseq
		"""
	
	def p_emptyseq (self,p):
		"""
		emptyseq : 
		"""

	def p_atomicsentence(self,p):
		"""
		atomicsentence : OPEN predicate termseq CLOSE
		"""
		
	def p_boolsent(self, p):
		"""
		booleansentence : OPEN AND multsentences CLOSE
							| OPEN OR multsentences CLOSE
							| OPEN IF multsentences CLOSE
							| OPEN IFF sentence sentence CLOSE
							| OPEN NOT sentence CLOSE
		"""
		## Use for ops as defined in constructor method ##
		##self.ops = +1##

	def p_error(self, p):

		if p is None:
			raise TypeError("Unexpectedly reached end of file (EOF)")

		# Note the location of the error before trying to lookahead
		error_pos = p.lexpos

		# Reading the symbols from the Parser stack
		stack = [symbol for symbol in self.parser.symstack][1:]

		print("Parsing error; current stack: " + str(stack))


	def parse(self, input_string):
		# initialize the parser
		#parser = yacc.yacc(module=self)

		self.parser.parse(input_string)

LexAndParse = True
CLIFfilePath = "./test.clif"

main(CLIFfilePath, LexAndParse)



# parser = ClifParser()
# s = "(or (not ('TODAY=03/26/22')) (not ('TODAY=03/26/22')) (and ('FRIDAY' 13)))" #Boolean#
# print('\nLexing '+s)
# parser.lexer.lex(s)
# print('\nParsing '+s)
# parser.parse(s)

# parser = ClifParser()
# s = "(and (0))" #Boolean#
# print('\nLexing '+s)
# parser.lexer.lex(s)
# print('\nParsing '+s)
# parser.parse(s)

# parser = ClifParser()
# s = "(and (0 1 2 3 4 'more;'))" #Boolean#
# print('\nLexing '+s)
# parser.lexer.lex(s)
# print('\nParsing '+s)
# parser.parse(s)

# parser = ClifParser()
# s = "(if (not ('True')) (and (0 '=' 1) (0 '=' 2) (not ('FalseStatement3'))))" #Boolean#
# print('\nLexing '+s)
# parser.lexer.lex(s)
# print('\nParsing '+s)
# parser.parse(s)

# parser = ClifParser()
# s = "(and (1000) (1001) ('1001+'))" #Boolean#
# print('\nLexing '+s)
# parser.lexer.lex(s)
# print('\nParsing '+s)
# parser.parse(s)

# parser = ClifParser()
# s = "(or (100) ('and' 1000 1001 '1001+'))" #Boolean#
# print('\nLexing '+s)
# parser.lexer.lex(s)
# print('\nParsing '+s)
# parser.parse(s)
