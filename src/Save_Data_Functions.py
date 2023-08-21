"""!
@file Save_Data_Functions.py
@brief This sub-program includes the functions needed to save and remove/delete data ( CSV, png ).
@author 
     - Mr. Mohamed Ali Haoufa
     - Mr. Mohamed Nacer Namane
@date Jun 7, 2022
@copyright Copyright (c) 2022.  All rights reserved.
"""
import os 
import csv
import time

def write_to_csv(data,filename):
    """!
    @brief Write data to a CSV file.
    
    This function appends a timestamp and data to a CSV file. It uses the current time as a timestamp,
    and the provided data is appended to the file along with the timestamp.
    
    @param data The data to be written to the CSV file.
    @param filename The name of the CSV file to write to.
    
    @return write_to_log The result of the write operation (1 for success, 0 for failure).
    """
    time0=time.time()  # Get the current time
    print ( time0 )

    # Create a list with timestamp and data
    apend = [time0 , data]

    # Open the CSV file for appending : 
    # the a is for append, if w for write is used then it overwrites the file
    with open(filename,'a') as sensor_readings:
       sensor_write = csv.writer(sensor_readings, delimiter=',', quotechar='"' , quoting=csv.QUOTE_MINIMAL)
       write_to_log = sensor_write.writerow(apend)  # Write the data to the file

       return(write_to_log)

def remove_csv(filename):
    """!
    @brief Remove a CSV file if it exists.

    This function checks if the specified file exists and is a regular file. If it does, the file is deleted.
    If the file does not exist or is not a regular file, a corresponding message is printed.

    @param filename The name of the CSV file to be removed.

    @return message A message indicating whether the file was deleted or not.
    """
    file =filename 
    if(os.path.exists(file) and os.path.isfile(file)):
      os.remove(file)  # Delete the file
      return   print("file deleted")
    else:
      return   print("file not found")  

def delete_png(png_name): 
  """!
  @brief Delete a PNG image file.

  This function removes the specified PNG image file from the file system.

  @param png_name The name of the PNG image file to be deleted.

  @return None
  """
  import os
  os.remove(png_name)   # Delete the PNG image file
  return 