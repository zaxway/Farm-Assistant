import firebase_admin
import csv
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('firebase-adminsdk.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iotworldhackathon-b6bb4.firebaseio.com/'
})

ref = db.reference('data/coordinates')
my_string = ref.get()
my_string = my_string.replace(')', '')
my_string = my_string.replace('(', '')
listOfNums = [x.strip() for x in my_string.split(',')]
lats = []
longs = []
minNum = 0;
maxNum = 0;
result = []
i = 1
for num in listOfNums:
    if (num != ''):
        if (i % 2 == 1):
            lats.append(float(num))
        elif (i % 2 == 0):
            longs.append(float(num))
    i = i + 1

minLats = min(lats)
minLongs = min(longs)
maxLats = max(lats)
maxLongs = max(longs)

result.append(str(minLongs))
result.append(str(maxLongs))
result.append(str(minLats))
result.append(str(maxLats))

fp = open('getCoordinates.txt', mode='w')

coord_writer = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
coord_writer.writerow(result)

fp.close()
