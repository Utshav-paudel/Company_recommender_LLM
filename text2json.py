#@ Scirpt for converting text file to JSON object using Structuring.py script

import structuring as sh
import json
import time
with open('data/company_profile_list.txt' , 'r') as file:
    company_profile = file.read()


# adding json data
# function to add score to JSON formats
def write_json(new_data, filename='company_data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["company_score"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)


for company in company_profile:
    print(f"{company}\n")
    out = sh.company_score_generator(f"{company}")           # text to score
    update = write_json(out)                                 # add on json file
    time.sleep(20)                                            
    print(out)
    
if __name__=="__main__":
    write_json()



