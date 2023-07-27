import urllib.request

MASS_URL = "https://pdg.lbl.gov/2023/mcdata/mass_width_2023.txt"
TABLE_URL = "https://raw.githubusercontent.com/root-project/root/master/etc/pdg_table.txt"

# Character positions for extracting data from "mass_width_2023.txt"
MASS_WIDTH_ID_START = 0
MASS_WIDTH_ID_END = 8
MASS_WIDTH_MASS_START = 33
MASS_WIDTH_MASS_END = 51
MASS_WIDTH_WIDTH_START = 70
MASS_WIDTH_WIDTH_END = 88
MASS_WIDTH_NAME_WITH_CHARGE_START = 107
MASS_WIDTH_NAME_WITH_CHARGE_END = 128

#------------------------
# Gets the text document
#------------------------

def getFileTextFromURL(link):
    try:
        with urllib.request.urlopen(link) as f:
            text = f.read().decode("utf-8")
            lines = text.splitlines()
            return lines
    except Exception as e:
        print(f"Error while fetching data from URL: {e}")
        return None

#-------------------------------------
# Gets the correct Data for particles
#-------------------------------------

def fixedParticleData(infoLine):
    elements = infoLine.split()
    
    name = elements[1]
    trueId = int(elements[2])

    if len(elements) < 6:  # If it's an Antiparticle
        return f"{elements[0]:>5} {name:<16} {trueId:>6} {elements[3]:>7} {elements[4]:>5}\n"
    else:  # If it's not an Antiparticle
        mass = float(elements[7])
        width = float(elements[8])
            
        if trueId in massWidthData:
            if massWidthData[trueId]['Mass']:
                mass = float(massWidthData[trueId]['Mass'])
            if massWidthData[trueId]['Width']:
                width = float(massWidthData[trueId]['Width'])
                
        # Formatting the output line with the updated mass and width
        return f"{elements[0]:>5} {name:<16} {trueId:>6} {elements[3]:>2} {elements[4]:>3} {elements[5]:<10} {elements[6]:>2} {mass:<11e} {width:<11e} {elements[9]:>3} {elements[10]:>2} {elements[11]:>3} {elements[12]:>2} {elements[13]:>4} {elements[14]:>3}\n"

#---------------------------------
# Save the data of the mass_width
#---------------------------------

def getMassWidthValues(lines):
    data = {}  # Dictionary to store the data
    for line in lines:
        if line.startswith('*'):
            continue  # Skip comments

        # Extracting relevant information based on the character column positions
        particleId = line[MASS_WIDTH_ID_START:MASS_WIDTH_ID_END].strip()

        if line[MASS_WIDTH_MASS_START:MASS_WIDTH_MASS_END].strip():
            mass = line[MASS_WIDTH_MASS_START:MASS_WIDTH_MASS_END].strip()
        else:
            mass = 0.0  # No value is given
        
        if line[MASS_WIDTH_WIDTH_START:MASS_WIDTH_WIDTH_END].strip():
            width = line[MASS_WIDTH_WIDTH_START:MASS_WIDTH_WIDTH_END].strip()
        else:
            width = 0.0  # No value is given

        nameWithCharge = line[MASS_WIDTH_NAME_WITH_CHARGE_START:MASS_WIDTH_NAME_WITH_CHARGE_END].strip()
        name = nameWithCharge.split()[0]  # Extract only the name, excluding the charge

        # Storing the data in the dictionary
        if particleId in data:
            print("Duplicated ID " + particleId)
        else:
            data[particleId] = {'Mass': float(mass), 'Width': float(width), 'Name': name}

    return data

#------------------------------
# Create updated pdg_table.txt
#------------------------------

def createTable():
    if originalTable is None or massWidthData is None:
        print("Data not available. Aborting table creation.")
        return

    outputLines = []

    for line in originalTable:
        if line.strip().startswith('#'):
            outputLines.append(f"{line}\n")
        else:
            if line.split()[0].isdigit() and line.split()[1].isdigit():
                outputLines.append(f"{line}\n")
            else:
                outputLines.append(fixedParticleData(line))

    with open("etc/pdg_table.txt", 'w') as file:
        file.writelines(outputLines)

#------------------
# Setup everything
#------------------

# Fetch mass_width_2023.txt and pdg_table.txt content from URLs
massDataLines = getFileTextFromURL(MASS_URL)
originalTable = getFileTextFromURL(TABLE_URL)

# Check if the data was fetched successfully before proceeding
if massDataLines:
    massWidthData = getMassWidthValues(massDataLines)
else:
    massWidthData = None

createTable()
