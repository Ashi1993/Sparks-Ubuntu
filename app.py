# - coding: utf-8 --
from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from cosine import *

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'sparks'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/loadBooks", methods=['POST', 'GET'])
def loadBooks():
    _name = request.form['name']
    print(_name)
    
    _type = request.form['searchtype']
    print(_type)

    conn = mysql.connect()
    cursor = conn.cursor()

    books= []

    if _type == "general" :
        data = relevance(_name)
        if len(data) != 0:
            # conn.commit()
            for d in data:
                print(d[0])
                id = d[0]
                value = d[1]
                if value != 0.0:
                    cursor.callproc('loadbooks', [id])
                    book = cursor.fetchall()
                    print(book[0])
                    if len(book) != 0:
                        conn.commit()
                        books.append(book[0])
                            
            # print(books)
        else:
            return render_template('error.html', name=_name, text = "No Data Found")
    elif _type == "book":
        cursor.callproc('loadbookbyname', [_name])
        data = cursor.fetchall()
        # print(data)
        if len(data) != 0:
            conn.commit()
            for d in data:
                print("data")
                print(d)
                if len(books) == 0:
                    books.append(d)
                else:
                    for book in books:
                        if book[0]==d[0]:
                            continue
                        else:
                            print("books")
                            books.append(d)

            print(books)
        else:
            return render_template('error.html', name=_name, text = "No Data Found")
    elif _type == "author" :
        print("author")
        cursor.callproc('loadbookbyauthor', [_name])
        data = cursor.fetchall()
        # print(data)
        if len(data) != 0:
            conn.commit()
            for d in data:
                print("data")
                print(d)
                if len(books) == 0:
                    books.append(d)
                else:
                    for book in books:
                        if book[0]==d[0]:
                            continue
                        else:
                            print("books")
                            books.append(d)

            # print(books)
        else:
            return render_template('error.html', name=_name, text = "No Data Found")

    # print(data)
    if len(data) != 0:
        conn.commit()
        if len(books) == 0:
            return render_template('error.html', name=_name, text = "No Data Found")
        else:
            return render_template('book.html', name=_name, data = books)
    else:
        return render_template('error.html', name=_name, text = "No Data Found")


@app.route("/loadBookDetails/<id>", methods=['POST', 'GET'])
def loadBookDetails(id):
    print(id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('loadbookdetails', [id])
    data = cursor.fetchall()
    print(data)

    if len(data) != 0:
        conn.commit()
        return render_template('loadbookdetails.html', data = data)
    else:
        return json.dumps({'error': 'No data Found'})



@app.route("/books")
def books():
    return render_template('book.html')


if __name__ == "__main__":
	app.run(debug=True)
