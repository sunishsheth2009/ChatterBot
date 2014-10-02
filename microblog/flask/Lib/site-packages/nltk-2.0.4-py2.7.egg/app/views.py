from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db
from forms import LoginForm
from models import Positive, Negative, Assertive, Wikipedia, Chats
from app import db, models
from wikipedia import wikipedia
from sqlalchemy import func

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



@app.route('/test', methods = ['GET', 'POST'])
def test():
    form = LoginForm()
    if form.validate_on_submit():
        flash(form.openid.data , 'Question')
        text = form.openid.data.lower()
        data = form.openid.data.lower()
        data1 = form.openid.data
        text = text.split()
        negator = ['not', 'never', 'not possible', 'does not', 'abort', 'neither', 'nor', 'no', 'negative', 'negate']
        assertor = ['may be', 'can be', 'not sure', 'might', 'may']
        preposition = ['have', 'is', 'are', 'about', 'above', 'across', 'after', 'against', 'along', 'among', 'around', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'by', 'down', 'during', 'except', 'for', 'from', 'front', 'inside', 'instead', 'into', 'like', 'near', 'of', 'off', 'on', 'onto', 'top', 'out', 'outside', 'over', 'past', 'since', 'through', 'to', 'toward', 'under', 'underneath', 'until', 'up', 'upon', 'with', 'within', 'without']
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
        flag = 0
        answer = 0
        wikiflag = 0
        ans = 0

        data = ''
        asser = 0
        nege = 0
        posi = 0
        #Assertive Section
        for ser in text:
            inflag = 0
            for ass in assertor:
                if ser == ass and flag == 0 or data.find(ass) != -1 and flag == 0:
                    inflag = 1
                    asser = 1
                    flash('Assertive', 'Answer')
                    flag=1
            if inflag == 0:
                data = data + ser + ' '
        if asser == 1:
            data = data.strip()
            abc = models.Assertive.query.all()
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
                flash(a.answer, 'Answer')

        #Negative Section
        if asser == 0:
            data = '' 
        for ser in text:
            inflag = 0           
            for neg in negator:
                if ser == neg and flag == 0 or data.find(neg) != -1 and flag == 0:
                    inflag = 1
                    nege = 1
                    flash('Negative', 'Answer')
                    flag = 1
            if inflag == 0:
                data = data + ser + ' '
        if nege == 1:
            data = data.strip()
            abc = models.Negative.query.all()
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
                flash(a.answer, 'Answer')

        #Postive Section

        if flag == 0:
            data = form.openid.data.lower()
            flash('Positive', 'Answer')
            abc = models.Positive.query.all()
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
                flash(a.answer, 'Answer')

        #Wiki Section
        ans = 0
        if wikiflag == 1:
            abc = models.Wikipedia.query.all()
            for a in abc:
                if (data.find(a.question.lower()) != -1 or a.question.lower().find(data) != -1) and len(data) >= 4:
                    ans = 1
                    break
            if ans == 0:
                answer = 0
            else:
                answer = 1

            if answer == 0:
                flash('Answer not in Wikipedia database... Lets search Wikipedia Internet', 'Answer')
                ny = wikipedia.search(data)
                if ny == []:
                    return redirect ('http://www.lmgtfy.com/?q=' + data1)
                else:
                    try:
                        ny1 = wikipedia.summary(data1, chars=0, auto_suggest=True, redirect=True, sentences=3)
                        finalans=ny1
                        flash(ny1, 'Answer')
                        ny2 = wikipedia.page(data1)
                        flash('Source: '+ ny2.url, 'Answer')
                        #u = models.Wikipedia(question=data, answer=ny1)
                        #db.session.add(u)
                        #db.session.commit()
                    except Exception as inst:
                        flash('Your question is either out of scope of very trival for me to answer', 'Answer')
                        finalans = 'Your question is either out of scope of very trival for me to answer'
            else:
                finalans=a.answer
                flash(a.answer, 'Answer')
        display = '\n'
        s = models.Chats.query.all()
        for chat in reversed(s):
            flash('Question: ' + chat.question, 'Display')
            flash('Answer: ' + chat.answer , 'Display')
            flash('.', 'Display')
        u = models.Chats(question=data1, answer=finalans)
        db.session.add(u)
        db.session.commit() 

        return redirect('/test')
    return render_template("index2.html",
        title = 'ChatterBot',
        form = form)