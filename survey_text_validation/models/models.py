# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SurveyQuestion(models.Model):
    _inherit = 'survey.question'
    validate_text = fields.Boolean('Validate text')
    value_validate = fields.Char('Validation Text')
    answer_score = fields.Float('Score', help="Score value for a correct answer to this question.")

class SurveyUserInput(models.Model):
    """ Metadata for a set of one user's answers to a particular survey """
    _inherit = "survey.user_input"
    @api.depends('user_input_line_ids.answer_score', 'user_input_line_ids.question_id')
    def _compute_quizz_score(self):
        for user_input in self:
            total_text_score = sum([
                answer_score if answer_score > 0 else 1
                for answer_score in user_input.question_ids.filtered('validate_text').mapped('answer_score')
                ])

            total_choice_score = sum([
                answer_score if answer_score > 0 else 0
                for answer_score in user_input.question_ids.mapped('labels_ids.answer_score')
            ])
            
            total_possible_score = total_text_score + total_choice_score
            if total_possible_score == 0:
                user_input.quizz_score = 0
            else:
                score = (sum(user_input.user_input_line_ids.mapped('answer_score')) / total_possible_score) * 100
                user_input.quizz_score = round(score, 2) if score > 0 else 0
                
class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input_line'
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            value_suggested = vals.get('value_suggested')
            id = vals.get('question_id')
            value_validate = vals.get('value_text')
            if value_suggested:
                vals.update({'answer_score': self.env['survey.label'].browse(int(value_suggested)).answer_score})
            
            if value_validate:
                if self.env['survey.question'].browse(id).validate_text == True and value_validate.lower() ==  self.env['survey.question'].browse(id).value_validate.lower():
                    vals.update({'answer_score': self.env['survey.question'].browse(id).answer_score})    
        return super(SurveyUserInputLine, self).create(vals_list)

    def write(self, vals):
        value_suggested = vals.get('value_suggested')
        id = vals.get('question_id')
        value_validate = vals.get('value_text')
        if value_suggested:
            vals.update({'answer_score': self.env['survey.label'].browse(int(value_suggested)).answer_score})
       
        if value_validate:
            if self.env['survey.question'].browse(id).validate_text == True and value_validate.lower() ==  self.env['survey.question'].browse(id).value_validate.lower():
                vals.update({'answer_score': self.env['survey.question'].browse(id).answer_score})  
        return super(SurveyUserInputLine, self).write(vals)

    
    @api.depends('value_text','value_suggested', 'question_id')
    def _compute_answer_is_correct(self):
        for answer in self:
            if answer.value_suggested and answer.question_id.question_type in ['simple_choice', 'multiple_choice']:
                answer.answer_is_correct = answer.value_suggested.is_correct
            elif answer.value_text and answer.question_id.validate_text == True and answer.value_text.lower() == answer.question_id.value_validate.lower():
                answer.answer_is_correct = True
            else:
                answer.answer_is_correct = False
    
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
