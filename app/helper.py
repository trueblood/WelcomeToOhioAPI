import re
import string
class Helper:
    def find_person_info_from_drivers_license(text):
        x = text.find("First Name")


    def check_string(s):
        if len(s) < 2:
            return False
        if s[0].isdigit() and s[1].isalpha():
            return True
        return False
    
    def find_first_last_name_from_license(text):
        string = text
        pattern = r"\d[a-zA-Z]"
        result = re.findall(pattern, string)
        whiteSpace = re.findall(r'[\s]', string)
        for val in whiteSpace:
            value = string.index(val)
            print(str(value) + " " + val)
        for val in result:
            value = string.index(val)
            print(str(value) + " " + val)

            
        
        substring = string[result[1]:whiteSpace[0]] 
        print("Substring using slicing:", substring)


       # value = text.index(str(result))
        
    def find_person_info_from_license(text):
        array = text.split(" ")
        startIndex = array.index("1SAMPLE")
        endIndex = array.index("46204-0000")
        return (array[startIndex:endIndex+1])


Helper.find_person_info_from_license("a INDIANA... IDENTIFICATION CARD bmv.IN.gov PETER L. LACY, COMMISSIONER sow 1234-96-7890 exe 11/17/2023 1SAMPLE 2JELANI 8123 MAIN STREET INDIANAPOLIS, IN 46204-0000 9 CLASS NONE 9a END B 3 12RES NONE 15SEX M16 HGT 5'-11 17 WGT - 18EYES BRO 19 HAIR BRO sos CS 5 DD 12345678901234 DONOR® MEDICAL ALERT ")
#Helper.find_whitespace("a INDIANA... IDENTIFICATION CARD bmv.IN.gov PETER L. LACY, COMMISSIONER sow 1234-96-7890 exe 11/17/2023 1SAMPLE 2JELANI 8123 MAIN STREET INDIANAPOLIS, IN 46204-0000 9 CLASS NONE 9a END B 3 12RES NONE 15SEX M16 HGT 5'-11 17 WGT - 18EYES BRO 19 HAIR BRO sos CS 5 DD 12345678901234 DONOR® MEDICAL ALERT ")
#Helper.find_first_last_name_from_license("a INDIANA... IDENTIFICATION CARD bmv.IN.gov PETER L. LACY, COMMISSIONER sow 1234-96-7890 exe 11/17/2023 1SAMPLE 2JELANI 8123 MAIN STREET INDIANAPOLIS, IN 46204-0000 9 CLASS NONE 9a END B 3 12RES NONE 15SEX M16 HGT 5'-11 17 WGT - 18EYES BRO 19 HAIR BRO sos CS 5 DD 12345678901234 DONOR® MEDICAL ALERT ")