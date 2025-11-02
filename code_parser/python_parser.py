import ast

def parse_code(filepath):
    with open(filepath, "r") as f:
        code = f.read()

    tree = ast.parse(code)
    logic_blocks = []

    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            logic_blocks.append({
                "type": "if",
                "condition": ast.unparse(node.test),
                "body": [ast.unparse(stmt) for stmt in node.body],
                "else": [ast.unparse(stmt) for stmt in node.orelse]
            })
        elif isinstance(node, ast.For):
            logic_blocks.append({
                "type": "for",
                "target": ast.unparse(node.target),
                "iter": ast.unparse(node.iter),
                "body": [ast.unparse(stmt) for stmt in node.body]
            })
        elif isinstance(node, ast.While):
            logic_blocks.append({
                "type": "while",
                "condition": ast.unparse(node.test),
                "body": [ast.unparse(stmt) for stmt in node.body]
            })

    return logic_blocks
