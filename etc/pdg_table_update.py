import urllib.request
import pdg

api = pdg.connect()
TABLE_URL = "https://raw.githubusercontent.com/root-project/root/master/etc/pdg_table.txt"

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
        
        try:
            particle = api.get_particle_by_mcid(trueId)
            mass = float(particle.mass)
            width = particle.
        except:
            pass    
        # Formatting the output line with the updated mass and width
        # return f"{elements[0]:>5} {name:<16} {trueId:>6} {elements[3]:>2} {elements[4]:>3} {elements[5]:<10} {elements[6]:>2} {mass:<11e} {width:<11} {elements[9]:>3} {elements[10]:>2} {elements[11]:>3} {elements[12]:>2} {elements[13]:>4} {elements[14]:>3}\n"
        return "{:>5} {:<16} {:>6} {:>2} {:>3} {:<10} {:>2} {:<11e} {:<11e} {:>3} {:>2} {:>3} {:>2} {:>4} {:>3}\n".format(
            elements[0] if elements[0] is not None else "",
            name,
            trueId if trueId is not None else "",
            elements[3] if elements[3] is not None else "",
            elements[4] if elements[4] is not None else "",
            elements[5] if elements[5] is not None else "",
            elements[6] if elements[6] is not None else "",
            mass if mass is not None else "",
            width if width is not None else "",
            elements[9] if elements[9] is not None else "",
            elements[10] if elements[10] is not None else "",
            elements[11] if elements[11] is not None else "",
            elements[12] if elements[12] is not None else "",
            elements[13] if elements[13] is not None else "",
            elements[14] if elements[14] is not None else ""
        )


#------------------------------
# Create updated pdg_table.txt
#------------------------------

def createTable():
    if originalTable is None or api.get_particles is None:
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

# Fetch pdg_table.txt content from URLs
originalTable = getFileTextFromURL(TABLE_URL)

createTable()
