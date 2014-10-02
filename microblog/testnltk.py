import nltk
import nltk.chunk
import re

def main():

	"""data1 = "404 not found"
	tokenized = nltk.word_tokenize(data1)
	p = nltk.pos_tag(tokenized)
	name = nltk.ne_chunk(p, binary=True)
	ent = re.findall(r'NE\s(.*?)/', str(name))"""
	#chunkGram = r"""Number: {<CD\w?>} """
	"""chunkParser = nltk.RegexpParser(chunkGram)
	CDNumber = chunkParser.parse(p)
	ip_number = re.findall(r'Number\s(.*?)/', str(CDNumber))
	print ip_number"""


	ip_noun = ['Sleeping','s','find', 'Sleeping', 'so', 's']
	db_noun = ['sleep','ss','finds']

	count_noun = 0
     	for ip in ip_noun:
            for dbs in db_noun:
                db_plural = re.escape(dbs) + 's?'
                ip_plural = re.escape(ip) + 's?'
                if re.match(db_plural, ip,flags=0):
                	print dbs,ip,'Found1'
                	count_noun = count_noun + 1
                if re.match(ip_plural,dbs,flags=0):
                	print ip,dbs,'Found2'
                	count_noun = count_noun + 1
                if ip == dbs:
                    count_noun = count_noun - 1
        #text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
        #text.similar('famous')

        print int(4 * 0.8 + 0.5)
        print "before duplicate removal" , ip_noun
        ip_noun = list(set(ip_noun))
        print "after duplicate removal" , ip_noun

        ip = ['sunish']

        i = ip_noun + ip

        print i

if __name__ == "__main__":
    main()