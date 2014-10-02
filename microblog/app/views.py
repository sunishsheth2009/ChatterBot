from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db
from forms import LoginForm
from formadmin import dbent
from models import Positive, Negative, Assertive, Wikipedia, Chats, Similar
from app import db, models
from wikipedia import wikipedia
from sqlalchemy import func
import re
import nltk
import datetime
import time

@app.route('/')
@app.route('/index')
def index():
    dell = models.Chats.query.all()
    for d in dell:
        db.session.delete(d)
    db.session.commit()
    return redirect('/test')

@app.route('/positive')
def poss():
    poss = models.Positive.query.all()
    for p in poss:
        flash(p.question , 'Question')
        flash(p.answer , 'Answer')
    return render_template("positive.html",
                title = 'Information Bot: Final Year Project')

@app.route('/negative')
def negg():
    negg = models.Negative.query.all()
    for n in negg:
        flash(n.question , 'Question')
        flash(n.answer , 'Answer')
    return render_template("negative.html",
                title = 'Information Bot: Final Year Project')

@app.route('/assertive')
def asss():
    asss = models.Assertive.query.all()
    for a in asss:
        flash(a.question , 'Question')
        flash(a.answer , 'Answer')
    return render_template("assertive.html",
                title = 'Information Bot: Final Year Project')

@app.route('/wikipedia')
def wikii():
    wiki = models.Wikipedia.query.all()
    for w in wiki:
        flash(w.question , 'Question')
        flash(w.answer , 'Answer')
    return render_template("wikipedia.html",
                title = 'Information Bot: Final Year Project')



@app.route('/admin')
def admin():
    return render_template("admin.html",
                title = 'Information Bot: Final Year Project')


@app.route('/dbentry', methods = ['GET', 'POST'])
def dbentry():
    formdb = dbent()
    if formdb.validate_on_submit():
        if formdb.tablename.data == 'Negative' or formdb.tablename.data == 'Positive' or formdb.tablename.data == 'Assertive':    
            error = 0
        else:
            error = 1
            flash("Enter Negative Positive Assertive in the Table name", "Error")

        if error == 0:
            if formdb.tablename.data == 'Negative':
                table = formdb.tablename.data.lower()
                q = formdb.quess.data
                a = formdb.answ.data
                u = models.Negative(question = q, answer = a)
                db.session.add(u)
                db.session.commit()
                flash("1 value added in " + table  , "Error")
            if formdb.tablename.data == 'Positive':
                table = formdb.tablename.data.lower()
                q = formdb.quess.data
                a = formdb.answ.data
                u = models.Positive(question = q, answer = a)
                db.session.add(u)
                db.session.commit()
                flash("1 value added in " + table  , "Error") 
            if formdb.tablename.data == 'Assertive':
                table = formdb.tablename.data.lower()
                q = formdb.quess.data
                a = formdb.answ.data
                u = models.Assertive(question = q, answer = a)
                db.session.add(u)
                db.session.commit()
                flash("1 value added in " + table  , "Error")  
        
        return redirect('/dbentry')
    return render_template("dbentry.html",
        title = 'Information Bot: Final Year Project',
        formdb = formdb)



@app.route('/test', methods = ['GET', 'POST'])
def test():
    form = LoginForm()
    if form.validate_on_submit():
        flash(form.openid.data , 'Question')
        text = form.openid.data.lower()
        data = form.openid.data.lower() # for processing of answer(data mining)
        data1 = form.openid.data # for finding verbs nouns adjectives and number
        text = text.split() # for finding positive negative and assertive

        # Finding Nouns
        tokenized = nltk.word_tokenize(data1)
        p = nltk.pos_tag(tokenized)
        flash(p, 'Answer')
        name = nltk.ne_chunk(p, binary=True)
        ent = re.findall(r'NE\s(.*?)/', str(name))
        chunkGram = r"""Noun: {<NN\w?>} """
        chunkParser = nltk.RegexpParser(chunkGram)
        NNnoun = chunkParser.parse(p)
        ip_noun = re.findall(r'Noun\s(.*?)/', str(NNnoun))
        #noun = re.findall(r'<NN\w?>*', str(p))
        #print ent
        #nouns = ''
        #for n in ip_noun:
        #    nouns = nouns + n + ' '
        #flash ('Nouns: ' + str(nouns), 'Answer')
        flash ('Nouns list: ' + str(ip_noun), 'Answer')

        # Finding Verbs
        tokenized = nltk.word_tokenize(data1)
        p = nltk.pos_tag(tokenized)
        name = nltk.ne_chunk(p, binary=True)

        chunkGram = r"""Verb: {<VB\w?>} """
        chunkParser = nltk.RegexpParser(chunkGram)
        VBverb = chunkParser.parse(p)
        ip_verb = re.findall(r'Verb\s(.*?)/', str(VBverb))
        #noun = re.findall(r'<NN\w?>*', str(p))
        #print ent
        #verbs = ''
        #for v in ip_verb:
        #    verbs = verbs + v + ' '
        #flash ('Verbs: ' + str(verbs), 'Answer')
        flash ('Verb List: ' + str(ip_verb), 'Answer')

        # Finding Adjective
        tokenized = nltk.word_tokenize(data1)
        p = nltk.pos_tag(tokenized)
        name = nltk.ne_chunk(p, binary=True)

        chunkGram = r"""Verb: {<JJ\w?>} """
        chunkParser = nltk.RegexpParser(chunkGram)
        JJAdj = chunkParser.parse(p)
        ip_adj = re.findall(r'Verb\s(.*?)/', str(JJAdj))
        #noun = re.findall(r'<NN\w?>*', str(p))
        #print ent
        #adjs = ''
        #for a in ip_adj:
        #    adjs = adjs + a + ' '
        #flash ('Ajectives: ' + str(adjs), 'Answer')
        flash ('Adjective list: ' + str(ip_adj), 'Answer')

        # Finding Numbers
        tokenized = nltk.word_tokenize(data1)
        p = nltk.pos_tag(tokenized)
        name = nltk.ne_chunk(p, binary=True)
        chunkGram = r"""Number: {<CD\w?>} """
        chunkParser = nltk.RegexpParser(chunkGram)
        CDNumber = chunkParser.parse(p)
        ip_number = re.findall(r'Number\s(.*?)/', str(CDNumber))
        flash ('Number list: ' + str(ip_number), 'Answer')

        max_check = len(ip_noun) + len(ip_verb) + len(ip_adj) + len(ip_number) #counting the number of max hits

        # Similar Noun Form
        simi = models.Similar.query.all()
        count_n = len(ip_noun)
        max_n = 0
        for noun_sim in ip_noun:
            for sim in simi:
                if sim.word1 == noun_sim:
                    ip_noun.append(str(sim.word2))
                    ip_noun.append(str(sim.word3))
                if sim.word2 == noun_sim:
                    ip_noun.append(str(sim.word1))
                    ip_noun.append(str(sim.word3))
                if sim.word3 == noun_sim:
                    ip_noun.append(str(sim.word1))
                    ip_noun.append(str(sim.word2))
            max_n = max_n + 1
            if max_n >= count_n:
                break


        # Similar Verb Form
        simi = models.Similar.query.all()
        count_v = len(ip_verb)
        max_v = 0
        for verb_sim in ip_verb:
            for sim in simi:
                if sim.word1 == verb_sim:
                    ip_verb.append(str(sim.word2))
                    ip_verb.append(str(sim.word3))
                if sim.word2 == verb_sim:
                    ip_verb.append(str(sim.word1))
                    ip_verb.append(str(sim.word3))
                if sim.word3 == verb_sim:
                    ip_verb.append(str(sim.word1))
                    ip_verb.append(str(sim.word2))
            max_v = max_v + 1
            if max_v >= count_v:
                break

        # Similar Adjective Form
        simi = models.Similar.query.all()
        count_a = len(ip_adj)
        max_a = 0
        for adj_sim in ip_adj:
            for sim in simi:
                if sim.word1 == adj_sim:
                    ip_adj.append(str(sim.word2))
                    ip_adj.append(str(sim.word3))
                if sim.word2 == adj_sim:
                    ip_adj.append(str(sim.word1))
                    ip_adj.append(str(sim.word3))
                if sim.word3 == adj_sim:
                    ip_adj.append(str(sim.word1))
                    ip_adj.append(str(sim.word2))
            max_a = max_a + 1
            if max_a >= count_a:
                break

        #Printing the new appended list        
        flash ('Nouns list: ' + str(ip_noun), 'Answer')
        flash ('Verb List: ' + str(ip_verb), 'Answer')
        flash ('Adjective list: ' + str(ip_adj), 'Answer')
        flash ('Number list: ' + str(ip_number), 'Answer')

        ip_total = ip_noun + ip_verb + ip_adj + ip_number
        ip_total = list(set(ip_total))

        negator = ['not', 'never', 'not possible', 'does not', 'abort', 'neither', 'nor', 'negative', 'negate', 'can\'t', 'doesn\'t','can not','cant','doesnt','dont','don\'t']
        assertor = ['may be', 'can be', 'not sure', 'might', 'may']
        '''preposition = ['have', 'is', 'are', 'about', 'above', 'across', 'after', 'against', 'along', 'among', 'around', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'by', 'down', 'during', 'except', 'for', 'from', 'front', 'inside', 'instead', 'into', 'like', 'near', 'of', 'off', 'on', 'onto', 'top', 'out', 'outside', 'over', 'past', 'since', 'through', 'to', 'toward', 'under', 'underneath', 'until', 'up', 'upon', 'with', 'within', 'without']
        wh = ['why', 'what', 'how', 'Who', 'whoever', 'whom', 'whomever', 'whose', 'which']
        pronoun = ['i', 'me', 'you', 'she', 'her', 'he', 'him', 'it', 'we', 'us', 'you', 'they', 'them', 'my', 'mine', 'your', 'yours', 'hers', 'his', 'its', 'yours', 'ours', 'theirs', 'myself', 'yourself', 'himself', 'herself', 'itself', 'all', 'another', 'any', 'anybody', 'anyone', 'anything', 'both', 'each', 'either', 'everybody', 'everyone', 'everything', 'few', 'many', 'neither', 'nobody', 'none', 'nothing', 'one', 'several', 'some', 'somebody', 'someone', 'something', 'this', 'that', 'these', 'those']
        # Removing Wh Question
        wh_q=''
        for ser in text:
            inflag = 0
            for w in wh:
                if w == ser:
                    inflag = 1
            if inflag == 0:
                wh_q = wh_q + ser + ' '


        # Removing Prepostion
        wh_q = wh_q.split()
        prep_q = ''
        for ser in wh_q:
            inflag = 0
            for prep in preposition:
                if ser == prep:
                    inflag = 1
            if inflag == 0:
                prep_q = prep_q + ser + ' '


        # Removing Pronoun
        prep_q = prep_q.split()
        pro_q = ''
        for ser in prep_q:
            inflag = 0
            for pro in pronoun:
                if ser == pro:
                    inflag = 1
            if inflag == 0:
                pro_q = pro_q + ser + ' '

        text = pro_q
        text = text.split()
        data = pro_q.strip()
        
        '''
        flag = 0
        answer = 0
        wikiflag = 0
        ans = 0
        asser = 0
        nege = 0
        posi = 0
        #Assertive Section
        for ser in text:
            for ass in assertor:
                if ser == ass and flag == 0 or data.find(ass) != -1 and flag == 0:
                    asser = 1
                    flash('Assertive', 'Answer')
                    flag=1
        if asser == 1:
            display_ans = ''
            max_value = int(max_check * 0.8 + 0.5) # counting the no of hits
            abc = models.Positive.query.all()
            for a in abc:
                # Noun
                tokenized = nltk.word_tokenize(a.question)
                p = nltk.pos_tag(tokenized)
                name = nltk.ne_chunk(p, binary=True)
                ent = re.findall(r'NE\s(.*?)/', str(name))
                chunkGram = r"""Noun: {<NN\w?>} """
                chunkParser = nltk.RegexpParser(chunkGram)
                NNnoun = chunkParser.parse(p)
                db_noun = re.findall(r'Noun\s(.*?)/', str(NNnoun))

                # Verbs
                tokenized = nltk.word_tokenize(a.question)
                p = nltk.pos_tag(tokenized)
                name = nltk.ne_chunk(p, binary=True)
                chunkGram = r"""Verb: {<VB\w?>} """
                chunkParser = nltk.RegexpParser(chunkGram)
                VBverb = chunkParser.parse(p)
                db_verb = re.findall(r'Verb\s(.*?)/', str(VBverb))

                # Adjective
                tokenized = nltk.word_tokenize(a.question)
                p = nltk.pos_tag(tokenized)
                name = nltk.ne_chunk(p, binary=True)
                chunkGram = r"""Verb: {<JJ\w?>} """
                chunkParser = nltk.RegexpParser(chunkGram)
                JJAdj = chunkParser.parse(p)
                db_adj = re.findall(r'Verb\s(.*?)/', str(JJAdj))


                # Number
                tokenized = nltk.word_tokenize(a.question)
                p = nltk.pos_tag(tokenized)
                name = nltk.ne_chunk(p, binary=True)
                chunkGram = r"""Number: {<CD\w?>} """
                chunkParser = nltk.RegexpParser(chunkGram)
                CDNumber = chunkParser.parse(p)
                db_number = re.findall(r'Number\s(.*?)/', str(CDNumber))

                db_total = db_noun + db_adj + db_verb + db_number
                db_total = list(set(db_total))

                count = 0
                for ip in ip_total:
                    for dbs in db_total:
                        db_plural = re.escape(dbs) + 's?'
                        ip_plural = re.escape(ip) + 's?'
                        if re.match(db_plural, ip,flags=0|re.IGNORECASE):
                            count = count + 1
                        if re.match(ip_plural,dbs,flags=0|re.IGNORECASE):
                            count = count + 1
                        if ip == dbs:
                            count = count - 1

                if max_value < count:
                    display_ans = a.answer
                    max_value = count

            if display_ans == '':
                answer = 0
            else:
                answer = 1

            if answer == 0:
                flash('Answer not in database... Lets search Wikipedia Database', 'Answer')
                wikiflag = 1
            else:
                extra = 'Please be more sure about the problem you are facing so that we can provide you with precise answers. According to me the most relevant solution to your problem is: '
                display_ans = extra + '\n' + display_ans
                flash(display_ans, 'Answer')

             
            """for a in abc:
                if (data.find(a.question.lower()) != -1 or a.question.lower().find(data) != -1) and len(data) >= 4:
                    ans = 1
                    break
            if ans == 0:
                answer = 0
            else:
                answer = 1

            if answer == 0:
                flash('Answer not in database... Lets search Wikipedia Database', 'Answer')
                wikiflag = 1
                #return redirect ('http://www.lmgtfy.com/?q=' + data)
            else:
                finalans=a.answer
                flash(a.answer, 'Answer')"""

        #Negative Section
        if asser != 1:
            for ser in text:          
                for neg in negator:
                    if ser == neg and flag == 0 or data.find(neg) != -1 and flag == 0:
                        nege = 1
                        flash('Negative', 'Answer')
                        flag = 1
            if nege == 1:
                display_ans = ''
                max_value = int(max_check * 0.8 + 0.5) # counting the no of hits
                abc = models.Negative.query.all()
                for a in abc:
                    # Noun
                    tokenized = nltk.word_tokenize(a.question)
                    p = nltk.pos_tag(tokenized)
                    name = nltk.ne_chunk(p, binary=True)
                    ent = re.findall(r'NE\s(.*?)/', str(name))
                    chunkGram = r"""Noun: {<NN\w?>} """
                    chunkParser = nltk.RegexpParser(chunkGram)
                    NNnoun = chunkParser.parse(p)
                    db_noun = re.findall(r'Noun\s(.*?)/', str(NNnoun))

                    # Verbs
                    tokenized = nltk.word_tokenize(a.question)
                    p = nltk.pos_tag(tokenized)
                    name = nltk.ne_chunk(p, binary=True)
                    chunkGram = r"""Verb: {<VB\w?>} """
                    chunkParser = nltk.RegexpParser(chunkGram)
                    VBverb = chunkParser.parse(p)
                    db_verb = re.findall(r'Verb\s(.*?)/', str(VBverb))

                    # Adjective
                    tokenized = nltk.word_tokenize(a.question)
                    p = nltk.pos_tag(tokenized)
                    name = nltk.ne_chunk(p, binary=True)
                    chunkGram = r"""Verb: {<JJ\w?>} """
                    chunkParser = nltk.RegexpParser(chunkGram)
                    JJAdj = chunkParser.parse(p)
                    db_adj = re.findall(r'Verb\s(.*?)/', str(JJAdj))

                   # Number
                    tokenized = nltk.word_tokenize(a.question)
                    p = nltk.pos_tag(tokenized)
                    name = nltk.ne_chunk(p, binary=True)
                    chunkGram = r"""Number: {<CD\w?>} """
                    chunkParser = nltk.RegexpParser(chunkGram)
                    CDNumber = chunkParser.parse(p)
                    db_number = re.findall(r'Number\s(.*?)/', str(CDNumber))

                    db_total = db_noun + db_adj + db_verb + db_number
                    db_total = list(set(db_total))

                    count = 0
                    for ip in ip_total:
                        for dbs in db_total:
                            db_plural = re.escape(dbs) + 's?'
                            ip_plural = re.escape(ip) + 's?'
                            if re.match(db_plural, ip,flags=0|re.IGNORECASE):
                                count = count + 1
                            if re.match(ip_plural,dbs,flags=0|re.IGNORECASE):
                                count = count + 1
                            if ip == dbs:
                                count = count - 1

                    if max_value < count:
                        display_ans = a.answer
                        max_value = count

                if display_ans == '':
                    answer = 0
                else:
                    answer = 1

                if answer == 0:
                    flash('Answer not in database... Lets search Wikipedia Database', 'Answer')
                    wikiflag = 1
                else:
                    flash(display_ans, 'Answer')


                """for a in abc:
                    if (data.find(a.question.lower()) != -1 or a.question.lower().find(data) != -1) and len(data) >= 4:
                        ans = 1
                        break
                if ans == 0:
                    answer = 0
                else:
                    answer = 1

                if answer == 0:
                    flash('Answer not in database... Lets search Wikipedia Database', 'Answer')
                    wikiflag = 1
                    #return redirect ('http://www.lmgtfy.com/?q=' + data)
                else:
                    finalans=a.answer
                    flash(a.answer, 'Answer')"""

        #Postive Section
        if asser != 1 and nege != 1:
            if flag == 0:
                data = form.openid.data.lower()
                flash('Positive', 'Answer')
                flag = 1
                display_ans = ''
                max_value = int(max_check * 0.8 + 0.5) # counting the no of hits
                abc = models.Positive.query.all()
                for a in abc:
                    # Noun
                    tokenized = nltk.word_tokenize(a.question)
                    p = nltk.pos_tag(tokenized)
                    name = nltk.ne_chunk(p, binary=True)
                    ent = re.findall(r'NE\s(.*?)/', str(name))
                    chunkGram = r"""Noun: {<NN\w?>} """
                    chunkParser = nltk.RegexpParser(chunkGram)
                    NNnoun = chunkParser.parse(p)
                    db_noun = re.findall(r'Noun\s(.*?)/', str(NNnoun))

                    # Verbs
                    tokenized = nltk.word_tokenize(a.question)
                    p = nltk.pos_tag(tokenized)
                    name = nltk.ne_chunk(p, binary=True)
                    chunkGram = r"""Verb: {<VB\w?>} """
                    chunkParser = nltk.RegexpParser(chunkGram)
                    VBverb = chunkParser.parse(p)
                    db_verb = re.findall(r'Verb\s(.*?)/', str(VBverb))

                    # Adjective
                    tokenized = nltk.word_tokenize(a.question)
                    p = nltk.pos_tag(tokenized)
                    name = nltk.ne_chunk(p, binary=True)
                    chunkGram = r"""Verb: {<JJ\w?>} """
                    chunkParser = nltk.RegexpParser(chunkGram)
                    JJAdj = chunkParser.parse(p)
                    db_adj = re.findall(r'Verb\s(.*?)/', str(JJAdj))

                    # Number
                    tokenized = nltk.word_tokenize(a.question)
                    p = nltk.pos_tag(tokenized)
                    name = nltk.ne_chunk(p, binary=True)
                    chunkGram = r"""Number: {<CD\w?>} """
                    chunkParser = nltk.RegexpParser(chunkGram)
                    CDNumber = chunkParser.parse(p)
                    db_number = re.findall(r'Number\s(.*?)/', str(CDNumber))

                    db_total = db_noun + db_adj + db_verb + db_number
                    db_total = list(set(db_total))

                    count = 0
                    for ip in ip_total:
                        for dbs in db_total:
                            db_plural = re.escape(dbs) + 's?'
                            ip_plural = re.escape(ip) + 's?'
                            if re.match(db_plural, ip,flags=0|re.IGNORECASE):
                                count = count + 1
                            if re.match(ip_plural,dbs,flags=0|re.IGNORECASE):
                                count = count + 1
                            if ip == dbs:
                                count = count - 1

                    if max_value < count:
                        display_ans = a.answer
                        max_value = count

                if display_ans == '':
                    answer = 0
                else:
                    answer = 1

                if answer == 0:
                    flash('Answer not in database... Lets search Wikipedia Database', 'Answer')
                    wikiflag = 1
                else:
                    flash(display_ans, 'Answer')

                """abc = models.Positive.query.all()
                for a in abc:
                    if (data.find(a.question.lower()) != -1 or a.question.lower().find(data) != -1) and len(data) >= 4:
                        ans = 1
                        break
                if ans == 0:
                    answer = 0
                else:
                    answer = 1

                if answer == 0:
                    flash('Answer not in database... Lets search Wikipedia Database', 'Answer')
                    wikiflag = 1
                    #return redirect ('http://www.lmgtfy.com/?q=' + data)
                else:
                    finalans=a.answer
                    flash(a.answer, 'Answer')"""

        #Wiki Section
        ans = 0
        if wikiflag == 1:

            display_ans = ''
            max_value = int(max_check * 0.8 + 0.5) # counting the no of hits
            abc = models.Wikipedia.query.all()
            for a in abc:
                # Noun
                tokenized = nltk.word_tokenize(a.question)
                p = nltk.pos_tag(tokenized)
                name = nltk.ne_chunk(p, binary=True)
                ent = re.findall(r'NE\s(.*?)/', str(name))
                chunkGram = r"""Noun: {<NN\w?>} """
                chunkParser = nltk.RegexpParser(chunkGram)
                NNnoun = chunkParser.parse(p)
                db_noun = re.findall(r'Noun\s(.*?)/', str(NNnoun))

                # Verbs
                tokenized = nltk.word_tokenize(a.question)
                p = nltk.pos_tag(tokenized)
                name = nltk.ne_chunk(p, binary=True)
                chunkGram = r"""Verb: {<VB\w?>} """
                chunkParser = nltk.RegexpParser(chunkGram)
                VBverb = chunkParser.parse(p)
                db_verb = re.findall(r'Verb\s(.*?)/', str(VBverb))

                # Adjective
                tokenized = nltk.word_tokenize(a.question)
                p = nltk.pos_tag(tokenized)
                name = nltk.ne_chunk(p, binary=True)
                chunkGram = r"""Verb: {<JJ\w?>} """
                chunkParser = nltk.RegexpParser(chunkGram)
                JJAdj = chunkParser.parse(p)
                db_adj = re.findall(r'Verb\s(.*?)/', str(JJAdj))

                # Number
                tokenized = nltk.word_tokenize(a.question)
                p = nltk.pos_tag(tokenized)
                name = nltk.ne_chunk(p, binary=True)
                chunkGram = r"""Number: {<CD\w?>} """
                chunkParser = nltk.RegexpParser(chunkGram)
                CDNumber = chunkParser.parse(p)
                db_number = re.findall(r'Number\s(.*?)/', str(CDNumber))

                db_total = db_noun + db_adj + db_verb + db_number
                db_total = list(set(db_total))

                count = 0
                for ip in ip_total:
                    for dbs in db_total:
                        db_plural = re.escape(dbs) + 's?'
                        ip_plural = re.escape(ip) + 's?'
                        if re.match(db_plural, ip,flags=0|re.IGNORECASE):
                            count = count + 1
                        if re.match(ip_plural,dbs,flags=0|re.IGNORECASE):
                            count = count + 1
                        if ip == dbs:
                            count = count - 1

                if max_value < count:
                    display_ans = a.answer
                    max_value = count

            if display_ans == '':
                answer = 0
            else:
                answer = 1

            """abc = models.Wikipedia.query.all()
            for a in abc:
                if (data.find(a.question.lower()) != -1 or a.question.lower().find(data) != -1) and len(data) >= 4:
                    ans = 1
                    break
            if ans == 0:
                answer = 0
            else:
                answer = 1"""

            if answer == 0:
                flash('Answer not in Wikipedia database... Lets search Wikipedia Internet', 'Answer')
                ny = wikipedia.search(data)
                if ny == []:
                    return redirect ('http://www.lmgtfy.com/?q=' + data1)
                else:
                    try:
                        ny1 = wikipedia.summary(data1, chars=0, auto_suggest=True, redirect=True, sentences=3)
                        max_value = int(max_check * 0.8 + 0.5)
                        ip_wiki = ny1.encode('ascii','ignore')
                        # Noun
                        tokenized = nltk.word_tokenize(ip_wiki)
                        p = nltk.pos_tag(tokenized)
                        name = nltk.ne_chunk(p, binary=True)
                        ent = re.findall(r'NE\s(.*?)/', str(name))
                        chunkGram = r"""Noun: {<NN\w?>} """
                        chunkParser = nltk.RegexpParser(chunkGram)
                        NNnoun = chunkParser.parse(p)
                        db_noun = re.findall(r'Noun\s(.*?)/', str(NNnoun))

                        # Verbs
                        tokenized = nltk.word_tokenize(ip_wiki)
                        p = nltk.pos_tag(tokenized)
                        name = nltk.ne_chunk(p, binary=True)
                        chunkGram = r"""Verb: {<VB\w?>} """
                        chunkParser = nltk.RegexpParser(chunkGram)
                        VBverb = chunkParser.parse(p)
                        db_verb = re.findall(r'Verb\s(.*?)/', str(VBverb))

                        # Adjective
                        tokenized = nltk.word_tokenize(ip_wiki)
                        p = nltk.pos_tag(tokenized)
                        name = nltk.ne_chunk(p, binary=True)
                        chunkGram = r"""Verb: {<JJ\w?>} """
                        chunkParser = nltk.RegexpParser(chunkGram)
                        JJAdj = chunkParser.parse(p)
                        db_adj = re.findall(r'Verb\s(.*?)/', str(JJAdj))

                        # Number
                        tokenized = nltk.word_tokenize(ip_wiki)
                        p = nltk.pos_tag(tokenized)
                        name = nltk.ne_chunk(p, binary=True)
                        chunkGram = r"""Number: {<CD\w?>} """
                        chunkParser = nltk.RegexpParser(chunkGram)
                        CDNumber = chunkParser.parse(p)
                        db_number = re.findall(r'Number\s(.*?)/', str(CDNumber))

                        db_total = db_noun + db_adj + db_verb + db_number
                        db_total = list(set(db_total))

                        count = 0
                        for ip in ip_total:
                            for dbs in db_total:
                                db_plural = re.escape(dbs) + 's?'
                                ip_plural = re.escape(ip) + 's?'
                                if re.match(db_plural, ip,flags=0|re.IGNORECASE):
                                    count = count + 1
                                if re.match(ip_plural,dbs,flags=0|re.IGNORECASE):
                                    count = count + 1
                                if ip == dbs:
                                    count = count - 1

                        if max_value <= count:
                            display_ans = ny1

                        if display_ans == '':
                            answer = 0
                        else:
                            answer = 1

                        if answer == 0:
                            flash('Answer not precise in wikipedia Interet', 'Answer')
                            flash(ny1, 'Answer')
                            wikiflag = 1
                        else:
                            display_ans=ny1
                            flash(ny1, 'Answer')
                            ny2 = wikipedia.page(data1)
                            flash('Source: '+ ny2.url, 'Answer')
                            #u = models.Wikipedia(question=data1, answer=ny1)
                            #db.session.add(u)
                            #db.session.commit()
                    except Exception as inst:
                        flash('Your question is either out of scope of very trival for me to answer  ' + str(inst), 'Answer')
                        display_ans = 'Your question is either out of scope of very trival for me to answer'
            else:
                flash(display_ans, 'Answer')
        #s = models.Chats.query.all()
        #for chat in reversed(s):
            #flash('Question: ' + chat.question, 'Display')
            #flash('Answer: ' + chat.answer , 'Display')
            #flash('.', 'Display')
        #u = models.Chats(question=data1, answer=display_ans)
        #db.session.add(u)
        #db.session.commit() 
        return redirect('/test')
    return render_template("index2.html",
        title = 'ChatterBot',
        form = form)