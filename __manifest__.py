{
    'name':'Hospital Management',
    'version':'13.0.1.0.0',
    'category':'Extra Tools',
    'summary':'Module for Hospital management',
    'sequence':'10',
    'license':'AGPL-3',
    'author':'haris',
    'maintainer':'haris',
    'website':'haris.com',
    'depends':['mail','sale'],
    'demo':[],
    'data':[
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/appointment.xml',
        'views/patient.xml',
        'reports/report.xml',
        'reports/patient_card.xml'
    ],
    'installable':True,
    'application':True,
    'auto_install':False,

}