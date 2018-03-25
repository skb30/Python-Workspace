# 
# Example file for parsing and processing JSON
# (For Python 3.x, be sure to use the ExampleSnippets3.txt file)

import tkinter
import urllib.request
import json
import operator
import datetime
from datetime import date, time


# from http.client import HTTPSConnection
# from base64 import b64encode
from pyfoo.pyfoo import PyfooAPI

api = PyfooAPI("skb30", '8HPC-V0V6-DYDE-NBRK')
for form in api.forms:
    print( '%s (%s)' % (form.Name, form.entry_count) )

# for report in api.reports:
#     print( '%s (%s)' % (report.Name, report.entry_count) )
#
# for user in api.users:
#     print( '%s (%s)' % (report.Name, report.entry_count) )

contact_form = api.forms[0]

dropOff = contact_form.get_field('Drop off and Pick up Time and Dates:')
name_breed = contact_form.get_field("Pet's Name and Breed")
age_gender_weight = contact_form.get_field('Age, Gender, Weight')
emergery_contact = contact_form.get_field('Emergency Contact. (Please include veterinarian contact information)')
feeding_instructions = contact_form.get_field('Feeding Instructions. (Please include treat habits)')
exercise_habits = contact_form.get_field('Exercise habits (Number of walks per day? Ball fetching?)')
sleeping_instructions = contact_form.get_field('Sleeping Instructions? (Create trained, has own bed, etc.)')

form_entires = contact_form.get_entries()
for entry in form_entires:
    print("*****************************************************************")
    print("Date Details> {}".format(entry[dropOff.ID]))
    print("Name and Breed> {}".format(entry[name_breed.ID]))
    print("Age and Gender> {}".format(entry[age_gender_weight.ID]))
    print("Emergency Contact> {}".format(entry[emergery_contact.ID]))
    print("Feeding Instructions> {}".format(entry[feeding_instructions.ID]))
    print("Exercise Habits> {}".format(entry[exercise_habits.ID]))
    print("Sleeping Instructions> {}".format(entry[sleeping_instructions.ID]))
    print("*****************************************************************")


# for field in contact_form.fields:
#     print(field.Type)
# print(contact_form)
# email_field = contact_form.get_field('Email')
# entries = contact_form.get_entries() # By default this returns 100 entries sorted by DateCreated descending
# for entry in entries:
#     print( entry[email_field.ID] )

# entry = entries[0]
# for field in contact_form.fields:
#     if field.SubFields:
#         for subfield in field.SubFields:
#             print( '%s: %s' % (subfield.Label, entry[subfield.ID]) )
#     else:
#         print( '%s: %s' % (field.Title, entry[field.ID]) )

