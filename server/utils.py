import pickle
import settings
import graph


def load_graph(path):
    with open(path, 'rb') as raw_data:
        graph = pickle.load(raw_data)

    return graph


# prepare_for_view: article,
# prepare_for_view_left_items: title
def strip_element(items, title, length):
    for item in items:
        if len(item[title]) < length:
            continue

        item[title] = item[title][:length] + "..."

    return items

