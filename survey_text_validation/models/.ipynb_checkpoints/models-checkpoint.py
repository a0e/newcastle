# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class survey_text_validation(models.Model):
#     _name = 'survey_text_validation.survey_text_validation'
#     _description = 'survey_text_validation.survey_text_validation'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
