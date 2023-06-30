# 3D-print-club-website
A python flask website for managing resources and printer usage of 3D printing student club, stored in SQL database.

# How it looks

## Main page showing usage of printers  
Allowing you to start/abort/end current printings
![xd](https://github.com/sklimasz/3D-print-club-website/assets/80223720/b2494d97-8f8c-4dbe-af0c-f8c872507435)

## Start a new printing page  
![image](https://github.com/sklimasz/3D-print-club-website/assets/80223720/c532bee9-984e-4234-b989-e1c52a170915)

## End/abort printing page  
![image](https://github.com/sklimasz/3D-print-club-website/assets/80223720/d927521c-b6ec-4acd-b9e0-1b4406cf1bbd)

## Home page for managing resources
![image](https://github.com/sklimasz/3D-print-club-website/assets/80223720/4fec8dbd-5741-4c5c-8532-2889362003c1)






## Instructions
If you run it for the first time, you need to initialize the database. Run the sql.py file.  
Now you have the database ready, so you can just run the USETHIS.py file, and type in your browser the specified IP  
(that should be displayed in your python console).  
If you want to keep current data, don't run sql.py.  
You can terminate the USETHIS.py process and the data will be saved,  
and you can run USETHIS.py again to resume.  
If you want a clear start, just delete database and run sql.py again.  

## Notes
The codes comes with commented out lines of code for MAX7219 display and DHT11 sensor,  
because the code was hosted on RaspberryPI with additional functionalites  
(progress on MAX7219, sensor data displayed on website)  
If you have the necessary electronics, feel free to uncomment the code.  
The code with commented lines works on normal PC.  

## Necessary libraries
flask  
sqlite3  
datetime  
random (for debugging )  


