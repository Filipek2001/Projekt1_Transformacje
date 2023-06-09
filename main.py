import argparse
from transformacje_wsp import Transformator

def set_parser():
    desc = """
    The program allows the user to convert coordinates. It supports the following transformations:
    XYZ -> BLH,
    BLH -> XYZ,
    XYZ -> NEUp,
    BL(choosen model) -> XY2000,
    BL(choosen model) -> XY1992,
    XYZ -> XY2000,
    XYZ -> XY1992
    Please put choosen formats in entry_format and out_format
    """
    parser = argparse.ArgumentParser(description=desc)
    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument('--model', help="choose elipsoid model(only grs80, wgs84)", required=True)
    requiredNamed.add_argument('-e', '--entry_format', help="format of data You enter(XYZ, BLH, BL)", required=True)      # option that takes a value
    requiredNamed.add_argument('-o', '--out_format', help="format of out data(XYZ, BLH, NEUp, XY2000, XY1992)", required=True)
    files_arguments = parser.add_argument_group("file write/read options")
    files_arguments.add_argument("-f", "--input_filename", help="path to data file")
    files_arguments.add_argument("-n", "--out_filename", help="path to file You want to save data in")
    parser.add_argument("-x", help="first argument")
    parser.add_argument("-y", help="second argument")
    parser.add_argument("-z", help="third argument(optional in conversion from BL)")
    parser.add_argument("-r", help="BL/BLH in radians", action='store_true')
    NEUpArguments = parser.add_argument_group("NEUp arguments")
    NEUpArguments.add_argument("-a", help="phi argument")
    NEUpArguments.add_argument("-b", help="lam argument")
    NEUpArguments.add_argument("-c", help="h argument")
    args = parser.parse_args()
    return args

def check_given_arguments(args, transformator: Transformator):
    entry_formates = ["XYZ", "BLH", "BL"]
    entry_format = args.entry_format
    if entry_format not in entry_formates: raise ValueError("Bledny format wejsciowy")

    out_formates = ["BLH", "XYZ", "NEUp", "XY2000", "XY1992"]
    out_format = args.out_format
    if out_format not in out_formates: raise ValueError("Bledny format wyjsciowy")

    operations = list(transformator.method_dict.keys())
    operation_str = entry_format + out_format
    if operation_str not in operations: raise ValueError("Nieobslugiwana konwersja")

    models = ["wgs84", "grs80"]
    model = args.model
    if model not in models: raise ValueError("Podano bledny model")

    return True

def check_len(splited_line, entry_format:str, out_format):
    if entry_format == "BL":
        if len(splited_line) != 2:
            raise ValueError(str(splited_line))
    if entry_format in ["BLH", "XYZ"] and out_format != "NEUp":
        if len(splited_line) != 3:
            raise ValueError(str(splited_line))
    if out_format == "NEUp":
        if len(splited_line) != 6:
            raise ValueError(str(splited_line))

def convert_data_from_file(args, transformator: Transformator, entry_format: str, out_format: str):
    try:
        filename = args.input_filename
        operation_func = select_operation(entry_format, out_format, transformator)
        with open(filename, 'r') as f:
            output_lines = []
            lines = f.readlines()
            for line in lines:
                splited_line = line.split(',')
                check_len(splited_line, entry_format, out_format)
                splited_line[-1] = splited_line[-1].replace("\n", "")
                if entry_format == "BL":
                    if args.model != "grs80": raise ValueError("BL uses only grs80 model")
                    x, y = float(splited_line[0]), float(splited_line[1])
                    result = operation_func(x, y, 0, args.r)
                elif entry_format in ["XYZ", "BLH"]:
                    if out_format == "NEUp":
                        arguments = [float(splited_line[i]) for i in range(0, 6)]
                        result = operation_func(arguments)
                    else:
                        x, y, z = float(splited_line[0]), float(splited_line[1]), float(splited_line[2])
                        result = operation_func(x, y, z, args.r)
                output_lines.append(result)
            f.close()
            output_lines.reverse()
            return output_lines
    except:
        raise ValueError("Nie znaleziono podanego pliku albo zly format pliku")

def write_data_to_file(converted_data, arguments):
    out_file_name = arguments.out_filename
    with open(out_file_name, 'w') as file:
        for line in converted_data:
            comma = ','
            s = comma.join(map(str, line))
            file.write(s + "\n")
        file.close()

def select_operation(entry_format, out_format, trans=Transformator):
    operation = entry_format + out_format
    operation_func = trans.method_dict[operation]
    return operation_func

def convert_single_line(args, entry_format, out_format, trans=Transformator):
    try:
        if entry_format in ["XYZ", "BLH"]:
            x, y, z = float(args.x), float(args.y), float(args.z)
        elif entry_format == "BL":
            x, y, z = float(args.x), float(args.y), 0
        if entry_format in ["BLH", "BL"]:
            if x < 0 or y < 0: raise ValueError("phi or lam are negative")
    except:
        raise ValueError("Given argument are incorrect")
    operation_func = select_operation(entry_format, out_format, trans)
    if out_format == "NEUp":
        phi, lam, h = float(args.a), float(args.b), float(args.c)
        arguments = [x, y, z, phi, lam, h]
        result = operation_func(arguments)
    else:
        result = operation_func(x, y, z, args.r)
    return result


def main():
    transformator = Transformator()
    args = set_parser()
    check_given_arguments(args, transformator)
    model = args.model
    transformator.set_model(model)
    entry_format, out_format = args.entry_format, args.out_format
    if args.input_filename is not None:
        converted_data = convert_data_from_file(args, transformator, entry_format, out_format)
        write_data_to_file(converted_data, args)
        print(f"Converted data saved in {args.out_filename}")
    else:
        converted_data = convert_single_line(args, entry_format, out_format, transformator)
        print(f"Converted data from {entry_format} to {out_format}: {converted_data}")


if __name__ == "__main__":
    main()
