import logging

logger = logging.getLogger('utilities_logger')

def get_value_ini(info, keyname):
        """
        Get the value associated with a specific keyname from the provided info.

        Parameters:
            info (list): List of tuples containing key-value pairs.
            keyname (str): The key to search for in the dictionaries within the tuples.

        Returns:
            The value associated with the specified keyname. Returns None if the key is not found.

        Exceptions:
            An exception is raised if an error occurs while searching for the keyname in the info list.
        """
        try:
            for tupla in info:
                if keyname in tupla[1]:
                    return tupla[1][keyname]
            return None
        except Exception:
            logger.exception("An error occurred when get key types of ini file.")
            raise
        
def get_car_number():
    car_number_txt = r'C:\CCAR_EOL_Project\settings\car.txt'
    try:
        with open(car_number_txt, 'r') as file:
            car_number = int(file.read())
            next_car_number = car_number + 1
            if next_car_number == 10000:
                next_car_number = 1

        with open(car_number_txt, 'w') as file:
            file.write(str(next_car_number))

        return car_number
    
    except FileNotFoundError:
        return None
    except ValueError:
        return None
