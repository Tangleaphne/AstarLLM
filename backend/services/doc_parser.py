# backend/services/doc_parser.py
import re


def extract_facts_from_doc(doc_text: str):
    lines = doc_text.splitlines()
    facts = []
    for line in lines:
        if "@param" in line:
            match = re.findall(r"@param\s+(\w+)", line)
            if match:
                facts.append({"param": match[0], "source": line.strip()})
        elif "Requirements:" in line:
            facts.append({"requirement": line.strip()})
        elif "Emits" in line:
            facts.append({"event": line.strip()})
    return facts
