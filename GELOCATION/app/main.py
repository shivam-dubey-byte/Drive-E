from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import webbrowser

app = Flask(__name__)


GoogleMaps(app, key="AIzaSyCs_7u2FgIvY7-WjBpEGFhVhfI272vf6Fs")
@app.route("/",methods=['GET','POST'])
def __index__():
    if request.method == 'POST':
        y = request.form.get('longitude')
        x = request.form.get('latitude')
        print(str(x) +" | "+ str(y))
        return str(x) +" | "+ str(y)
    return render_template('geo.html')
@app.route("/map")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': 37.4419,
             'lng': -122.1419,
             'infobox': "<b>Hello World</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
             'lat': 37.4300,
             'lng': -122.1400,
             'infobox': "<b>Hello World from other place</b>"
          }
        ]
    )
    return render_template('example.html', mymap=mymap, sndmap=sndmap)


if __name__=='__main__':
    app.run(debug=True)
