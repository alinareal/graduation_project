from collections import OrderedDict

from config import (HEADER_ID, TRANS_ID, TRAILER_ID)


class Header(object):
    __slots__ = ('header_id', 'name', 'surname', 'patronymic', 'address')

    def __init__(self):
        self.header_id = HEADER_ID
        self.name = self.surname = self.patronymic = self.address = ''


class Transaction(object):
    __slots__ = ('trans_id', 'trans_counter', 'trans_sum', 'currency_code', 'trans_filler')

    def __init__(self):
        self.trans_id = TRANS_ID
        self.trans_counter = self.trans_sum = self.currency_code = self.trans_filler = ''


class Trailer(object):
    __slots__ = ('trailer_id', 'trailer_trans_number', 'trailer_trans_amount', 'trailer_filler')

    def __init__(self):
        self.trailer_id = TRAILER_ID
        self.trailer_trans_number = self.trailer_trans_amount = self.trailer_filler = ''


class GeneralInformation:
    __slots__ = ('header', 'trailer', 'transactions')

    def __init__(self):
        self.header = Header()
        self.trailer = Trailer()
        self.transactions = []

    def _prepare_header(self) -> OrderedDict:
        header_id, name, surname, patronymic, address = self.header.__slots__
        return OrderedDict(
            [
                (header_id, HEADER_ID),
                (name, self.header.name),
                (surname, self.header.surname),
                (patronymic, self.header.patronymic),
                (address, self.header.address),
            ]
        )

    def _prepare_trailer(self) -> OrderedDict:
        trailer_id, trailer_trans_number, trailer_trans_amount = self.trailer.__slots__[:-1]
        return OrderedDict(
            [
                (trailer_id, TRAILER_ID),
                (trailer_trans_number, self.trailer.trailer_trans_number),
                (trailer_trans_amount, str(self.trailer.trailer_trans_amount)),
            ]
        )

    def _fill_transactions(self, transaction) -> OrderedDict:
        trans_id, trans_counter, trans_sum, currency_code = Transaction.__slots__[:-1]
        return OrderedDict(
                [
                    (trans_id, TRANS_ID),
                    (trans_counter, transaction.trans_counter),
                    (trans_sum, str(transaction.trans_sum)),
                    (currency_code, transaction.currency_code)
                ]
            )

    def convert_to_dict(self) -> OrderedDict:
        header, trailer, transactions = self.__slots__

        header_data = self._prepare_header()
        trailer_data = self._prepare_trailer()

        json_data = OrderedDict(
            [
                (header, header_data),
                (transactions, []),
                (trailer, trailer_data)
            ]
        )

        for transaction in self.transactions:
            trans_data = self._fill_transactions(transaction)
            json_data[transactions].append(trans_data)
        return json_data
