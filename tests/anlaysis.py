"""

这是模块的文档字符串

"""

import ast


def get_classes_methods_and_module_doc(filename):
    with open(filename, "r", encoding="utf-8") as file:
        node = ast.parse(file.read(), filename=filename)

    module_docstring = ast.get_docstring(node)  # 获取模块的文档字符串
    classes_info = {}

    # 遍历 AST 节点
    for n in node.body:
        if isinstance(n, ast.ClassDef):
            class_name = n.name
            class_docstring = ast.get_docstring(n)
            methods_info = {}

            for item in n.body:
                if isinstance(item, ast.FunctionDef):
                    method_name = item.name
                    method_docstring = ast.get_docstring(item)
                    methods_info[method_name] = method_docstring

            classes_info[class_name] = {
                "docstring": class_docstring,
                "methods": methods_info,
            }

    return {"module_docstring": module_docstring, "classes": classes_info}


# 使用示例
if __name__ == "__main__":
    result = get_classes_methods_and_module_doc("example.py")

    if result["module_docstring"]:
        print(f"Module Docstring: {result['module_docstring']}")

    for class_name, info in result["classes"].items():
        print(f"Class: {class_name}")
        print(f"  Docstring: {info['docstring']}")
        for method_name, method_doc in info["methods"].items():
            print(f"  Method: {method_name}")
            print(f"    Docstring: {method_doc}")
