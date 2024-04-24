from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sensor import sensors
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import datetime

app = FastAPI()

hallitemp = sensors()

# time = datetime.datetime.now()
# time = time.strftime("%d/%m/%Y %H:%M")

@app.get("/")
def displaySensors():
    return hallitemp

@app.get("/allSensors")
def allSensors():
    xdict = {}
    for x, x_value in hallitemp.items():
        tmpDict = {}
        for y, y_value in x_value.items():
            tmpValues = {}
            for z, z_value in y_value.items():
                if z == "status":
                    tmpValues[z] = z_value
            tmpDict[y] = tmpValues
        xdict[x] = tmpDict
    return xdict

@app.get("/zoneSensors")
def zoneSensors(zone):
    for x, x_value in hallitemp.items():
        tmpDict = {}
        if x == zone:
            for y, y_value in x_value.items():
                tmpValues = {}
                for z, z_values in y_value.items():
                    if z == "status" or z == "values":
                        tmpValues[z] = z_values
                tmpDict[y] = tmpValues
            return tmpDict

@app.get("/oneSensor")
def Sensordata(sensor):
    mainDict = {}
    xDict = {}
    for x, x_value in hallitemp.items():
        tmpDict = {}
        for y, y_value in x_value.items():
            tmpValues = {}
            if y == sensor:
                xDict[x] = y_value
                mainDict[y] = xDict
                for z, z_values in y_value.items():
                    tmpValues[z] = z_values
                tmpDict[y] = tmpValues
    return mainDict

@app.get("/sensorStatus")
def Sensorstatus(sensor):
    for x, x_value in hallitemp.items():
        tmpDict = {}
        for y, y_value in x_value.items():
            tmpValues = {}
            if sensor == y:
                for z, z_values in y_value.items():
                    if z == "status":
                        tmpValues[z] = z_values
                tmpDict[y] = tmpValues
                return tmpDict

@app.get("/sensorsByStatus")
def sensorsByStatus(status):
    mainDict = {}
    xDict = {}
    for x, x_value in hallitemp.items():
        tmpDict = {}
        for y, y_value in x_value.items():
            tmpValues = {}
            for z, z_values in y_value.items():
                if z == "status":
                    if y_value.get("status", {}).get(1, [None, None])[1] == status:
                        tmpValues[z] = z_values
                        tmpDict[y] = tmpValues
        if tmpDict:
            mainDict[x] = tmpDict
    return mainDict

def check_error_status(data):
    error_times = []

    for lohko, sensors in data.items():
        for sensor, sensor_data in sensors.items():
            for time, status in sensor_data["status"].values():
                if status == "Error":
                    error_times.append(datetime.datetime.strptime(time, "%d/%m/%Y %H:%M"))

    return error_times

@app.get("/statusGraph")
def statusGraph():
    data = sensors()
    error_times = check_error_status(data)

    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot_date(error_times, [1]*len(error_times), "o")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y %H:%M"))
    plt.title("Error Status Over Time")
    plt.xlabel("Time")
    plt.yticks([])
    plt.grid(True)

    plt.xticks(rotation=45)

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
