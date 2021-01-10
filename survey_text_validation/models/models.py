# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SurveyQuestion(models.Model):
    _inherit = 'survey.question'
    validate_text = fields.Boolean('Validate text input')
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

    
class Survey(models.Model):
    _inherit = 'survey.survey'
    def _get_answers_correctness(self, user_answers):
        if not user_answers.mapped('survey_id') == self:
            raise UserError(_('Invalid performance computation'))

        res = dict((user_answer, {
            'correct': 0,
            'incorrect': 0,
            'partial': 0,
            'skipped': 0,
        }) for user_answer in user_answers)

        scored_questions = self.question_ids
        
        for question in scored_questions:
            if question.question_type in ['simple_choice', 'multiple_choice']:
                question_answer_correct = question.labels_ids.filtered(lambda answer: answer.is_correct)
            
            elif question.question_type == 'textbox' and question.validate_text == True:
                question_answer_correct = question.labels_ids
                
            for user_answer in user_answers:
                if question not in user_answer.question_ids:
                    # the question may be in the survey, but not be selected by the random selection
                    continue

                user_answer_lines_question = user_answer.user_input_line_ids.filtered(lambda line: line.question_id == question)
                user_answer_correct = user_answer_lines_question.filtered(lambda line: line.answer_is_correct and not line.skipped).mapped('value_suggested')
                user_answer_incorrect = user_answer_lines_question.filtered(lambda line: not line.answer_is_correct and not line.skipped)
                user_answer_lines_textquestion = user_answer.user_input_line_ids.filtered(lambda line: line.question_id == question)

                if question.question_type in ['simple_choice', 'multiple_choice']:
                    if question_answer_correct and user_answer_correct == question_answer_correct:
                        res[user_answer]['correct'] += 1
                    elif user_answer_correct and user_answer_correct < question_answer_correct:
                        res[user_answer]['partial'] += 1
                    if not user_answer_correct and user_answer_incorrect:
                        res[user_answer]['incorrect'] += 1
                    if not user_answer_correct and not user_answer_incorrect:
                        res[user_answer]['skipped'] += 1  
                
                elif question.question_type == 'textbox' and question.validate_text == True:
                    if question_answer_correct.value_validate == user_answer_lines_question.value_text:
                        res[user_answer]['correct'] += 1
                    if question_answer_correct.value_validate != user_answer_lines_question.value_text:
                        res[user_answer]['incorrect'] += 1
                    else:
                        res[user_answer]['skipped'] += 1
                    
        return res
    
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
