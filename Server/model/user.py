# -*- coding: utf-8 -*-

class user():
    def __init__(self, id, permission, cell_phone, email, name, password=None, sponsor_status = 0, m_delete = 0):
        self.id = id
        self.password = password
        self.permission = permission
        self.cell_phone =cell_phone
        self.email = email
        self.name = name
        self.sponsor_status = sponsor_status
        self.m_delete = m_delete
        