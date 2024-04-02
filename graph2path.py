import json
import os.path


def graph2path(graph_data_path, mode="paths", output_file_path="data/paths.json"):
    if not os.path.isdir(graph_data_path):
        print("The path is not a directory")
        return
    i = 0
    number_of_files = len(os.listdir(graph_data_path))
    for filename in os.listdir(graph_data_path):
        #print(i,"/",number_of_files)
        if filename.endswith(".json"):
            try:
                build_tree_graph(os.path.join(graph_data_path, filename), mode)
                print("Processed file: " + filename) if (filename != "tmp_AST_output.json") else None
            except Exception as e:
                print(e)
                print("Error in processing file: " + filename)
                continue
        i += 1

def build_tree_graph(graph_data_file_path, mode, output_file_path="data/paths.json"):
    if not os.path.isfile(graph_data_file_path):
        print("The path is not a file")
        return
    method_name = graph_data_file_path.split("_")[0].split("\\")[1]
    head_node_id = -1
    with open(graph_data_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        raw_nodes = data["nodes"]
        raw_links = data["links"]
        nodes = dict()
        links = dict()
        for node in raw_nodes:
            if node["node_type"] == "program":
                head_node_id = node["id"]
            nodes[node["id"]] = node["label"]
        for link in raw_links:
            if link["source"] not in links:
                links[link["source"]] = [link["target"]]
            else:
                links[link["source"]].append(link["target"])
        # print(nodes)
        # print(links)
        # print(head_node_id)
        # print(method_name)
        paths = []
        method_paths = {}
        if mode == "paths":
            traverse_graph_to_paths(nodes, links, head_node_id, paths, "")
        elif mode == "onePath":
            serialize_tree(nodes, links, head_node_id, paths, "")
        method_paths[method_name] = paths
        # print(paths)
        if os.path.exists(output_file_path) is False:
            with open(output_file_path, "x") as f:
                json.dump(method_paths, f, indent=4)
                return
        with open(output_file_path, "r", encoding="utf-8") as f:
            file_data = json.load(f)
            file_data.update(method_paths)
        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(file_data, f, indent=4)


# source:https://leetcode.com/problems/binary-tree-paths/editorial/
def traverse_graph_to_paths(nodes, links, head_node_id, paths, path):
    path += str(nodes[head_node_id])
    if head_node_id not in links:  # if reach a leaf
        paths.append(path)  # update paths
    else:
        path += " -> "  # extend the current path
        for next_id in links[head_node_id]:
            traverse_graph_to_paths(nodes, links, next_id, paths, path)


def serialize_tree(nodes, links, head_node_id, paths, path):
    path = serialize_tree_recur(nodes, links, head_node_id, "")
    paths.append(path)


def serialize_tree_recur(nodes, links, head_node_id, path):
    path += str(nodes[head_node_id])
    path += " "
    if head_node_id in links:
        path += "("
        for next_id in links[head_node_id]:
            path = serialize_tree_recur(nodes, links, next_id, path)
        path += ")"
    return path
