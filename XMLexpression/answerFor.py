
from lxml import etree

def well_formed(source):  
    try:
        etree.parse(source)
        return True 
    except etree.XMLSyntaxError:
        return False 
    '''This function takes a filepath to a well-formed XML file
    and  the other to a RELAXNG schema in XML syntax. This function returns
    True if  the XML file is well-formed and False otherwise.'''
    
def valid(source, schema):
    '''This function takes two filepaths, one to a *well-formed* XML file
    and  the other to a RELAXNG schema in XML syntax. This function returns
    True if  the XML file is valid wrt the schema and False otherwise.'''
    with open(schema, 'r') as schema_file:
        rng_doc = etree.parse(schema_file)
        relaxng = etree.RelaxNG(rng_doc)

    with open(source, 'r') as xml_file:
        doc = etree.parse(xml_file)

    if relaxng.validate(doc):
        return True
    else:
        return False

def evaluate(source):
    try:
        tree = etree.parse(source)
        root = tree.getroot()
        result = compute_expression(root[0])
        return round(result, 2)
    except Exception as e:
        return str(e)

def compute_expression(element):
    if element.tag =="int":
        return int(element.get("value"))
    elif element.tag == "plus":
        return sum(compute_expression(child) for child in element)
    elif element.tag == "minus":
        operands = [compute_expression(child) for child in element]
        return operands[0]-sum(operands[1:])
    elif element.tag == "times":
        operands = [compute_expression(child) for child in element]
        result = 1
        for operand in operands:
            result*= operand
        return result
    else:
        raise ValueError(f"Unsopported operation:{element.tag}")
    


def check_then_evaluate(source, schema):
    if not well_formed(source): 
        return 'Not well formed'     
    if not valid(source, schema):
        return 'Not valid' 
    # This will only return if you pass both tests
    return evaluate(source)


if __name__ == '__main__':
    # Importing here is not standard, but convenient for this assignment.
    import argparse
    parser = argparse.ArgumentParser(description='Check a calc format file for validatity and evaluated it if it is valid.')
    parser.add_argument('source', type=str, default='example.xml', nargs='?',
                    help='the name of the xml file with the arithmetic expression')
    parser.add_argument('--schema', '-s', type=str,
                    help='the name of RELAXNG scheme (in XML syntax)')

    args = parser.parse_args()

    print(check_then_evaluate(args.source, args.schema))
