from __future__ import print_function
import os, sys
import regex as re # regular expression

'''
More info at:
https://backstagecoding.blogspot.com/p/adding-furigana-on-blogger.html
'''

def insertKanjiFurigana(kanji, furigana):
	return '<ruby>'+kanji+'<rt>'+furigana+'</rt></ruby>'

def readAllLines(filepath):
	file_ = open(filepath, 'r')
	data  = file_.read()
	lines = data.split("\n")
	if  lines[len(lines)-1] == '':
		lines = lines[0:len(lines)-1] # removing empty string of the last line
	file_.close()
	return lines

def htmlFuriganizer(infilepath, htmlfilepath):
	lines = readAllLines(infilepath)
	
	fileout = open(os.path.join(os.getcwd(),htmlfilepath), 'w')
	for line in lines:
		kanji = ''
		furigana = ''
		newLine = ''
		kanjiRead = False
		furiRead = False
		for l in line:
			if l == '}':
				if furiRead == True:
					#print('Kanji:', kanji)
					#print('Furigana:', furigana)
					furiganized = insertKanjiFurigana(kanji, furigana)
					newLine = newLine+furiganized
					#print(furiganized)
					#print(newLine)
					#print('')
					kanji = ''
					furigana = ''
				furiRead = False
				kanjiRead = False
				continue	
			if l == '^':
				furiRead = True
				continue			
			if l == '{':
				kanjiRead = True if furiRead == False else False
				continue
			if kanjiRead == True:
				kanji = kanji+l
			elif furiRead == True:
				furigana = furigana+l
			else:
				newLine = newLine+l
		if newLine == '':
			fileout.write('<div><br /></div>\n')
		else:
			fileout.write('<div>'+newLine+'</div>\n')
	fileout.close()	
			
def organizeFuriganizedText(inputfilepath, outputfilepath):
	lines = readAllLines(inputfilepath)
	#pattern = re.compile(r'([\p{IsHan}\p{IsBopo}\p{IsHira}\p{IsKatakana}]+)', re.UNICODE)
	patternKanji = re.compile(r'([\p{IsHan}\p{IsBopo}]+)', re.UNICODE)
	patternHiragana = re.compile(r'([\p{IsHira}]+)', re.UNICODE)

	concatenateLines = ''
	# If the first word  of the original text is a kanji, 
	# then its furigana is written before it whe using furiganizer.com.
	# So the first word of the input file is never a kanji.
	for l in range(0,len(lines)-1):
		# if the next word is a kanji, then the current one 
		# is a furigana that will be appnded later.
		# Son, continue to the next word.
		line = lines[l+1]
		lineKanji = patternKanji.sub(r'{\1}^', line)
		if '^' in lineKanji:
			#print(lineKanji)
			continue
			
		line = lines[l]
		# when reading all lines, the line breaker is substituted by an empty string 
		# putting it back to keep the paragraph structure.
		if line == '':
			line = '\n'
			
		# Identify a Kanji by adding {kanji}^ on the string
		# If there is no kanji, nothing is changed
		lineKanji = patternKanji.sub(r'{\1}^', line)
		
		# If there is a kanji, the previous line is its furigana, 
		# always written in hiragana
		lineFuri = ''
		if '^' in lineKanji:
			prevLine = lines[l-1]
			lineFuri = patternHiragana.sub(r'{\1}', prevLine)
		concatenateLines = concatenateLines+lineKanji+lineFuri
	
	#print(concatenateLines)
	
	fileout = open(os.path.join(os.getcwd(),outputfilepath), 'w')
	fileout.write(concatenateLines)
	fileout.close()
	
	
if __name__ == '__main__':
	infilename = 'japaneseText'
	infilepath = os.path.join(os.getcwd(), infilename+'.txt')
	if os.path.exists(infilepath) == False:
		print('Error: path not found. Aborting.')
		print(filepath)
		sys.exit()	
	outfilepath = os.path.join(os.getcwd(), infilename+'New.txt')
	htmlfilepath = os.path.join(os.getcwd(), infilename+'Html.txt')
	
	organizeFuriganizedText(infilepath, outfilepath)
	htmlFuriganizer(outfilepath, htmlfilepath)
	
	
	print('Done.')
