import ast
from collections import defaultdict
import typing

class Node:
    def __init__(self, value: typing.Union[ast.Assign, ast.For], name: str, type: str):
        self.value = value
        self.name = name
        self.type = type


class Analysis:
    def __init__(self):
        self.found: typing.Dict[str, typing.List[Node]] = defaultdict(list)
        self.class_context = None
        self.context = None

    def analyze_nodes(self, nodes: typing.Union[typing.List[ast.AST], typing.Iterator[ast.AST]]):
        def is_self(x: ast.expr):
            return isinstance(x, ast.Attribute) and isinstance(x.value, ast.Name) and x.value.id

        for subnode in nodes:
            if isinstance(subnode, ast.Assign) and isinstance(subnode.value, ast.ListComp) and isinstance(
                    subnode.targets[0], (ast.Attribute, ast.Name)):
                if is_self(subnode.targets[0]):
                    self.found[self.class_context + f".{subnode.targets[0].value.id}.{subnode.targets[0].attr}"].append(
                        Node(subnode, f"{subnode.targets[0].value.id}.{subnode.targets[0].attr}", "list"))
                else:
                    self.found[self.context + "." + subnode.targets[0].id].append(
                        Node(subnode, subnode.targets[0].id, "list"))
            elif isinstance(subnode, ast.For) and hasattr(subnode, "iter"):
                if is_self(subnode.iter) and hasattr(subnode.iter, "attr"):
                    self.found[self.class_context + f".{subnode.iter.value.id}.{subnode.iter.attr}"].append(
                        Node(subnode, f"{subnode.iter.value.id}.{subnode.iter.attr}", "for"))
                elif hasattr(subnode.iter, "id"):
                    self.found[self.context + "." + subnode.iter.id].append(Node(subnode, subnode.iter.id, "for"))

    def analyze_function(self, node: ast.FunctionDef):
        self.context = self.class_context + "." + node.name if self.class_context else node.name
        self.analyze_nodes(ast.walk(node))

    def analyze_class(self, node: ast.ClassDef):
        self.class_context = node.name
        for subnode in ast.iter_child_nodes(node):
            if isinstance(subnode, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.analyze_function(subnode)
        self.class_context = None

    def analyze_tree(self, tree: ast.AST):
        outer_nodes = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                self.analyze_class(node)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.context = self.class_context = "-module"
                self.analyze_function(node)
            else:
                outer_nodes.append(node)
        if outer_nodes:
            self.context = self.class_context = "-module"
            self.analyze_nodes(outer_nodes)

    def find_unnecessary(self):
        unnecessary = {}
        for k, v in self.found.items():
            counter = 0
            for x in v:
                if x.type == "list":
                    counter += 1
                elif x.type == "for":
                    counter -= 1
            if counter == 0:
                unnecessary[k] = v
        return unnecessary

    def analyze_code(self, code: str):
        tree = ast.parse(code)
        self.analyze_tree(tree)
        return self.find_unnecessary()
