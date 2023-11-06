"""gets list of all functions in main.py and main_plot.py"""
from data import FlightData
import query_list as ql
import flight_data as main
import ioput as io


def get_main_functions_name():
    """gets list of all functions in main.py"""
    count = 1
    main_functions = {}
    function_names = [name for name in dir(main) if callable(getattr(main, name))]
    not_allowed_modules = ["datetime"]
    for name in function_names:
        if not any(name.startswith(prefix) for prefix in not_allowed_modules):
            main_functions[count] = name
            count += 1
    return main_functions


def user_menu():
    """prints menu for user"""
    opening_scene = "Main function list:"
    main_functions = get_main_functions_name()
    main_func_len = len(main_functions)

    name_map = map(
        lambda x: f"{x[0]}: {x[1].replace('_', ' ')}", main_functions.items()
    )
    main_functions_str = "\n".join(name_map)
    menu = f"""
    {opening_scene}
{main_functions_str}
{main_func_len + 1}: Exit\n"""
    while True:
        command = io.read_int_ranged(
            menu + "Please enter a number: ", 1, main_func_len + 1
        )
        if command == main_func_len + 1:
            break

        nesne = FlightData(ql.DATABASE_URI)
        func = main_functions[command]
        print(getattr(main, func)(nesne))


if __name__ == "__main__":
    user_menu()
