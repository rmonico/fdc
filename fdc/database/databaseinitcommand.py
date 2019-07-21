from di_container.injector import Inject, di_container


class DatabaseInitCommand(object):

    def __init__(self):
        self._configs = Inject('app configuration')

    def database_parser_created_handler(self, db_parser):
        db_parser.add_parser(
            "init", help="Inicializa o banco de dados em fdc.db").set_defaults(event='database_init_command')

    def database_init_command_handler(self, args):
        import os

        if os.path.exists(self._configs['db.path']):
            os.remove(self._configs['db.path'])

        connection = di_container.get_resource('database connection')

        # TODO Move this to ContaCommand class (may that class should be
        # renamed)
        connection.executescript(
            "create table conta (nome text not null, contabilizavel boolean not null, fechamento date);")

        # FIXME Não armazenar monetários como float
        connection.executescript(
            "create table contrato (compra date not null, conta, total_parcelas integer, valor_parcela float, observacao text, foreign key(conta) references conta);")

        connection.executescript(
            "create table lancamento (debito date not null, compra date, valor float, valor_local float not null, origem, destino, parcela integer not null, observacao text not null, foreign key(origem) references conta, foreign key(destino) references conta);")

        # TODO Commit and handle errors

        return 'ok'
