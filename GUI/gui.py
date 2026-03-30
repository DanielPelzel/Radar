import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("QT5Agg")
import time


ser = serial.Serial("/dev/cu.usbmodem14201", 9600, timeout=0.1)
time.sleep(2)

plt.ion()
fig = plt.figure(figsize=(8, 8), dpi=100)
ax = fig.add_subplot(111, projection='polar')

#Backend Design
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.tick_params(colors = "lime")
ax.grid(color = "lime", alpha=0.3)
ax.set_title("Radar", color = "lime", fontsize = 14 )

points = []



ax.set_ylim(0,400)
ax.set_theta_zero_location("W")
ax.set_theta_direction(-1)
ax.set_thetalim(0, np.pi)
ax.set_rticks([0, 100, 200, 300, 400])

beam_bg, = ax.plot([0,0], [0, 400], color = "lime", lw=3)
beam_obj, = ax.plot([0,0], [0, 0], color = "red", lw=3)

plt.show()
plt.pause(0.001)

print("Lese Daten ...")


ser.reset_input_buffer()
try:
    while True:

        line = ser.readline().decode("utf-8", errors = "ignore").strip()

        if line:
            print("data: " + line)

        if line and "," in line:

            parts = line.split(",")

            if len(parts) == 2:

                    theta = np.deg2rad(float(parts[0]))
                    r = float(parts[1])

                    beam_bg.set_data([theta, theta], [0, 400])
                    beam_obj.set_data([theta, theta], [0, r])

                    dot, = ax.plot(theta, r, "o", color="r", markersize=4)
                    points.append((time.time(), dot))

                    neue_liste = []
                    for t, d in points:
                        if time.time() - t < 2.0:
                            neue_liste.append((t, d))  # jung → behalten
                        else:
                            d.remove()  # alt → aus Plot löschen
                    points = neue_liste


                    # Diese drei Zeilen wecken das Fenster auf:
                    fig.canvas.draw_idle()


                    fig.canvas.flush_events()
                    plt.pause(0.01)
except ValueError:
    print("Fehler beim Parsen der Daten.")
finally:
    ser.close()
    print("Serielle Schnittstelle geschlossen.")

