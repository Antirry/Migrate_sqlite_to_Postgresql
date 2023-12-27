from collections import defaultdict


def check_ref_table(queries:tuple) -> list[dict[str: list[str]]]:
    """Found data tables which use another tables

    Args:
        queries (tuple): query to create database in sqlite

    Returns:
        list[dict[str: list[str]]]: Graph tables
    """
    queries = queries[1]
    name_table = queries.split('"', 2)[1]
    find_ref = 'REFERENCES'
    table_names = []

    for line_query in queries.split('\n')[::-1][1:]:
        if (find:=line_query.rfind(find_ref)) != -1:
            table_name = line_query[find:].split('"', 2)
            table_names.append(table_name[1])

    return {name_table: table_names}


def topological_sort(graph: dict[str: list[str]]) -> list:
    """topological sorting

    Args:
        graph (dict[str: list[str]]): Returned from check_ref_table

    Returns:
        List: From parent to child (Table names)
    """
    # Create a dictionary to store the adjacency list of the graph
    # Создаю словарь для хранения списка смежности графа
    adj_list = defaultdict(list)
    in_degree = defaultdict(int)

    # Populating the adjacency list and in-degree
    # Пополнение списка смежности и степеней родства
    for node, neighbors in graph.items():
        in_degree[node]  # Ensure all nodes are present in the in-degree dictionary
        # Убедитесь, что все узлы присутствуют в словаре in-degree.
        for neighbor in neighbors:
            adj_list[neighbor].append(node)
            in_degree[node] += 1

    # Initialize queue with nodes having in-degree of 0
    # Инициализируем очередь узлами с внутренней степенью 0
    queue = [node for node in graph if in_degree[node] == 0]

    # Initialize sorted list
    # Инициализация отсортированного списка
    result = []

    # Perform topological sorting
    # Выполните топологическую сортировку
    while queue:
        node = queue.pop(0)
        result.append(node)
        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Return the sorted nodes
    # Верните отсортированные узлы
    return result
