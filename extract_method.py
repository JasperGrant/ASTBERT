import json
import os
import javalang


# source:https://stackoverflow.com/questions/49603495/java-regular-expression-to-match-any-method-signature
def extract_method_from_folder(directory_path):
    # print(directory_path)
    if os.path.isfile(directory_path):
        if directory_path.endswith(".java"):
            print(directory_path)
            extract_method_from_file(directory_path)
            return
    for filename in os.listdir(directory_path):
        # print(filename)
        full_path = os.path.join(directory_path, filename)
        if os.path.isdir(full_path):
            try:
             extract_method_from_folder(full_path)
            except:
                print(f"Error in the folder {full_path}")
        if filename.endswith(".java"):
            print(full_path)
            extract_method_from_file(full_path)


# source:https://github.com/c2nes/javalang/issues/49
# source:https://www.geeksforgeeks.org/append-to-json-file-using-python/
def extract_method_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            class_code = file.read()
            ast_tree = javalang.parse.parse(class_code)
            print("parse successfully")
            methods = {}
            for _, node in ast_tree.filter(javalang.tree.MethodDeclaration):
                start, end = __get_start_end_for_node(node, ast_tree)
                body = __get_string(node.position, end, class_code).strip()
                index = body.find('{')
                last_index = body.rfind('}')
                new_body = body[index + 1:last_index]
                methods[node.name] = new_body
                # start, end = __get_start_end_for_node(node, ast_tree)
                # methods[node.name] = __get_string(start, end, class_code)
            # print(methods)
    except javalang.parser.JavaSyntaxError as e:
        print(f"Syntax error in the file parsing : {e}")
        return
    except Exception as e:
        print(f"Unexpected error in the file parsing : {e}")
        return
    if os.path.exists("data/methods.json") is False:
        with open("data/methods.json", "x") as file:
            json.dump(methods, file, indent=4)
            return
    with open("data/methods.json", 'r', encoding='utf-8') as file:
        file_data = json.load(file)
        file_data.update(methods)
    with open("data/methods.json", 'w', encoding='utf-8') as file:
        json.dump(file_data, file, indent=4)


def __get_start_end_for_node(node_to_find, tree):
    start = None
    end = None
    for path, node in tree:
        if start is not None and node_to_find not in path:
            end = node.position
            return start, end
        if start is None and node == node_to_find:
            start = node.position
    return start, end


def __get_string(start, end, data):
    if start is None:
        return ""

    # positions are all offset by 1. e.g. first line -> lines[0], start.line = 1
    end_pos = None

    if end is not None:
        end_pos = end.line - 1

    lines = data.splitlines(True)
    string = "".join(lines[start.line:end_pos])
    string = lines[start.line - 1] + string

    # When the method is the last one, it will contain a additional brace
    if end is None:
        left = string.count("{")
        right = string.count("}")
        if right - left == 1:
            p = string.rfind("}")
            string = string[:p]

    return string
