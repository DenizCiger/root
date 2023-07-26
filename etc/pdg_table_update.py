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

#--------------------------------
# Check if the line is a comment
#--------------------------------

def isTableComment(line):
    for char in line:
        if char == '#':
            return True
    return False

#------------------------------
# Create updated pdg_table.txt
#------------------------------

def createTable():
    outputFile = ""

    for line in originalTable:
        if (isTableComment(line)):
            lineToWrite = f"{line}\n"
        else:
            if line.split()[0].isdigit() and line.split()[1].isdigit():
                lineToWrite = f"{line}\n"
            else:
                lineToWrite = fixedParticleData(line)

        outputFile += lineToWrite

    with open("pdg_table.txt", 'w') as file:
        file.write(outputFile)

#-------------------------------------
# Gets the correct Data for particles
#-------------------------------------

def fixedParticleData(infoLine):
    name = infoLine[6:23].strip()
    trueID = infoLine[24:29].strip()

    if (trueID in massWidthData):
        if (massWidthData[trueID]['Mass'][0]):
            mass = massWidthData[trueID]['Mass'][0]
        else:
            mass = infoLine[51:62]
        if (massWidthData[trueID]['Width'][0]):
            width = massWidthData[trueID]['Width'][0]
        else:
            width = infoLine[63:74]
    else:
        mass = infoLine[51:62]
        width = infoLine[63:74]
    
    
        

    return f"{infoLine[0:5]} {name:<16} {trueID:>6} {infoLine[30:32]} {infoLine[33:36]} {infoLine[37:43]} {infoLine[44:50]} {mass:<11} {width:<11} {infoLine[75:79]} {infoLine[80:82]} {infoLine[83:87]} {infoLine[88:90]}\n"


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
        mass = line[33:51].strip()
        width = line[70:88].strip()
        nameWithCharge = line[107:128].strip()
        name = nameWithCharge.split()[0]  # Extract only the name, excluding the charge

        # Storing the data in the dictionary
        if particleId not in data:
            data[particleId] = {'Mass': [], 'Width': [], 'Name': []}
        data[particleId]['Mass'].append(mass)
        data[particleId]['Width'].append(width)
        data[particleId]['Name'].append(name)

    # Debug log the saved values
    #with open("mass_width_log.txt", 'w') as file:
    #    file.write(f"{'ID':<10} {'Mass':<20} {'Width':<15} {'Name':<15}")
    #    for particle_id, values in data.items():
    #        for i in range(len(values['Mass'])):
    #            file.write(f"\n{particle_id:<10} {values['Mass'][i]:<20} {values['Width'][i]:<15} {values['Name'][i]:<15}")
    return data


#------------------
# Setup everything
#------------------

massDataLines = getFileText(massURL)
originalTable = getFileText(tableURL)

massWidthData = getMassWidthValues(massDataLines)

createTable()