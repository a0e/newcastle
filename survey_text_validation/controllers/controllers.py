# -*- coding: utf-8 -*-
# from odoo import http


# class SurveyTextValidation(http.Controller):
#     @http.route('/survey_text_validation/survey_text_validation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/survey_text_validation/survey_text_validation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('survey_text_validation.listing', {
#             'root': '/survey_text_validation/survey_text_validation',
#             'objects': http.request.env['survey_text_validation.survey_text_validation'].search([]),
#         })

#     @http.route('/survey_text_validation/survey_text_validation/objects/<model("survey_text_validation.survey_text_validation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('survey_text_validation.object', {
#             'object': obj
#         })
