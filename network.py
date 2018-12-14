from api import get_friends
import time
import igraph
import config

def get_network(user_id: int, as_edgelist) -> list:
    gf = get_friends(user_id)['response']['count']
    users_id = get_friends(user_id)['response']['items']
    edges = []
    matrix = [[0] * gf for i in range(gf)]

    for user1 in range(gf):
        friends = get_friends(users_id[user1])['response']['items']
        for user2 in range(user1 + 1, gf):
            if users_id[user2] in friends:
                if as_edgelist:
                    edges.append((user1, user2))
                else:
                    matrix[user1][user2] = 1
                    matrix[user2][user1] = 1
        time.sleep(0.4)

    if as_edgelist:
        return edges
    return matrix


def plot_graph(user_id: int) -> None:
    surnames = get_friends(user_id, 'last_name')['response']['items']
    vertices = [i['last_name'] for i in surnames]
    edges = get_network(user_id, True)

    graphic = igraph.Graph(vertex_attrs={"shape": "circle",
                                   "label": vertices,
                                   "size": 10},
                     edges=edges, directed=False)

    n = len(vertices)
    visual_style = {
        "vertex_label_dist": 1.6,
        "vertex_size": 20,
        "edge_color": "gray",
        "margin": 75,
        "autocurve": True,
        "layout": graphic.layout_fruchterman_reingold(
            maxiter=100000,
            area = n ** 2,
            repulserad = n ** 2)
    }
    graphic.simplify(multiple=True, loops=True)
    clusters = graphic.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    graphic.vs['color'] = pal.get_many(clusters.membership)
    igraph.plot(graphic, **visual_style)

if __name__ == '__main__':
	user_id = config.VK_CONFIG['user_id']
	plot_graph(user_id)
