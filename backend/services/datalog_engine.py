# backend/services/datalog_engine.py

def compare_facts(code_facts, doc_facts):
    """
    简单对比函数名是否一致（模拟更复杂的 Datalog 查询）
    """
    func_names = set(f["function"] for f in code_facts)
    doc_params = set(f.get("param") for f in doc_facts if f.get("param"))
    missing = doc_params - func_names
    return {"missing_functions_in_code": list(missing)}

