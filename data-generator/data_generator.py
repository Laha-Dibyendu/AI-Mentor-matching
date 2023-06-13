import time
import os
import openai
import random

## Setting open ai key
openai.api_key = "open_ai_key"


## lis, lis1, lis2, lis3 are the list of job titles fpor which we are creating the data
lis = ['Software Developer',
       'Marketing Manager',
       'Human Resources Generalist',
       'Customer Service Representative',
       'Data Analyst',
       'Web Developer',
       'Sales Representative',
       'Graphic Designer',
       'Content Writer',
       'Project Manager',
       "Social Media Manager",
       'Business Analyst',
       'Financial Analyst',
       'Operations Manager',
       'Account Manager',
       'Systems Engineer',
       'Product Manager',
       'Supply Chain Analyst',
       'Quality Assurance Analyst',
       'Network Administrator',
       'IT Manager',
       'Customer Success Manager',
       'Mechanical Engineer',
       'Electrical Engineer',
       'Chemical Engineer',
       'Aerospace Engineer',
       'Biomedical Engineer',
       'Software Tester',
       'UI/UX Designer',
       'Technical Writer',
       'Logistics Coordinator',
       'Legal Assistant',
       'Executive Assistant',
       'Project Coordinator',
       'Event Planner',
       "Marketing Coordinator",
       'Public Relations Specialist',
       'Market Research Analyst',
       'Sales Manager',
       'IT Support Specialist',
       'Database Administrator',
       'Cloud Architect']

lis1 = ['Cloud Engineer',
        'Full Stack Developer',
        'Front End Developer',
        'Back End Developer',
        'DevOps Engineer',
        'Network Engineer',
        'Cybersecurity Analyst',
        'Business Development Manager',
        'Account Executive',
        'Brand Manager',
        'Art Director',
        'Digital Marketing Manager',
        'SEO Specialist',
        'SEM Specialist',
        'UI Designer',
        'UX Researcher',
        'Product Owner',
        'Scrum Master',
        'Data Scientist',
        'Machine Learning Engineer',
        'Artificial Intelligence Specialist',
        'Blockchain Developer',
        'ERP Specialist',
        'QA Engineer',
        'Technical Project Manager',
        'Technical Program Manager',
        'System Administrator',
        'Database Developer',
        'Software Architect',
        'iOS Developer',
        'Android Developer',
        'Mobile Application Developer',
        'Embedded Systems Engineer',
        'Robotics Engineer',
        'Quality Control Inspector',
        'Manufacturing Engineer',
        'Production Manager',
        'Materials Manager',
        'Procurement Specialist',
        'Vendor Manager',
        'Environmental Scientist']
lis2 = [
    'Geologist',
    'Archaeologist',
    'Anthropologist',
    'Historian',
    'Biologist',
    'Chemist',
    'Physicist',
    'Mathematician',
    'Economist',
    "Sociologist",
    'Political Scientist',
    'Psychologist',
    'Counselor',
    'Physical Therapist',
    'Occupational Therapist',
    'Nurse Practitioner',
    'Physician Assistant',
    'Doctor',
    'Dentist',
    'Optometrist',
    'Pharmacist',
    'Veterinarian',
    'Food Scientist',
    'Food Technologist',
    'Culinary Chef',
    'Bartender',
    'Restaurant Manager',
    'Hotel Manager',
    'Travel Agent',
    'Tour Guide',
    'Real Estate Agent',
    'Real Estate Appraiser',
    'Real Estate Broker',
    'Property Manager',
    'Construction Manager',
    'General Contractor',
    'Electrician',
    'Plumber',
    'Carpenter',
    'Painter',
    'HVAC Technician']

lis3 = [
    'Automotive Mechanic',
    'Diesel Mechanic',
    'Motorcycle Mechanic',
    'Aircraft Mechanic',
    'Marine Mechanic',
    'Truck Driver',
    'Delivery Driver',
    'Bus Driver',
    'Train Operator',
    'Flight Attendant',
    'Pilot',
    'Air Traffic Controller',
    'Border Patrol Agent',
    'Correctional Officer',
    'Police Officer',
    'Detective',
    'Security Guard',
    'Firefighter',
    'EMT']

L = []
## Code for generating the data 
for j in lis3:
    count = 0

    while count < 10:
        g = {}
        p = round(random.uniform(0, 1), 2)
        response = openai.Completion.create(
            model="text-curie-002", # Open ai model we are using for more info you should go to open ai play ground
            prompt="Generate an about thinking yourself as an experienced working professional of {} field.".format(
                j),
            temperature=p,# based on this parameter the accuracy or how it is created changes
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        g["Name"] = j+str(count)
        g["About"] = response["choices"][0]["text"]
        L.append(g)
        count += 1

    #print(g)
    time.sleep(3)
#sprint(response)


print("#########################  Final ")
print(L)
