import urllib.request

massURL = "https://pdg.lbl.gov/2023/mcdata/mass_width_2023.txt"
tableURL = "https://raw.githubusercontent.com/root-project/root/master/etc/pdg_table.txt"

#------------------------
# Gets the text document
#------------------------

def getFileText(link):
    with urllib.request.urlopen(link) as f:
        text = f.read().decode("utf-8")
        lines = text.splitlines()
        return lines

#------------------------------
# Create updated pdg_table.txt
#------------------------------

def createTable():
    outputFile = ""

    for line in originalTable:
        if (line.strip().startswith('#')):
            lineToWrite = f"{line}\n"
        else:
            if line.split()[0].isdigit() and line.split()[1].isdigit():
                lineToWrite = f"{line}\n"
            else:
                lineToWrite = fixedParticleData(line)

        outputFile += lineToWrite

    with open("etc/pdg_table.txt", 'w') as file:
        file.write(outputFile)

#-------------------------------------
# Gets the correct Data for particles
#-------------------------------------

def fixedParticleData(infoLine):
    elements = infoLine.split()
    
    name = elements[1]
    trueID = int(elements[2])

    if (len(elements) < 6): # If it's an Antiparticle
            return f"{elements[0]:>5} {name:<16} {trueID:>6} {elements[3]:>7} {elements[4]:>5}\n"
    else: # If it's not an Antiparticle
        mass = float(elements[7])
        width = float(elements[8])
            
        if (trueID in massWidthData):
            if (massWidthData[trueID]['Mass']):
                mass = float(massWidthData[trueID]['Mass'])
            if (massWidthData[trueID]['Width']):
                width = float(massWidthData[trueID]['Width'])
                
        return f"{elements[0]:>5} {name:<16} {trueID:>6} {elements[3]:>2} {elements[4]:>3} {elements[5]:<10} {elements[6]:>2} {mass:<11e} {width:<11e} {elements[9]:>3} {elements[10]:>2} {elements[11]:>3} {elements[12]:>2} {elements[13]:>4} {elements[14]:>3}\n"

#---------------------------------
# Save the data of the mass_width
#---------------------------------
def getMassWidthValues(lines):
    data = {}  # Dictionary to store the data
    for line in lines:
        if line.startswith('*'):
            continue  # Skip comments

        # Extracting relevant information based on the character column positions
        particleId = line[0:8].strip()

        if (line[33:51].strip()):
            mass = line[33:51].strip()
        else:
            mass = 0.0 # No value is given
        
        if (line[70:88].strip()):
            width = line[70:88].strip()
        else:
            width = 0.0 # No value is given

        nameWithCharge = line[107:128].strip()
        name = nameWithCharge.split()[0]  # Extract only the name, excluding the charge

        # Storing the data in the dictionary
        if particleId in data:
            print("Duplicated ID " + particleId)
        else:
            data[particleId] = {'Mass': float(mass), 'Width': float(width), 'Name': name}

    return data


#------------------
# Setup everything
#------------------

massDataLines = getFileText(massURL)
originalTable = getFileText(tableURL)

massWidthData = getMassWidthValues(massDataLines)

createTable()