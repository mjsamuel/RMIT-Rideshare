import requests, json

try:
    response = requests.get(
        'http://localhost:5000/api/cars?{}={}'
        .format("colour", "black"))
    data = json.loads(response.text)
    cars = data['cars']
except:
    print("Problem communicating with server")
    cars = []

print('%-2s | %-10s | %-10s | %-8s | %s | %s | %s' % (
    "ID",
    "Make",
    "Body Type",
    "Colour",
    "No. Seats",
    "Cost/Hour",
    "Location"))
print('---+------------+------------+----------+-----------+-----------+----------------------')

for car in cars:
    print('%-2d | %-10s | %-10s | %-8s | %-9d | $%-8d | %s' % (
        car['id'],
        car['make'],
        car['body_type'],
        car['colour'],
        car['no_seats'],
        car['cost_per_hour'],
        car['location']))
