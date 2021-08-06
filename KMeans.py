import pygame
from random import randint
import math 
from sklearn.cluster import KMeans

def distance(a,b):  #Hàm tính khoảng cách 2 điểm
	return math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))
pygame.init() # Khởi tạo các phương thức của pygame

screen = pygame.display.set_mode((1000,600))  #Tạo màn hình

pygame.display.set_caption("K_MEANS ")

running = 1

clock = pygame.time.Clock()

BLACK = (0,0,0)
WHITE =(255,255,255)
BACKGROUND_PANEL = (255,250,190)
BACKGROUND = (185, 211, 238)
LEMONCHIFFON = (139 ,137, 112)

RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(147,153,35)
PURPLE=(255,0,255)
SKY=(0,255,255)
ORANGE=(255,125,25)
GRAPE=(100,25,125)
GRASS=(55,155,65)
COLORS =[RED,GREEN,BLUE,YELLOW,PURPLE,SKY,ORANGE,GRAPE,GRASS]


# Tạo các text
font = pygame.font.SysFont('san',50);
font_mouse = pygame.font.SysFont('san',15);
text_plus = font.render('+', True, BLACK)
text_minus = font.render('-',True,BLACK)
text_run = font.render("RUN",True,BLACK)
text_random = font.render("Random",True,BLACK)
text_algorithm = font.render("Algorithm",True,BLACK)
text_reset= font.render("Reset",True,BLACK)

K = 0
error = 0
points =[]
clusters = [] # Điểm trung tâm
labels = [] # Nhãn

while running:
	clock.tick(60)
	mouse_x, mouse_y = pygame.mouse.get_pos()
	screen.fill(BACKGROUND)
    # Tạo background
	pygame.draw.rect(screen, BLACK, (50,50,650, 500))
	pygame.draw.rect(screen,BACKGROUND_PANEL,(55,55,640,490))

	#Tạo nút K+
	pygame.draw.rect(screen, LEMONCHIFFON,(725,50,50,50) )
	screen.blit(text_plus,(742,55))
	#Tạo nút K -
	pygame.draw.rect(screen, LEMONCHIFFON,(900,50,50,50) )
	screen.blit(text_minus,(920,55))

	#Tạo giá trị K

	text_k = font.render("K = " + str(K), True, BLACK)
	screen.blit(text_k, (800,60))

	#Tạo text_run
	pygame.draw.rect(screen,LEMONCHIFFON, (750,150,150,50))
	screen.blit(text_run, (790,160))

	#Tạo text_random
	pygame.draw.rect(screen, LEMONCHIFFON, (750,250,150,50))
	screen.blit(text_random, (756,255))

	#Tạo text_reset
	pygame.draw.rect(screen, LEMONCHIFFON, (750,500,150,50))
	screen.blit(text_reset, (775,505))	

	#Tạo hàm text_algorithm
	pygame.draw.rect(screen, LEMONCHIFFON, (740,400,170,50))
	screen.blit(text_algorithm, (745,405))	

	#Tạo text_error
	text_error = font.render("Error = " + str(int(error)), True, BLACK)
	screen.blit(text_error, (745,325))

	#Draw mouse position when mouse is in panel
	if 55 <= mouse_x <695 and 55<=mouse_y<545:
		text_mouse = font_mouse.render("("+str(mouse_x-55)+","+str(mouse_y-55)+")", True, BLACK)
		screen.blit(text_mouse, (mouse_x+10,mouse_y-10)) 
	
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT: #Out khỏi screen
			running = 0
		if event.type == pygame.MOUSEBUTTONDOWN:

			#Change point on panel
			if 55 <= mouse_x <695 and 55<=mouse_y<545:
				labels=[]
				point = [mouse_x-55,mouse_y-55]
				points.append(point)
				print(points)

			#Change K button +
			if 725 < mouse_x < 775 and 50 < mouse_y <100:
				if K <8:
					K +=1
				print("Press K +")

			#Change K button -
			if 900 < mouse_x < 950 and 50 < mouse_y <100:
				if K > 0:
					K -= 1
				print("Press K -")

			# Run button
			if 750 < mouse_x < 900 and 150 < mouse_y <200:
				if clusters ==[]:
					continue
				labels=[]

				#Assign points to closet cluster
				for p in points:
					distances_to_clusters = []
					for c in clusters:
						dis = distance(p,c)
						distances_to_clusters.append(dis)
					min_distances =  min(distances_to_clusters)
					label = distances_to_clusters.index(min_distances)
					labels.append(label)
					print("run pressed")

				#Update clusters
				for i in range(K):
					sum_x=0
					sum_y=0
					count=0
					for j in range(len(points)):
						if labels[j] == i:
							sum_x+=points[j][0]
							sum_y+=points[j][1]
							count+=1
					if count!=0:
						new_cluster_x= sum_x/count
						new_cluster_y=sum_y/count
						clusters[i]=[new_cluster_x,new_cluster_y]

			# Random button
			if 750 < mouse_x < 900 and 250 < mouse_y<300:
				labels=[]
				clusters=[]
				for i in range(K):
					random_point = [randint(0,650),randint(0,500)]
					clusters.append(random_point)
				print("random pressed")

			# Reset button
			if 750 < mouse_x < 900 and 500 < mouse_y < 550:
				points=[]
				labels=[]
				clusters=[]
				K=0
				error=0
				print("reset button pressed")

			# Algorithm 
			if 740 < mouse_x <910 and 400 < mouse_y < 450: #fil huân luyện, predict dự đoán
				try:
					kmeans = KMeans(n_clusters=K).fit(points)
					labels = kmeans.predict(points)
					clusters = kmeans.cluster_centers_
				except:
					print("ERROR")
				print("Algorithm button pressed")			

	#Draw cluster
	for i in range(len(clusters)):
		pygame.draw.circle(screen,COLORS[i],(int(clusters[i][0])+55,int(clusters[i][1])+55),6)

	#Draw point
	for i in range(len(points)):
		pygame.draw.circle(screen,BLACK,(points[i][0]+55,points[i][1]+55),5)
		if labels ==[]:
			pygame.draw.circle(screen,WHITE,(points[i][0]+55,points[i][1]+55),4)
		else:
			pygame.draw.circle(screen,COLORS[labels[i]],(points[i][0]+55,points[i][1]+55),4)
			
	#Calculate and draw error
	error=0
	if clusters!=[] and labels!=[]:
		for i in range(len(points)):
			error+=distance(points[i],clusters[labels[i]])

	pygame.display.flip()		

pygame.quit()			