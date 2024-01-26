from flask import Flask,render_template,request
import pickle 
import pandas as pd
import numpy as np

popular= pd.read_pickle("popular.pkl")
books=pd.read_pickle('books.pkl')
table=pd.read_pickle('table.pkl')
similarity_scores=pd.read_pickle('similarity_scores.pkl')
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular['Book-Title'].values),
                           author=list(popular['Book-Author'].values),
                           image=list(popular['Image-URL-M'].values),
                           votes=list(popular['num_rating'].values),
                           rating=list(popular['avg_rating'].values.round(1))
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    index=np.where(table.index==user_input)[0][0]
    similar_books = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data=[]
    for i in similar_books:
        item=[]
        temp=books[books['Book-Title']==table.index[i[0]]]
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    print(data)
    return render_template('recommend.html',data=data)

if __name__=='__main__':
    app.run(debug=True)