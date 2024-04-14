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


"""
class Object(pygame.sprite.Sprite):
     def __init__(self):
        super().__init__()

class Node(Object):
    def __init__(self, pos_x, pos_y, ident):
        super().__init__()
        self.weight = None
        self.width = red_node_img.get_width()
        self.height = red_node_img.get_height()
        self.ident = text_font.render(str(ident), True, (0, 0, 0))
        if self.weight != None:
            self.weight_display = text_font.render(str(self.weight), True, (0, 0, 0))
        elif self.weight == None:
            self.weight_display = text_font.render("-", True, (0, 0, 0))


        self.image = red_node_img
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]



    def set_weight(self, weight):
        self.weight = weight

    def update(self):
        screen.blit(self.ident, (self.rect.x+(self.rect.width/2)-(self.ident.get_width()/2), self.rect.y+(self.rect.height/2)-(self.ident.get_height()/1.5))) 
        screen.blit(self.weight_display, (self.rect.x+(self.rect.width/2)-(self.weight_display.get_width()/2), self.rect.y+(self.rect.height/2))) 
"""

class Mesh:
    def __init__(self):
        self.adjacencies = {}
        self.nodes = {}
        

    def getAdjacencies(self):
        print(self.adjacencies)

    def getNodes(self):
        print(self.nodes)

    def addNode(self, value, pos_x, pos_y, weight):
        if weight == None:
            weight = 40
        self.adjacencies[value] = []
        self.nodes[value] = [(pos_x, pos_y), weight]
        

    def joinNodes(self, from_node, *to_nodes):
        for to_node in to_nodes:
            self.adjacencies[from_node].append(to_node)



myMesh = Mesh()
myMesh.addNode("A", 100, 100, 50)
myMesh.addNode("B", 200, 400, 45)
myMesh.addNode("C", 600, 350, 60)
myMesh.addNode("D", 800, 25, 30)
myMesh.addNode("F", 350, 150, 75)
#myTree.addNode("G")
#myTree.addNode("H")
#myTree.root = "A"
myMesh.getNodes()

myMesh.joinNodes("A",("B", 25), ("D", 40))
myMesh.joinNodes("B",("C", 40), ("A", 25))
myMesh.joinNodes("C",("B", 20), ("F", 25))
myMesh.joinNodes("D",("C", 45), ("F", 15))
myMesh.joinNodes("F",("A", 30), ("D", 50))
myMesh.getAdjacencies()

current_position = "A"
previous_node = ""
next_positions = [j[0] for j in myMesh.adjacencies[current_position]]
cumulative_distance = 0

text_font_current_data = pygame.font.SysFont("Arial", 35, bold=True)

node_names = [x for x in myMesh.nodes]

#square = pygame.Rect(0, 0, 30, 30)
#square.center = (myMesh.nodes["A"][0][0]+(red_node_img.get_width()*(myMesh.nodes["A"][1]/50)/2)), (myMesh.nodes["A"][0][1]+(red_node_img.get_height()*(myMesh.nodes["A"][1]/50)/2))
def look_for_distance(prev, to):
    for i in myMesh.adjacencies[prev]:
        if i[0] == to:
            return i[1]
          
while run:
    screen.fill(bg_colour)

    path_distance_x_coor = 40
    path_distance_y_coor = 585
    for node, adjs in myMesh.adjacencies.items():
        for adj in adjs:
            pygame.draw.line(screen, (255, 255, 0), (myMesh.nodes[node][0][0]+(red_node_img.get_width()*(myMesh.nodes[node][1]/50)/2), myMesh.nodes[node][0][1]+(red_node_img.get_height()*(myMesh.nodes[node][1]/50)/2)), (myMesh.nodes[adj[0]][0][0]+(red_node_img.get_width()*(myMesh.nodes[adj[0]][1]/50)/2), myMesh.nodes[adj[0]][0][1]+(red_node_img.get_height()*(myMesh.nodes[adj[0]][1]/50)/2)), width = 10)

            text_font_distance = pygame.font.SysFont("Arial", 20, bold=True)
            display_distance = text_font_distance.render(f"{node}->{adj[0]}: {adj[1]}", True, (0, 0, 0))
            #screen.blit(display_distance, ( ((myMesh.nodes[node][0][0]+(red_node_img.get_width()*(myMesh.nodes[node][1]/50)/2))+(myMesh.nodes[adj[0]][0][0]+(red_node_img.get_width()*(myMesh.nodes[adj[0]][1]/50)/2)))/2 , ((myMesh.nodes[node][0][1]+(red_node_img.get_height()*(myMesh.nodes[node][1]/50)/2))+(myMesh.nodes[adj[0]][0][1]+(red_node_img.get_height()*(myMesh.nodes[adj[0]][1]/50)/2)))/2))
            screen.blit(display_distance, (path_distance_x_coor, path_distance_y_coor))

            path_distance_x_coor += 100
        
            
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
        
        
    #pygame.draw.rect(screen, (255, 255, 255), square)

    
    display_total_distance = text_font_current_data.render(f"cd: {cumulative_distance}", True, (0, 0, 0))
    display_previous_node = text_font_current_data.render(f"p_node: {previous_node}", True, (0, 0, 0))
    
    screen.blit(display_total_distance, (1145, 20))
    screen.blit(display_previous_node, (1145, 50))
        
    

    key = pygame.key.get_pressed()
    if key[pygame.K_a] and (any("A" in i for i in myMesh.adjacencies[current_position])):
        previous_node = current_position
        current_position = "A"
        next_positions = [j[0] for j in myMesh.adjacencies[current_position]]
        cumulative_distance += look_for_distance(previous_node, current_position)
    if key[pygame.K_b] and (any("B" in i for i in myMesh.adjacencies[current_position])):
        previous_node = current_position
        current_position = "B"
        next_positions = [j[0] for j in myMesh.adjacencies[current_position]]
        cumulative_distance += look_for_distance(previous_node, current_position)
    if key[pygame.K_c] and (any("C" in i for i in myMesh.adjacencies[current_position])):
        previous_node = current_position
        current_position = "C"
        next_positions = [j[0] for j in myMesh.adjacencies[current_position]]
        cumulative_distance += look_for_distance(previous_node, current_position)
    if key[pygame.K_d] and (any("D" in i for i in myMesh.adjacencies[current_position])):
        previous_node = current_position
        current_position = "D"
        next_positions = [j[0] for j in myMesh.adjacencies[current_position]]
        cumulative_distance += look_for_distance(previous_node, current_position)
    if key[pygame.K_f] and (any("F" in i for i in myMesh.adjacencies[current_position])):
        previous_node = current_position
        current_position = "F"
        next_positions = [j[0] for j in myMesh.adjacencies[current_position]]
        cumulative_distance += look_for_distance(previous_node, current_position)


    if key[pygame.K_p]:
        cumulative_distance = 0
    
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()