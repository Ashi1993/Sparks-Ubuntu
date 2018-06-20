# - coding: utf-8 --
from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL

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
        _words = _name.split(" ")
        for word in _words:
            print(word)
            cursor.callproc('loadbooks', [word])
            data = cursor.fetchall()
            print(data)
            if len(data) != 0:
                conn.commit()
                for d in data:
                    if d not in books:
                        books.append(d)

                print(books)
            else:
                return render_template('error.html', name=_name, text = "No Data Found")
    elif _type == "book":
        cursor.callproc('loadbookbyname', [_name])
        data = cursor.fetchall()
        print(data)
        if len(data) != 0:
            conn.commit()
            for d in data:
                if d not in books:
                    books.append(d)

            print(books)
        else:
            return render_template('error.html', name=_name, text = "No Data Found")
    elif _type == "author" :
        cursor.callproc('loadbookbyauthor', [_name])
        data = cursor.fetchall()
        print(data)
        if len(data) != 0:
            conn.commit()
            for d in data:
                books.append(d)

            print(books)
        else:
            return render_template('error.html', name=_name, text = "No Data Found")

    print(data)
    if len(data) != 0:
        conn.commit()
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
