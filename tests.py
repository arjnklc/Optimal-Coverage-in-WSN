from matplotlib import pyplot as plt
import random
from solver import Solver
import json
import time


def visualize(point_locations, sensor_locations, sensor_radius):
    plt.grid()
    for i in sensor_locations:
        circle1 = plt.Circle((i[0], i[1]), sensor_radius, color='y')
        plt.gcf().gca().add_artist(circle1)
    for i in point_locations:
        plt.plot(i[0], i[1], marker='s',color='b')

    plt.show()


def plot_coverage_comparison(num_points, bip_coverage, heuristic_coverage):
    plt.plot(bip_coverage, marker="o")
    plt.plot(heuristic_coverage, marker="o")

    plt.xticks(range(len(num_points)), num_points)

    plt.xlabel("Number of Points")
    plt.ylabel("Coverage")

    plt.legend(['BIP', 'Greedy'], loc='best')
    plt.grid()
    plt.show()

def plot_runtime_comparison(num_points, bip_runtime, heuristic_runtime):
    plt.plot(bip_runtime, marker="o")
    plt.plot(heuristic_runtime, marker="o")

    plt.xticks(range(len(num_points)), num_points)

    plt.xlabel("Number of Points")
    plt.ylabel("Runtime (seconds)")

    plt.legend(['BIP', 'Greedy'], loc='best')
    plt.grid()
    plt.show()

def write_test_files(filename, M, budget, sensor_cost, sensor_radius, locations):
    test_data = {}
    test_data['M'] = M
    test_data['budget'] = budget
    test_data['sensor_cost'] = sensor_cost
    test_data['sensor_radius'] = sensor_radius
    test_data['locations'] = []

    for i in range(len(locations)):
        loc = [locations[i][0], locations[i][1]]
        test_data['locations'].append(loc)


    with open("tests/" + filename + ".json", 'w+') as f:
        json.dump(test_data, f)


def create_test_folder():
    import os
    if not os.path.exists('tests'):
        os.makedirs('tests')

def generate_tests():
    create_test_folder()
    sensor_radius = 8
    sensor_cost = 8
    num_instances = 25
    M = 100

    for i in range(num_instances):
        num_points = 150 * (i + 1)
        budget = random.randint(M, M * 5)
        locations = []
        for k in range(num_points):
            x = random.randint(0, M - 1)
            y = random.randint(0, M - 1)
            locations.append((x, y))

        write_test_files("test_" + str(i), M, budget, sensor_cost, sensor_radius, locations)


def run_all_tests():
    len_locs = []
    bip_coverages = []
    heuristic_coverages = [] # ratio
    bip_runtimes = []  # seconds
    heuristic_runtimes = []  # seconds

    for i in range(24):
        filepath = "tests/test_" + str(i) + ".json"

        with open(filepath) as f:
            test_data = json.load(f)
            M = test_data['M']
            budget = test_data['budget']
            sensor_cost = test_data['sensor_cost']
            sensor_radius = test_data['sensor_radius']
            locations = []
            for loc in test_data['locations']:
                locations.append( (loc[0], loc[1] ))

        s = Solver(M, sensor_radius, sensor_cost, budget, locations)

        start_time = time.time()
        BIP_solution, BIP_covered = s.solve()
        end_time = time.time()
        bip_runtimes.append(end_time - start_time)

        start_time = time.time()
        heuristic_solution, heuristic_covered = s.heuristic_solve()
        end_time = time.time()
        heuristic_runtimes.append(end_time - start_time)

        print("----------------------------")
        print("BIP coverage:       {}, number of sensors used: {}".format(BIP_covered/len(locations), len(BIP_solution)))
        print("Heuristic coverage: {}, number of sensors used: {}".format(heuristic_covered/len(locations), len(heuristic_solution)))
        print("----------------------------")

        len_locs.append(len(locations))
        bip_coverages.append(BIP_covered / len(locations))
        heuristic_coverages.append(heuristic_covered/ len(locations))

        #visualize(locations, BIP_solution, sensor_radius)
        #visualize(locations, heuristic_solution, sensor_radius)

    """
    print(len_locs)
    print(bip_coverages)
    print(heuristic_coverages)
    print(bip_runtimes)
    print(heuristic_runtimes)
    """

    plot_coverage_comparison(len_locs, bip_coverages, heuristic_coverages)
    plot_runtime_comparison(len_locs, bip_runtimes, heuristic_runtimes)