from word2number import w2n

class mtW2N:
	debug = False
	all_num_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety', 'hundred', 'thousand', 'lac', 'crore', 'million', 'billion', 'trillion']
	def get_exact_words_2_num(num_words):
		if mtW2N.debug: print('Num words: ', num_words)
		try:
			nn = w2n.word_to_num(' '.join(num_words))
			if mtW2N.debug: print('Num w2n: ', nn)
			return [str(nn)]
		except:
			return num_words

	def rep_w2n(text):
		if mtW2N.debug: print('Input text for w2n is: ', text)
		spl_text = text.split()
		tmp_words = []
		for w in spl_text:
			if w[-1] == '.':
				tmp_words.extend( [w[:-1], '.'] )
			else:
				tmp_words.append(w)

		if mtW2N.debug: print('Split words: ', tmp_words)
		num_words = []
		out_words = []
		for w in tmp_words:
			if w.lower() in mtW2N.all_num_words: num_words.append(w)
			elif len(num_words) > 0 and w.lower() in ['and', 'point']: num_words.append(w)
			else:
				if len(num_words) > 0:
					out_words.extend(mtW2N.get_exact_words_2_num(num_words))
					num_words = []
				out_words.append(w)
		if len(num_words) > 0: out_words.extend(mtW2N.get_exact_words_2_num(num_words))
		if mtW2N.debug: print('Out words: ', out_words)
		return ' '.join(out_words)

