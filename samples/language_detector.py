def detect_language(code):
    """
    Detects the programming language (Python, C, or Java)
    based on common syntax patterns.
    """
    code_lower = code.lower()

    if "def " in code_lower or "import " in code_lower:
        return "python"
    elif "#include" in code_lower or "printf(" in code_lower:
        return "c"
    elif "public static void main" in code_lower or "system.out.println" in code_lower:
        return "java"
    else:
        return "unknown"
