def parse_java_code(filepath):
    with open(filepath, "r") as f:
        code = f.read()

    # simple logic to simulate parsing Java code
    code = code.replace("if(", "IF (")
    code = code.replace("else", "ELSE")
    code = code.replace("{", "")
    code = code.replace("}", "END_IF;")
    code = code.replace("==", "=")
    code = code.replace(";", "")

    return code
