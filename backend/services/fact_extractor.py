# backend/services/fact_extractor.py
from slither.slither import Slither
from tempfile import NamedTemporaryFile


def extract_facts_from_solidity(code: str):
    with NamedTemporaryFile(suffix=".sol", delete=False, mode="w") as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    slither = Slither(tmp_path)
    facts = []
    for contract in slither.contracts:
        for function in contract.functions_declared:
            facts.append({
                "contract": contract.name,
                "function": function.name,
                "visibility": function.visibility,
                "modifiers": [m.name for m in function.modifiers],
            })
    return facts