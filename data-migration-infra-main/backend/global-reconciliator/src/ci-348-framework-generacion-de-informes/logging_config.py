"""function that we use to write the login."""
import logging


def configure_logging():
    """Function Loggin."""
    logger = logging.getLogger()  
    logger.setLevel(logging.INFO) 

    if not logger.handlers:
        
        fh = logging.FileHandler("logs/proteccion.log")
        fh.setLevel(
            logging.INFO
        ) 

        
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y/%m/%d"
        )
        fh.setFormatter(formatter)

        logger.addHandler(fh)
