"""Created a vector of 3 to keep all 3 skills."""
class Vector3:
    def __init__(self,skillH,skillE,skillP):
        self.skillH = skillH
        self.skillE = skillE
        self.skillP = skillP

class Circuit:
    maxJugglers = 0
    def __init__(self,name,skillH,skillE,skillP):
        self.name = name
        self.vec = Vector3(skillH,skillE,skillP)
        self.AssignedJugglers = []

    def add(self,juggler):
        """
        If the circuit has reached the maximum juggler capacity,
        compare the new juggler's dot product to the juggler
        with the minimum points in the circuit. If the new
        juggler's dot product is higher, kick the loser from
        the list and add the new juggler, then return the kicked
        juggler. If not, return False.
        If the circuit has not reached
        the maximum juggler capacity, add the juggler to the list,
        and return True.

        """
        if len(self.AssignedJugglers) >= self.maxJugglers:
            minJuggler = min(self.AssignedJugglers, key= lambda x:x.dots[self.name])
            if juggler.dots[self.name] > minJuggler.dots[self.name]:
                loser = minJuggler
                self.AssignedJugglers.remove(minJuggler)
                self.AssignedJugglers.append(juggler)
                return loser
            elif juggler.dots[self.name] <= minJuggler.dots[self.name]:
                return False
        else:
            self.AssignedJugglers.append(juggler)
            return True


class Juggler:
    def __init__(self,name,skillH,skillE,skillP,pref_list):
        self.name = name
        self.vec = Vector3(skillH,skillE,skillP)
        self.pref_list = pref_list
        self.dots = {}
        self.counter = -1

    def getNext(self):
        """
        Get the next circuit from the juggler's preference list.

        """
        self.counter += 1
        return self.pref_list[self.counter]

        
def dotproduct(juggler,circuit):
    """
    Calculate the dot product of the juggler-circuit duo.

    """
    return int(juggler.vec.skillH) * int(circuit.vec.skillH) \
         + int(juggler.vec.skillE) * int(circuit.vec.skillE) \
         + int(juggler.vec.skillP) * int(circuit.vec.skillP) \


def jugglerAdd(juggler):
    """
    If the juggler has tried all its preferred circuits
    and still has no match, add the juggler to the leftJugglers.
    Else, get the next preference of the juggler, calculate the
    dot product, try to assign the juggler to the circuit.
    If it returns True, juggler is assigned to the circuit with no problem.
    If it returns a juggler, our juggler is assigned to the circuit,
    but it kicked another juggler, try to assign the kicked juggler,
    with the same process for its next preference.
    If returns false, the juggler is not assigned to the circuit,
    try to assign the juggler with the same process for its next preference.

    """
    global leftJugglers,circuits
    dest = juggler.getNext()
    if int(juggler.counter) >= 6:
        leftJugglers.append(juggler)
        return
    juggler.dots[dest] = dotproduct(juggler, circuits[dest])
    r = circuits[dest].add(juggler)
    if r == True:
        print("juggler: " + juggler.name + "is assigned to: " + circuits[dest].name)
        return
    elif type(r) == Juggler:
        print("juggler: " + r.name + "is kicked out of: " + circuits[dest].name)
        jugglerAdd(r)
        return
    elif r == False:
        print("juggler: " + juggler.name + "is too low for the circuit: " + circuits[dest].name)
        jugglerAdd(juggler)


def leftJugglerAdd(leftjuggler):
    """
    Try to add the lefJugglers to the circuits that are not full,
    with the same process.

    """
    global leftJugglers, circuits
    for dest in circuits.keys():
        if len(circuits[dest].AssignedJugglers) < Circuit.maxJugglers:
            leftjuggler.dots[dest] = dotproduct(leftjuggler,circuits[dest])
            r = circuits[dest].add(leftjuggler)
            if r == True:
                return
            elif type(r) == Juggler:
                leftJugglerAdd(r)
            elif r == False:
                leftJugglerAdd(leftjuggler)


leftJugglers = []
circuits = {}
def main(text):
    """
    extract the name, skills, etc...
    add the circuit to a map with key: name val: circuit object.
    add the juggler objects to a list.

    """
    jugglers = []
    with open(text) as input:
        for line in input:
            if line[:1] == "C":
                name = line.split(' ')[1]
                skillH = line.split(' ')[2]
                skillH = skillH.split('H:')[1]
                skillE = line.split(' ')[3]
                skillE = skillE.split('E:')[1]
                skillP = line.split(' ')[4]
                skillP = skillP.split('P:')[1]
                skillP = skillP.split('\n')[0]
                circuits[name] = Circuit(name,skillH,skillE,skillP)

            elif line[:1] == "J":
                name = line.split(' ')[1]
                skillH = line.split(' ')[2]
                skillH = skillH.split('H:')[1]
                skillE = line.split(' ')[3]
                skillE = skillE.split('E:')[1]
                skillP = line.split(' ')[4]
                skillP = skillP.split('P:')[1]
                preferred_dest = line.split(' ')[5]
                preferred_dest = preferred_dest.split('\n')[0]
                preferred_dest = [x.strip() for x in preferred_dest.split(',')]
                jugglers.append(Juggler(name,skillH, skillE, skillP,preferred_dest))

        """ Maximum juggler capacity per circuit. """
        Circuit.maxJugglers = len(jugglers) / len(circuits)

        """Assign all jugglers to circuits"""
        for juggler in jugglers:
            jugglerAdd(juggler)

        """Assign all leftjugglers to circuits that are not full."""
        for juggler in leftJugglers:
            leftJugglerAdd(juggler)
            # for juggler in leftJugglers:
            #     for dest in circuits.keys():
            #         if len(circuits[dest].AssignedJugglers) < 6:
            #             juggler.dots = dotproduct(juggler, circuits[dest])
            #             r = circuits[dest].add(juggler)
            #             if r == True:
            #                 break
            #             else:
            #                 leftJugglers.append(r)


        for circuit in circuits.keys():
            print(circuit + " ")
            for i in range (len(circuits[circuit].AssignedJugglers)):
                print(circuits[circuit].AssignedJugglers[i].name, circuits[circuit].AssignedJugglers[i].dots)


if __name__ == '__main__':
      main("input.txt")

