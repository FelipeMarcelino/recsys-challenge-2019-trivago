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
    """ This class is reponsible to make transformations in dataset.
        keyword arguments:
        train_path_file -- The file path of training data
        metadata_path_file -- Tje file path of metadata
        train -- Is a panda object that already contain the data loaded
        metadata -- Is a panda object that already contain the metadada loaded
        keys -- Is the primary key(index) of each row. Can be a list if a dataframe is multiindex

        ** Is not necessary to pass all parameters. You can pass train or metada object or the file paths

    """
    def __init__(self,train_path_file=None, metadata_path_file=None, interim_path_folder=None, train=None, metadata=None, keys=None):
        self.__train_path_file = train_path_file
        self.__metadata_path_file = metadata_path_file
        self.__categorical_map = dict()
        self.__keys_dataframe = keys
        self.__interim_path_folder = interim_path_folder

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

    def __save_transformation(self,columns, transformation):
        if  self.__keys_dataframe is not None:
            keys = self.__keys_dataframe + columns
            partial_dataframe = self.__train[keys]
            if self.__interim_path_folder is not None:
                logger.info("Saving transformation in %s",self.__interim_path_folder)
                name =  transformation + "_"
                name += "_".join(columns)
                path = self.__interim_path_folder + name
                path += ".csv"
                partial_dataframe.to_csv(path)
            else:
                logger.info("self.__interim_path_folder is None, so can't save transformation")

        else:
            logger.info("self.__keys_dataframe is None, so can't save transformation")

    def set_keys_dataframe(self, keys):
        self.__keys_dataframe = keys

    def set_interim_path_folder(self, interim_path_folder):
        self.__interim_path_folder = interim_path_folder

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
            ##self.__save_transformation([column], "categorical_to_discret")
        except AssertionError as error:
            logger.exception(error)
        except Exception as exception:
            logger.exception(exception)

    def transform_categorical_to_one_host_encoding(column):
        pass

    def groupby(self, columns_index):
        logger.info("Grouping dataframe using %s column(s)",columns_index)
        self.__train = self.__train.groupby(columns_index)

    def split_column_elements_and_count(self, column, delimit):
        logger.info("Transformando os elementos da coluna %s em uma lista através do split %s",column,delimit)
        self.__train[column] = self.__train[column].str.split(delimit)
        column_count = column + "_count"
        self.__train[column_count] = self.__train[column].apply(lambda x:  len(x) if isinstance(x,list) else 0) #pylint:disable=unnecessary-lambda
        #self._DataTransform__save_transformation([column,column_count], "split_column_count")
