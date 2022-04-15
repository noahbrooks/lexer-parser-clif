# lexer-parser-clif

Grammar

char = digit | ’~’ | ’!’ | ’#’ | ’$’ | ’%’ | ’^’ | ’&’ | ’*’ | ’_’ | ’+’ | ’{’ | ’}’
| ’|’ | ’:’ | ’<’ | ’>’ | ’?’ | ’‘’ | ’-’ | ’=’ | ’[’ | ’]’ | ’;’| ’,’ | ’.’ | ’/’
| ’A’ | ’B’ | ’C’ | ’D’ | ’E’ | ’F’ | ’G’ | ’H’ | ’I’ | ’J’ | ’K’ | ’L’ | ’M’ | ’N’
| ’O’ | ’P’ | ’Q’ | ’R’ | ’S’ | ’T’ | ’U’ | ’V’ | ’W’ | ’X’ | ’Y’ | ’Z’
| ’a’ | ’b’ | ’c’ | ’d’ | ’e’ | ’f’ | ’g’ | ’h’ | ’i’ | ’j’ | ’k’ | ’l’ | ’m’ | ’n’
| ’o’ | ’p’ | ’q’ | ’r’ | ’s’ | ’t’ | ’u’ | ’v’ | ’w’ | ’x’ | ’y’ | ’z’
digit = ’0’ | ’1’ | ’2’ | ’3’ | ’4’ | ’5’ | ’6’ | ’7’ | ’8’ | ’9’
open = ’(’
close = ’)’
white = U+0020 | U+0009 | U+000A | U+000B | U+000C | U+000D
numeral = digit { digit }
reservedelement = ’and’ | ’or’ | ’iff’ | ’if’ | ’not’ | ’cl:comment’
stringquote = ’’’
namequote= ’"’
quotedstring = stringquote { char | namequote } stringquote
lexicaltoken = open | close | quotedstring | reservedelement

interpretedname = numeral | quotedstring
predicate = interpretedname
termseq = { interpretedname }
sentence = atomsent | boolsent
atomsent = open predicate termseq close
boolsent = ( open (’and’ | ’or’) { sentence } close )
| ( open (’if’ | ’iff’) sentence sentence close )
| ( open ’not’ sentence close )
