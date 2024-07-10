import pulp

def optimize_arbitrage(initial_usd_amount):
    # Define the problem
    prob = pulp.LpProblem("Arbitrage", pulp.LpMaximize)

    # Define the nodes and edges with profit, fees, and risks
    nodes = ['USD', 'Exchange1', 'Exchange2', 'Exchange3', 'Exchange4']
    edges = {
        ('USD', 'Exchange1'): {'profit': 1.05, 'fee': 0.02, 'risk': 0.01},
        ('USD', 'Exchange2'): {'profit': -0.03, 'fee': 0.01, 'risk': 0.01},
        ('Exchange1', 'Exchange2'): {'profit': 1.10, 'fee': 0.03, 'risk': 0.02},
        ('Exchange1', 'Exchange3'): {'profit': -0.05, 'fee': 0.02, 'risk': 0.02},
        ('Exchange2', 'Exchange3'): {'profit': 1.08, 'fee': 0.01, 'risk': 0.01},
        ('Exchange2', 'Exchange4'): {'profit': -0.02, 'fee': 0.01, 'risk': 0.01},
        ('Exchange3', 'Exchange4'): {'profit': 1.07, 'fee': 0.02, 'risk': 0.01},
        ('Exchange3', 'USD'): {'profit': 1.06, 'fee': 0.02, 'risk': 0.01},
        ('Exchange4', 'USD'): {'profit': 1.04, 'fee': 0.02, 'risk': 0.01},
        ('Exchange4', 'Exchange1'): {'profit': -0.04, 'fee': 0.01, 'risk': 0.01},
    }

    # Define binary variables for path selection
    x = pulp.LpVariable.dicts("Path", edges, cat='Binary')

    # Define continuous variables for trade amounts
    f = pulp.LpVariable.dicts("Trade", edges, lowBound=0)

    # Define order variables for nodes
    order = pulp.LpVariable.dicts("Order", nodes, lowBound=0, upBound=len(nodes)-1, cat='Integer')

    # Define the objective function
    prob += pulp.lpSum([(edges[e]['profit'] - edges[e]['fee'] - edges[e]['risk']) * f[e] for e in edges])

    # Flow conservation constraints
    for node in nodes:
        if node == 'USD':
            prob += pulp.lpSum([f[('USD', j)] for j in nodes if ('USD', j) in edges]) == initial_usd_amount  # initial USD amount
            prob += pulp.lpSum([f[(i, 'USD')] for i in nodes if (i, 'USD') in edges]) == initial_usd_amount  # initial USD amount + desired profit
        else:
            prob += (pulp.lpSum([f[(i, node)] for i in nodes if (i, node) in edges]) - 
                     pulp.lpSum([f[(node, j)] for j in nodes if (node, j) in edges])) == 0

    # Risk constraints
    for e in edges:
        prob += edges[e]['risk'] * f[e] <= 0.05  # allowed risk threshold

    # Ensure trade amount is positive if the path is selected
    M = 1000000  # A large constant
    for e in edges:
        prob += f[e] <= M * x[e]
        prob += f[e] >= 0

    # Order constraints
    for (i, j) in edges:
        if i != 'USD' and j != 'USD':
            prob += order[j] >= order[i] + 1 - (len(nodes) * (1 - x[(i, j)]))

    # Ensure each node is visited at most once
    for node in nodes:
        if node != 'USD':
            prob += pulp.lpSum([x[(i, node)] for i in nodes if (i, node) in edges]) <= 1
            prob += pulp.lpSum([x[(node, j)] for j in nodes if (node, j) in edges]) <= 1

    # Ensure the start and end at USD
    prob += pulp.lpSum([x[('USD', j)] for j in nodes if ('USD', j) in edges]) == 1
    prob += pulp.lpSum([x[(i, 'USD')] for i in nodes if (i, 'USD') in edges]) == 1

    # Solve the problem
    prob.solve()

    # Extract the order of nodes from the solution
    order_values = {node: pulp.value(order[node]) for node in nodes}
    path = sorted(order_values, key=lambda x: order_values[x] if order_values[x] is not None else float('inf'))

    # Print the results
    for v in prob.variables():
        if v.varValue is not None and v.varValue > 0:
            print(v.name, "=", v.varValue)

    print("Total Profit =", pulp.value(prob.objective))
    print("Optimal Path:", path)

# Example usage with initial USD amount of 1000
optimize_arbitrage(1000)