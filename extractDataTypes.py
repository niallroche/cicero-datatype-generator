"""
A utility class to assist with extraction of data types from cicero contracts
to produce variables and (candidate) data types to assist with creating concerto files

## Usage
extractDataTypes.py pathToInputCiceroFile.md --outputfile optionalPathToOuputConcertoFile.cto
"""

import re
import os.path
import argparse

"""
:returns a text String from a text or md file input
"""


def loadContractText(file_location):
    # check file type
    print("File exists:" + str(os.path.exists(file_location)))

    assert os.path.exists(file_location)
    assert os.path.isfile(file_location)
    extension = os.path.splitext(file_location)[1]
    print("ext part of '% s':" % file_location, extension)

    assert extension == '.txt' or extension == '.md'

    file = open(file_location)

    contents = file.read()
    file.close()
    return contents


"""
:returns a dictionary of terms prepended with approximate data types, or default to String
"""


def extractContractDataTypes(input_text):
    terms = {}
    imports = []
    p = re.compile(r'{{(\w+)}}')
    iterator = p.finditer(input_text)
    for match in iterator:
        print(match.span())
        print(match.group())
        # key = input_text[match.span()[0], match.span()[1]]
        key = match.group()[2:len(match.group()) - 2]
        val, potential_imports = matchDataType(key)
        terms[key] = val
        if potential_imports:
            imports.append(potential_imports)
    # tokenise inputText and extract {{}}
    return terms, set(imports)


def matchDataType(variable_name):
    returned_type = 'String'
    imports = ''

    variable_name = variable_name.lower()

    # check for specific types like currency after generics like integer

    test_bool_list = ['bool', 'boolean', 'true', 'false', 'exists', 'is', 'flag', 'yesno', 'does']
    res = [ele for ele in test_bool_list if (ele in variable_name)]
    if len(res):
        returned_type = "Boolean"

    test_double_list = ['num', 'min', 'max', 'number']
    res = [ele for ele in test_double_list if (ele in variable_name)]
    if len(res):
        returned_type = "Double"

    test_int_list = ['count']
    res = [ele for ele in test_int_list if (ele in variable_name)]
    if len(res):
        returned_type = "Integer"

    test_currency_list = ['currency', 'usd', 'dollar', 'value', 'money']
    res = [ele for ele in test_currency_list if (ele in variable_name)]
    if len(res):
        returned_type = "Currency"

    test_monetary_list = ['value', 'amount', 'sum']
    res = [ele for ele in test_monetary_list if (ele in variable_name)]
    if len(res):
        returned_type = "MonetaryAmount"

    test_date_list = ['date', 'datetime']
    res = [ele for ele in test_date_list if (ele in variable_name)]
    if len(res):
        returned_type = "DateTime"

    test_duration_list = ['dur', 'duration', 'time', 'day', 'month', 'second', 'minute', 'week', 'quarter']
    res = [ele for ele in test_duration_list if (ele in variable_name)]
    if len(res):
        returned_type = "Duration"
        imports = 'import org.accordproject.time.* from https://models.accordproject.org/time@0.2.0.cto'

    test_party_list = ['party', 'buyer', 'seller', 'insured', 'insurer']
    res = [ele for ele in test_party_list if (ele in variable_name)]
    if len(res):
        returned_type = "AccordParty"

    test_add_list = ['address', 'postaladdress', 'location']
    res = [ele for ele in test_add_list if (ele in variable_name)]
    if len(res):
        returned_type = "PostalAddress"
        imports = 'import org.accordproject.address.PostalAddress from https://models.accordproject.org/address.cto'

    # other fields to check -
    return returned_type, imports


"""
:returns a formatted output data types
"""


def formatContractDataTypes(terms, imports):
    formatted_terms = ""
    for imported_lib in imports:
        formatted_terms = formatted_terms + imported_lib + '\n'

    formatted_terms = formatted_terms + '\n'

    for term, datatype in terms.items():
        formatted_terms = formatted_terms + '  o ' + datatype + " " + term + "\n"
    return formatted_terms


def main():
    parser = argparse.ArgumentParser(description='Process some cicero file and extract the variables in the text.')
    # parser.add_argument('input_filename', type=open,
    parser.add_argument('input_filename', type=argparse.FileType('r'),
                        help='a full or relative path to a valid cicero file in txt or markdown format')

    parser.add_argument('--outputfile', type=argparse.FileType('w'), nargs=1,
                        help='a full or relative path to a valid output file')

    args = parser.parse_args()
    # print(args.accumulate(args.filename))
    print(args.input_filename)
    print(args.input_filename.name)
    assert args.input_filename

    file_content = loadContractText(args.input_filename.name)
    assert len(file_content)

    terms, imports = extractContractDataTypes(file_content)
    assert len(terms)

    formatted_terms = formatContractDataTypes(terms, imports)
    assert len(formatted_terms)

    print(formatted_terms)

    if args.outputfile:
        args.outputfile[0].name
        f = open(args.outputfile[0].name, "w+")
        f.write(formatted_terms)
        f.flush()
        f.close()


if __name__ == "__main__":
    main()
