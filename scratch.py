pattern = {
    -1.0: 0,
    -0.9: 5,
    -0.8: 10,
    -0.7: 15,
    -0.6: 20,
    -0.5: 25,
    -0.4: 30,
    -0.3: 35,
    -0.2: 40,
    -0.1: 45,
    0.0: 50,
    0.1: 55,
    0.2: 60,
    0.3: 65,
    0.4: 70,
    0.5: 75,
    0.6: 80,
    0.7: 85,
    0.8: 90,
    0.9: 95,
    1.0: 100
}

#print(pattern.get(-0.0))

message = "55"

if len(message) <= 3:
    if int(message) > 100:
       print(f"DEBUG LINE1: {message}")
    else:
       print(f"Works: {message}")
else:
   print(f"DEBUG LINE2: {message}")