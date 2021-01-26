from collections import OrderedDict

HEADER_DEF = OrderedDict([('header_id', '01'),
                          ('name', 'Ivan'),
                          ('surname', 'Ivanov'),
                          ('patronymic', 'Ivanovich'),
                          ('address', 'Sovetskaya9/23MinskBelarus')])

TRANS_DEF = OrderedDict([('trans_id', '02'),
                         ('trans_counter', '000001'),
                         ('trans_sum', '000000002000'),
                         ('currency_code', '974'),
                         ('trans_filler', ' ' * 87)])

TRAILER_DEF = OrderedDict([('trailer_id', '03'),
                           ('trailer_filler', ' ' * 100)])
