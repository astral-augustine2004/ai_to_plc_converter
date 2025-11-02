def convert_to_plc(logic_blocks):
    plc_lines = []

    for block in logic_blocks:
        if block["type"] == "if":
            plc_lines.append(f"IF {block['condition'].replace('==', '=')} THEN")
            for line in block["body"]:
                plc_lines.append(f"    {line}")
            if block["else"]:
                plc_lines.append("ELSE")
                for line in block["else"]:
                    plc_lines.append(f"    {line}")
            plc_lines.append("END_IF;")

        elif block["type"] == "for":
            plc_lines.append(f"FOR {block['target']} IN {block['iter']} DO")
            for line in block["body"]:
                plc_lines.append(f"    {line}")
            plc_lines.append("END_FOR;")

        elif block["type"] == "while":
            plc_lines.append(f"WHILE {block['condition']} DO")
            for line in block["body"]:
                plc_lines.append(f"    {line}")
            plc_lines.append("END_WHILE;")

    return "\n".join(plc_lines)
