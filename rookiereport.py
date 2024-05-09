#!/usr/bin/env python3
"""
Extract a summary of ROOKIE activity from the database. The submitted
log must have 'ROOKIE' in the log header CATEGORY-OVERLAY: field.
"""
DEBUG = True

from rookiereport.__init__ import VERSION
from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from datetime import datetime
from htmlutils.htmldoc import *
#from cabrilloutils.CabrilloUtils import CabrilloUtils

class rookieReport(): 
    def __init__(self, args = None):
        self.args = args
        if args:
            self.appMain(args)
            
    def appMain(self, args):
        if args.location:
            #r = self.getRookies(args.location)
            #t=self.buildTSV(r)
            self.displayLog()
            
    def buildTSV(self, rookies):
        """Build TSV report from rookie db data."""
        TSV = ['CALLSIGN\tLOCATION\tQSOs\tSCORE']
        if rookies:
            for r in rookies:
                TSV.append('{}\t{}\t{}\t{}'.format(\
                             r['CALLSIGN'],
                             r['LOCATION'],
                             r['QSOS'],
                             r['SCORE']))
        return TSV
                
    def displayLog(self, data=None):
        if data == None:
            data = self.buildTSV(self.getRookies(self.args.location))
            if self.args.reportType == 'html':
                data = self.buildHTML(data)
            else:
                for l in data:
                    print(l)            
 
    def getRookies(self, location):
        db= MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
        db.setCursorDict()
        query = """SELECT * FROM ROOKIE_VIEW """
        if location == 'mo':
            query += """WHERE `LOCATION` = 'MO' """
        elif location =='non-mo':
            query += """WHERE `LOCATION` != 'MO' """
        query += """ORDER BY `SCORE` DESC"""
        """
        Get rookies from database - currently requires the view 
        ROOKIE_VIEW to exist. Should probably add code to create it
        if it's not in the database already.
        """
        rookies = db.read_query(query) 
        return rookies  
        
    def buildHTML(self, data):
        htmld = self.makeHTML(data)
        #print (htmd)
        d = htmlDoc()
        d.openHead(\
           '{} Missouri QSO Rookie Report'\
               .format(YEAR),'./styles.css')
        d.closeHead()
        d.openBody()
        d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
        d.add_unformated_text(\
           """<h2 align='center'>{} Missouri QSO Party Rookie Report</h2>\n""".format(YEAR))

        d.addTable(htmld, header=True, caption =\
            """{} Rookie report</p> """.\
            format(self.args.location.upper()))

        d.closeBody()
        d.closeDoc()

        d.showDoc()

    def makeHTML(self, csvd):
        htmd = []
        for crow in csvd:
            hrow = crow.split('\t')
            htmd.append(hrow)
        #print(htmd)
        return htmd
        
