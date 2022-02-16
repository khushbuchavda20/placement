from odoo import models, fields

class Placement(models.Model):
    _name = 'placement.placement'
    _description = 'Placement Management System'

    name = fields.Char(string="Name",required=True)
    address = fields.Char(string="Address")
    # description = fields.Text(string="Description")
    email_id = fields.Char(string="Email-ID")
    contact = fields.Integer(string="Contact")
    cv_upload = fields.Binary()
    interested_subject = fields.Selection([
        ('python','Python'),
        ('java','Java'),
        ('sql','SQL'),
        ('ml','Machine Learning'),
        ('cs','Cyber Security'),
        ('php','PHP'),
        ('ds','Data Structure'),
        ('dp','Design Pattern')
    ])
    
    branch = fields.Selection([
        ('mca','MCA (Master in Computer Application'),
        ('ma','M.A.'),
        ('msw','M.S.W.'),
        ('mphill','M.Phil and Ph.D.')
    ])
    university = fields.Char(string="University Name", default="Gujarat Vidyapith")
    dob = fields.Date(string="Date Of Birth",default = lambda self: fields.Datetime.now())
    year = fields.Char(string="Year", default="2nd", readonly=True)
    
    std_school = fields.Char(string="School name")
    std_board = fields.Selection([
        ('cbse','Central Board of Secondary Education (CBSE)'),
        ('gseb','Gujarat Secondary and Higher Secondary Education Board (GSEB)'),
        ('mb','Maharashtra Board'),
        ('icse','Indian Certificate of Secondary Education (ICSE)')
    ])
    std_comp_school = fields.Selection([
        ('2016','2016'),
        ('2017','2017'),
        ('2018','2018'),
        ('2019','2019')],
    string="Year Completed")
    std_percentage = fields.Integer(string="Aggregate Percentage")
    
    std12_school = fields.Char(string="School name")
    std12_board = fields.Selection([
        ('gshseb','GUJARAT SECONDARY AND HIGHER SECONDARY EDUCATION BOARD'),
        ('msbshse',' MAHARASHTRA STATE BOARD OF SECONDARY AND HIGHER SECONDARY EDUCATION'),
        ('isce',' ICSE BOARD ( INDIAN COUNCIL OF SECONDARY EDUCATION')        
    ])
    std12_comp_school = fields.Selection([
        ('2017','2017'),
        ('2018','2018'),
        ('2019','2019'),
        ('2020','2020')],string="Year Complated")
    std12_percentage = fields.Integer(string="Aggregate Percentage")
    
class Company(models.Model):
    _name = "company.placement"
    _description = "company placement"
    
    company_name = fields.Char(string="Company Name")
    #company_type = fields.Char(string="Company Type")
    company_details = fields.Text(string="Company Details")
    position = fields.Char(string="Position")
    city = fields.Char(string="City")
    state = fields.Char(string="state")
    country = fields.Char(string="country")
    ctc = fields.Integer(string="CTC")
    intern_duration = fields.Integer(string="Intership Duration")
    intern_stpd = fields.Integer(string="stipend")
    reg_close = fields.Date(string="Registration close")
    
    def open_company(self):
        view_id = self.env.ref('placement.company_form').id
        print("asdfghgfdsasdfg",view_id)
        
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"company.placement",
            "views":[[view_id, 'tree']],
            # "res_id": 2,
            "target":"new",
            "domain": [('id', '=', self.id)]
            }
    