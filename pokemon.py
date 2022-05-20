import csv
import collections

def fire_pokemon_above_level(pokemonBox, level):
    firePokemonCount = 0
    above40 = 0
    for pokemon in pokemonBox:
        if pokemon.get('type') == 'fire':
            firePokemonCount+=1
            if ((float)(pokemon.get('level'))) >= 40:
                above40+= 1
    if firePokemonCount == 0:
        firePokemonPercent = 0
    else:
        firePokemonPercent = round((above40/firePokemonCount)*100.0000)
    with open('pokemon1.txt', 'w') as f:
        f.write("Percentage of fire type Pokemons at or above level 40 = " + str(firePokemonPercent))
    return

def fill_in_type(pokemonBox):
    dictOfTypes = { 
       # 'fakeWeakness'  : { 'fakeType' : 1 } 
    }
    for pokemon in pokemonBox:
        currentType = pokemon.get('type')
        currentWeakness = pokemon.get('weakness')
        if currentWeakness in dictOfTypes.keys():
            if currentType in dictOfTypes[currentWeakness].keys() and currentType != 'NaN':
                dictOfTypes[currentWeakness][currentType] += 1
            elif currentType != 'NaN':
                dictOfTypes[currentWeakness][currentType] = 1
        elif currentType != 'NaN':
            dictOfTypes[currentWeakness] = {currentType:1}

    mostWeak = {}
    for weakness, dictTypesWeaktoThatWeakness in dictOfTypes.items():
        highestNum = -1
        highestType = ''
        for Type, num in dictTypesWeaktoThatWeakness.items():
            if highestNum < num:
                highestType = Type
                highestNum = num
            elif highestNum == num:
                if highestType> Type:
                    highestType = Type
                    highestNum = num
        mostWeak[weakness] = highestType

    for pokemon in pokemonBox:
        if pokemon['type'] == 'NaN':
            pokemon['type'] = mostWeak[pokemon['weakness']]
    return pokemonBox

def fill_in_stats(pokemonBox, levelThreshold):
    averageAtkUnder, averageDefUnder, averageHpUnder, averageAtkOver, averageDefOver, averageHpOver = 0,0,0,0,0,0
    numAtkUnder, numDefUnder, numHpUnder, numAtkOver, numDefOver, numHpOver = 0,0,0,0,0,0
    for pokemon in pokemonBox:
        if (float)(pokemon['level']) > 40:
            if pokemon['atk'] != 'NaN':
                averageAtkOver += (float)(pokemon['atk'])
                numAtkOver += 1
            if pokemon['def'] != 'NaN':
                averageDefOver += (float)(pokemon['def'])
                numDefOver += 1
            if pokemon['hp'] != 'NaN':
                averageHpOver += (float)(pokemon['hp'])
                numHpOver += 1
        else:
            if pokemon['atk'] != 'NaN':
                averageAtkUnder += (float)(pokemon['atk'])
                numAtkUnder += 1
            if pokemon['def'] != 'NaN':
                averageDefUnder += (float)(pokemon['def'])
                numDefUnder += 1
            if pokemon['hp'] != 'NaN':
                averageHpUnder += (float)(pokemon['hp'])
                numHpUnder += 1

    averageAtkUnder /= round(numAtkUnder , 1)
    averageDefUnder /=round(numDefUnder , 1)
    averageHpUnder /=round(numHpUnder , 1)
    averageAtkOver /=round(numAtkOver , 1)
    averageDefOver /=round(numDefOver , 1)
    averageHpOver /=round(numHpOver , 1)

    averageAtkUnder = round(averageAtkUnder , 1)
    averageDefUnder =round(averageDefUnder , 1)
    averageHpUnder =round(averageHpUnder , 1)
    averageAtkOver =round(averageAtkOver , 1)
    averageDefOver =round(averageDefOver , 1)
    averageHpOver =round(averageHpOver , 1)

    for pokemon in pokemonBox:
        if pokemon['atk'] == 'NaN' and (float)(pokemon['level']) > 40:
            pokemon['atk'] = averageAtkOver
        elif pokemon['atk'] == 'NaN':
            pokemon['atk'] = averageAtkUnder
        if pokemon['def'] == 'NaN' and (float)(pokemon['level']) > 40:
            pokemon['def'] = averageDefOver
        elif pokemon['def'] == 'NaN':
            pokemon['def'] = averageDefUnder
        if pokemon['hp'] == 'NaN' and (float)(pokemon['level']) > 40:

            pokemon['hp'] =averageHpOver
        elif pokemon['hp'] == 'NaN':
            pokemon['hp'] = averageHpUnder

    return pokemonBox

def map_pokemon_to_type(pokemonBox):
    personalities = []
    x = {}
    
    for pokemon in pokemonBox:
        if (pokemon['type'] == 'NaN'):
            continue
        if (pokemon['type'] not in x.items()):
            x[pokemon['type']] = []
    for pokemon in pokemonBox:
        pokemonType = pokemon['type']
        pokemonPersonality = pokemon['personality']
        if (pokemonType in x.keys()):
            if (pokemonPersonality not in x[pokemonType]):
                x[pokemonType].append(pokemonPersonality)
                
    typesToPersonalities =  collections.OrderedDict(sorted(x.items()))
    for x,y in typesToPersonalities.items():
        typesToPersonalities[x].sort()
    f = open("pokemon4.txt", "w")
    f.write("Pokemon type to personality mapping:\n")
    for x,y in typesToPersonalities.items():
        listItems = str(x) + ": "
        for z in range(len(y)):
            if (z == len(y)-1):
                listItems+= str(y[z])
            else:
                listItems+= str(y[z]) +", "
        f.write(listItems+"\n")
    
    f.close()    
        
        
   
            
def average_hp_stage_3(pokemonBox):
    numHp =0
    totalHp=0
    for pokemon in pokemonBox:
        if ((float)(pokemon['stage']) == 3.0):
            #print(pokemon)
            totalHp += (float)(pokemon['hp'])
            numHp   +=1
    average = 0
    if numHp == 0:
        average = 0
    else:
        average = round(totalHp/numHp)
    f = open("pokemon5.txt", "w")
    f.write("Average hit point for Pokemons of stage 3.0 = ")
    f.write(str(average)+"\n")
    f.close()
    
def main():
    reader = csv.DictReader(open('pokemonTrain.csv'))
    pokemonBox= []
    for index, row in enumerate(reader):
        pokemonBox.append(row)

    fire_pokemon_above_level(pokemonBox,40)
    pokemonBox = fill_in_type(pokemonBox)
    pokemonBox = fill_in_stats(pokemonBox, 40)

    f = open('pokemonResults.csv', 'w') 
    writer = csv.writer(f)
    writer.writerow(pokemonBox[0])
    for pokemon in pokemonBox:
        tempList = []
        tempList.append(pokemon['id'])
        tempList.append(pokemon['name'])
        tempList.append(pokemon['level'])
        tempList.append(pokemon['personality'])
        tempList.append(pokemon['type'])
        tempList.append(pokemon['weakness'])
        tempList.append(pokemon['atk'])
        tempList.append(pokemon['def'])
        tempList.append(pokemon['hp'])
        tempList.append(pokemon['stage'])
        writer.writerow(tempList)
    f.close()

    map_pokemon_to_type(pokemonBox)
    average_hp_stage_3(pokemonBox)
    
main()
    