import copy
import numpy as np

class ssa():
    def __init__(self, component_stack):
        self.component_stack = component_stack
        self.number_of_sources = 0
        self.number_of_unknowns = 0 # equivalent to the number of passive elements (e.g. resistors)
        self.dict_of_unknowns = {} # dictionary of the unknown elements
        self.ang_frequency = 2*np.pi*ssa.get_frequency(component_stack) #get angular frequency of operation
        self.calc_currents()

    def calc_currents(self):
        for comp in self.component_stack:
            if comp.name[0] == "S":
                self.number_of_sources += 1
            elif comp.name[0] in ("R", "C", "L"):
                self.dict_of_unknowns.update({ssa.get_first_name(comp.name): self.number_of_unknowns})
                self.number_of_unknowns += 1

        #get list of wires
        list_of_wires = []
        for comp in self.component_stack:
            if comp.name[0] != "W":
                continue
            else:
                list_of_wires.append([comp])

        #find which wires are connected together
        union_made, list_of_wires = ssa.united_wires(list_of_wires)
        while union_made !=0:
            union_made, list_of_wires = ssa.united_wires(list_of_wires)

        #make a list of component nodes connected together
        list_of_connected_nodes = []
        for connected_wire in list_of_wires:
            list_of_nodes = []
            for wire in connected_wire:
                for comp in self.component_stack:
                    if comp.name[0] == "W":
                        continue
                    if (comp.x_coord[0] == wire.x_coord[0] and comp.y_coord[0] == wire.y_coord[0]) or (comp.x_coord[0] == wire.x_coord[1] and comp.y_coord[0] == wire.y_coord[1]):
                        if comp.name + " node 1" not in list_of_nodes:
                            list_of_nodes.append(comp.name + " node 1")
                    elif (comp.x_coord[1] == wire.x_coord[0] and comp.y_coord[1] == wire.y_coord[0]) or (comp.x_coord[1] == wire.x_coord[1] and comp.y_coord[1] == wire.y_coord[1]):
                        if comp.name + " node 2" not in list_of_nodes:
                            list_of_nodes.append(comp.name + " node 2")
            list_of_connected_nodes.append(list_of_nodes)

        # find circles such that every non-wire component is in at least one circle
        list_of_circles = []
        for node_bunch in list_of_connected_nodes:
            for node in node_bunch:
                a_circle = []
                if node not in ssa.flat_the_list(list_of_circles):
                    list_of_connected_nodes_copy = copy.deepcopy(list_of_connected_nodes)
                    a = ssa.find_circle(a_circle, node, list_of_connected_nodes_copy)
                    list_of_circles.append(a_circle)

        impedance_matrix = np.zeros(shape=(self.number_of_unknowns, self.number_of_unknowns),dtype=complex)
        voltage_vector = np.zeros(shape=(self.number_of_unknowns,1), dtype=complex)
        current_rank = 0

        # apply KVL (all currents go from node 1 to node 2)
        for circle in list_of_circles:
            for index, node in enumerate(circle):
                if index % 2 == 1 or index == len(circle)-1:
                    continue
                if node[0] == "S":
                    if node[-1] == "1":
                        voltage_vector[current_rank,0] = -float(ssa.get_value(node))
                    else:
                        voltage_vector[current_rank,0] = float(ssa.get_value(node))
                elif node[0] == "R":
                    if node[-1] == "1":
                        impedance_matrix[current_rank, self.dict_of_unknowns[ssa.get_first_name(node)]] = float(ssa.get_value(node))
                    else:
                        impedance_matrix[current_rank, self.dict_of_unknowns[ssa.get_first_name(node)]] = -float(ssa.get_value(node))
                elif node[0] == "L":
                    if node[-1] == "1":
                        impedance_matrix[current_rank, self.dict_of_unknowns[ssa.get_first_name(node)]] = 1j*self.ang_frequency*float(ssa.get_value(node))
                    else:
                        impedance_matrix[current_rank, self.dict_of_unknowns[ssa.get_first_name(node)]] = -1j*self.ang_frequency*float(ssa.get_value(node))
                elif node[0] == "C":
                    if node[-1] == "1":
                        impedance_matrix[current_rank, self.dict_of_unknowns[ssa.get_first_name(node)]] = 1/(1j*self.ang_frequency*float(ssa.get_value(node)))
                    else:
                        impedance_matrix[current_rank, self.dict_of_unknowns[ssa.get_first_name(node)]] = -1/(1j*self.ang_frequency*float(ssa.get_value(node)))
            if np.linalg.matrix_rank(impedance_matrix) > current_rank:
                current_rank += 1
            if current_rank == self.number_of_unknowns:
                break

        # check if enough equations have been collected
        if current_rank == self.number_of_unknowns:
            pass
        #otherwise, apply KCL
        else:
            for node_bunch in list_of_connected_nodes:
                source_in_node_bunch = 0 #sources must be excluded since source currents are not part of the unknowns
                for node in node_bunch:
                    if node[0] == "S":
                        source_in_node_bunch += 1
                if source_in_node_bunch > 0:
                    continue
                for node in node_bunch:
                    if node[-1] == "2":
                        impedance_matrix[current_rank, self.dict_of_unknowns[ssa.get_first_name(node)]] = 1
                    else:
                        impedance_matrix[current_rank, self.dict_of_unknowns[ssa.get_first_name(node)]] = -1
                if np.linalg.matrix_rank(impedance_matrix) > current_rank:
                    current_rank += 1
                if current_rank == self.number_of_unknowns:
                    break

        current_vector = np.matmul(np.linalg.inv(impedance_matrix), voltage_vector)

        for index, key in enumerate(self.dict_of_unknowns.keys()):
            print ("I_" + key + " = " + str(current_vector[index,0]) + " A")

        #clear the neighbors list
        for comp in self.component_stack:
            comp.neighbors = [[],[]]

    @staticmethod
    def get_first_name(the_name):  # for example, "R8 1000" => "R8"
        n = 0
        while the_name[n] != " ":
            n += 1
        return the_name[0:n]

    @staticmethod
    def get_value(the_name): # for example, "R8 1000" => "1000
        n = 0
        k = 0
        m = 0
        return_name = ""
        while k < 2:
            if the_name[n] == " ":
                k += 1
            elif k == 1:
                return_name += the_name[n]
                m += 1
            n += 1
        return return_name

    @staticmethod
    def flat_the_list(some_list):
        if not some_list:
            return some_list
        return_list = []
        for item in some_list:
            for item_2 in item:
                return_list.append(item_2)
        return return_list

    @staticmethod
    def find_circle(a_circle, a_node, all_nodes):
        circle_found = 0
        choices = []
        selected_node = ""
        a_circle.append(a_node)
        if len(a_circle) > 1:
            if ssa.get_node_bunch(a_circle[0], all_nodes) == ssa.get_node_bunch(a_circle[-1], all_nodes):
                return 1 # circle found
        if len(a_circle) > 4:
            for i in range(1,len(a_circle)-2):
                if ssa.get_node_bunch(a_circle[i], all_nodes) == ssa.get_node_bunch(a_circle[-1], all_nodes):
                    return 0 # incorrect circle
        for node_bunch in all_nodes:
            for some_node in node_bunch:
                if some_node[0:-1] == a_node[0:-1] and some_node[-1] != a_node[-1]:
                    a_circle.append(some_node)
                    choices = copy.deepcopy(node_bunch)
                    selected_node = some_node

        for ch in choices:
            if ch == selected_node:
                continue
            circle_found = ssa.find_circle(a_circle, ch, all_nodes)
            if circle_found == 1:
                return 1
            else:
                a=a_circle.pop()
        a=a_circle.pop()
        return 0

    @staticmethod
    def get_node_bunch(node, list_of_nodes):
        for node_bunch in list_of_nodes:
            for some_node in node_bunch:
                if some_node == node:
                    return node_bunch

    @staticmethod
    def united_wires(wirelist): #takes the list of wires and return a list of united wires
        union_made = 0
        for i in range(len(wirelist)):
            for comp in wirelist[i]:
                for j in range(len(wirelist)):
                    if i == j:
                        continue
                    for comp2 in wirelist[j]:
                        if (comp.x_coord[0] == comp2.x_coord[0] and comp.y_coord[0] == comp2.y_coord[0]) or (comp.x_coord[0] == comp2.x_coord[1] and comp.y_coord[0] == comp2.y_coord[1]) or (comp.x_coord[1] == comp2.x_coord[0] and comp.y_coord[1] == comp2.y_coord[0]) or (comp.x_coord[1] == comp2.x_coord[1] and comp.y_coord[1] == comp2.y_coord[1]):
                            a=wirelist[i] + wirelist[j]
                            if i>j: # popping is changing the length so pop the larger first
                                wirelist.pop(i)
                                wirelist.pop(j)
                            else:
                                wirelist.pop(j)
                                wirelist.pop(i)
                            wirelist.append(a)
                            union_made = 1
                            return union_made, wirelist
        return union_made, wirelist

    @staticmethod
    def get_frequency(components):
        for comp in components:
            if comp.name[0] == "S":
                return comp.frequency