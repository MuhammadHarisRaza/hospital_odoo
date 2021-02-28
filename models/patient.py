from odoo import models, fields, _, api
from  odoo.exceptions import ValidationError

class SaleOrderInherit(models.Model):
   _inherit = 'sale.order'
   patient_name = fields.Char(string='Patient Name')

class HospitalPatient(models.Model):
   _name = 'hospital.patient'
   _description = 'patient records'
   _inherit = ['mail.thread','mail.activity.mixin']
   _rec_name = 'patient_name'
   _order = 'sequence desc'

   @api.constrains('patient_age')
   def check_age(self):
      for rec in self:
         if rec.patient_age <=5:
            raise ValidationError(_("The age must be greater than 5"))
         if rec.patient_age >=100:
            raise ValidationError(_("Invalid Age"))

   @api.depends('patient_age')
   def set_age_group(self):
      for rec in self:
         if rec.patient_age:
            if rec.patient_age <18:
               rec.age_group= 'minor'
            else:
               rec.age_group='major'

   def open_patient_appointments(self):
      return {
         'name':_('Appointments'),
         'domain':[('patient_id','=',self.id)],
         'view_mode':'tree,form',
         'res_model':'hospital.appointment',
         'view_id':False,
         'type':'ir.actions.act_window'
      }

   def get_appointment_count(self):
      count = self.env['hospital.appointment'].search_count([('patient_id','=',self.id)])
      self.appointment_count=count

   patient_name = fields.Char(string='Name', required=True, track_visibility="always")
   patient_age = fields.Integer('Age', track_visibility="always")
   gender = fields.Selection([
      ('male','Male'),
      ('fe_male','Female')
   ],default='male', string="Gender")
   age_group = fields.Selection([
      ('minor','Minor'),
      ('major','Major')
   ], string="Age", compute='set_age_group')
   notes= fields.Text(string='Notes')
   image = fields.Binary(string='Image')
   name = fields.Char(string='Contact Number')
   sequence = fields.Char(string='Patient ID', required=True, copy=False, readonly=True,
                         index=True, default=lambda self: _('New'))
   appointment_count = fields.Integer(string='Appointment', compute="get_appointment_count")

   @api.model
   def create(self, vals):
      if vals.get('sequence', _('New'))== _('New'):
         vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
      result= super(HospitalPatient,self).create(vals)
      return result