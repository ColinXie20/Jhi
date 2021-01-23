def adduser(filename, id, spirit):
    file = open(filename, "a")
    file.write("['" + str(id) + "', '" + spirit + "', '0', '0', '" + spirit + "', 'None', 'None', '0', '0', 'None', '0', '1.0']\n")
    file.close()

def addguild(filename, guildname):
    file = open(filename, "a")
    file.write(guildname + "\n")
    file.close()

def getallplayers(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    return lines

def getallguilds(filename):
    return getallplayers(filename)

def getinfo(filename, id):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        info = eval(line[:len(line)-1])
        if info[0] == str(id):
            return info
    print("Couldn't find user " + str(id))
    return -1


def updateinfo(filename, id, newinfo):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    for i in range(len(lines)):
        info = eval(lines[i][:len(lines[i])-1])
        if info[0] == str(id):
            lines[i] = str(newinfo) + "\n"
    file = open(filename, "w")
    file.write("".join(lines))
    file.close()


def swapspirits(filename, id1, id2):
    user1 = getinfo(filename, id1)
    user2 = getinfo(filename, id2)
    temp = user1[1]
    user1[1] = user2[1]
    user2[1] = temp
    temp = user1[4]
    user1[4] = user2[4]
    user2[4] = temp
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    for i in range(len(lines)):
        info = eval(lines[i][:len(lines[i]) - 1])
        if info[0] == str(id1):
            lines[i] = str(user1) + "\n"
        elif info[0] == str(id2):
            lines[i] = str(user2) + "\n"
    file = open(filename, "w")
    file.write("".join(lines))
    file.close()


def swaptalismans(filename, id1, id2):
    user1 = getinfo(filename, id1)
    user2 = getinfo(filename, id2)
    temp = user1[9]
    user1[9] = user2[9]
    user2[9] = temp
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    for i in range(len(lines)):
        info = eval(lines[i][:len(lines[i]) - 1])
        if info[0] == str(id1):
            lines[i] = str(user1) + "\n"
        elif info[0] == str(id2):
            lines[i] = str(user2) + "\n"
    file = open(filename, "w")
    file.write("".join(lines))
    file.close()
