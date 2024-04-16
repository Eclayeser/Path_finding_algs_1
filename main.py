import pygame


pygame.init()
scr_width = 1300
scr_height = 650
screen = pygame.display.set_mode((scr_width, scr_height))
clock = pygame.time.Clock()


run = True
bg_colour = (0, 255, 255)

red_node_img = pygame.image.load("red_node.png")
purple_node_img = pygame.image.load("purple_node.png")
orange_node_img = pygame.image.load("orange_node.png")

input_made = False
input_field_displayed = False
destination = ""


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
    
    def select_deselect(self):

        if self.selected == False and self.already_pressed == False:
            self.selected = True
            self.already_pressed = True
        if self.selected == True and self.already_pressed == False:
            self.selected = False
            self.already_pressed = True

    def deselect(self):
        self.selected = False
        self.already_pressed = True

    def getSelected(self):
        return self.selected
        

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


dijkstra_alg_btn = Button(pygame.image.load('dijkstra_btn_1.png'), pygame.image.load('dijkstra_btn_2.png'), 1090, 500, 0.5)
buttons_spr_group = pygame.sprite.Group()
buttons_spr_group.add(dijkstra_alg_btn)



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
myMesh.joinNodes("B",("A", 40), ("C", 25), ("I", 25))
myMesh.joinNodes("C",("A", 20), ("B", 25), ("E", 20))
myMesh.joinNodes("D",("G", 45), ("I", 15))
myMesh.joinNodes("E",("C", 30), ("D", 50), ("F", 50))
myMesh.joinNodes("F",("C", 40), ("G", 25))
myMesh.joinNodes("G",("D", 20), ("F", 25))
myMesh.joinNodes("H",("A", 45))
myMesh.joinNodes("I",("B", 30), ("D", 50))


myMesh.getNodes()
myMesh.getAdjacencies()



current_position = "A"
previous_node = ""
node_data = ""
next_positions = [j[0] for j in myMesh.adjacencies[current_position]]
cumulative_distance = 0
#keys_check = {"K_a": "A", "K_b": "B", "K_c": "C", "K_d": "D", "K_e": "E", "K_f": "F", "K_g": "G", "K_h": "H", "K_i": "I"}
text_font_current_data = pygame.font.SysFont("Arial", 35, bold=True)
text_font_table_data = pygame.font.SysFont("Arial", 20, bold=True)
node_names = [x for x in myMesh.nodes]
time_interval = 0
display_table = False
result_dict = {}



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

"""       
def dijkstar_alg_execute(start_node_name, end_node_name):
    unvisited_dictionary = {}
    visited = []

    for name, distance in myMesh.adjacencies[start_node_name]:
        unvisited_dictionary[name] = [distance, start_node_name]
    result_dict[start_node_name] = ["-", "-"]
    visited.append(start_node_name)

    while len(unvisited_dictionary) > 0:
        compare_distances = [j[0] for i,j in result_dict.items() if type(j[0])== int and i not in visited]
        min_value = min(compare_distances)
        for next_node, next_node_data in result_dict.items():
            if next_node_data[0] == min_value:
                next_node_name = next_node
           
        currentNode_distance, previous_node_name = unvisited_dictionary.pop(next_node_name)
        currentNode_name = next_node_name
            
       
        if result_dict[currentNode_name][0] > currentNode_distance:
            result_dict[currentNode_name] = []
"""   

def display_table_func(num_of_rows, dictionary):
    keys_dict = [i for i in dictionary.keys()]
    distance_dict = [i[0] for i in dictionary.values()]
    prervious_dict = [i[1] for i in dictionary.values()]

    y_coor_1 = 175
    y_coor_2 = y_coor_1
    x_coor_1 = 930
    x_coor_2 = 1280

    difference_y = 45
    difference_x = (x_coor_2-x_coor_1)/len(myMesh.nodes)

    x_coor_3 = x_coor_1 + difference_x/7
    y_coor_3 = y_coor_1 + difference_y/4


    for i in range(0, num_of_rows+1):
        pygame.draw.line(screen, (0, 0, 0), (x_coor_1, y_coor_1), (x_coor_2, y_coor_1), width = 3)
        
        if i < num_of_rows:
            for j in range(0, len(myMesh.nodes)):
                if i == 0:
                    try:
                        display_table_data = text_font_table_data.render(str(keys_dict[j]), True, (0,0,0))
                    except IndexError:
                        display_table_data = text_font_table_data.render("-", True, (0,0,0))
                    screen.blit(display_table_data, (x_coor_3, y_coor_3))
                if i == 1:
                    try:
                        display_table_data = text_font_table_data.render(str(distance_dict[j]), True, (0,0,0))
                    except IndexError:
                        display_table_data = text_font_table_data.render("-", True, (0,0,0))
                    screen.blit(display_table_data, (x_coor_3, y_coor_3))
                if i == 2:
                    try:
                        display_table_data = text_font_table_data.render(str(prervious_dict[j]), True, (0,0,0))
                    except IndexError:
                        display_table_data = text_font_table_data.render("-", True, (0,0,0))
                    screen.blit(display_table_data, (x_coor_3, y_coor_3))

                x_coor_3 += difference_x
                
                if j == len(myMesh.nodes)-1:
                    x_coor_3 = x_coor_1 + difference_x/7
        
        y_coor_1 += difference_y
        y_coor_3 += difference_y

    y_coor_1 -= difference_y
   
    for j in range(0, len(myMesh.nodes)+1):
        pygame.draw.line(screen, (0, 0, 0), (x_coor_1, y_coor_2), (x_coor_1, y_coor_1), width = 3)
        x_coor_1 += difference_x
    



while run:
    screen.fill(bg_colour)

    buttons_spr_group.update()
    buttons_spr_group.draw(screen)




    path_distance_x_coor = 40
    path_distance_y_coor = 585
    count = 0
    for node, adjs in myMesh.adjacencies.items():
        for adj in adjs:
            pygame.draw.line(screen, (255, 255, 0), (myMesh.nodes[node][0][0]+(red_node_img.get_width()*(myMesh.nodes[node][1]/50)/2), myMesh.nodes[node][0][1]+(red_node_img.get_height()*(myMesh.nodes[node][1]/50)/2)), (myMesh.nodes[adj[0]][0][0]+(red_node_img.get_width()*(myMesh.nodes[adj[0]][1]/50)/2), myMesh.nodes[adj[0]][0][1]+(red_node_img.get_height()*(myMesh.nodes[adj[0]][1]/50)/2)), width = 10)

            text_font_distance = pygame.font.SysFont("Arial", 20, bold=True)
            display_distance = text_font_distance.render(f"{node}->{adj[0]}: {adj[1]}", True, (0, 0, 0))
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
        display_node = text_font_node.render(str(node), True, (0, 0, 0))
        screen.blit(display_node, (info[0][0]+(work_image.get_width()/2)-(display_node.get_width()/2), info[0][1]+(work_image.get_height()/2)-(display_node.get_height()/1.5)))
        
        text_font_weight = pygame.font.SysFont("Arial", int(info[1]*0.8), bold=True)
        display_weight = text_font_weight.render(str(info[1]), True, (0, 0, 0))
        screen.blit(display_weight, (info[0][0]+(work_image.get_width()/2)-(display_weight.get_width()/2), info[0][1]+(work_image.get_height()/1.3)-(display_weight.get_height()/2)))
        
    
    display_total_distance = text_font_current_data.render(f"cd: {cumulative_distance}", True, (0, 0, 0))
    display_previous_node = text_font_current_data.render(f"p_node: {previous_node}", True, (0, 0, 0))
    display_node_data = text_font_current_data.render(f"data: {node_data}", True, (0, 0, 0))
    
    screen.blit(display_total_distance, (1100, 20))
    screen.blit(display_previous_node, (1100, 50))
    screen.blit(display_node_data, (1100, 85))


    key = pygame.key.get_pressed()
      
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


    if dijkstra_alg_btn.check_clicked() and time_interval > 3:
        display_table = True
        
        time_interval = 0
        num_ofrows = 3

    
    if time_interval < 6:
        time_interval += 1

    if display_table:
        display_table_func(num_ofrows, result_dict)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()