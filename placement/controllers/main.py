from odoo import http
from odoo.http import request


class wesite(http.Controller):
    @http.route('/student_form', website=True)
    def student_form(self, **kw):
        return request.render('placement.placement_std_form')
    
    @http.route('/company_form', website=True)
    def company_form(self, **kw):
        return request.render('placement.placement_com_form')
    
    @http.route('/submitform', website=True)
    def st_submit(self, **kw):
        request.env['placement.placement'].sudo().create(kw)
        return request.redirect('opportunities')
    
    @http.route('/submitcomform', website=True)
    def cm_submit(self, **kw):
        request.env['company.placement'].sudo().create(kw)
        return request.redirect('company_form')
    
    @http.route('/opportunities', website=True)
    def opportunities_form(self, **kw):
        com = request.env['company.placement'].search([('ctc','>','1')])
        print(com)
        return request.render('placement.company_details',{'com':com})