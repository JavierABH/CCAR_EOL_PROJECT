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