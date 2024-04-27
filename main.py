from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sensor import sensors
from pydantic import BaseModel
from models import Sensor
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import datetime



app = FastAPI()
#zoneTmp hold the hard coded values 
zoneTmp = sensors()
#Takes current time and coverts it to a optimal format
currtime = datetime.datetime.now()
currtime = currtime.strftime("%d/%m/%Y %H:%M")


#####################################################
#                                                   #
#                   Get Methods                     #
#                                                   #
#####################################################


@app.get("/", tags=["ShowAll/Simulation"])
def displaySensors():
    return zoneTmp

@app.get("/allSensors", tags=["Get"])
def allSensors():
    """
    This function shows all the sensors with identification, zone and status.\n
    This function doesn't need any parameters
    """
    xdict = {}
    for x, x_value in zoneTmp.items():
        tmpDict = {}
        for y, y_value in x_value.items():
            tmpValues = {}
            for z, z_value in y_value.items():
                if z == "status":
                    tmpValues[z] = z_value
            tmpDict[y] = tmpValues
        xdict[x] = tmpDict
    return xdict

@app.get("/zoneSensors/{zone}", tags=["Get"])
def zoneSensors(zone):
    """
    This function shows all the data inside of a zone except the nickname of the sensor.\n
    Function takes the name of the zone e.g **Lohko1**.
    """
    for x, x_value in zoneTmp.items():
        tmpDict = {}
        if x == zone:
            for y, y_value in x_value.items():
                tmpValues = {}
                for z, z_values in y_value.items():
                    if z == "status" or z == "values":
                        tmpValues[z] = z_values
                tmpDict[y] = tmpValues
            return tmpDict
    else:
        return{"message": "Zone not found"}
                

@app.get("/oneSensor", tags=["Get"])
def Sensordata(sensor):
    """
    This function shows all data about a specific sensor.\n
    Function takes a parameter identification of the sensor e.g **Sensor_1**\n
    **!!NOTICE!!** the zone is displayed inside of the sensor but actualy it is outside of the sensor.
    """
    mainDict = {}
    xDict = {}
    for x, x_value in zoneTmp.items():
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
    else:
        return{"message": "Sensor not found"}

@app.get("/sensorStatus/{sensor}", tags=["Get"])
def Sensorstatus(sensor):
    """
    This function displays all status history.\n
    Status section has a integer id as a key and list value which has the timestamp and the status of the sensory at that moment\n
    Function takes a parameter that is the identification of the sensor e.g **Sensor_1**
    """
    for x, x_value in zoneTmp.items():
        tmpDict = {}
        for y, y_value in x_value.items():
            tmpValues = {}
            if sensor == y:
                for z, z_values in y_value.items():
                    if z == "status":
                        tmpValues[z] = z_values
                tmpDict[y] = tmpValues
                return tmpDict
    else:
        return{"message": "Sensor not found"}

@app.get("/sensorsByStatus/{status}", tags=["Get"])
def sensorsByStatus(status):
    """
    This function display all the sensors with a specific status\n
    Function's parameter takes the status name e.g **Working** or **Error**.
    """
    mainDict = {}
    xDict = {}
    for x, x_value in zoneTmp.items():
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
    #This function takes all the errors timestamps and appends them to a list
    error_times = []

    for lohko, sensors in data.items():
        for sensor, sensor_data in sensors.items():
            for time, status in sensor_data["status"].values():
                if status == "Error":
                    error_times.append(datetime.datetime.strptime(time, "%d/%m/%Y %H:%M"))

    return error_times

@app.get("/statusGraph", tags=["Get"])
def statusGraph():
    """
    This function takes all the error's timestapms and creates a graph when the error's happened
    """
    data = sensors()
    error_times = check_error_status(data)
    #This part draws the graph
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot_date(error_times, [1]*len(error_times), "o")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y %H:%M"))
    plt.title("Error Status Over Time")
    plt.xlabel("Time")
    plt.yticks([])
    plt.grid(True)

    plt.xticks(rotation=45)

    plt.tight_layout()
    #Converts the graph into binary format so it can be used in the web
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


#####################################################
#                                                   #
#                  Post Methods                     #
#                                                   #
#####################################################

@app.post("/sensorSendSimulation", tags=["ShowAll/Simulation"])
def sensorSendSimulation(sensor, value: str):
    for x, x_value in zoneTmp.items():
        for y, y_value in x_value.items():
            if y == sensor:
                y_value["values"][len(y_value["status"]) + 1] = currtime + " " + value + "°C"
                return {"message": "Value added"}
        else:
            return{"message": "Sensor not found"}


@app.post("/addNewSensor", tags=["Post"])
def createNewSensor(zone: str, sensor_id: str, sensor: Sensor):
    """
    This function adds a new sensor to the backend\n
    Function parameters are name of the zone, sensor identification and the body of the sensor\n
    **!!NOTICE!!** that you need to be careful when filling the sensor body. Edit only the values except please retype the identification keys for the status dictionary starting from 0 from the top\n
    **TYPOS IN KEYS AND VALUES CAN AND WILL COUSE SOME OF THE FUNCTIONS NOT TO WORK ON THAT SENSOR.**
    """
    if zone not in zoneTmp:
        zoneTmp[zone] = {}
    zoneTmp[zone][sensor_id] = sensor
    return {"message": "Sensor added successfully"}

@app.post("/changeStatus", tags=["Post"])
def changeStatus(sensor):
    """
    This function changes the status of a specific sensor from Working to Error and via versa\n
    Parameter takes the identification of that sensor
    """
    for x, x_value in zoneTmp.items():
        for y, y_value in x_value.items():
            if y == sensor:
                if y_value["status"][0][1] == "Working":
                    y_value["status"][len(y_value["status"]) + 1] = [currtime, "Error"]
                elif y_value["status"][0][1] == "Error":
                    y_value["status"][len(y_value["status"]) + 1] = [currtime, "Working"]
                return {"message": "Sensor status changed"}
    else:
        return{"message": "Sensor not found"}

@app.post("/changeZone", tags=["Post"])
def changeZone(fromZone, sensor, toZone):
    """
    This function moves a sensor from zone to another
    """
    for x, x_value in zoneTmp.items():
        if x == fromZone:
            for y, y_value in list(x_value.items()):
                if y == sensor:
                    if toZone in zoneTmp:
                        zoneTmp[toZone][y] = y_value
                        del zoneTmp[fromZone][y]
                        return{"message": "Sensor zone changed"}
        else:
            return {"message": "Zone or sensor not found"}

@app.post("/deleteValue", tags=["Post"])
def deleteValue(sensor, id: int):
    """
    This function deletes a specific value by its identification
    """
    for x, x_value in zoneTmp.items():
        for y, y_value in x_value.items():
            if y == sensor:
                del y_value["values"][id]
                return{"message": "Value deleted"}
        else:
            return{"message": "Sensor not found"}