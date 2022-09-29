import numpy as np
import cv2 as cv
import pytesseract
import re
import json
import io


# Deployment Libraries
import streamlit as st

#Title
st.title('OCR Demo')
st.write('OCR Of Invoice Bill')

# Specifying the path
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Function to Find a particular Word in a Sentence.
def findword(textlist, wordlist):
  for text in textlist:
    for word in wordlist:
      if re.search(word, text):
        return text

# File Upload
filename = st.file_uploader("Choose your file :", type=['png', 'jpg'], accept_multiple_files=False)


if filename is not None:
  image = cv.imread(filename.name,0)
  text = pytesseract.image_to_string(image, lang = 'eng', config = '--psm 3 --oem 3')
  text1 = []
  lines = text.split('\n')
  for lin in lines:
    s = lin.strip()
    s = lin.replace('\n','')
    s = s.rstrip()
    s = s.lstrip()
    text1.append(s)

  text1 = list(filter(None, text1))
  
  #Creating Variable
  INO = None
  IND = None

  #Getting Invoice Number
  ino = findword(text1, ['INVOICE NO','INVOICE NO.','SALES CONTRACT','SC REF.', 'OUR REF'])
  ind = findword(text1, ['INVOICE DATE', 'DATE'])


  # Cleaning Invoice Number
  ino = re.findall(r'\d+',ino)
  INO = ino[0]

  #Cleang Invoice date
  ind = re.search(r'(\d+/\d+/\d+|\d+.\d+.\d+)',ind).group()
  IND = ind

  data = {}
  data['ID TYPE'] = 'Invoice'
  data['INVOICE NUMBER'] = INO
  data['INVOICE DATE'] = IND
  #st.write(data)


  try:
    with io.open('info.json', 'w', encoding='utf-8') as outfile:
      data_extracted = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
      outfile.write(data_extracted)

  #Reading the JSON
    with open('info.json', encoding = 'utf-8') as data_load:
      data_loaded = json.load(data_load)

    if data_loaded['ID TYPE'] == 'Invoice':
      st.write("\n---------- Invoice Details ----------")
      st.write("\nINVOICE NUMBER: ",data_loaded['INVOICE NUMBER'])
      st.write("\nINVOICE DATE: ",data_loaded['INVOICE DATE'])
      st.write("\n-------------------------------------")

    if st.button("See Raw Extraction"):
      st.write("\n---------- Invoice Raw Extraction ----------")
      st.write(text)
      st.write("\n--------------------------------------------")

  except:
    st.write("\n------------------------- False Documents ---------------------------")
    st.write("\n The Uploaded Document is Not Correct Please Upload Correct Documents")