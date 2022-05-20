import csv

def round_age(covidData):
    for covidCase in covidData:
        if '-' in covidCase['age']:
            splitAgeList = covidCase['age'].split('-')
            avgAge = (float)(splitAgeList[0]) + ((float)(splitAgeList[1]) - (float)(splitAgeList[0]))/2.0
            avgAge = round(avgAge)
            covidCase['age'] = str(avgAge)
    return covidData
    
def change_date_format(covidData):
    for covidCase in covidData:
        splitOnsetList        = covidCase['date_onset_symptoms'].split('.')
        splitHospitalList     = covidCase['date_admission_hospital'].split('.')
        splitConfirmationList = covidCase['date_confirmation'].split('.')
        mmddyyyyOnset         = splitOnsetList[1] + "." + splitOnsetList[0] + "." + splitOnsetList[2]
        mmddyyyyHospital      = splitHospitalList[1] + "." + splitHospitalList[0] + "." + splitHospitalList[2]
        mmddyyyyConfirmation  = splitConfirmationList[1] + "." + splitConfirmationList[0] + "." + splitConfirmationList[2]
        #print(covidCase)
        covidCase['date_onset_symptoms'] = mmddyyyyOnset
        covidCase['date_admission_hospital'] = mmddyyyyHospital
        covidCase['date_confirmation'] = mmddyyyyConfirmation
        #print(covidCase)
    return covidData
        
def fill_missing_latitude_longitude(covidData):
    provinceWithLatitude = {}
    provinceWithLongitude = {}
    
    totalLatitude = 0.0;
    countLatitude = 0.0;
    totalLongitude = 0.0;
    countLongitude = 0.0;
    for covidCase in covidData:
        provinceWithLatitude[covidCase['province']] =0.0 
        provinceWithLongitude[covidCase['province']] =0.0 
        
    #find avg latitude for each province  
    for x,y in provinceWithLatitude.items():
        for covidCase in covidData:
            if covidCase['province'] == x:
                if covidCase['latitude'] != 'NaN':
                    totalLatitude += (float)(covidCase['latitude'])
                    countLatitude +=1
        provinceWithLatitude[x] = round( (totalLatitude/countLatitude) ,2)
        totalLatitude =0
        countLatitude =0
        
    #find avg longitude for each province 
    for x,y in provinceWithLongitude.items():
        for covidCase in covidData:
            if covidCase['province'] == x:
                if covidCase['longitude'] != 'NaN':
                    totalLongitude += (float)(covidCase['longitude'])
                    countLongitude +=1
        provinceWithLongitude[x] = round( (totalLongitude/countLongitude) ,2)
        totalLongitude =0
        countLongitude =0
        
    #set latitude and longitude of each 'NaN' based on the avg for their respective province               
    for covidCase in covidData:
        if covidCase['latitude'] == 'NaN':
            covidCase['latitude'] = provinceWithLatitude[covidCase['province']]
        if covidCase['longitude'] == 'NaN':
            covidCase['longitude'] = provinceWithLongitude[covidCase['province']]
    return covidData
    
def fill_missing_city(covidData):
    dictOfCities = { 
       # 'fakeProvince'  : { 'fakecity' : 1 } 
    }
    for covidCase in covidData:
        currentCity = covidCase.get('city')
        currentProvince = covidCase.get('province')
     
        if currentProvince in dictOfCities.keys():
            if currentCity in dictOfCities[currentProvince].keys() and currentCity != 'NaN':
                dictOfCities[currentProvince][currentCity] += 1
            elif currentCity != 'NaN':
                dictOfCities[currentProvince][currentCity] = 1
        elif currentCity != 'NaN':
            dictOfCities[currentProvince] = {currentCity:1}
    
    
    mostProvince = {}
    for province, dictCitysInProvince in dictOfCities.items():
        highestNum = -1
        highestCity = ''
        for city, num in dictCitysInProvince.items():
            if highestNum < num:
                highestCity = city
                highestNum = num
            elif highestNum == num:
                if highestCity> city:
                    highestCity = city
                    highestNum = num
        mostProvince[province] = highestCity
        
   
    for covidCase in covidData:
        if covidCase['city'] == 'NaN':
            if covidCase['province'] in mostProvince:
                covidCase['city'] = mostProvince[covidCase['province']]
            else:
                covidCase['city'] = 'NaN'
    return covidData

def fill_missing_symptoms(covidData):
    dictOfSymptoms = { 
       # 'fakeProvince'  : { 'fakeSymptom' : 1 } 
    }
    for covidCase in covidData:
        currentSymptom = covidCase.get('symptoms')
        symptomInCurrentSymptom = currentSymptom.split(';')
        for symp in symptomInCurrentSymptom:
            symp = symp.strip()
            if 'fever' in symp:
                symp = 'fever'
            currentProvince = covidCase.get('province')
            if currentProvince in dictOfSymptoms.keys():
                if symp in dictOfSymptoms[currentProvince] and symp != 'NaN':
                    dictOfSymptoms[currentProvince][symp] += 1
                elif symp != 'NaN':
                    dictOfSymptoms[currentProvince][symp] = 1
            elif symp != 'NaN':
                dictOfSymptoms[currentProvince] = {symp:1}
                
    mostProvince = {}
    for province, dictSymptomsInProvince in dictOfSymptoms.items():
        highestNum = -1
        highestSymptom = ''
        for symptom, num in dictSymptomsInProvince.items():
            if highestNum < num:
                highestSymptom = symptom
                highestNum = num
            elif highestNum == num:
                if highestSymptom> symptom:
                    highestSymptom = symptom
                    highestNum = num
        mostProvince[province] = highestSymptom
 
    
    for covidCase in covidData:
        if covidCase['symptoms'] == 'NaN':
            covidCase['symptoms'] = mostProvince[covidCase['province']]
    return covidData
    
def main():
    reader = csv.DictReader(open('covidTrain.csv'))
    covidData = []
    for index, row in enumerate(reader):
        covidData.append(row)
   
    covidData  = round_age(covidData)
    covidData  = change_date_format(covidData)
    covidData  = fill_missing_latitude_longitude(covidData)
    covidData  = fill_missing_city(covidData)
    covidData  = fill_missing_symptoms(covidData)
    
    
    f = open('covidResult.csv', 'w') 
    writer = csv.writer(f)
    writer.writerow(covidData[0])
    for covidCase in covidData:
        tempList = []
        tempList.append(covidCase['ID'])
        tempList.append(covidCase['age'])
        tempList.append(covidCase['sex'])
        tempList.append(covidCase['city'])
        tempList.append(covidCase['province'])
        tempList.append(covidCase['country'])
        tempList.append(covidCase['latitude'])
        tempList.append(covidCase['longitude'])
        tempList.append(covidCase['date_onset_symptoms'])
        tempList.append(covidCase['date_admission_hospital'])
        tempList.append(covidCase['date_confirmation'])
        tempList.append(covidCase['symptoms'])
        writer.writerow(tempList)
    f.close()
    
    
main()