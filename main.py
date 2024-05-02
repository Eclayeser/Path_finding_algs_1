import pygame
import time


pygame.init()
scr_width = 1300
scr_height = 650
screen = pygame.display.set_mode((scr_width, scr_height))
clock = pygame.time.Clock()


run = True
bg_colour = (0, 0, 0)

red_node_img = pygame.image.load("red_node.png")
purple_node_img = pygame.image.load("purple_node.png")
orange_node_img = pygame.image.load("orange_node.png")

input_made = False
input_field_displayed = False
destination = ""
dijkstar_alg = False
a_star_alg = False
user_input_1 = ""
user_input_2 = ""
active_input_1 = False
active_input_2 = False
user_input_rect_1 = pygame.Rect(1040, 30, 35, 35)
user_input_rect_2 = pygame.Rect(1040, 80, 35, 35)


class Button(pygame.sprite.Sprite):
    def __init__(self, image, image_highlight, pos_x, pos_y, scale):
        super().__init__()
        width = image.get_width()
        height= image.get_height()
        

        self.image_normal = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        
        self.image_highlight = pygame.transform.scale(image_highlight, (int(width*scale), int(height*scale)))
        
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.clicked = False
        self.new_image = False
        self.selected = False
        self.already_pressed = False
        
        
        

    def check_clicked(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.new_image = True
            if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == False:
                self.clicked = False
                self.already_pressed = False
        if self.rect.collidepoint(pos) == False:
            self.new_image = False

        return action
    
        

    def update(self):
         if self.new_image == True or self.selected == True:
            self.image = self.image_highlight
         if self.new_image == False and self.selected == False:
            self.image = self.image_normal


class Mesh:
    def __init__(self):
        self.adjacencies = {}
        self.nodes = {}
        

    def getAdjacencies(self):
        print(self.adjacencies)

    def getNodes(self):
        print(self.nodes)

    def addNode(self, value, pos_x, pos_y, weight, data):
        if weight == None:
            weight = 40
        self.adjacencies[value] = []
        self.nodes[value] = [(pos_x, pos_y), weight, data]
        

    def joinNodes(self, from_node, *to_nodes):
        for to_node in to_nodes:
            self.adjacencies[from_node].append(to_node)
    
    def formListOfNodes(self):
        list = []
        for i in self.nodes.keys():
            list.append(i)
        return list
    
    def nodeExists(self, node):
        if node in self.formListOfNodes():
            return True
        else:
            return False
        
    def getCoorOfNode(self, node_name):
        return self.nodes[node_name][0]
        


dijkstra_alg_btn = Button(pygame.image.load('dijkstra_btn_1.png'), pygame.image.load('dijkstra_btn_2.png'), 1150, 520, 0.4)
a_star_alg_btn = Button(pygame.image.load('a_alg_btn_1.png'), pygame.image.load('a_alg_btn_2.png'), 1150, 470, 0.4)
buttons_spr_group = pygame.sprite.Group()
buttons_spr_group.add(dijkstra_alg_btn, a_star_alg_btn)



myMesh = Mesh()
myMesh.addNode("A", 100, 100, 40, "Apple")
myMesh.addNode("B", 200, 400, 40, "Banana")
myMesh.addNode("C", 400, 275, 30, "Cider")
myMesh.addNode("D", 800, 25, 25, "Dong")
myMesh.addNode("E", 350, 150, 30, "Ear")
myMesh.addNode("F", 700, 350, 35, "Fire")
myMesh.addNode("G", 700, 125, 25, "Grape")
myMesh.addNode("H", 50, 490, 23, "Heat")
myMesh.addNode("I", 850, 490, 27, "Iguana")


myMesh.joinNodes("A",("D", 25), ("E", 40), ("H", 40))
myMesh.joinNodes("B",("A", 5), ("C", 25), ("I", 25))
myMesh.joinNodes("C",("A", 120), ("B", 25), ("E", 20))
myMesh.joinNodes("D",("G", 45), ("I", 15))
myMesh.joinNodes("E",("C", 30), ("D", 50), ("F", 50))
myMesh.joinNodes("F",("C", 40), ("G", 25))
myMesh.joinNodes("G",("D", 20), ("F", 25))
myMesh.joinNodes("H",("A", 45))
myMesh.joinNodes("I",("B", 30), ("D", 50))


#myMesh.getNodes()
#myMesh.getAdjacencies()
#print(myMesh.nodeExists("P"))
#print(myMesh.getCoorOfNode("A"))


current_position = "A"
previous_node = ""
node_data = ""
next_positions = [j[0] for j in myMesh.adjacencies[current_position]]
cumulative_distance = 0
text_font_current_data = pygame.font.SysFont("Arial", 35, bold=True)
text_font_table_data = pygame.font.SysFont("Arial", 20, bold=True)
text_font_input = pygame.font.SysFont("Times New Roman", 30)

node_names = [x for x in myMesh.nodes]
time_interval = 0
display_table = False
#result_dict = {}

text_input_1_label_surface = text_font_current_data.render("Start:", True, (255, 255, 255))
text_input_2_label_surface = text_font_current_data.render("End:", True, (255, 255, 255))



def look_for_distance(prev, to):
    for i in myMesh.adjacencies[prev]:
        if i[0] == to:
            return i[1]
        
def key_procedure_execute(name):
    global previous_node
    global current_position
    global node_data
    global next_positions
    global cumulative_distance
    previous_node = current_position
    current_position = name
    next_positions = [j[0] for j in myMesh.adjacencies[current_position]]
    cumulative_distance += look_for_distance(previous_node, current_position)
    node_data = myMesh.nodes[current_position][2]
   
def calc_h_val(from_node_name, to_node_name):
    const_div = 10
    h_val = round((((myMesh.getCoorOfNode(from_node_name)[0]-myMesh.getCoorOfNode(to_node_name)[0])**2 + (myMesh.getCoorOfNode(from_node_name)[1]-myMesh.getCoorOfNode(to_node_name)[1])**2) ** 0.5)/const_div)
    return h_val

def a_star_alg_execute(start_node_name, endNode):
    dictionary = {}
    visited_nodes_names = []
    f_value_endNode = 1000000
    f_value_endNode_bigger = True
    dictionary[start_node_name] = [0, calc_h_val(start_node_name, endNode), calc_h_val(start_node_name, endNode), "-", ""]
    
    while f_value_endNode_bigger == True and len(visited_nodes_names) < len(myMesh.nodes):

        
        compare_f_values = [j[2] for i,j in dictionary.items() if type(j[0])== int and i not in visited_nodes_names]
        min_value = min(compare_f_values)
        if min_value > f_value_endNode:
            f_value_endNode_bigger = False
        else:
            for k, v in dictionary.items():
                if v[2] == min_value:
                    visit_node_name = k
            
            visited_nodes_names.append(visit_node_name)
      
            
            for adj in myMesh.adjacencies[visit_node_name]:
                if adj[0] not in visited_nodes_names:
                    heuristic_value = calc_h_val(adj[0], endNode)
                    f_value = adj[1] + dictionary[visit_node_name][0] + heuristic_value
                    
                    try:
                        if f_value < dictionary[adj[0]][2]:
                            dictionary[adj[0]] = [adj[1]+dictionary[visit_node_name][0], heuristic_value, f_value, visit_node_name, "-"]
                    except:
                        dictionary[adj[0]] = [adj[1]+dictionary[visit_node_name][0], heuristic_value, f_value, visit_node_name, "-"]
            

            if endNode in visited_nodes_names:
                f_value_endNode = dictionary[endNode][2]
            

    for node, info in dictionary.items():
        if node in visited_nodes_names:
            if node == endNode:
                info[4] = "!"
            else:
                info[4] = "V"
        result_dict[node] = [info[0], info[1], info[2], info[3], info[4]]

    list_for_the_route = []
    pointer = endNode
    while pointer != start_node_name:
        for key, value in result_dict.items():
            if key == pointer:
                list_for_the_route.append(pointer)
                pointer = value[3]
    list_for_the_route.append(start_node_name)

    return list_for_the_route

def dijkstar_alg_execute(start_node_name, endNode):
    dictionary = {}
    visited_nodes_names = []

    dictionary[start_node_name] = [0, "-"]

    while len(dictionary) > 0:
        #print(dictionary)
        compare_distances = [j[0] for i,j in dictionary.items() if type(j[0])== int and i not in visited_nodes_names]
        min_value = min(compare_distances)
        for k, v in dictionary.items():
            if v[0] == min_value:
                visit_node_name = k
                
        visited_nodes_names.append(visit_node_name)
            
        for adj in myMesh.adjacencies[visit_node_name]:
            if adj[0] not in visited_nodes_names:
                try:
                    if adj[1]+dictionary[visit_node_name][0] < dictionary[adj[0]][0]:
                        dictionary[adj[0]] = [adj[1]+dictionary[visit_node_name][0], visit_node_name]
                except:
                    dictionary[adj[0]] = [adj[1]+dictionary[visit_node_name][0], visit_node_name]


        result_dict[visit_node_name] = [dictionary[visit_node_name][0], dictionary[visit_node_name][1]]
        dictionary.pop(visit_node_name)


    
    #show the route
    list_for_the_route = []
    pointer = endNode
    while pointer != start_node_name:
        for key, value in result_dict.items():
            if key == pointer:
                list_for_the_route.append(pointer)
                pointer = value[1]
    list_for_the_route.append(start_node_name)

    return list_for_the_route
     
def display_table_func(num_of_rows, dictionary, type_alg):
    
    if type_alg == "a_star":
        nodes_dict = [i for i in dictionary.keys()]
        distance_dict = [i[0] for i in dictionary.values()]
        heuristic_dict = [i[1] for i in dictionary.values()]
        f_value_dict = [i[2] for i in dictionary.values()]
        previous_dict = [i[3] for i in dictionary.values()]
        visited_dict = [i[4] for i in dictionary.values()]
    elif type_alg == "dijkstra's":
        nodes_dict = [i for i in dictionary.keys()]
        distance_dict = [i[0] for i in dictionary.values()]
        previous_dict = [i[1] for i in dictionary.values()]
      

    y_coor_1 = 175
    y_coor_2 = y_coor_1
    x_coor_1 = 900
    x_coor_2 = 1250

    difference_y = 45
    difference_x = (x_coor_2-x_coor_1)/len(myMesh.nodes)

    x_coor_3 = x_coor_1 + difference_x/7
    y_coor_3 = y_coor_1 + difference_y/4


    for i in range(0, num_of_rows+1):
        pygame.draw.line(screen, (255, 255, 255), (x_coor_1, y_coor_1), (x_coor_2+38, y_coor_1), width = 3) #find proper way instead of +38
        
        if i < num_of_rows:
            for j in range(0, len(myMesh.nodes)+1):
                if i == 0:
                    try:
                        display_table_data = text_font_table_data.render(str(nodes_dict[j]), True, (255, 255, 255))
                    except IndexError:
                        display_table_data = text_font_table_data.render("-", True, (255, 255, 255))
                    
                if i == 1:
                    try:
                        if type_alg == "dijkstra's":
                            display_table_data = text_font_table_data.render(str(distance_dict[j]), True, (255, 255, 255))
                        if type_alg == "a_star":
                            display_table_data = text_font_table_data.render(str(distance_dict[j]), True, (255, 255, 255))
                    except IndexError:
                        display_table_data = text_font_table_data.render("-", True, (255, 255, 255))
                    
                if i == 2:
                    try:
                        if type_alg == "dijkstra's":
                            display_table_data = text_font_table_data.render(str(previous_dict[j]), True, (255, 255, 255))
                        if type_alg == "a_star":
                            display_table_data = text_font_table_data.render(str(heuristic_dict[j]), True, (255, 255, 255))
                    except IndexError:
                        display_table_data = text_font_table_data.render("-", True, (255, 255, 255))
                    

                if type_alg == "a_star" and i >= 3:
                    if i == 3:
                        try:
                            display_table_data = text_font_table_data.render(str(f_value_dict[j]), True, (255, 255, 255))
                        except IndexError:
                            display_table_data = text_font_table_data.render("-", True, (255, 255, 255))
                        
                    if i == 4:
                        try:
                            display_table_data = text_font_table_data.render(str(previous_dict[j]), True, (255, 255, 255))
                        except IndexError:
                            display_table_data = text_font_table_data.render("-", True, (255, 255, 255))
                        
                    if i == 5:
                        try:
                            display_table_data = text_font_table_data.render(str(visited_dict[j]), True, (255, 255, 255))
                        except IndexError:
                            display_table_data = text_font_table_data.render("-", True, (255, 255, 255))
                        
                screen.blit(display_table_data, (x_coor_3, y_coor_3))


                x_coor_3 += difference_x
                
                if j == len(myMesh.nodes):
                    x_coor_3 = x_coor_1 + difference_x/7
        
        y_coor_1 += difference_y
        y_coor_3 += difference_y

    y_coor_1 -= difference_y
   
    for j in range(0, len(myMesh.nodes)+2):
        pygame.draw.line(screen, (255, 255, 255), (x_coor_1, y_coor_2), (x_coor_1, y_coor_1), width = 3)
        x_coor_1 += difference_x

def backtrack_list(list):
    new_list = []
    while len(list) > 0:
        new_list.append(list.pop())
    return new_list

def validInput():
    if myMesh.nodeExists(user_input_1) and myMesh.nodeExists(user_input_2):
        return True
    else:
        return False



while run:
    screen.fill(bg_colour)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if user_input_rect_1.collidepoint(event.pos):
                    active_input_1 = True
                    active_input_2 = False
                elif user_input_rect_2.collidepoint(event.pos):
                    active_input_2 = True
                    active_input_1 = False
                else:
                    active_input_1 = False
                    active_input_2 = False

            if active_input_1 == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_input_1 = user_input_1[:-1]
                    else :
                        if len(user_input_1) < 1:
                            user_input_1 += event.unicode
            if active_input_2 == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_input_2 = user_input_2[:-1]
                    else:
                        if len(user_input_2) < 1:
                            user_input_2 += event.unicode

    buttons_spr_group.update()
    buttons_spr_group.draw(screen)

    pygame.draw.rect(screen, (255, 255, 255), user_input_rect_1, 2)
    pygame.draw.rect(screen, (255, 255, 255), user_input_rect_2, 2)

    text_input_1_surface = text_font_input.render(user_input_1, True, (255, 255, 255))
    text_input_2_surface = text_font_input.render(user_input_2, True, (255, 255, 255))
    screen.blit(text_input_1_surface, (user_input_rect_1.x + 5, user_input_rect_1.y))
    screen.blit(text_input_2_surface, (user_input_rect_2.x + 5, user_input_rect_2.y))

    screen.blit(text_input_1_label_surface, (user_input_rect_1.x - 80, user_input_rect_1.y))
    screen.blit(text_input_2_label_surface, (user_input_rect_2.x - 80, user_input_rect_2.y))


    path_distance_x_coor = 40
    path_distance_y_coor = 585
    count = 0
    for node, adjs in myMesh.adjacencies.items():
        for adj in adjs:
            pygame.draw.line(screen, (255, 255, 0), (myMesh.nodes[node][0][0]+(red_node_img.get_width()*(myMesh.nodes[node][1]/50)/2), myMesh.nodes[node][0][1]+(red_node_img.get_height()*(myMesh.nodes[node][1]/50)/2)), (myMesh.nodes[adj[0]][0][0]+(red_node_img.get_width()*(myMesh.nodes[adj[0]][1]/50)/2), myMesh.nodes[adj[0]][0][1]+(red_node_img.get_height()*(myMesh.nodes[adj[0]][1]/50)/2)), width = 10)

            text_font_distance = pygame.font.SysFont("Arial", 20, bold=True)
            display_distance = text_font_distance.render(f"{node}->{adj[0]}: {adj[1]}", True, (255, 255, 255))
            #screen.blit(display_distance, ( ((myMesh.nodes[node][0][0]+(red_node_img.get_width()*(myMesh.nodes[node][1]/50)/2))+(myMesh.nodes[adj[0]][0][0]+(red_node_img.get_width()*(myMesh.nodes[adj[0]][1]/50)/2)))/2 , ((myMesh.nodes[node][0][1]+(red_node_img.get_height()*(myMesh.nodes[node][1]/50)/2))+(myMesh.nodes[adj[0]][0][1]+(red_node_img.get_height()*(myMesh.nodes[adj[0]][1]/50)/2)))/2))
            screen.blit(display_distance, (path_distance_x_coor, path_distance_y_coor))

            if count <= 10:
                path_distance_x_coor += 100
                count += 1
            else:
                path_distance_x_coor = 40
                path_distance_y_coor += 25
                count = 1
                 
    for node, info in myMesh.nodes.items():
        if node == current_position:
            prework_node_image = purple_node_img
        elif node in next_positions:
            prework_node_image = orange_node_img
        else:
            prework_node_image = red_node_img
        work_image = pygame.transform.scale(prework_node_image, (prework_node_image.get_width()*(info[1]/50), prework_node_image.get_height()*(info[1]/50)))
        screen.blit(work_image, info[0])

        text_font_node = pygame.font.SysFont("Arial", int(info[1]*1.4), bold=True)
        display_node = text_font_node.render(str(node), True, (255, 255, 255))
        screen.blit(display_node, (info[0][0]+(work_image.get_width()/2)-(display_node.get_width()/2), info[0][1]+(work_image.get_height()/2)-(display_node.get_height()/1.5)))
        
        text_font_weight = pygame.font.SysFont("Arial", int(info[1]*0.8), bold=True)
        display_weight = text_font_weight.render(str(info[1]), True, (255, 255, 255))
        screen.blit(display_weight, (info[0][0]+(work_image.get_width()/2)-(display_weight.get_width()/2), info[0][1]+(work_image.get_height()/1.3)-(display_weight.get_height()/2)))
        
    
    display_total_distance = text_font_current_data.render(f"cd: {cumulative_distance}", True, (255, 255, 255))
    display_previous_node = text_font_current_data.render(f"p_node: {previous_node}", True, (255, 255, 255))
    display_node_data = text_font_current_data.render(f"data: {node_data}", True, (255, 255, 255))
    
    screen.blit(display_total_distance, (1100, 20))
    screen.blit(display_previous_node, (1100, 50))
    screen.blit(display_node_data, (1100, 85))


    key = pygame.key.get_pressed()
      
    if active_input_1 == False and active_input_2 == False:
        if key[pygame.K_a] and (any("A" in i for i in myMesh.adjacencies[current_position])):
            key_procedure_execute("A")
        if key[pygame.K_b] and (any("B" in i for i in myMesh.adjacencies[current_position])):
            key_procedure_execute("B")
        if key[pygame.K_c] and (any("C" in i for i in myMesh.adjacencies[current_position])):
            key_procedure_execute("C")
        if key[pygame.K_d] and (any("D" in i for i in myMesh.adjacencies[current_position])):
            key_procedure_execute("D")
        if key[pygame.K_e] and (any("E" in i for i in myMesh.adjacencies[current_position])):
            key_procedure_execute("E")
        if key[pygame.K_f] and (any("F" in i for i in myMesh.adjacencies[current_position])):
            key_procedure_execute("F")
        if key[pygame.K_g] and (any("G" in i for i in myMesh.adjacencies[current_position])):
            key_procedure_execute("G")
        if key[pygame.K_h] and (any("H" in i for i in myMesh.adjacencies[current_position])):
            key_procedure_execute("H")
        if key[pygame.K_i] and (any("I" in i for i in myMesh.adjacencies[current_position])):
            key_procedure_execute("I")
    

    if key[pygame.K_p]:
        cumulative_distance = 0


    if dijkstra_alg_btn.check_clicked() and validInput() and time_interval > 3:
        result_dict = {"N": ["g", "P"]} 
        dijkstar_alg = True
        num_ofrows = 3
        list_display = backtrack_list(dijkstar_alg_execute(user_input_1, user_input_2))
        display_string = str(list_display[0])
        for j in range(len(list_display)-1):
            display_string += f" -> {list_display[j+1]}"
        display_string_obj = text_font_table_data.render(display_string, True, (255, 255, 255))
        time_interval = 0
        a_star_alg = False

    if a_star_alg_btn.check_clicked() and validInput() and time_interval > 3:
        result_dict = {"N": ["g", "h", "f", "P", "S"]} 
        num_ofrows = 6
        time_interval = 0
        a_star_alg = True
        dijkstar_alg = False
        list_display = backtrack_list(a_star_alg_execute(user_input_1, user_input_2))
        display_string = str(list_display[0])
        for j in range(len(list_display)-1):
            display_string += f" -> {list_display[j+1]}"
        display_string_obj = text_font_table_data.render(display_string, True, (255, 255, 255))
        
        

    #if display_table:
        #display_table_func(num_ofrows, result_dict, "test")
        #display_table = True
        
    if dijkstar_alg:
        display_table_func(num_ofrows, result_dict, "dijkstra's")
        screen.blit(display_string_obj, (950, 140))

    if a_star_alg:
        display_table_func(num_ofrows, result_dict, "a_star")
        screen.blit(display_string_obj, (950, 140))
        


        

    
    if time_interval < 200:
        time_interval += 1


    


    
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()