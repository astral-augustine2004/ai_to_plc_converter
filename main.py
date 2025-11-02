from code_parser.python_parser import parse_code
from ai_model.logic_converter import convert_to_plc
from language_detector import detect_language

def main():
    input_file = "samples/example1.py"  # change to example_c.c or example_java.java later

    # Read the input code
    with open(input_file, "r") as f:
        code = f.read()

    # 🔍 Step 1: Detect programming language
    lang = detect_language(code)
    print(f"🔹 Detected Language: {lang}")

    # 🔄 Step 2: Convert according to detected language
    if lang == "python":
        logic_blocks = parse_code(input_file)
        plc_output = convert_to_plc(logic_blocks)

    elif lang == "c":
        plc_output = (
            code.replace("if", "IF")
                .replace("else", "ELSE")
                .replace("{", "")
                .replace("}", "END_IF;")
                .replace("==", "=")
        )

    elif lang == "java":
        plc_output = (
            code.replace("if", "IF")
                .replace("else", "ELSE")
                .replace("{", "")
                .replace("}", "END_IF;")
                .replace("System.out.println", "PRINT")
        )

    else:
        plc_output = "⚠️ Unknown language pattern!"

    # 💾 Step 3: Save PLC output
    with open("samples/output_ai.st", "w") as f:
        f.write(plc_output)

    print("✅ AI Conversion Complete! Check 'samples/output_ai.st'")

if __name__ == "__main__":
    main()
