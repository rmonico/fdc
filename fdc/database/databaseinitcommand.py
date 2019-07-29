from di_container.injector import Inject, di_container

import os


class FDCInitCommand(object):

    def __init__(self):
        self._configs = Inject('app configuration')
        self._git = Inject('fdc git wrapper')
        self._logger = Inject('logger')

    def database_parser_created_handler(self, db_parser):
        db_parser.add_parser(
            "init",
            help="Inicializa a pasta do FDC e o banco de dados com uma estrutura vazia. Se houver um banco de dados já "
                 "existente o mesmo será excluído e reiniciado.").set_defaults(event='database_init_command')

    def database_init_command_handler(self, args):
        # TODO Verificar se o arquivo de banco de dados é um SQLITE válido!

        self._ensure_fdc_folder_exists()

        self._ensure_fdc_folder_is_git_repository()

        self._ensure_database_structure_with_no_data()

        return 'ok'

    def _ensure_fdc_folder_exists(self):
        if not os.path.isdir(self._configs['fdc.folder']):
            self._logger.info('Creating fdc folder at "{}"', self._configs['fdc.folder'])
            os.makedirs(self._configs['fdc.folder'], exist_ok=True)
        else:
            self._logger.info('fdc folder found at "{}"', self._configs['fdc.folder'])

    def _ensure_fdc_folder_is_git_repository(self):
        if not self._git.is_repository():
            self._logger.info('Git repository not found at fdc folder, creating it...')
            if not self._git.init():
                raise FDCInitializationException('Error initializing git repository at "{}"',
                                                 self._git.repository_folder)

    def _ensure_database_structure_with_no_data(self):
        if os.path.isfile(self._configs['fdc.db_full_path']):
            self._logger.warn('Database file "{}" found, removing it...', self._configs['fdc.db_full_path'])
            os.remove(self._configs['fdc.db_full_path'])

        connection = di_container.get_resource('database connection')

        # TODO Create these tables via controller events to centralize table handling in specialized classes
        self._logger.debug('Creating table "conta"...')
        connection.executescript(
            "create table conta (nome text not null, contabilizavel boolean not null, fechamento date);")

        # FIXME Dont store currency values as float
        self._logger.debug('Creating table "contrato"...')
        connection.executescript(
            "create table contrato (compra date not null, conta, total_parcelas integer, valor_parcela float, observacao text, foreign key(conta) references conta);")

        self._logger.debug('Creating table "lancamento"...')
        connection.executescript(
            "create table lancamento (debito date not null, compra date, valor float, valor_local float not null, origem, destino, parcela integer not null, observacao text not null, foreign key(origem) references conta, foreign key(destino) references conta);")

        # TODO Handle errors

    def database_init_command_ok_handler(self):
        print('Structure created successfully')


class FDCInitializationException(Exception):
    pass
