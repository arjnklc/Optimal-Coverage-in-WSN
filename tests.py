from matplotlib import pyplot as plt

from solver import Solver

def visualize(point_locations, sensor_locations, sensor_radius):
    plt.grid()
    for i in sensor_locations:
        circle1 = plt.Circle((i[0], i[1]), sensor_radius, color='g')
        plt.gcf().gca().add_artist(circle1)
    for i in point_locations:
        plt.plot(i[0], i[1], marker='s',color='y')

    plt.show()

def test1():
    M = 10  # Grid Size 2d ( MxM )
    sensor_radius = 3
    sensor_cost = 5
    budget = 5
    locations = [(0, 0), (2, 2), (4, 4)]  # Locations of the points that must be covered

    s = Solver(M, sensor_radius, sensor_cost, budget, locations)
    solution = s.solve()
    visualize(locations, solution, sensor_radius)


def test2():
    M = 10  # Grid Size 2d ( MxM )
    sensor_radius = 3
    sensor_cost = 5
    budget = 12
    locations = [(0, 0), (2, 2), (4, 4), (7,9)]  # Locations of the points that must be covered

    s = Solver(M, sensor_radius, sensor_cost, budget, locations)
    print(s.solve())
