import logging
import pandas as pd
import sys

# Logger
logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler() # Log que será mostrado na tela
f_handler = logging.FileHandler('/tmp/recsys') # Log no arquivo, contendo os erros
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.setLevel(logging.DEBUG)

class DataTransform():
    def __init__(self,train_path_file=None, metadata_path_file=None, train=None, metadata=None):
        self.__train_path_file = train_path_file
        self.__metadata_path_file = metadata_path_file
        self.__categorical_map = dict()

        if(train_path_file is not None and metadata_path_file is not None):
            try:
                logger.info("Arquivo que será carregado: %s",train_path_file)
                logger.info("Arquivo que será carregado: %s",metadata_path_file)
                self.__load_train_data() # Função para carregar os dados de treino
                self.__load_metadata() # Função para carregar os metadados
                logger.info("Arquivos carregados!")
            except FileNotFoundError as error:
                logger.exception(error)
        elif(train is not None and metadata is not None):
            self.__train = train
            self.__metadata = metadata
        else:
            logger.error("O path dos arquivos e nem o objeto de dados foi passado como argumentos. Programa\
                        irá finalizar")
            sys.exit(1)

    def __load_train_data(self):
        self.__train = pd.read_csv(self.__train_path_file,sep=",")

    def __load_metadata(self):
        self.__metadata = pd.read_csv(self.__metadata_path_file,sep=",")

    def transform_categorical_to_discret(self, column):
        try:
            assert self.__train[column].dtype == 'object'
            string_values = self.__train[column].unique()
            count = 0
            for value in string_values:
                if value in self.__categorical_map:
                    logger.info("Value categórico \"%s\" já está presente no dicinário, logo será mantido o valor:\
                                %s",value,self.__categorical_map[value])
                else:
                    logger.debug("Valor categórico \"%s\" passou a ter o valor %s: ",value,count)
                    self.__categorical_map[value] = count
                    count =  count + 1

            self.__train[column] = self.__train[column].map(self.__categorical_map)
        except AssertionError as error:
            logger.exception(error)
        except Exception as exception:
            logger.exception(exception)

    def transform_categorical_to_one_host_encoding(column):
        pass
