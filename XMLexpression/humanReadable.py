
from lxml import etree

def convert_to_readable(source):
    '''This takes a valid XML arithmetical expression and
    returns a "human readable" version. We count a string
    as human readable if is an executable Python arithmetic
    expression which is isomorphic to the XML and evaluates
    to the same answer'''
    xml_tree = etree.parse(source)
    
    def build_readable_expression(node):
        if node.tag == "plus":
            children = list(node)
            child_expr = "+".join(build_readable_expression(child) for child in children)
            return f"({child_expr})"
        elif node.tag == "times":
            children = list(node)
            child_expr = "*".join(build_readable_expression(child) for child in children)
            return f"({child_expr})"
        elif node.tag == "minus":
            children = list(node)
            if len(children) == 2:
                child_expr = f"({build_readable_expression(children[0])}-{build_readable_expression(children[1])})"
                return child_expr
            else:
                raise ValueError("Minus operation should have exactly two children")
        elif node.tag == "int":
            return node.get("value")
        
        # Handle unsupported elements
        children_results = [build_readable_expression(child) for child in node]
        if None in children_results:
            return ""  # Return an empty string if any child result is None
        return f"{'+'.join(children_results)}"
   
    expression = build_readable_expression(xml_tree.getroot())

    # Remove the first brackets
    if expression.startswith("(") and expression.endswith(")"):
        expression = expression[1:-1]

    return expression




if __name__ == '__main__':
    # Importing here is not standard, but convenient for this assignment.
    import argparse
    parser = argparse.ArgumentParser(description='Translate a valid XML expression into normal Python arithmetic')
    parser.add_argument('source', type=str, default='example.xml', nargs='?',
                    help='the name of the xml file with the arithmetic expression')

    args = parser.parse_args()

    print(convert_to_readable(args.source))
