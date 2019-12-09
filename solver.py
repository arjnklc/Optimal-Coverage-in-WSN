from gurobipy import *
import math


class Solver:
    def __init__(self, M, sensor_radius, sensor_cost, budget, point_locations):
        self.M = M
        self.sensor_radius = sensor_radius
        self.sensor_cost = sensor_cost
        self.budget = budget
        self.point_locations = point_locations
        self.site = self.calculate()

    @staticmethod
    def euclidean_distance(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return math.sqrt(dx ** 2 + dy ** 2)

    # Returns which locations can cover which given points with given radius
    def calculate(self):
        res = []
        for i in range(self.M):
            sub_res = []
            for j in range(self.M):
                sub_sub_res = []
                for loc in range(len(self.point_locations)):
                    if self.euclidean_distance(self.point_locations[loc], (i, j)) <= self.sensor_radius:
                        sub_sub_res.append(loc)

                sub_res.append(sub_sub_res)

            res.append(sub_res)

        return res

    def get_diff(self, sites, covered):
        diff = 0
        for site in sites:
            if site not in covered:
                diff += 1

        return diff

    def get_most_effective(self, covered):
        x = 0
        y = 0
        num_cover = 0
        M = self.M
        for i in range(M):
            for j in range(M):
                difference = self.get_diff(self.site[i][j], covered)
                if difference > num_cover:
                    x, y = i, j
                    num_cover = difference

        return x, y

    def heuristic_solve(self):
        solution = []
        covered_so_far = set()
        money = self.budget
        # While we still have money and we did not cover all points
        num_locs = len(self.point_locations)
        num_covered = len(covered_so_far)
        while money >= self.sensor_cost and num_covered < num_locs:
            effective = self.get_most_effective(covered_so_far)
            solution.append(effective)
            covered_so_far.update(self.site[effective[0]][effective[1]])

            money -= self.sensor_cost
            num_covered = len(covered_so_far)

        return solution, len(covered_so_far)

    def solve(self):
        m = Model()
        t = {}  # Decision variables for sensors (1 if sensor located, 0 otherwise)
        r = {}  # Decision variables for points (1 if covered, 0 otherwise)

        M = self.M
        for i in range(M):
            for j in range(M):
                t[(i, j)] = m.addVar(vtype=GRB.BINARY, name="t%d,%d" % (i, j))

        for i in range(len(self.point_locations)):
            r[i] = m.addVar(vtype=GRB.BINARY, name="r%d" % i)

        m.update()

        for k in range(len(self.point_locations)):
            m.addConstr(quicksum(t[(i, j)] for i in range(M) for j in range(M) if k in self.site[i][j]) >= r[k])

        m.addConstr(quicksum(self.sensor_cost * t[(i, j)] for i in range(M) for j in range(M)) <= self.budget)
        m.setObjective(quicksum(r[i] for i in range(len(self.point_locations))), GRB.MAXIMIZE)
        m.Params.outputFlag = 0  # disable verbose output
        m.optimize()

        result = []
        for i in range(M):
            for j in range(M):
                if t[(i, j)].X == 1:
                    result.append((i, j))

        ctr = 0
        for i in range(len(self.point_locations)):
            if r[i].x == 1:
                ctr+= 1

        return result, ctr


