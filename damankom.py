# -*- coding: utf-8 -*-

from openerp.osv import osv,fields
import csv
from datetime import datetime
from openerp import api
import base64

#dictionnaire des données
data = {'email' : "hb182453@gmail.com" , 'smig': "1500" }

#la liste des erreurs 
list_erreur = []
erreur = {'cle_1' : list_erreur }

#liste pour reconstutuer la teledeclaration pour l'envoi(mail)
list_1=[]
list_2=[]
list_3=[]
list_4=[]
list_5=[]
list_6=[]
list_7=[]
tele_to_send = {'cle_1':list_1 ,'cle_2':list_2 , 'cle_3':list_3 ,'cle_4':list_4 ,'cle_5':list_5, 'cle_6':list_6 ,'cle_7':list_7}



class erreurs(osv.Model):
    _name = 'py.dacom.erreurs'
    def erreur_method(self,cr , uid , ids,context=None):
        list = []
        for i in erreur.get('cle_1'):
            print "hamza",i
            id=self.create(cr,uid,
                             {   
                                 'erreurs': i,
                        } )
            list.append(id)
        return list
#    
    _columns={'periode_id_16':fields.many2one('py.dacom.erreur'), 
               'erreurs':fields.char('erreur', size=128)
               }
erreurs()

class periode(osv.osv):
    _name = 'py.dacom.periode'
       
    def exercice(self,cr , uid,ids,periode_id,context=None):
        condi =True
        periode_pool=self.pool.get('account.period')
        year_pool=self.pool.get('account.fiscalyear')
        periode_ids= periode_pool.browse(cr,uid,periode_id,context)
        year_ids= year_pool.browse(cr,uid,periode_ids.fiscalyear_id.id,context)
        periode_edbs = str(periode_ids.name)[3:]
        year = str(year_ids.name)
        if(periode_id):    
            if(periode_edbs == year):
                condi =True
            else:
                condi =False
                erreur.get('cle_1').append("Verifiez votre datte: l'annee doit etre "+year)
        return condi
        
    
    def condi_chrono(self, cr , uid ,ids,periode_id,type,context=None):
        print "le type est :",type
        condi = True
        if(periode_id):
            periode_pool=self.pool.get('account.period')
            periode_ids= periode_pool.browse(cr,uid,periode_id,context)
            periode_edbs = str(periode_ids.name)
            actuelle = self.search(cr, uid ,[], context=context)
            if(actuelle != []):
                periode = self.browse(cr,uid,actuelle[len(actuelle)-1],context)
                periode_2 = periode.periode.id
                periode_3 = periode_pool.browse(cr,uid,periode_2,context)
                periode_pre = str(periode_3.name)
                periode_pre_aff = str(int(periode_pre[0:2])+1)
                periode_pre_affi = 0
                if(int(periode_pre[0:2]) == int(periode_edbs[0:2]) and type == True):
                    print "c fait"
                    condi = True
                else:
                    if(len(periode_pre_aff) == 2):
                        periode_pre_affi = str(int(periode_pre[0:2])+1)+"/"+periode_pre[3:]
                    else:
                        periode_pre_affi = "0"+str(int(periode_pre[0:2])+1)+"/"+periode_pre[3:]
                    print periode_edbs[0:2]
                    print periode_pre[0:2]               
                    if(int(periode_pre[0:2]) != int(periode_edbs[0:2])-1):
                        condi = False
                        erreur.get('cle_1').append("Vous n'avez pas suivi l'ordre des periodes: la periode "+periode_pre_affi+" manque")
            else:
                if(int(periode_edbs[0:2]) != 1):
                    condi = False
                    erreur.get('cle_1').append("Vous n'avez pas suivi l'ordre des periodes :la periode 01/"+periode_edbs[3:]+" manque")
        return condi
         
         
    
    def cloture(self,cr , uid , ids,context=None):
        values={}
        periode_pool=self.pool.get('account.period')
        periode=periode_pool.browse(cr,uid,context.get('cle_2'),context) 
        periode.state = 'done'
        values['value'] = { 
                            'Cloture':False,
                        }  
        return values 
    
    def creation_tele_send(self,cr , uid,ids,context=None):
        list=[]
        j=0
        k=15
        data =open("/home/dev/Bureau/MONFICHIER.csv","wb")
        c = csv.writer(data)
        list.append(tele_to_send.get('cle_1'))
        list.append(tele_to_send.get('cle_2'))
        for i in tele_to_send.get('cle_7'):
            if(i == "B02"):
                list.append(tele_to_send.get('cle_7')[j:k])
                j=j+len(tele_to_send.get('cle_7')[j:k])
                k=k+15
            else: pass
        list.append(tele_to_send.get('cle_3'))
        list.append(tele_to_send.get('cle_4'))
        list.append(tele_to_send.get('cle_5'))
        list.append(tele_to_send.get('cle_6'))
        #c.writerows([tele_to_send.get('cle_1'),tele_to_send.get('cle_2'),tele_to_send.get('cle_7'),tele_to_send.get('cle_3'),tele_to_send.get('cle_4'),tele_to_send.get('cle_5'),tele_to_send.get('cle_6')])
        c.writerows(list)
        data.close()
        ifile = open("/home/dev/Bureau/MONFICHIER.csv", "r" )
        ms=base64.b64encode(ifile.read())
        return ms 
    
    def envoyer(self,cr , uid , ids,context=None): 
        ir_mail_server = self.pool.get('mail.mail')
        #DATA ="SUQsQ0lOLE51bSBBU1NVUkUsTk9NIEVUIFBSRU5PTSxOT01CUkUgRU5GQU5UUyxNT05UQU5UIEFGIEEgUEFZRVIsTU9OVEFOVCBBRiBBIERFRFVJUkUsTU9OVEFOVCBBRiBBIFBBWUVSLE1PTlRBTlQgQUYgUkVTRVJWRVIgLE5PTUJSRSBKT1VSUyBERUNMQVJFUyxTTEFJUkUgUkVFTCAsU0FMQUlSRSBQTEFGT05ORSxTSVRVQVRJT04sREFURSBFTlRSRSxEQVRFIFNPUlRJRQoxLEVFMzY5NTY4LDE0Mzg5MDk4OSwgU0VCQkFOIEJBRFIsMywxMiw0LDgsOCw4LDcsNCxTTywwMS8yMDE0LAoyLEVFMzY5NTMxLDE0OTYxMzMzNSxNT1VXQUZBUSAgUkFISUQsMSwxMiw0LDgsNSwyMCwwLDAsQ1MsMDEvMjAwNCwKMyxFRTM2OTU4OSwxNzQwNDk2ODgsS0FSS09VUkkgTUFSSUFNICAsMSwxMiw1LDcsNjUsMiw3OCwyNSxERSwwMS8yMDA0LAo0LEVFMzY5NTk1LDE4Mjc2MDU4MSxFTCBHVUVSTkFPVUkgIEFMIE1BSERJICw0LDQ1LDYsMzIsMzc4LDIzLDI1MCwzMixNUCwwMS8yMDA0LAo1LEVFMzY5NTk2LDE4Mjc2MDU4MixCQVFBICBIQU1aQSAsNCw0NSw2LDMyLDM3OCwyMywyNTAsMzIsTVAsMDEvMjAwNCwKNixFRTQ5wrAwOTgsMTgyNzYwNTgzLFRPVE8gQU1JTkUgLDQsNDUsNiwzMiwzNzgsMjMsMjUwLDMyLE1QLDAxLzIwMDQsMDEvMjAxNQo="        
        DATA = self.creation_tele_send(cr , uid,ids,context)
        periode_pool=self.pool.get('account.period')
        periode= periode_pool.browse(cr,uid,context.get('cle_4'),context)
        message= "Télédeclation "+ str(periode.name)
        attachment_id = self.pool.get('ir.attachment').create(cr, uid, {  
           'name': 'ATTACHMENT_ID',  
           'datas': DATA,  
           'datas_fname': message,  
           'type': 'binary', 
            
         })  
        hb_id=ir_mail_server.create(cr, uid, {'email_to': data.get('email'),
                                              'subject': message,
                                              #'body_html' : message ,
                                               'headers': "télédeclaration_",
                                              'attachment_ids': [(6, 0, [attachment_id])]
                                              }
                                    )
          
        ir_mail_server.send(cr, uid, hb_id)
        
        return True  
        
    def annuler(self,cr , uid , ids,context=None):
        actuelle = self.search(cr, uid , [('periode', '=', context.get('cle_3'))])
        return self.unlink(cr, uid, actuelle[len(actuelle)-1], context=context)
        
    
    def intialisation(self, cr , uid , ids,context=None):
        values={}
        while erreur.get('cle_1'): erreur.get('cle_1').pop()
        erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
        values['value'] = {'Validation':False,
                           'num_declaration_comp': '',
                           'type':False,
                           'periode_ids_16':[(6,0,erreur_ids)]
                           }
        return values
    
    
    
    def intialisation_type(self, cr , uid , ids,context=None):
        values = {}
        while erreur.get('cle_1'): erreur.get('cle_1').pop()
        erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
        values['value'] = {'Validation':False,
                            'periode_ids_16':[(6,0,erreur_ids)]
                               }
        return values
       
    def agenda_teledeclation(self, cr , uid ,ids,periode_id,context=None): 
            values_agenda={}
            context.get('cle_1')
            print context.get('cle_1')
            periode_pool=self.pool.get('account.period')
            periode= periode_pool.browse(cr,uid,periode_id,context)
            periode_edbs = str(periode.name)
            periode_adapte = periode_edbs[3:] + periode_edbs[0:2]
            actuelle = self.search(cr, uid , [('periode', '=', periode_id)])
            print actuelle
            condi_year = self.exercice(cr , uid,ids,periode_id,context)
            condi =True
            if(condi_year == False):
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                values_agenda['value'] = {'periode_ids_16':[(6,0,erreur_ids)]}

            condi=self.condi_chrono(cr , uid ,ids,periode_id,context.get('cle_1'),context)
            if(condi == False):
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                values_agenda['value'] = {'periode_ids_16':[(6,0,erreur_ids)]}

            if(periode.state == 'done'  and context.get('cle_1') == False ):
                erreur.get('cle_1').append("Cette periode est deja cloturée")
                print "hamza"
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                values_agenda['value'] = {'periode_ids_16':[(6,0,erreur_ids)]}
            
            if(periode.state == 'draft'  and context.get('cle_1') == False and len(actuelle) == 1):
                print "nice"  
                values_agenda['value'] = {}
            
            if(periode.state == 'draft'  and context.get('cle_1') == False and actuelle != []):
                erreur.get('cle_1').append("Cette periode existe dejà comme periode principal.Si vous voulez la declarer comme une declaration complementaire cliquez sur valider")
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                values_agenda['value'] = {'periode_ids_16':[(6,0,erreur_ids)]}
                #raise osv.except_osv(('Error'), ('Cette periode existe dejà comme periode principal'))
                
            
            if(periode.state == 'draft'  and context.get('cle_1') == True ):
                print "hamza"
                erreur.get('cle_1').append("Il faut declarer tout d'abord la periode principal")
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                #values_agenda['value'] = {'type' : False,}
                values_agenda['value'] = {'periode_ids_16':[(6,0,erreur_ids)]}
          
            if(periode.state == 'done' and context.get('cle_1') == True):
                while erreur.get('cle_1'): erreur.get('cle_1').pop()
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                if(periode_adapte == periode_edbs[3:]+ "01"):
                    context_1=self.pool.get('ir.sequence').get(cr, uid, 'reg_code_1')
                    values_agenda['value'] = {'num_declaration_comp':context_1,
                                              'periode_ids_16':[(6,0,erreur_ids)]}
                    
            
            if(periode.state == 'done' and context.get('cle_1') == True):                             
                while erreur.get('cle_1'): erreur.get('cle_1').pop()
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                if(periode_adapte == periode_edbs[3:]+ "02"):
                    context_2=self.pool.get('ir.sequence').get(cr, uid, 'reg_code_2')
                    values_agenda['value'] = {'num_declaration_comp':context_2,
                                              'periode_ids_16':[(6,0,erreur_ids)]}
                                       
            
            if(periode.state == 'done' and context.get('cle_1') == True):
                while erreur.get('cle_1'): erreur.get('cle_1').pop()
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                if(periode_adapte == periode_edbs[3:]+ "03"):
                    context_3=self.pool.get('ir.sequence').get(cr, uid, 'reg_code_3')
                    values_agenda['value'] = {'num_declaration_comp':context_3,
                                              'periode_ids_16':[(6,0,erreur_ids)]}
                                      
            
            if(periode.state == 'done' and context.get('cle_1') == True):
                while erreur.get('cle_1'): erreur.get('cle_1').pop()
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                if(periode_adapte == periode_edbs[3:]+ "04"):
                    context_4=self.pool.get('ir.sequence').get(cr, uid, 'reg_code_4')
                    values_agenda['value'] = {'num_declaration_comp':context_4,
                                              'periode_ids_16':[(6,0,erreur_ids)]}
                                       
                    
            
            if(periode.state == 'done' and context.get('cle_1') == True):                         
                while erreur.get('cle_1'): erreur.get('cle_1').pop()
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                if(periode_adapte == periode_edbs[3:]+ "05"):
                    context_5=self.pool.get('ir.sequence').get(cr, uid, 'reg_code_5')
                    print context_5
                    values_agenda['value'] = {'num_declaration_comp': context_5,
                                              'periode_ids_16':[(6,0,erreur_ids)]}
                    
                
            if(periode.state == 'done' and context.get('cle_1') == True):    
                while erreur.get('cle_1'): erreur.get('cle_1').pop()
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                if(periode_adapte == periode_edbs[3:]+ "06"):
                    context_6=self.pool.get('ir.sequence').get(cr, uid, 'reg_code_6')
                    values_agenda['value'] = {'num_declaration_comp':context_6,
                                              'periode_ids_16':[(6,0,erreur_ids)]}
                    
                                       
            
            if(periode.state == 'done' and context.get('cle_1') == True):                           
                while erreur.get('cle_1'): erreur.get('cle_1').pop()
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                if(periode_adapte == periode_edbs[3:]+ "07"):
                    context_7=self.pool.get('ir.sequence').get(cr, uid, 'reg_code_7')
                    values_agenda['value'] = {'num_declaration_comp':context_7,
                                              'periode_ids_16':[(6,0,erreur_ids)]}
                    
                                       
            
            if(periode.state == 'done' and context.get('cle_1') == True):                           
                while erreur.get('cle_1'): erreur.get('cle_1').pop()
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                if(periode_adapte == periode_edbs[3:]+ "08"):
                    context_8=self.pool.get('ir.sequence').get(cr, uid, 'reg_code_8')
                    values_agenda['value'] = {'num_declaration_comp':context_8,
                                              'periode_ids_16':[(6,0,erreur_ids)]}
                                       
                                        
            if(periode.state == 'done' and context.get('cle_1') == True):                           
                while erreur.get('cle_1'): erreur.get('cle_1').pop()
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                if(periode_adapte == periode_edbs[3:]+ "09"):
                    context_9=self.pool.get('ir.sequence').get(cr, uid, 'reg_code_9')
                    values_agenda['value'] = {'num_declaration_comp':context_9,
                                              'periode_ids_16':[(6,0,erreur_ids)]}
            
            if(periode.state == 'done' and context.get('cle_1') == True):     
                while erreur.get('cle_1'): erreur.get('cle_1').pop()
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                if(periode_adapte == periode_edbs[3:]+ "10"):
                    context_10=self.pool.get('ir.sequence').get(cr, uid, 'reg_code_10')
                    values_agenda['value'] = {'num_declaration_comp':context_10,
                                              'periode_ids_16':[(6,0,erreur_ids)]}
            
            if(periode.state == 'done' and context.get('cle_1') == True): 
                while erreur.get('cle_1'): erreur.get('cle_1').pop()
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                if(periode_adapte == periode_edbs[3:]+ "11"):
                    context_11=self.pool.get('ir.sequence').get(cr, uid, 'reg_code_11')
                    values_agenda['value'] = {'num_declaration_comp':context_11,
                                              'periode_ids_16':[(6,0,erreur_ids)]}
            
            if(periode.state == 'done' and context.get('cle_1') == True):   
                while erreur.get('cle_1'): erreur.get('cle_1').pop()
                erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None)
                if(periode_adapte == periode_edbs[3:]+ "12"):
                    context_12=self.pool.get('ir.sequence').get(cr, uid, 'reg_code_12')
                    values_agenda['value'] = {'num_declaration_comp':context_12,
                                              'periode_ids_16':[(6,0,erreur_ids)]}
            
            
            return values_agenda
   
   
     
    #_defaults = {  'type': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'reg_code'), }     
    
    def recup_periode(self, cr , uid , ids,periode_id,url, url_ebds,context = None):
        values={} 
        if(periode_id and url and url_ebds):
            condi_1 =self.pool.get('py.dacom.fiche_paie').condi_nbr_jours(cr,uid,ids,url,context)          
            condi_2 =self.pool.get('py.dacom.fiche_paie').condi_situation(cr,uid,ids,url,context)
            condi_3 =self.pool.get('py.dacom.fiche_paie').condi_sal_pla(cr,uid,ids,url,context)
            condi_4 =self.pool.get('py.dacom.fiche_paie').condi_situation_ms_cs(cr,uid,ids,url,context)
            condi_5 =self.pool.get('py.dacom.fiche_paie').condi_situation_null(cr,uid,ids,url,context)
            condi_6 =self.pool.get('py.dacom.fiche_paie').condi_smig(cr,uid,ids,url,context)
            erreur_ids =self.pool.get('py.dacom.erreurs').erreur_method(cr , uid ,ids,context=None) 
            if(condi_1 and condi_2 and condi_3 and condi_4 and condi_5 and condi_6):
                list_ids_fiche_paie = self.pool.get('py.dacom.fiche_paie').fiche_paie(cr,uid,ids,periode_id,url,url_ebds,context=context)
                list_ids_import_edbs = self.pool.get('py.dacom.import_edbs').edbs(cr,uid,ids,periode_id,url,url_ebds,context=context)
                list_ids= self.pool.get('py.dacom.enreg_b02').enreg(cr,uid,ids,periode_id,url,url_ebds,context=context)
                list_ids_enreg_a00= self.pool.get('py.dacom.enreg_a00').enreg_a00(cr,uid,ids,periode_id,url_ebds,context=context)
                list_ids_enreg_a01= self.pool.get('py.dacom.enreg_a01').enreg_a01(cr,uid,ids,periode_id,url_ebds,context=context)
                list_ids_enreg_a03= self.pool.get('py.dacom.enreg_a03').enreg_a03(cr,uid,ids,periode_id,url_ebds,context=context)
                list_ids_enreg_b00= self.pool.get('py.dacom.enreg_b00').enreg_b00(cr,uid,ids,periode_id,url_ebds,context=context)
                list_ids_enreg_b01= self.pool.get('py.dacom.enreg_b01').enreg_b01(cr,uid,ids,periode_id,url_ebds,context=context)
                list_ids_enreg_b03= self.pool.get('py.dacom.enreg_b03').enr(cr,uid,ids,periode_id,url,url_ebds,context=context)
                list_ids_enreg_b04= self.pool.get('py.dacom.enreg_b04').enre(cr,uid,ids,periode_id,url,url_ebds,context=context)
                list_ids_enreg_b05= self.pool.get('py.dacom.enreg_b05').enreg_b05(cr,uid,ids,periode_id,url,url_ebds,context=context)
                list_ids_enreg_b06= self.pool.get('py.dacom.enreg_b06').enreg_b06(cr,uid,ids,periode_id,url,url_ebds,context=context)
                values['value']={
                                 'periode' : periode_id,
                                 'Validation' : True,
                                 'directive' : "cliquez sur enregister pour valider choix ",
                                 'url': url,
                                 'url_ebds': url_ebds,
                                 'periode_ids_1':[(6,0,list_ids_fiche_paie)],
                                 'periode_ids_3':[(6,0,list_ids)] ,
                                 'periode_ids_11':[(6,0,list_ids_enreg_a00)],
                                 'periode_ids_12':[(6,0,list_ids_enreg_a01)], 
                                 'periode_ids_13':[(6,0,list_ids_enreg_a03)], 
                                 'periode_ids_4':[(6,0,list_ids_import_edbs)],
                                 'periode_ids_14':[(6,0,list_ids_enreg_b00)],
                                 'periode_ids_15':[(6,0,list_ids_enreg_b01)],
                                'periode_ids_5':[(6,0,list_ids_enreg_b03)],
                                'periode_ids_7':[(6,0,list_ids_enreg_b04)],
                                'periode_ids_9':[(6,0,list_ids_enreg_b05)],
                                'periode_ids_10':[(6,0,list_ids_enreg_b06)],
                                'periode_ids_16':[(6,0,erreur_ids)]
                                }
        return  values
    
    
    
    
    
    @api.one
    def action_draft_information(self):
        if(erreur.get('cle_1') != []):
            raise osv.except_osv(('Error'),('Corriger vos erreurs avant de passer'))
        else: self.state = 'sent_import'
   
            
    @api.one
    def action_sent_import(self):
        if(erreur.get('cle_1') != []):
            raise osv.except_osv(('Error'),('Corriger vos erreurs avant de passer'))
        else: self.state = 'progress_declaration'
        
    @api.one
    def action_precedent_sent_import(self):
        self.state = 'draft_information'
            
    @api.one
    def action_progress_declaration(self):
        if(erreur.get('cle_1') != []):
            raise osv.except_osv(('Error'),('Corriger vos erreurs avant de passer'))
        else: self.state = 'done_cloture'
    
    @api.one
    def action_precedent_progress_declaration(self):
        self.state = 'sent_import'
    
    @api.one
    def action_precedent_done_cloture(self):
        self.state = 'progress_declaration'
               
    @api.one
    def action_done_cloture(self):
        self.state = 'done_cloture'
     
        
    _columns={
              'type':fields.boolean('Principal/Complementaire Period'),
              'message_send':fields.binary('Texto'),
              'periode':fields.many2one('account.period','periode'),
              'Validation':fields.boolean('Validation',required=True),
              'Cloture':fields.boolean('Cloture'),
              'Validation2':fields.boolean('Importer'),
              'erreur':fields.text('NB',readonly=True),
              'directive':fields.text('Consigne',readonly=True),
              'url':fields.char('url de la fiche de paie', size=128),
              'url_ebds':fields.char('url du ebds', size=128),        
              'num_declaration_comp':fields.text('num declation complaimentaire', readonly=True,size=128),            
              'periode_ids_1':fields.one2many('py.dacom.fiche_paie','periode_id_1'),
              #'periode_ids_2':fields.one2many('py.dacom.recherche_perso','periode_id_2'),
              'periode_ids_3':fields.one2many('py.dacom.enreg_b02','periode_id_3'),
              'periode_ids_4':fields.one2many('py.dacom.import_edbs','periode_id_4'),
              'periode_ids_5':fields.one2many('py.dacom.enreg_b03','periode_id_5'),
              'periode_ids_6':fields.one2many('py.dacom.enreg_b02_2','periode_id_6'),
              'periode_ids_7':fields.one2many('py.dacom.enreg_b04','periode_id_7'),
              'periode_ids_8':fields.one2many('py.dacom.recherche_perso_2','periode_id_8'),
              'periode_ids_9':fields.one2many('py.dacom.enreg_b05','periode_id_9'),
              'periode_ids_10':fields.one2many('py.dacom.enreg_b06','periode_id_10'),
              'periode_ids_11':fields.one2many('py.dacom.enreg_a00','periode_id_11'),
              'periode_ids_12':fields.one2many('py.dacom.enreg_a01','periode_id_12'),
              'periode_ids_13':fields.one2many('py.dacom.enreg_a03','periode_id_13'),
              'periode_ids_14':fields.one2many('py.dacom.enreg_b00','periode_id_14'),
              'periode_ids_15':fields.one2many('py.dacom.enreg_b01','periode_id_15'),
               'periode_ids_16':fields.one2many('py.dacom.erreurs','periode_id_16'),
              'state': fields.selection([('draft_information', 'Information'),
                                        ('sent_import', 'Importer document'),
                                        ('progress_declaration', 'Declaration'),
                                        ('done_cloture', 'Cloture'),
                                        ], 'Status', readonly=True, copy=False, help="Gives the status of the quotation or sales order.\
              \nThe exception status is automatically set when a cancel operation occurs \
              in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception).\nThe 'Waiting Schedule' status is set when the invoice is confirmed\
               but waiting for the scheduler to run on the order date.", select=True),
              
              
             }
    _defaults = {
                'state': 'draft_information',
            }

                      

              
              
             
periode() 


class wizard(osv.TransientModel):
    _name = 'wiz'
    _columns = {
        'chemin': fields.char('chemin'),
    }       
wizard()

    
    



class List_paie(osv.osv):
    _name = 'py.dacom.paie'
    def List_paie(self, cr , uid , ids,url,context):        
            ifile = open(url, "r" )
            read = csv.reader(ifile,delimiter=',')
            list_ids_paie = [] 
            list_CIN_paie = []
            list_num_assu_paie = []
            list_nom_pre_paie = []
            list_nbr_enf_paie = []
            list_mnt_paye_paie = []
            list_mnt_deduire_paie = []
            list_mnt_net_paye_paie = []
            list_mnt_reserver_paie = []
            list_nbr_jour_dec_paie = []
            list_sal_reel_paie = []
            list_sal_plaf_paie = []
            list_situa_paie = []
            list_actif_perso = []
            list_date_entree_paie = []
            list_date_sortie_paie= []
            
            for row in read :
                    list_ids_paie.append(row[0])
                    list_CIN_paie.append(row[1])
                    list_num_assu_paie.append(row[2])
                    list_nom_pre_paie.append(row[3])
                    list_nbr_enf_paie.append(row[4])
                    list_mnt_paye_paie.append(row[5])
                    list_mnt_deduire_paie.append(row[6])
                    list_mnt_net_paye_paie.append(row[7])
                    list_mnt_reserver_paie.append(row[8])
                    list_nbr_jour_dec_paie.append(row[9])
                    list_sal_reel_paie.append(row[10])
                    list_sal_plaf_paie.append(row[11])
                    list_situa_paie.append(row[12])
                    list_date_entree_paie.append(row[13])
                    list_date_sortie_paie.append(row[14])
                    
                    
            values= {'list_ids_paie':list_ids_paie,
                    'list_CIN_paie':list_CIN_paie ,
                    'list_num_assu_paie':list_num_assu_paie,
                    'list_nom_pre_paie':list_nom_pre_paie,
                    'list_nbr_enf_paie':list_nbr_enf_paie,
                    'list_mnt_paye_paie':list_mnt_paye_paie,
                    'list_mnt_deduire_paie':list_mnt_deduire_paie,
                    'list_mnt_net_paye_paie':list_mnt_net_paye_paie,
                    'list_mnt_reserver_paie':list_mnt_reserver_paie,
                    'list_nbr_jour_dec_paie':list_nbr_jour_dec_paie,
                    'list_sal_reel_paie':list_sal_reel_paie,
                    'list_sal_plaf_paie':list_sal_plaf_paie,
                    'list_situa_paie':list_situa_paie,
                    'list_date_entree_paie':list_date_entree_paie,
                    'list_date_sortie_paie':list_date_sortie_paie
                            }
            return values
    
    def N_Nbr_Salaries_entrants(self,cr,uid,ids,url,url_ebds,context):
        return len(self.pool.get('py.dacom.fichier_ebds').list_assu_entrants(cr,uid,ids,url,url_ebds,context))

    def N_T_Enfants_entrants(self,cr,uid,ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_assu_entrants(cr,uid,ids,url,url_ebds,context):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme +int(dico['list_nbr_enf_paie'][k]) 
        return somme
    
    def N_T_AF_A_Payer_entrants(self,cr,uid,ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_assu_entrants(cr,uid,ids,url,url_ebds,context):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme =somme+ int(dico['list_mnt_paye_paie'][k]) 
        return somme
    
    def N_T_AF_A_Deduire_entrants(self,cr,uid,ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_assu_entrants(cr,uid,ids,url,url_ebds,context):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_mnt_deduire_paie'][k]) 
        return somme
    
    
    def N_T_AF_Net_A_Payer_entrants(self,cr,uid,ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_assu_entrants(cr,uid,ids,url,url_ebds,context):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_mnt_net_paye_paie'][k]) 
        return somme
        
    
    def N_T_Num_Imma_entrants(self,cr,uid,ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_assu_entrants(cr,uid,ids,url,url_ebds,context):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_num_assu_paie'][k]) 
        return somme
        
    def N_T_AF_A_Reverser_entrants(self,cr,uid,ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_assu_entrants(cr,uid,ids,url,url_ebds,context):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_mnt_reserver_paie'][k]) 
        return somme
    
    
    def N_T_Jours_Declares_entrants(self,cr,uid,ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_assu_entrants(cr,uid,ids,url,url_ebds,context):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_nbr_jour_dec_paie'][k]) 
        return somme
    
    
    def N_T_Salaire_Reel_entrants(self,cr,uid,ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_assu_entrants(cr,uid,ids,url,url_ebds,context):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_sal_reel_paie'][k]) 
        return somme
    
        
    def N_T_Salaire_Plaf_entrants(self,cr,uid,ids,url,url_ebds,context): 
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_assu_entrants(cr,uid,ids,url,url_ebds,context):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_sal_plaf_paie'][k]) 
        return somme
        
    
    def N_T_Ctr_entrants(self,cr,uid,ids,url,url_ebds,context):   
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_assu_entrants(cr,uid,ids,url,url_ebds,context):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + self.pool.get('py.dacom.fichier_ebds').S_Ctr(cr,uid,ids,url,url_ebds,int(dico['list_num_assu_paie'][k]),context) 
        return somme
        
    def N_Nbr_Salaries_global(self,cr,uid,ids,url,url_ebds,context):
        return self.N_Nbr_Salaries_entrants(cr,uid,ids,url,url_ebds,context)+self.pool.get('py.dacom.fichier_ebds').N_Nbr_Salaries(url_ebds)

    def N_T_Num_Imma_global(self,cr,uid,ids,url,url_ebds,context):
        return self.N_T_Num_Imma_entrants(cr,uid,ids,url,url_ebds,context)+self.pool.get('py.dacom.paie').N_T_Num_Imma(cr , uid , ids,url,url_ebds,context)
    
    def N_T_Jours_Declares_global(self,cr,uid,ids,url,url_ebds,context):
        return self.N_T_Jours_Declares(cr,uid,ids,url,url_ebds,context)+ self.pool.get('py.dacom.paie').N_T_Jours_Declares_entrants(cr , uid , ids,url,url_ebds,context)
    
    def N_T_Salaire_Reel_global(self,cr,uid,ids,url,url_ebds,context):
        return self.N_T_Salaire_Reel_entrants(cr,uid,ids,url,url_ebds,context)+self.pool.get('py.dacom.paie').N_T_Salaire_Reel(cr , uid , ids,url,url_ebds,context)
    
    def N_T_Salaire_Plaf_global(self,cr,uid,ids,url,url_ebds,context): 
        return self.N_T_Salaire_Plaf_entrants(cr,uid,ids,url,url_ebds,context)+self.pool.get('py.dacom.paie').N_T_Salaire_Plaf(cr , uid , ids,url,url_ebds,context)
        
    def N_T_Ctr_global(self,cr,uid,ids,url,url_ebds,context):   
        return self.N_T_Ctr_entrants(cr,uid,ids,url,url_ebds,context)+self.pool.get('py.dacom.paie').N_T_Ctr(cr , uid , ids,url,url_ebds,context)  
    
    def ass_to_id(self, cr , uid , ids,url,num,context):
        try : 
            id=1
            k1 = int(num)
            dico = self.List_paie(cr , uid , ids,url,context)
            for mot in dico['list_num_assu_paie'][1:]:
                if(mot == str(num)):
                    break
                else: 
                    id=id+1
        except ValueError:
            print("Vous n'avez pas saisi de nombre")
        return id
    
    def N_Num_Assure_entrants(self, cr , uid , ids,url,num,context):
        dico = self.List_paie(cr , uid , ids,url,context)
        k = self.ass_to_id( cr , uid , ids,url,num,context)
        return dico['list_num_assu_paie'][k]

    def L_Nom_Prenom_entrants(self, cr , uid , ids,url,num,context):
        dico = self.List_paie(cr , uid , ids,url,context)
        k= self.ass_to_id( cr , uid , ids,url,num,context)    
        return dico['list_nom_pre_paie'][k]
    
    def N_T_Enfants(self, cr , uid , ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme +int(dico['list_nbr_enf_paie'][k]) 
        return somme

    def N_T_AF_A_Payer(self, cr , uid , ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme =somme+ int(dico['list_mnt_paye_paie'][k]) 
        return somme
    
    def N_T_AF_A_Deduire(self, cr , uid , ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_mnt_deduire_paie'][k]) 
        return somme
    
    
    def N_T_AF_Net_A_Payer(self, cr , uid , ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_mnt_net_paye_paie'][k]) 
        return somme
        
    
    def N_T_Num_Imma(self, cr , uid , ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_num_assu_paie'][k]) 
        return somme
        
    def N_T_AF_A_Reverser(self, cr , uid , ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_mnt_reserver_paie'][k]) 
        return somme
    
    
    def N_T_Jours_Declares(self, cr , uid , ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_nbr_jour_dec_paie'][k]) 
        return somme
    
    
    def N_T_Salaire_Reel(self, cr , uid , ids,url,url_ebds,context):
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_sal_reel_paie'][k]) 
        return somme
    
        
    def N_T_Salaire_Plaf(self, cr , uid , ids,url,url_ebds,context): 
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + int(dico['list_sal_plaf_paie'][k]) 
        return somme
        
    
    def N_T_Ctr(self, cr , uid , ids,url,url_ebds,context):   
        somme = 0
        dico = self.List_paie(cr , uid , ids,url,context)
        for i in self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds):
            k = self.ass_to_id( cr , uid , ids,url,i,context)
            somme = somme + self.pool.get('py.dacom.fichier_ebds').S_Ctr(cr,uid,ids,url,url_ebds,int(dico['list_num_assu_paie'][k]),context)
        return somme
    _columns={
        
            }
    
    
    


class fiche_paie(osv.osv):
   
    _name='py.dacom.fiche_paie'
    
    def condi_smig(self,cr,uid,ids,url,context):
        condi =True
        k=0
        dico= self.pool.get('py.dacom.paie').List_paie(cr,uid,ids,url,context=context)
        for i in dico['list_nbr_jour_dec_paie'][1:]:
            k=k+1
            cal=(data.get('smig')/26)*(int(i)-1)
            if(cal >= dico['list_sal_reel_paie'][k] ):
                condi = False
                erreur.get('cle_1').append("si n est le nombre de jours déclarés le salaire doit être supérieur strictement au SMIG en vigueur/26*(n-1).")
                break
        return condi    
        
    
    def condi_nbr_jours(self,cr,uid,ids,url,context):
        condi = True
        dico= self.pool.get('py.dacom.paie').List_paie(cr,uid,ids,url,context=context)        
        for i in dico['list_nbr_jour_dec_paie'][1:]:
            if(int(i)>26 or int(i) ==0):
                condi = False
                erreur.get('cle_1').append("Le nombre de jours (B02_N_Jours_Declares) doit être inférieur ou égal à 26.")
                break
        return condi    
    
    def condi_situation(self,cr,uid,ids,url,context):
        condi = True
        dico= self.pool.get('py.dacom.paie').List_paie(cr,uid,ids,url,context=context)                
        for i in dico['list_situa_paie'][1:]:
            if((i in ["" , "SO" ,"DE" ,"IT" ,"IL" ,"AT" ,"CS" ,"MS" ,"MP"]) == False):
                condi = False
                erreur.get('cle_1').append("L'element doit appartenir a la liste [ , SO ,DE ,IT ,IL ,AT ,CS ,MS ,MP]")
                break
        return condi
    
    def condi_sal_pla(self,cr,uid,ids,url,context):
        k=1
        condi = True
        dico= self.pool.get('py.dacom.paie').List_paie(cr,uid,ids,url,context=context) 
        for i in dico['list_sal_plaf_paie'][1:]:
            if(int(i) > int(dico['list_sal_reel_paie'][k])):
                condi = False
                erreur.get('cle_1').append("Le salaire plafonné doit être inférieur ou égal au salaire réel")
                break
            k=k+1
        return condi
    
    def condi_situation_ms_cs(self,cr,uid,ids,url,context):
        k=1
        condi = True
        dico= self.pool.get('py.dacom.paie').List_paie(cr,uid,ids,url,context=context) 
        for mot in dico['list_situa_paie'][1:]:
            if(mot == "CS" or mot == "MS"):
                if(int(dico['list_sal_plaf_paie'][k]) != 0 or int(dico['list_sal_reel_paie'][k]) != 0):
                    condi = False
                    erreur.get('cle_1').append("Pour les situations « CS » et « MS » le nombre de jours et les salaires réels et plafonnés doivent être nuls")
                    break
            else: k=k+1
        return condi
    
    def condi_situation_null(self,cr,uid,ids,url,context):
        k=1
        condi = True
        dico= self.pool.get('py.dacom.paie').List_paie(cr,uid,ids,url,context=context)
        for i in dico['list_situa_paie'][1:]:
            if(i == " "):
                if(dico['list_sal_plaf_paie'][k] == "" or dico['list_sal_reel_paie'][k] == ""):
                    condi = False
                    erreur.get('cle_1').append("Pour la situation « » le nombre de jours et les salaires réels et plafonnés doivent être renseignés")
                    break
        return condi 
    
             
        
    def fiche_paie(self,cr,uid,ids,periode_id,url,url_ebds,context):
        list_ids=[]
        dico= self.pool.get('py.dacom.paie').List_paie(cr,uid,ids,url,context=context)
        print "periode :",periode_id
        periode_pool=self.pool.get('account.period')
        periode=periode_pool.browse(cr,uid,periode_id,context)
        periode_edbs = str(periode.name)
        periode_adapte = periode_edbs[3:] + periode_edbs[0:2]
        print 'periode name:',periode_adapte
        enreg_ids =self.search(cr, uid , [('Periode', '=',periode_adapte )])
        self.unlink(cr, uid, enreg_ids, context=context)   
        print enreg_ids
        for j in dico['list_num_assu_paie'][1:]:
            if(periode_adapte == self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds)[1],context)):
                
                id=self.create(cr,uid,
                        {   
                            'ID': dico['list_ids_paie'][self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)],
                            'Periode': periode_adapte,
                            'CIN':dico['list_CIN_paie'][self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)],
                            'num_assure': dico['list_num_assu_paie'][self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)],
                            'nom_pre': dico['list_nom_pre_paie'][self.pool.get('py.dacom.paie').ass_to_id(cr , uid , ids,url,j,context)],
                            'nombre_enfants' : dico['list_nbr_enf_paie'][self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)],
                            'mnt_AF_payer' : dico['list_mnt_paye_paie'][self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)],
                            'mnt_AF_deduire' : dico['list_mnt_deduire_paie'][self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)],
                            'mnt_AF_net_payer' : dico['list_mnt_net_paye_paie'][self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)],
                            'mnt_AF_rev' : dico['list_mnt_reserver_paie'][self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)],
                            'nbr_dec' : dico['list_nbr_jour_dec_paie'][self.pool.get('py.dacom.paie').ass_to_id(cr , uid , ids,url,j,context)],
                            'sal_reel' : dico['list_sal_reel_paie'][self.pool.get('py.dacom.paie').ass_to_id(cr , uid , ids,url,j,context)],
                            'sal_plafonne':dico['list_sal_plaf_paie'][self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)],
                            'situation' : dico['list_situa_paie'][self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)],
                            'list_date_entree_paie':dico['list_date_entree_paie'][self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)],
                            'list_date_sortie_paie' :dico['list_date_sortie_paie'][self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)]            
                   } )
                list_ids.append(id)
        return list_ids
    _columns={
        'periode_id_1':fields.many2one('py.dacom.periode'),
        'Periode': fields.char('Periode', size=128) ,
        'ID': fields.char('ID', size=128),
        'CIN':fields.char('CIN', size=128),
        'num_assure': fields.char('Num Assure', size=128),
        'nom_pre': fields.char('nom et prenom', size=128),
        'nombre_enfants' : fields.char('nombre enfants', size=64),
        'mnt_AF_payer' : fields.char('montant AF a payer', size=64),
        'mnt_AF_deduire' : fields.char('montant AF a deduire', size=64),
        'mnt_AF_net_payer' : fields.char('montant AF net a payer ', size=64),
        'mnt_AF_rev' : fields.char('montant AF a reverser', size=64),
        'nbr_dec' : fields.char('nombre de jours declare', size=64),
        'sal_reel' : fields.char('salaire reel', size=64),
        'sal_plafonne':fields.char('sal plafonne', size=64),
        'situation' : fields.char('Situation', size=64),
        'list_date_entree_paie':fields.char('date entree', size=128),
        'list_date_sortie_paie' : fields.char('date sortie', size=128),
        }
    
fiche_paie()




class fichier_ebds(osv.osv):
    _name='py.dacom.fichier_ebds'
    def contenu(self,url_ebds):
        try:
            source = open(url_ebds, "r" )
            contenu   = source.read()
        except IOError:
            raise osv.except_osv(('Error'), ('Le fichier ebds est vide'))
        return contenu
    
    def N_Nbr_Salaries(self,url_ebds):
        return len(self.list_num_assu_enreg_a02(url_ebds))
    
    def nombre_enreg(self,url_ebds):
        k=0
        z=0
        while self.contenu(url_ebds)[522+z:525+z] != "A03":
            if(self.contenu(url_ebds)[522+z:525+z] == "A02"):
                z=z+261
                k=k+1
        return k 
    
    
    def list_enreg_a02_ebds(self,cr,uid,ids,url_ebds,context):
        i=0
        l=0
        list_enreg_a02_edbs = []
        while i< self.nombre_enreg(url_ebds):
            list_enreg_a02_edbs.append(self.contenu(url_ebds)[522+l:525+l])
            list_enreg_a02_edbs.append(self.contenu(url_ebds)[525+l:532+l])
            list_enreg_a02_edbs.append(self.contenu(url_ebds)[532+l:538+l])
            list_enreg_a02_edbs.append(self.contenu(url_ebds)[538+l:547+l])
            list_enreg_a02_edbs.append(self.contenu(url_ebds)[547+l:607+l])
            list_enreg_a02_edbs.append(self.contenu(url_ebds)[607+l:609+l])
            list_enreg_a02_edbs.append(self.contenu(url_ebds)[609+l:615+l])
            list_enreg_a02_edbs.append(self.contenu(url_ebds)[615+l:621+l])
            list_enreg_a02_edbs.append(self.contenu(url_ebds)[621+l:527+l])
            list_enreg_a02_edbs.append(self.contenu(url_ebds)[627+l:782+l])
            l=l+261
            i=i+1
        
        values= {'list_enreg_a02_edbs':list_enreg_a02_edbs,
                        }
        return values
    def list_num_assu_enreg_a02(self,url_ebds):
        my_list16 =[]
        m=0
        i=0
        while i< self.nombre_enreg(url_ebds):
            my_list16.append(self.contenu(url_ebds)[538+m:547+m])
            m=m+261
            i=i+1
        return my_list16
    def list_assu_entrants(self,cr,uid,ids,url,url_ebds,context):
        dico= self.pool.get('py.dacom.paie').List_paie(cr,uid,ids,url,context=context)
        my_list17 = []
        for i in dico['list_num_assu_paie'][1:]:
            if(i in self.list_num_assu_enreg_a02(url_ebds) or  dico['list_date_sortie_paie'][self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,i,context)] != '' ):
                pass
            else: my_list17.append(i)
        return my_list17

    def position_num_assure(self,cr,uid,ids,num,url_ebds,context):
        i=0
        for mot in self.list_num_assu_enreg_a02(url_ebds):
            if(mot != str(num)):
                i=i+1
            else: break
        return i 
    
    def N_Num_Affilie(self,cr,uid,ids,url_ebds,num,context):
        dico2=self.list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        return dico2['list_enreg_a02_edbs'][1+ 10*self.position_num_assure(cr,uid,ids,num,url_ebds,context)]

    
    def N_Num_affilie_entrants(self,cr,uid,ids,url_ebds,context):
        for i in self.list_num_assu_enreg_a02(url_ebds):
            return self.N_Num_Affilie(cr,uid,ids,url_ebds,i,context)
            
    
    def Periode(self,cr,uid,ids,url_ebds,num,context):
        dico2=self.list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        return dico2['list_enreg_a02_edbs'][2+ 10*self.position_num_assure(cr,uid,ids,num,url_ebds,context)]    
    
    def N_Num_Assure(self,cr,uid,ids,url_ebds,num,context):
        dico2=self.list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        return dico2['list_enreg_a02_edbs'][3+ 10*self.position_num_assure(cr,uid,ids,num,url_ebds,context)] 
    
    def L_Nom_Prenom(self,cr,uid,ids,url_ebds,num,context):
        dico2=self.list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        return dico2['list_enreg_a02_edbs'][4+ 10*self.position_num_assure(cr,uid,ids,num,url_ebds,context)]
    
    def N_Enfants(self,cr,uid,ids,url_ebds,num,context):
        dico2=self.list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        return dico2['list_enreg_a02_edbs'][5+ 10*self.position_num_assure(cr,uid,ids,num,url_ebds,context)]
        
    def N_AF_A_Payer(self,cr,uid,ids,url_ebds,num,context):
        dico2=self.list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        return dico2['list_enreg_a02_edbs'][6+ 10*self.position_num_assure(cr,uid,ids,num,url_ebds,context)]
    
    def N_AF_A_Deduire(self,cr,uid,ids,url_ebds,num,context):
        dico2=self.list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        return dico2['list_enreg_a02_edbs'][7+ 10*self.position_num_assure(cr,uid,ids,num,url_ebds,context)]
    
    def N_AF_Net_A_Payer(self,cr,uid,ids,url_ebds,num,context):
        dico2=self.list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        return dico2['list_enreg_a02_edbs'][8+ 10*self.position_num_assure(cr,uid,ids,num,url_ebds,context)]
    
    def L_filler(self,cr,uid,ids,url_ebds,num,context):
        dico2=self.list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        return dico2['list_enreg_a02_edbs'][9+ 10*self.position_num_assure(cr,uid,ids,num,url_ebds,context)]
    
    def S_Ctr(self,cr,uid,ids,url,url_ebds,num,context):
        dico2=self.pool.get('py.dacom.paie').List_paie(cr,uid,ids,url,context=context)
        k=self.pool.get('py.dacom.paie').ass_to_id(cr , uid , ids,url,num,context)
        somme = int(dico2['list_num_assu_paie'][k])+ int(dico2['list_mnt_reserver_paie'][k]) + int(dico2['list_sal_plaf_paie'][k])+ int(dico2['list_nbr_jour_dec_paie'][k])+ int(dico2['list_sal_reel_paie'][k])+int(situation(dico2['list_situa_paie'][k]))
        return somme
    _columns={
        
            }  
    


def situation(sit):
    s=0
    if(sit == "SO"):
        s=1
    if(sit == "DE"):
        s=2
    if(sit == "IT"):
        s=3
    if(sit == "IL"):
        s=4
    if(sit == "AT"):
        s=5
    if(sit == "CS"):
        s=6
    if(sit == "MS"):
        s=7
    if(sit == "MP"):
        s=8
    return s


class enreg_a00(osv.Model):
    _name = 'py.dacom.enreg_a00' 
    def list_enreg_a00(self,url_ebds):
        contenu=self.pool.get('py.dacom.fichier_ebds').contenu(url_ebds)
        L_Type_EnregA00=contenu[0:3]
        N_Identif_TransfertA00 =contenu[3:17]
        L_CatA00 =contenu[17:19]
        L_fillerA00 =contenu[19:260]
        listeA00=[]
        listeA00.append([L_Type_EnregA00,N_Identif_TransfertA00,L_CatA00,L_fillerA00])
        print(listeA00)
        return listeA00 
   
    def enreg_a00(self,cr,uid,ids,periode_id,url_ebds,context):
        list_ids=[]
        print "periode :",periode_id
        periode_pool=self.pool.get('account.period')
        periode=periode_pool.browse(cr,uid,periode_id,context)
        periode_edbs = str(periode.name)
        periode_adapte = periode_edbs[3:] + periode_edbs[0:2]
        print 'periode name:',periode_adapte
        dico2=self.pool.get('py.dacom.fichier_ebds').list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        if(periode_adapte == self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds)[1],context)):
                enreg_ids =self.search(cr, uid , [('N_Identif_TransfertA00', '=',self.list_enreg_a00(url_ebds)[0][1] )])
                self.unlink(cr, uid, enreg_ids, context=context)
                id=self.create(cr,uid,
                            {
                             'L_Type_EnregA00': "A00",
                             'N_Identif_TransfertA00' : self.list_enreg_a00(url_ebds)[0][1],
                             'L_CatA00' : self.list_enreg_a00(url_ebds)[0][2],
                            }
                    )
                list_ids.append(id)
        return list_ids
        
    _columns= {
               'periode_id_11':fields.many2one('py.dacom.periode'),
               'L_Type_EnregA00': fields.char('Le type enreg', size=3),
               'N_Identif_TransfertA00': fields.char('Identifiant des infos a transferer', size=14),
               'L_CatA00': fields.char('L_CatA00', size=2),
               } 
    
enreg_a00()


class enreg_b00(osv.Model):
    _name = 'py.dacom.enreg_b00' 
    def enreg_b00(self,cr,uid,ids,periode_id,url_ebds,context):
        list_ids=[]
        print "periode :",periode_id
        periode_pool=self.pool.get('account.period')
        periode=periode_pool.browse(cr,uid,periode_id,context)
        periode_edbs = str(periode.name)
        periode_adapte = periode_edbs[3:] + periode_edbs[0:2]
        print 'periode name:',periode_adapte
        enreg_b00_ids = self.search(cr, uid , [('L_Type_EnregA00', '=', 'B00')])
        enreg_b00_obj = self.browse(cr, uid,  enreg_b00_ids, context=context)
        for record in enreg_b00_obj:
            tele_to_send.get('cle_1').append(record.L_Type_EnregA00)
            tele_to_send.get('cle_1').append(record.N_Identif_TransfertA00)
            tele_to_send.get('cle_1').append(record.L_CatA00)
        dico2=self.pool.get('py.dacom.fichier_ebds').list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        if(periode_adapte == self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds)[1],context)):
                enreg_ids =self.search(cr, uid , [('N_Identif_TransfertA00', '=',self.pool.get('py.dacom.enreg_a00').list_enreg_a00(url_ebds)[0][1] )])
                self.unlink(cr, uid, enreg_ids, context=context)
                id=self.create(cr,uid,
                            {
                             'L_Type_EnregA00': "B00",
                             'N_Identif_TransfertA00' : self.pool.get('py.dacom.enreg_a00').list_enreg_a00(url_ebds)[0][1],
                             #'L_CatA00' : self.pool.get('py.dacom.enreg_a00').list_enreg_a00(url_ebds)[0][2],
                            'L_CatA00':"B01"
                            }
                    )
                list_ids.append(id)
        return list_ids
        
    _columns= {
               'periode_id_14':fields.many2one('py.dacom.periode'),
               'L_Type_EnregA00': fields.char('Le type enreg', size=3),
               'N_Identif_TransfertA00': fields.char('Identifiant des infos a transferer', size=14),
               'L_CatA00': fields.char('L_CatA00', size=2),
               }    
enreg_b00()




class enreg_a01(osv.Model):
    _name = 'py.dacom.enreg_a01' 
    def list_a01(self,url_ebds):
        contenu=self.pool.get('py.dacom.fichier_ebds').contenu(url_ebds)
        L_Type_EnregA01=contenu[260:265]
        N_Num_AffilieA01=contenu[264:271]
        L_PeriodeA01=contenu[271:277]
        L_Raison_SocialeA01=contenu[277:317]
        L_ActiviteA01=contenu[317:357]
        L_AdresseA01=contenu[357:477]                 
        L_VilleA01=contenu[477:497]
        C_Code_PostalA01=contenu[497:503]
        C_Code_AgenceA01=contenu[503:505]
        D_Date_EmissionA01=contenu[505:513]
        D_Date_ExigA01=contenu[513:521]
        listeA01=[]
        listeA01.append([L_Type_EnregA01,N_Num_AffilieA01,L_PeriodeA01,L_Raison_SocialeA01,L_ActiviteA01,L_AdresseA01,L_VilleA01,C_Code_PostalA01,C_Code_AgenceA01,D_Date_EmissionA01,D_Date_ExigA01])
        print(listeA01)
        return listeA01
    def enreg_a01(self,cr,uid,ids,periode_id,url_ebds,context):
        list_ids=[]
        print "periode :",periode_id
        periode_pool=self.pool.get('account.period')
        periode=periode_pool.browse(cr,uid,periode_id,context)
        periode_edbs = str(periode.name)
        periode_adapte = periode_edbs[3:] + periode_edbs[0:2]
        print 'periode name:',periode_adapte
        dico2=self.pool.get('py.dacom.fichier_ebds').list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        if(periode_adapte == self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds)[1],context)):
                enreg_ids =self.search(cr, uid , [('L_Type_EnregA01', '=', "A01")])
                self.unlink(cr, uid, enreg_ids, context=context)
                id=self.create(cr,uid,
                                        {
                                         'L_Type_EnregA01': "A01",
                                         'N_Num_AffilieA01' : self.list_a01(url_ebds)[0][1],
                                         'L_PeriodeA01' : self.list_a01(url_ebds)[0][2],
                                         'L_Raison_SocialeA01' :self.list_a01(url_ebds)[0][3],
                                         'L_ActiviteA01': self.list_a01(url_ebds)[0][4],
                                         'L_AdresseA01' : self.list_a01(url_ebds)[0][5],
                                         'L_VilleA01' : self.list_a01(url_ebds)[0][6],
                                         'C_Code_PostalA01' :self.list_a01(url_ebds)[0][7],
                                         'C_Code_AgenceA01': self.list_a01(url_ebds)[0][8],
                                         'D_Date_EmissionA01' : self.list_a01(url_ebds)[0][9],
                                         'D_Date_ExigA01' : self.list_a01(url_ebds)[0][10],
                                         
                                         
                                        }
                               )
                list_ids.append(id)
        return list_ids
    _columns= {
               'periode_id_12':fields.many2one('py.dacom.periode'),
               'L_Type_EnregA01': fields.char('Le type enreg', size=3),
               'N_Num_AffilieA01': fields.char('Le num affilie', size=7),
               'L_PeriodeA01': fields.char('La periode', size=6),
               'L_Raison_SocialeA01': fields.char('Raison social', size=40),
               'L_ActiviteA01': fields.char('Activité de l’affilié', size=40),
               'L_AdresseA01': fields.char('Adresse de l’affilié', size=120),
               'L_VilleA01': fields.char('Ville de l’affilié', size=20),
               'C_Code_PostalA01': fields.char('Code Postal', size=6),
               'C_Code_AgenceA01': fields.char('Code de l’agence', size=2),
               'D_Date_EmissionA01': fields.char('Date de l’émission.', size=8),
               'D_Date_ExigA01': fields.char('Date limite de retour des BDS et de paiement des cotisations', size=8),
               
               } 
enreg_a01()

class enreg_b01(osv.Model):
    _name = 'py.dacom.enreg_b01' 
    def enreg_b01(self,cr,uid,ids,periode_id,url_ebds,context):
        list_ids=[]
        print "periode :",periode_id
        periode_pool=self.pool.get('account.period')
        periode=periode_pool.browse(cr,uid,periode_id,context)
        periode_edbs = str(periode.name)
        periode_adapte = periode_edbs[3:] + periode_edbs[0:2]
        print 'periode name:',periode_adapte
        enreg_b01_ids = self.search(cr, uid , [('L_Type_EnregA01', '=', 'B01')])
        enreg_b01_obj = self.browse(cr, uid,  enreg_b01_ids, context=context)
        for record in enreg_b01_obj:
            tele_to_send.get('cle_2').append(record.L_Type_EnregA01)
            tele_to_send.get('cle_2').append(record.N_Num_AffilieA01)
            tele_to_send.get('cle_2').append(record.L_PeriodeA01)
            tele_to_send.get('cle_2').append(record.L_Raison_SocialeA01)
            tele_to_send.get('cle_2').append(record.L_ActiviteA01)
            tele_to_send.get('cle_2').append(record.L_AdresseA01)
            tele_to_send.get('cle_2').append(record.L_VilleA01)
            tele_to_send.get('cle_2').append(record.C_Code_PostalA01)
            tele_to_send.get('cle_2').append(record.C_Code_AgenceA01)
            tele_to_send.get('cle_2').append(record.D_Date_EmissionA01)
            tele_to_send.get('cle_2').append(record.D_Date_ExigA01)
        dico2=self.pool.get('py.dacom.fichier_ebds').list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        if(periode_adapte == self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds)[1],context)):
                enreg_ids =self.search(cr, uid , [('L_Type_EnregA01', '=', "B01")])
                self.unlink(cr, uid, enreg_ids, context=context)
                id=self.create(cr,uid,
                                        {
                                         'L_Type_EnregA01': "B01",
                                         'N_Num_AffilieA01' : self.pool.get('py.dacom.enreg_a01').list_a01(url_ebds)[0][1],
                                         'L_PeriodeA01' : self.pool.get('py.dacom.enreg_a01').list_a01(url_ebds)[0][2],
                                         'L_Raison_SocialeA01' :self.pool.get('py.dacom.enreg_a01').list_a01(url_ebds)[0][3],
                                         'L_ActiviteA01': self.pool.get('py.dacom.enreg_a01').list_a01(url_ebds)[0][4],
                                         'L_AdresseA01' : self.pool.get('py.dacom.enreg_a01').list_a01(url_ebds)[0][5],
                                         'L_VilleA01' : self.pool.get('py.dacom.enreg_a01').list_a01(url_ebds)[0][6],
                                         'C_Code_PostalA01' :self.pool.get('py.dacom.enreg_a01').list_a01(url_ebds)[0][7],
                                         'C_Code_AgenceA01': self.pool.get('py.dacom.enreg_a01').list_a01(url_ebds)[0][8],
                                         'D_Date_EmissionA01' : self.pool.get('py.dacom.enreg_a01').list_a01(url_ebds)[0][9],
                                         'D_Date_ExigA01' : self.pool.get('py.dacom.enreg_a01').list_a01(url_ebds)[0][10],
                                         
                                         
                                        }
                               )
                list_ids.append(id)
        return list_ids
    _columns= {
               'periode_id_15':fields.many2one('py.dacom.periode'),
               'L_Type_EnregA01': fields.char('Le type enreg', size=3),
               'N_Num_AffilieA01': fields.char('Le num affilie', size=7),
               'L_PeriodeA01': fields.char('La periode', size=6),
               'L_Raison_SocialeA01': fields.char('Raison social', size=40),
               'L_ActiviteA01': fields.char('Activité de l’affilié', size=40),
               'L_AdresseA01': fields.char('Adresse de l’affilié', size=120),
               'L_VilleA01': fields.char('Ville de l’affilié', size=20),
               'C_Code_PostalA01': fields.char('Code Postal', size=6),
               'C_Code_AgenceA01': fields.char('Code de l’agence', size=2),
               'D_Date_EmissionA01': fields.char('Date de l’émission.', size=8),
               'D_Date_ExigA01': fields.char('Date limite de retour des BDS et de paiement des cotisations', size=8),
               
               } 
enreg_a01()




class enreg_a03(osv.Model):
    _name = 'py.dacom.enreg_a03'
    def list_a03(self,url_ebds):
        contenu=self.pool.get('py.dacom.fichier_ebds').contenu(url_ebds)
        p=0
        i=522
        while contenu[i:i+3]!= 'A03' :  #& i%261=0 :
            if contenu[i:i+3]== 'A02' :
                i=i+261
                p=p+1
        
        L_Type_EnregA03=contenu[i:i+3]
        N_Num_AffilieA03=contenu[i+3:i+10]
        L_PeriodeA03=contenu[i+10:i+16]
        N_Nbr_SalariesA03=contenu[i+16:i+22]
        N_T_EnfantsA03=contenu[i+22:i+28]
        N_T_AF_A_PayerA03=contenu[i+28:i+40]
        N_T_AF_A_DeduireA03=contenu[i+40:i+52]
        N_T_AF_Net_A_PayerA03=contenu[i+52:i+64]
        N_T_Num_ImmaA03=contenu[i+64:i+79]
        L_fillerA03=contenu[i+79:i+260]
        listeA03=[]
        listeA03.append([L_Type_EnregA03,N_Num_AffilieA03,L_PeriodeA03,N_Nbr_SalariesA03,N_T_EnfantsA03,N_T_AF_A_PayerA03,N_T_AF_A_DeduireA03,N_T_AF_Net_A_PayerA03,N_T_Num_ImmaA03])
        print(listeA03) 
        return listeA03
    def enreg_a03(self,cr,uid,ids,periode_id,url_ebds,context):
        list_ids=[]
        print "periode :",periode_id
        periode_pool=self.pool.get('account.period')
        periode=periode_pool.browse(cr,uid,periode_id,context)
        periode_edbs = str(periode.name)
        periode_adapte = periode_edbs[3:] + periode_edbs[0:2]
        print 'periode name:',periode_adapte
        dico2=self.pool.get('py.dacom.fichier_ebds').list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        if(periode_adapte == self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds)[1],context)):
                enreg_ids =self.search(cr, uid , [('L_PeriodeA03', '=',self.list_a03(url_ebds)[0][2] )])
                self.unlink(cr, uid, enreg_ids, context=context)
                id=self.create(cr,uid,
                                    {
                                     'L_Type_EnregA03': "A03",
                                     'N_Num_AffilieA03' : self.list_a03(url_ebds)[0][1],
                                     'L_PeriodeA03' : self.list_a03(url_ebds)[0][2],
                                     'N_Nbr_SalariesA03' :self.list_a03(url_ebds)[0][3],
                                     'N_T_EnfantsA03': self.list_a03(url_ebds)[0][4],
                                     'N_T_AF_A_PayerA03' : self.list_a03(url_ebds)[0][5],
                                     'N_T_AF_A_DeduireA03' : self.list_a03(url_ebds)[0][6],
                                     'N_T_AF_Net_A_PayerA03' :self.list_a03(url_ebds)[0][7],
                                     'N_T_Num_ImmaA03': self.list_a03(url_ebds)[0][8],
                                     #'L_fillerA03' : listeA03[0][9]     
                                    }
                                )
                list_ids.append(id)
        return list_ids
                
    _columns= {
               'periode_id_13':fields.many2one('py.dacom.periode'),
               'L_Type_EnregA03': fields.char('Le Type Enreg', size=3),
               'N_Num_AffilieA03': fields.char('Numéro d’affiliation de l’entreprise', size=14),
               'L_PeriodeA03': fields.char('Mois et Année de la déclaration', size=2),
               'N_Nbr_SalariesA03': fields.char('N_Nbr_SalariesA03', size=241),
               'N_T_EnfantsA03': fields.char('N_T_EnfantsA03', size=3),
               'N_T_AF_A_PayerA03': fields.char('N_T_AF_A_PayerA03', size=14),
               'N_T_AF_A_DeduireA03': fields.char('N_T_AF_A_DeduireA03', size=2),
               'N_T_AF_Net_A_PayerA03': fields.char('N_T_AF_Net_A_PayerA03', size=241),
               'N_T_Num_ImmaA03': fields.char('N_T_Num_ImmaA03', size=3),
               #'L_fillerA03': fields.char('L_fillerA03', size=14),
         
               } 
enreg_a03()

#la teledeclaration methode 1 en utilisant les listes "A02"
class enreg_b02(osv.Model):
    _name = 'py.dacom.enreg_b02'    
    def enreg(self,cr,uid,ids,periode_id,url,url_ebds,context):
        list_ids=[]
        print "periode :",periode_id
        periode_pool=self.pool.get('account.period')
        periode=periode_pool.browse(cr,uid,periode_id,context)
        periode_edbs = str(periode.name)
        periode_adapte = periode_edbs[3:] + periode_edbs[0:2]
        print 'periode name:',periode_adapte
        enreg_b02_ids = self.search(cr, uid , [('L_Type_ Enreg', '=', 'B02')])
        enreg_b02_obj = self.browse(cr, uid,  enreg_b02_ids, context=context)
        for record in enreg_b02_obj:
            tele_to_send.get('cle_7').append("B02")
            tele_to_send.get('cle_7').append(record.N_Num_Affilie)
            tele_to_send.get('cle_7').append(record.Periode)
            tele_to_send.get('cle_7').append(record.N_Num_Assure)
            tele_to_send.get('cle_7').append(record.L_Nom_Prenom)
            tele_to_send.get('cle_7').append(record.N_Enfants)
            tele_to_send.get('cle_7').append(record.N_AF_A_Payer)
            tele_to_send.get('cle_7').append(record.N_AF_A_Deduire)
            tele_to_send.get('cle_7').append(record.N_AF_Net_A_Payer)
            tele_to_send.get('cle_7').append(record.N_AF_A_Reverser)
            tele_to_send.get('cle_7').append(record.N_Jours_Declares)
            tele_to_send.get('cle_7').append(record.N_Salaire_Reel)
            tele_to_send.get('cle_7').append(record.N_Salaire_Plaf)
            tele_to_send.get('cle_7').append(record.L_Situation)
            tele_to_send.get('cle_7').append(record.S_Ctr)
        enreg_ids =self.search(cr, uid , [('Periode', '=',periode_adapte )])
        self.unlink(cr, uid, enreg_ids, context=context)
        dico= self.pool.get('py.dacom.paie').List_paie(cr,uid,ids,url,context=context)
        dico2=self.pool.get('py.dacom.fichier_ebds').list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        for j in self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds):  
            if(periode_adapte == self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,j,context)):
                k = self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)
                id=self.create(cr,uid,
                        {   
                            'L_Type_ Enreg': "B02",
                            'N_Num_Affilie': self.pool.get('py.dacom.fichier_ebds').N_Num_Affilie(cr,uid,ids,url_ebds,j,context),
                            'Periode' : self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,j,context),
                            'N_Num_Assure' : self.pool.get('py.dacom.fichier_ebds').N_Num_Assure(cr,uid,ids,url_ebds,j,context),
                            'L_Nom_Prenom' : self.pool.get('py.dacom.fichier_ebds').L_Nom_Prenom(cr,uid,ids,url_ebds,j,context),
                            'N_Enfants' :dico['list_nbr_enf_paie'][k],
                            'N_AF_A_Payer' :dico['list_mnt_paye_paie'][k],
                            'N_AF_A_Deduire' : dico['list_mnt_deduire_paie'][k],
                            'N_AF_Net_A_Payer':dico['list_mnt_net_paye_paie'][k],
                            'N_AF_A_Reverser' :dico['list_mnt_reserver_paie'][k],
                            'N_Jours_Declares':dico['list_nbr_jour_dec_paie'][k],
                            'N_Salaire_Reel':dico['list_sal_reel_paie'][k],
                            'N_Salaire_Plaf':dico['list_sal_plaf_paie'][k],
                            'L_Situation':dico['list_situa_paie'][k],  
                            'S_Ctr': self.pool.get('py.dacom.fichier_ebds').S_Ctr(cr,uid,ids,url,url_ebds,j,context)                    
                   } )
                list_ids.append(id)
        return list_ids
    
    _columns = {
            #'code2': fields.many2one('fiche_paie', 'Point Of Sale', required=True),
            #'hb': fields.function( user ,type ='char'),
            'periode_id_3':fields.many2one('py.dacom.periode'),
            'L_Type_ Enreg': fields.char('L_Type_ Enreg', size=3),
            'N_Num_Affilie': fields.char('N_Num_Affilie', size=7),
            'Periode' : fields.char('Periode', size=6),
            'N_Num_Assure' : fields.char('N_Num_Assure', size=9),
            'L_Nom_Prenom' : fields.char('L_Nom_Prenome', size=60),
            'N_Enfants' : fields.char('montant AF net a payer ', size=2),
            'N_AF_A_Payer' : fields.char('N_Enfants', size=6),
            'N_AF_A_Deduire' : fields.char('N_AF_A_Deduire', size=6),
            'N_AF_Net_A_Payer' : fields.char('N_AF_Net_A_Payer', size=6),
            'N_AF_A_Reverser' :fields.char('N_AF_A_Reverser', size=6),
            'N_Jours_Declares':fields.char('N_Jours_Declares', size=2),
            'N_Salaire_Reel':fields.char('N_Salaire_Reel', size=13),
            'N_Salaire_Plaf':fields.char('N_Salaire_Plaf', size=9),
            'L_Situation':fields.char('L_Situation', size=2),
            'S_Ctr':fields.char('S_Ctr', size=19),
            
        }
enreg_b02()   

#import de document edbs A02
class import_edbs(osv.osv):
    _name = 'py.dacom.import_edbs'
    
    def edbs(self,cr,uid,ids,periode_id,url,url_ebds,context):
        list_ids_import_edbs=[]
        
        print "periode :",periode_id
        periode_pool=self.pool.get('account.period')
        periode=periode_pool.browse(cr,uid,periode_id,context)
        periode_edbs = str(periode.name)
        periode_adapte = periode_edbs[3:] + periode_edbs[0:2]
        print 'periode name:',periode_adapte
        dico= self.pool.get('py.dacom.paie').List_paie(cr,uid,ids,url,context=context)
        dico2=self.pool.get('py.dacom.fichier_ebds').list_enreg_a02_ebds(cr,uid,ids,url_ebds,context)
        enreg_ids =self.search(cr, uid , [('Periode', '=',periode_adapte )])
        self.unlink(cr, uid, enreg_ids, context=context) 
        for j in self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds):  
            if(periode_adapte == self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,j,context)):
                id=self.create(cr,uid,
                        {   
                            'L_Type_ Enreg': dico2['list_enreg_a02_edbs'][0],
                            'N_Num_Affilie': self.pool.get('py.dacom.fichier_ebds').N_Num_Affilie(cr,uid,ids,url_ebds,j,context),
                            'Periode' : self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,j,context),
                            'N_Num_Assure' : self.pool.get('py.dacom.fichier_ebds').N_Num_Assure(cr,uid,ids,url_ebds,j,context),
                            'L_Nom_Prenom' : self.pool.get('py.dacom.fichier_ebds').L_Nom_Prenom(cr,uid,ids,url_ebds,j,context),
                            'N_Enfants' :self.pool.get('py.dacom.fichier_ebds').N_Enfants(cr,uid,ids,url_ebds,j,context),
                            'N_AF_A_Payer' :self.pool.get('py.dacom.fichier_ebds').N_AF_A_Payer(cr,uid,ids,url_ebds,j,context),
                            'N_AF_A_Deduire' : self.pool.get('py.dacom.fichier_ebds').N_AF_A_Deduire(cr,uid,ids,url_ebds,j,context),
                            'N_AF_Net_A_Payer':self.pool.get('py.dacom.fichier_ebds').N_AF_Net_A_Payer(cr,uid,ids,url_ebds,j,context),
                            
                        },
                                       
                    )
                list_ids_import_edbs.append(id)
        return list_ids_import_edbs
        
    _columns = {
            #'code2': fields.many2one('fiche_paie', 'Point Of Sale', required=True),
            #'hb': fields.function( user ,type ='char'),
            'periode_id_4':fields.many2one('py.dacom.periode'),
            'L_Type_ Enreg': fields.char('L_Type_ Enreg', size=3),
            'N_Num_Affilie': fields.char('N_Num_Affilie', size=7),
            'Periode' : fields.char('Periode', size=6),
            'N_Num_Assure' : fields.char('N_Num_Assure', size=9),
            'L_Nom_Prenom' : fields.char('L_Nom_Prenom', size=60),
            'N_Enfants' : fields.char('N_Enfants ', size=2),
            'N_AF_A_Payer' : fields.char('N_AF_A_Payer', size=6),
            'N_AF_A_Deduire' : fields.char('N_AF_A_Deduire', size=6),
            'N_AF_Net_A_Payer' : fields.char('N_AF_Net_A_Payer', size=6),
            
            
        }
import_edbs()  
 
#la teledeclaration methode 2  "A02"  
class enreg_b02_2(osv.Model):
    
    _name =  'py.dacom.enreg_b02_2'
    def calcul(self, cr , uid ,field_name, field_value,ids,context=None):
        res = {}
        actuelle_ids = self.search(cr, uid , [('L_Type_ Enreg', '=', 'B02')])
        for record in self.browse(cr, uid ,actuelle_ids):
            #res[record.id]= int(situation(record.L_Situation))
            res[record.id] = int(record.N_Num_Assure) + int(record.N_AF_A_Reverser)+ int(record.N_Jours_Declares)+int(record.N_Salaire_Reel) +int(record.N_Salaire_Plaf) +int(situation(record.L_Situation))
        return res    
            

        
    def enrgi(self, cr , uid , ids,context):
        paie = self.pool.get('py.dacom.fiche_paie')
        edbs = self.pool.get('py.dacom.import_edbs')
        edbs_ids = edbs.search(cr, uid , [('L_Type_ Enreg', '=', 'A02')])
        ebds_obj = edbs.browse(cr, uid, edbs_ids, context=context)
        for record in ebds_obj:
            paie_ids = paie.search(cr, uid , [('num_assure', '=', record.N_Num_Assure)])
            paie_obj= paie.browse(cr, uid, paie_ids, context=context)
            for record1 in paie_obj:    
                    self.create(cr,uid,
                                {   
                                    'L_Type_ Enreg':"B02",
                                    'N_Num_Affilie': record.N_Num_Affilie,
                                    'Periode' : record.Periode,
                                    'N_Num_Assure' : record.N_Num_Assure,
                                    'L_Nom_Prenom' : record.L_Nom_Prenom,
                                    'N_Enfants' :record1.nombre_enfants,
                                    'N_AF_A_Payer' :record1.mnt_AF_payer,
                                    'N_AF_A_Deduire' :record1.mnt_AF_deduire,
                                    'N_AF_Net_A_Payer':record1.mnt_AF_net_payer,
                                    'N_AF_A_Reverser' :record1.mnt_AF_rev,
                                    'N_Jours_Declares':record1.nbr_dec,
                                    'N_Salaire_Reel':record1.sal_reel,
                                    'N_Salaire_Plaf':record1.sal_plafonne,
                                    'L_Situation':record1.situation,  
                                    #'S_Ctr': S_Ctr(j)                    
                                    
                                }
                            )
        return True
    _columns = {
            'periode_id_6':fields.many2one('py.dacom.periode'),
            'L_Type_ Enreg': fields.char('L_Type_ Enreg', size=3),
            'N_Num_Affilie': fields.char('N_Num_Affilie', size=7),
            'Periode' : fields.char('Periode', size=6),
            'N_Num_Assure' : fields.char('N_Num_Assure', size=9),
            'L_Nom_Prenom' : fields.char('L_Nom_Prenom', size=60),
            'N_Enfants' : fields.char('N_Enfants ', size=2),
            'N_AF_A_Payer' : fields.char('N_AF_A_Payer', size=6),
            'N_AF_A_Deduire' : fields.char('N_AF_A_Deduire', size=6),
            'N_AF_Net_A_Payer' : fields.char('N_AF_Net_A_Payer', size=6),
            'N_AF_A_Reverser' : fields.char('montant AF a reverser', size=64),
            'N_Jours_Declares' : fields.char('nombre de jours declare', size=64),
            'N_Salaire_Reel' : fields.char('salaire reel', size=64),
            'N_Salaire_Plaf':fields.char('sal plafonne', size=64),
            'L_Situation' : fields.char('Situation', size=64),
            'S_Ctr': fields.function(calcul,type='integer',digits=(16,2),obj='py.dacom.enreg_b02_2',method=True,store=True,string='S_Ctr'),
        }
enreg_b02_2() 



class enreg_b03(osv.Model):
    _name = 'py.dacom.enreg_b03'
    def enr(self,cr,uid,ids,periode_id,url,url_ebds,context):
        list_ids=[]
        print "periode :",periode_id
        periode_pool=self.pool.get('account.period')
        periode=periode_pool.browse(cr,uid,periode_id,context)
        periode_edbs = str(periode.name)
        periode_adapte = periode_edbs[3:] + periode_edbs[0:2]
        print 'periode name:',periode_adapte 
        enreg_b03_ids = self.search(cr, uid , [('L_Type_ Enreg', '=', 'B03')])
        enreg_b03_obj = self.browse(cr, uid,  enreg_b03_ids, context=context)
        for record in enreg_b03_obj:
            tele_to_send.get('cle_3').append("B03")
            tele_to_send.get('cle_3').append(record.N_Num_Affilie)
            tele_to_send.get('cle_3').append(record.N_Nbr_Salaries)
            tele_to_send.get('cle_3').append(record.Periode)
            tele_to_send.get('cle_3').append(record.N_T_Enfants)
            tele_to_send.get('cle_3').append(record.N_T_AF_A_Payer)
            tele_to_send.get('cle_3').append(record.N_T_AF_A_Reverser)
            tele_to_send.get('cle_3').append(record.N_T_Num_Imma)
            tele_to_send.get('cle_3').append(record.N_T_Jours_Declares)
            tele_to_send.get('cle_3').append(record.N_T_Salaire_Reel)
            tele_to_send.get('cle_3').append(record.N_T_Salaire_Plaf)
            tele_to_send.get('cle_3').append(record.N_T_Ctr)
        if(periode_adapte == self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds)[1],context)):
                enreg_ids =self.search(cr, uid , [('Periode', '=',periode_adapte )])
                self.unlink(cr, uid, enreg_ids, context=context)        
                id=self.create(cr,uid,
                        {   
                            'L_Type_ Enreg': "B03",
                            'N_Num_Affilie':self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds)[1],context),
                            'N_Nbr_Salaries' : self.pool.get('py.dacom.fichier_ebds').N_Nbr_Salaries(url_ebds),
                            'Periode' : periode_adapte,
                            'N_T_Enfants' :self.pool.get('py.dacom.paie').N_T_Enfants(cr,uid,ids,url,url_ebds,context=context),
                            'N_T_AF_A_Payer' :self.pool.get('py.dacom.paie').N_T_AF_A_Payer(cr,uid,ids,url,url_ebds,context=context),
                            'N_T_AF_A_Reverser' : self.pool.get('py.dacom.paie').N_T_AF_A_Reverser(cr,uid,ids,url,url_ebds,context=context),
                            'N_T_Num_Imma' :self.pool.get('py.dacom.paie').N_T_Num_Imma(cr,uid,ids,url,url_ebds,context=context),
                            'N_T_Jours_Declares':self.pool.get('py.dacom.paie').N_T_Jours_Declares(cr,uid,ids,url,url_ebds,context=context),
                            'N_T_Salaire_Reel':self.pool.get('py.dacom.paie').N_T_Salaire_Reel(cr,uid,ids,url,url_ebds,context=context),
                            'N_T_Salaire_Plaf':self.pool.get('py.dacom.paie').N_T_Salaire_Plaf(cr,uid,ids,url,url_ebds,context=context),
                            'N_T_Ctr':self.pool.get('py.dacom.paie').N_T_Ctr(cr,uid,ids,url,url_ebds,context=context),                  
                   } )
                list_ids.append(id)
                    
        return list_ids
                
         
              
    _columns = {
            #'code2': fields.many2one('fiche_paie', 'Point Of Sale', required=True),
            #'hb': fields.function( user ,type ='char'),
            'periode_id_5':fields.many2one('py.dacom.periode'),
            'L_Type_ Enreg': fields.char('L_Type_ Enreg', size=3),
            'N_Num_Affilie': fields.char('N_Num_Affilie', size=7),
            'Periode' : fields.char('Periode', size=6),
            'N_Nbr_Salaries' : fields.char('N_Nbr_Salaries', size=9),
            'N_T_Enfants' : fields.char('N_T_Enfants', size=60),
            'N_T_AF_A_Payer' : fields.char('N_T_AF_A_Payer', size=6),
            'N_T_AF_A_Reverser' : fields.char('N_T_AF_A_Reverser', size=6),
            'N_T_Num_Imma' : fields.char('N_T_Num_Imma', size=6),
            'N_T_Jours_Declares':fields.char('N_T_Jours_Declares', size=2),
            'N_T_Salaire_Reel':fields.char('N_T_Salaire_Reel', size=13),
            'N_T_Salaire_Plaf':fields.char('N_T_Salaire_Plaf', size=9),
            'N_T_Ctr':fields.char('N_T_Ctr', size=19),
            
        }
    
enreg_b03()   


    

class enreg_b04(osv.Model):
    _name = 'py.dacom.enreg_b04'
    def enre(self,cr,uid,ids,periode_id,url,url_ebds,context):
        list_ids=[]
        print "periode :",periode_id
        periode_pool=self.pool.get('account.period')
        periode=periode_pool.browse(cr,uid,periode_id,context)
        periode_edbs = str(periode.name)
        periode_adapte = periode_edbs[3:] + periode_edbs[0:2]
        dico= self.pool.get('py.dacom.paie').List_paie(cr,uid,ids,url,context=context)
        print 'periode name:',periode_adapte
        enreg_b04_ids = self.search(cr, uid , [('L_Type_ Enreg', '=', 'B04')])
        enreg_b04_obj = self.browse(cr, uid,  enreg_b04_ids, context=context)
        for record in enreg_b04_obj:
            tele_to_send.get('cle_4').append("B04")
            tele_to_send.get('cle_4').append(record.N_Num_Affilie)
            tele_to_send.get('cle_4').append(record.Periode)
            tele_to_send.get('cle_4').append(record.N_Num_Assure)
            tele_to_send.get('cle_4').append(record.L_Nom_Prenom)
            tele_to_send.get('cle_4').append(record.L_Num_CIN)
            tele_to_send.get('cle_4').append(record.N_Jours_Declares)
            tele_to_send.get('cle_4').append(record.N_Salaire_Reel)
            tele_to_send.get('cle_4').append(record.N_Salaire_Plaf)
            tele_to_send.get('cle_4').append(record.S_Ctr) 
        enreg_ids =self.search(cr, uid , [('Periode', '=',periode_adapte )])
        self.unlink(cr, uid, enreg_ids, context=context)   
        for j in self.pool.get('py.dacom.fichier_ebds').list_assu_entrants(cr,uid,ids,url,url_ebds,context):  
                if(periode_adapte == self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds)[1],context)):
                        k=self.pool.get('py.dacom.paie').ass_to_id( cr , uid , ids,url,j,context)
                        id=self.create(cr,uid,
                                {   
                                    'L_Type_ Enreg': "B04",
                                    'N_Num_Affilie': self.pool.get('py.dacom.fichier_ebds').N_Num_affilie_entrants(cr,uid,ids,url_ebds,context),
                                    'Periode' : periode_adapte,
                                    'N_Num_Assure' : self.pool.get('py.dacom.paie').N_Num_Assure_entrants( cr , uid , ids,url,j,context),
                                    'L_Nom_Prenom' : self.pool.get('py.dacom.paie').L_Nom_Prenom_entrants( cr , uid , ids,url,j,context),
                                    'L_Num_CIN' : dico['list_CIN_paie'][k],
                                    'N_Jours_Declares':dico['list_nbr_jour_dec_paie'][k],
                                    'N_Salaire_Reel':dico['list_sal_reel_paie'][k],
                                    'N_Salaire_Plaf':dico['list_sal_plaf_paie'][k],
                                    'S_Ctr': self.pool.get('py.dacom.fichier_ebds').S_Ctr(cr,uid,ids,url,url_ebds,j,context)                  
                           } )
                        list_ids.append(id)
                            
        return list_ids
        
    _columns = {
            #'code2': fields.many2one('fiche_paie', 'Point Of Sale', required=True),
            #'hb': fields.function( user ,type ='char'),
            'periode_id_7':fields.many2one('py.dacom.periode'),
            'L_Type_ Enreg': fields.char('L_Type_ Enreg', size=3),
            'N_Num_Affilie': fields.char('N_Num_Affilie', size=7),
            'Periode' : fields.char('Periode', size=6),
            'N_Num_Assure' : fields.char('N_Num_Assure', size=9),
            'L_Nom_Prenom' : fields.char('L_Nom_Prenome', size=60),
            'L_Num_CIN' : fields.char('L_Num_CIN ', size=8),
            'N_Jours_Declares':fields.char('N_Jours_Declares', size=2),
            'N_Salaire_Reel':fields.char('N_Salaire_Reel', size=13),
            'N_Salaire_Plaf':fields.char('N_Salaire_Plaf', size=9),
            'S_Ctr':fields.char('S_Ctr', size=19),
            
        }
enreg_b04()          



class enreg_b05(osv.Model):
    _name = 'py.dacom.enreg_b05'
    def enreg_b05(self,cr,uid,ids,periode_id,url,url_ebds,context):
        list_ids_enreg_b05=[]
        print "periode :",periode_id
        periode_pool=self.pool.get('account.period')
        periode=periode_pool.browse(cr,uid,periode_id,context)
        periode_edbs = str(periode.name)
        periode_adapte = periode_edbs[3:] + periode_edbs[0:2]
        print 'periode name:',periode_adapte 
        enreg_b05_ids = self.search(cr, uid , [('L_Type_ Enreg', '=', 'B05')])
        enreg_b05_obj = self.browse(cr, uid,  enreg_b05_ids, context=context)
        for record in enreg_b05_obj:
            tele_to_send.get('cle_5').append("B05")
            tele_to_send.get('cle_5').append(record.N_Num_Affilie)
            tele_to_send.get('cle_5').append(record.Periode)
            tele_to_send.get('cle_5').append(record.N_Nbr_Salaries)
            tele_to_send.get('cle_5').append(record.N_T_Num_Imma)
            tele_to_send.get('cle_5').append(record.N_T_Jours_Declares)
            tele_to_send.get('cle_5').append(record.N_T_Salaire_Reel)
            tele_to_send.get('cle_5').append(record.N_T_Salaire_Plaf)
            tele_to_send.get('cle_5').append(record.N_T_Ctr)
        if(periode_adapte == self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds)[1],context)):
            enreg_ids =self.search(cr, uid , [('Periode', '=',periode_adapte )])
            self.unlink(cr, uid, enreg_ids, context=context)   
            id=self.create(cr,uid,
                        {   
                            'L_Type_ Enreg': "B05",
                            'N_Num_Affilie': self.pool.get('py.dacom.fichier_ebds').N_Num_affilie_entrants(cr,uid,ids,url_ebds,context),
                            'Periode' : periode_adapte,
                            'N_Nbr_Salaries' : self.pool.get('py.dacom.paie').N_Nbr_Salaries_entrants(cr,uid,ids,url,url_ebds,context),
                            'N_T_Num_Imma' :self.pool.get('py.dacom.paie').N_T_Num_Imma_entrants(cr,uid,ids,url,url_ebds,context),
                            'N_T_Jours_Declares':self.pool.get('py.dacom.paie').N_T_Jours_Declares_entrants(cr,uid,ids,url,url_ebds,context),
                            'N_T_Salaire_Reel':self.pool.get('py.dacom.paie').N_T_Salaire_Reel_entrants(cr,uid,ids,url,url_ebds,context),
                            'N_T_Salaire_Plaf':self.pool.get('py.dacom.paie').N_T_Salaire_Plaf_entrants(cr,uid,ids,url,url_ebds,context),
                            'N_T_Ctr':self.pool.get('py.dacom.paie').N_T_Ctr_entrants(cr,uid,ids,url,url_ebds,context),                  
                   } )
            list_ids_enreg_b05.append(id)
        return list_ids_enreg_b05
                
         
              
    _columns = {
            #'code2': fields.many2one('fiche_paie', 'Point Of Sale', required=True),
            #'hb': fields.function( user ,type ='char'),
            'periode_id_9':fields.many2one('py.dacom.periode'),
            'L_Type_ Enreg': fields.char('L_Type_ Enreg', size=3),
            'N_Num_Affilie': fields.char('N_Num_Affilie', size=7),
            'Periode' : fields.char('Periode', size=6),
            'N_Nbr_Salaries' : fields.char('N_Nbr_Salaries', size=9),
            'N_T_Num_Imma' : fields.char('N_T_Num_Imma', size=6),
            'N_T_Jours_Declares':fields.char('N_T_Jours_Declares', size=2),
            'N_T_Salaire_Reel':fields.char('N_T_Salaire_Reel', size=13),
            'N_T_Salaire_Plaf':fields.char('N_T_Salaire_Plaf', size=9),
            'N_T_Ctr':fields.char('N_T_Ctr', size=19),
            
        }
enreg_b05()   


        

class enreg_b06(osv.Model):
    _name = 'py.dacom.enreg_b06'
    def enreg_b06(self,cr,uid,ids,periode_id,url,url_ebds,context):
        list_ids_enreg_b06=[]
        print "periode :",periode_id
        periode_pool=self.pool.get('account.period')
        periode=periode_pool.browse(cr,uid,periode_id,context)
        periode_edbs = str(periode.name)
        periode_adapte = periode_edbs[3:] + periode_edbs[0:2]
        print 'periode name:',periode_adapte
        enreg_b06_ids = self.search(cr, uid , [('L_Type_ Enreg', '=', 'B06')])
        enreg_b06_obj = self.browse(cr, uid,  enreg_b06_ids, context=context)
        for record in enreg_b06_obj:
            tele_to_send.get('cle_6').append("B06")
            tele_to_send.get('cle_6').append(record.N_Num_Affilie)
            tele_to_send.get('cle_6').append(record.Periode)
            tele_to_send.get('cle_6').append(record.N_Nbr_Salaries)
            tele_to_send.get('cle_6').append(record.N_T_Num_Imma)
            tele_to_send.get('cle_6').append(record.N_T_Jours_Declares)
            tele_to_send.get('cle_6').append(record.N_T_Salaire_Reel)
            tele_to_send.get('cle_6').append(record.N_T_Salaire_Plaf)
            tele_to_send.get('cle_6').append(record.N_T_Ctr) 
        if(periode_adapte == self.pool.get('py.dacom.fichier_ebds').Periode(cr,uid,ids,url_ebds,self.pool.get('py.dacom.fichier_ebds').list_num_assu_enreg_a02(url_ebds)[1],context)):
            enreg_ids =self.search(cr, uid , [('Periode', '=',periode_adapte )])
            self.unlink(cr, uid, enreg_ids, context=context)   
            id=self.create(cr,uid,
                        {   
                            'L_Type_ Enreg': "B06",
                            'N_Num_Affilie': self.pool.get('py.dacom.fichier_ebds').N_Num_affilie_entrants(cr,uid,ids,url_ebds,context),
                            'Periode' : periode_adapte,
                            'N_Nbr_Salaries' : self.pool.get('py.dacom.paie').N_Nbr_Salaries_global(cr,uid,ids,url,url_ebds,context),
                            'N_T_Num_Imma' :self.pool.get('py.dacom.paie').N_T_Num_Imma_global(cr,uid,ids,url,url_ebds,context),
                            'N_T_Jours_Declares':self.pool.get('py.dacom.paie').N_T_Jours_Declares_global(cr,uid,ids,url,url_ebds,context),
                            'N_T_Salaire_Reel':self.pool.get('py.dacom.paie').N_T_Salaire_Reel_global(cr,uid,ids,url,url_ebds,context),
                            'N_T_Salaire_Plaf':self.pool.get('py.dacom.paie').N_T_Salaire_Plaf_global(cr,uid,ids,url,url_ebds,context),
                            'N_T_Ctr':self.pool.get('py.dacom.paie').N_T_Ctr_global(cr,uid,ids,url,url_ebds,context),                  
                   } )
            list_ids_enreg_b06.append(id)
        return list_ids_enreg_b06
                
         
              
    _columns = {
            #'code2': fields.many2one('fiche_paie', 'Point Of Sale', required=True),
            #'hb': fields.function( user ,type ='char'),
            'periode_id_10':fields.many2one('py.dacom.periode'),
            'L_Type_ Enreg': fields.char('L_Type_ Enreg', size=3),
            'N_Num_Affilie': fields.char('N_Num_Affilie', size=7),
            'Periode' : fields.char('Periode', size=6),
            'N_Nbr_Salaries' : fields.char('N_Nbr_Salaries', size=9),
            'N_T_Num_Imma' : fields.char('N_T_Num_Imma', size=6),
            'N_T_Jours_Declares':fields.char('N_T_Jours_Declares', size=2),
            'N_T_Salaire_Reel':fields.char('N_T_Salaire_Reel', size=13),
            'N_T_Salaire_Plaf':fields.char('N_T_Salaire_Plaf', size=9),
            'N_T_Ctr':fields.char('N_T_Ctr', size=19),
            
        }
enreg_b06()   


#la recherche_perso_2 des personnel actifs dans la fiche de paie       
class recherche_perso_2(osv.Model):
    _name = 'py.dacom.recherche_perso_2'
    def trouver(self, cr , uid , ids, arg ,context =None):
        #res = {}
        actuelle = self.pool.get('fiche_paie')
        ancien_ids = actuelle.search(cr, uid , [('situation', '=', 'CS')])
        ancien_obj = actuelle.browse(cr, uid, ancien_ids, context=context)
        for record in ancien_obj:
            print record
            self.create(cr, uid,
                    {   
                        'ID': record.ID,
                        'CIN':record.CIN,
                        'num_assure':record.num_assure,
                        'nom_pre': record.nom_pre,
                        'nombre_enfants' : record.nombre_enfants,
                        'mnt_AF_payer' : record.mnt_AF_payer,
                        'mnt_AF_deduire' : record.mnt_AF_deduire,
                        'mnt_AF_net_payer' :record.mnt_AF_net_payer,
                        'mnt_AF_rev' :record.mnt_AF_rev,
                        'nbr_dec' : record.nbr_dec,
                        'sal_reel':record.sal_reel,
                        'sal_plafonne':record.sal_plafonne,
                        'situation' : record.situation
                    },
                    context=context
                )
        return True
    _columns = {
                    'periode_id_8':fields.many2one('py.dacom.periode'),
                    'ID': fields.char('ID', size=128),
                    'CIN':fields.char('CIN', size=128),
                    'num_assure': fields.char('Num Assure', size=128),
                    #'num_assure': fields.many2one('damancom.present', 'Point Of Sale', required=True),
                    'nom_pre': fields.char('nom et prenom', size=128),
                    'nombre_enfants' : fields.char('nombre enfants', size=64),
                    'mnt_AF_payer' : fields.char('montant AF a payer', size=64),
                    'mnt_AF_deduire' : fields.char('montant AF a deduire', size=64),
                    'mnt_AF_net_payer' : fields.char('montant AF net a payer ', size=64),
                    'mnt_AF_rev' : fields.char('montant AF a reverser', size=64),
                    'nbr_dec' : fields.char('nombre de jours declare', size=64),
                    'sal_reel' : fields.char('salaire reel', size=64),
                    'sal_plafonne':fields.char('sal plafonne', size=64),
                    'situation' : fields.char('Situation', size=64)
                
                }
recherche_perso_2()





