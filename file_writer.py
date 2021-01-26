from decimal import Decimal, InvalidOperation

import config as conf
from data_defaults import (HEADER_DEF, TRANS_DEF, TRAILER_DEF)


class FileWriter(object):
    def __init__(self):
        self.trans_number = 0
        self.total_amount = Decimal()
        self.trans_list = []
        self.header_def_copy = HEADER_DEF.copy()
        self.trans_def_copy = TRANS_DEF.copy()

    def create_file(self):
        """
        Creates file and writes there header, transactions and trailer

        :return: None
        """
        with open(conf.INFILE_NAME, 'w') as infile_name:
            header_line = self._create_header()
            self._check_requirements(header_line)
            infile_name.write(header_line)
            trans_list = self._create_trans()
            for trans in trans_list:
                self._check_requirements(trans_list)
                infile_name.write(trans)
            infile_name.write(self._create_trailer())

    def set_header(self, key, value):
        if key not in conf.ALLOWED_FIELDS_TO_SET:
            raise ValueError('This field is not allowed to set!')
        self.header_def_copy[key] = value

    def _create_header(self):
        """
        Creates a header string from header fields

        :return: ''.join(header_values_list) (str)
        """
        header_values_list = [self.header_def_copy['header_id'].rjust(conf.ID.MAX_LEN),
                              self.header_def_copy['name'].rjust(conf.NAME.MAX_LEN),
                              self.header_def_copy['surname'].rjust(conf.SURNAME.MAX_LEN),
                              self.header_def_copy['patronymic'].rjust(conf.PATRONYMIC.MAX_LEN),
                              self.header_def_copy['address'].rjust(conf.ADDRESS.MAX_LEN),
                              conf.LINE_ENDING
                              ]
        header_str = ''.join(header_values_list)
        return header_str

    def set_trans(self, key, value):
        if key not in conf.ALLOWED_FIELDS_TO_SET:
            raise ValueError('This field is not allowed to set!')
        try:
            self.trans_list[-1][key] = value
        except IndexError:
            raise ValueError('First add transaction, then set values.')

    def _create_trans(self):
        """
        Creates a transaction string from transaction fields

        :return: ''.join(trans_values_list) (str)
        """
        trans_list = []
        for transactionDict in self.trans_list:
            self._process_amount(transactionDict)
            trans_values_list = [transactionDict['trans_id'].rjust(conf.ID.MAX_LEN),
                                 str(transactionDict['trans_counter']).rjust(conf.TRANS_COUNTER.MAX_LEN, '0'),
                                 transactionDict['trans_sum'].rjust(conf.TRANS_SUM.MAX_LEN),
                                 transactionDict['currency_code'].rjust(conf.CURRENCY_CODE.MAX_LEN),
                                 transactionDict['trans_filler'].rjust(conf.TRANS_FILLER.MAX_LEN),
                                 conf.LINE_ENDING
                                 ]
            trans_list.append(''.join(trans_values_list))
        return trans_list

    def _create_trailer(self):
        """
        Creates a trailer string from trailer fields

        :return: ''.join(trailer_values_list) (str)
        """
        trailer_values_list = [TRAILER_DEF['trailer_id'].rjust(conf.ID.MAX_LEN),
                               str(self.trans_number).rjust(conf.TRAILER_TRANS_NUMBER.MAX_LEN, '0'),
                               self._format_total_amount(),
                               TRAILER_DEF['trailer_filler'].rjust(conf.TRAILER_FILLER.MAX_LEN),
                               conf.LINE_ENDING
                               ]
        return ''.join(trailer_values_list)

    def _format_total_amount(self):  # +
        """
        Brings total_amount to the appropriate view

        :return: final_amount (str)
        """
        max_len = conf.TRAILER_TRANS_AMOUNT.MAX_LEN
        total_amount = self.total_amount.quantize(Decimal('1.00'))
        amount_without_dot = str(total_amount).replace('.', '')
        final_amount = amount_without_dot.rjust(max_len, '0')
        return final_amount

    def add_trans(self):
        """
        Adds the transaction to the list with transactions

        :return: None
        """
        self.trans_number += 1
        trans_def_copy = TRANS_DEF.copy()
        trans_def_copy['trans_counter'] = self.trans_number
        self.trans_list.append(trans_def_copy)

    @staticmethod
    def _check_requirements(line):  # +
        if len(line) > 121:
            raise ValueError('The length of your string is more than allowed!!')

    def _process_amount(self, trans_dict):  # +
        try:
            self.total_amount += Decimal(trans_dict['trans_sum']) / Decimal('100')
        except InvalidOperation:
            raise TypeError('Enter only numbers!')


write_obj = FileWriter()

write_obj.set_header('name', 'Andrei')

write_obj.set_header('surname', 'Vasilevskiy')
write_obj.set_header('patronymic', 'Ignatovich')
write_obj.set_header('address', 'Ostrovskogo6/18MozyrBelarus')

write_obj.add_trans()
write_obj.set_trans('trans_sum', '000000005500')
write_obj.set_trans('currency_code', '978')

write_obj.add_trans()
write_obj.set_trans('currency_code', '978')

write_obj.add_trans()
write_obj.set_trans('trans_sum', '000000005500')

write_obj.add_trans()

write_obj.add_trans()
write_obj.set_trans('currency_code', '974')

write_obj.add_trans()
write_obj.add_trans()
write_obj.add_trans()
write_obj.add_trans()
write_obj.add_trans()
write_obj.add_trans()
write_obj.add_trans()
write_obj.add_trans()

write_obj.create_file()
