from sklearn.cluster import KMeans
import pygame
from random import randint
import math
pygame.font.init()

WIDTH, HEIGHT = 1200, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kmeans visualization")

# Thiết lập giao diện pygame
FPS = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
BG = (214,214,214)
BG_PANEL = (249,255,230)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147, 153, 35)
PURPLE = (255, 0, 255)
SKY = (0, 255, 255)
ORANGE = (255, 125, 25)
GRAPE = (100, 25, 125)
GRASS = (55, 155, 65)
COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRAPE, GRASS]

# Function tính khoảng cách giữa 2 điểm 
def distance(p1, p2):
	return math.sqrt((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))

# Draw ----------------------------------
def draw_panel(color, rect):
	pygame.draw.rect(SCREEN, color, rect)

def draw_button(text, color, position):
	font = pygame.font.SysFont('sans', 40)
	text_render = font.render(text, 1, color)
	SCREEN.blit(text_render, position)

def draw_mouse(text, mouse_x, mouse_y):
	font = pygame.font.SysFont("sans", 20)
	text_mouse = font.render(text, 1, BLACK)
	if 55 < mouse_x < 745 and 55 < mouse_y < 545:
		SCREEN.blit(text_mouse, (mouse_x + 10, mouse_y) )

def draw_points(points, labels):
	for i in range(len(points)):		
		pygame.draw.circle(SCREEN, BLACK, (points[i][0] + 55, points[i][1] + 55), 6)
		if labels == []:
			pygame.draw.circle(SCREEN, WHITE, (points[i][0] + 55, points[i][1] + 55), 5)
		else:
			pygame.draw.circle(SCREEN, COLORS[labels[i]], (points[i][0] + 55, points[i][1] + 55), 5)

def draw_clusters(clusters):
	for i in range(len(clusters)):
		pygame.draw.circle(SCREEN, COLORS[i], (clusters[i][0] + 55, clusters[i][1] + 55), 10)

# khoảng cách giữa điểm đến cụm sau khi biến đổi
def caculate_error(clusters, labels, points):
	error = 0
	if clusters != [] and labels != []:
		for i in range(len(points)):
			error += distance(points[i], clusters[labels[i]])

		return int(error)

def draw_window(K, error, mouse_x, mouse_y, points, clusters, labels):	
	SCREEN.fill(BG)
	draw_panel(BLACK, (50,50,700,500))
	draw_panel(BG_PANEL, (55,55,690,490))
	draw_panel(BLACK, (850,50,50,50)) 
	draw_panel(BLACK, (950,50,50,50))
	draw_panel(BLACK, (850,150,150,50))
	draw_panel(BLACK, (850,250,150,50))
	draw_panel(BLACK, (850,550,150,50))
	draw_panel(BLACK, (850,450,170,50))

	draw_button("+", WHITE, (860,50))
	draw_button("-", WHITE, (960,50))
	draw_button("Run", WHITE, (890,150))
	draw_button("Random", WHITE,  (850,250))
	draw_button("Algorithm", WHITE, (850,450))
	draw_button("Reset", WHITE, (860,550))
	draw_button("K = " + str(K), BLACK, (1050,50))
	draw_button("Error = " + str(error), BLACK, (850,350))
	draw_mouse("(" + str(mouse_x - 55) + "," + str(mouse_y - 55) + ")", mouse_x, mouse_y)
	draw_points(points, labels)
	draw_clusters(clusters)

	pygame.display.update()

def main():
	K = 0
	error = 0
	points = []
	clusters = []
	labels = []

	clock  = pygame.time.Clock()
	run = True

	while run:
		clock.tick(FPS)
		mouse_x, mouse_y = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				# Add points
				if 55 < mouse_x < 745 and 55 < mouse_y < 545:
					labels = []
					point = [mouse_x - 55, mouse_y - 55]
					points.append(point)

				# Change K button +
				if 850 < mouse_x < 900 and 50 < mouse_y < 100:
					if K < 9:
						K = K+1
				
				# Change K button -
				if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
					if K > 0:
						K -= 1

				# Run button
				if 850 < mouse_x < 1000 and 150 < mouse_y < 200:
					# Xác định khoảng cách các điểm đến các cụm Random và gắn nhãn cho các điểm
					labels = []
					if clusters == [] or points == []:
						print("Please enter again")
					else:
						# Xác định khoảng cách các điểm đến các cụm Random và gắn nhãn cho các điểm	-> điểm thuộc phân cụm nào				
						for point in points:
							distances_to_cluster = []
							for cluster in clusters:
								dis = distance(point, cluster)
								distances_to_cluster.append(dis)

							min_distance = min(distances_to_cluster)
							label = distances_to_cluster.index(min_distance)
							labels.append(label)

						# Tính khoản cách từ các điểm đến phân cụm cho trước -> di chuyển điểm phân cụm vào trung tâm
						for i in range(len(clusters)):
							sum_x = 0
							sum_y = 0
							count = 0
							for j in range(len(points)):
								if labels[j] == i:
									sum_x += points[j][0]
									sum_y += points[j][1]
									count += 1

							if count != 0:
								new_cluster_x = int(sum_x/count)
								new_cluster_y = int(sum_y/count)
								clusters[i] = [new_cluster_x, new_cluster_y]

						# tính tổng khoảng cách từ điểm đến phân cụm đã di chuyển
						error = caculate_error(clusters, labels, points)	
				# Random button
				if 850 < mouse_x < 1000 and 250 < mouse_y < 300:
					clusters = []
					labels = []
					error = 0
					if K == 0:
						print("Enter K")
					else:
						for i in range(K):
							random_point = [randint(0,690), randint(0, 490)]
							clusters.append(random_point)

				# Reset button
				if 850 < mouse_x < 1000 and 550 < mouse_y < 600:
					points = []
					clusters = []
					K = 0
					error = 0

				# Algorithm 
				if 850 < mouse_x < 1020 and 450 < mouse_y < 500:
					try:
						kmeans = KMeans(n_clusters=K).fit(points)
						labels = kmeans.predict(points)
						clusters = kmeans.cluster_centers_
						error = caculate_error(clusters, labels, points)
					except:
						print("Error")
			if event.type == pygame.QUIT:
				run = False
				
		draw_window(K, error, mouse_x, mouse_y, points, clusters, labels)

	pygame.quit()

main()