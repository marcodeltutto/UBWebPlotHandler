#!/usr/bin/env python

import config

import os
import json
from time import strftime


# Ensure closing tag is written. Don't use for standalone tags like <img>
class Tag:
    # **kwargs seems like a nice idea here. Except "class" is a common thing to
    # want and is a reserved word :(
    def __init__(self, fout, tag, args = {}):
        self._fout = fout
        self._tag = tag
        self._args = args

    def __enter__(self):
        self._fout.write('<'+self._tag)

        for key in self._args:
            self._fout.write(' '+key+'="'+self._args[key]+'"')
        self._fout.write('>')

    def __exit__(self, a, b, c):
        self._fout.write('</'+self._tag+'>')


header = '''<!DOCTYPE html>
<!--#set var="META_TITLE" value="MicroBooNE | Analysis Tools"-->
<!--#set var="PAGE_HEADER" value="MicroBooNE at Work"-->
<!--#set var="BODY_CLASSES" value="section-default"-->

<!--#include virtual="/fnalincludes/wide-page-top.html"-->
<!--//***********************************************************
************ DO NOT REMOVE CODE ABOVE ***************************
*************************************************************//-->

<script src="https://unpkg.com/masonry-layout@4/dist/masonry.pkgd.min.js"></script>

    
<script>
function Hide()
{
  document.getElementById("showbutton").hidden = false;
  document.getElementById("hidebutton").hidden = true;

  cs = document.getElementsByClassName("caption")
  for(var i = 0; i < cs.length; i++){
    cs[i].hidden = true;
  }
}

function Show()
{
  document.getElementById("hidebutton").hidden = false;
  document.getElementById("showbutton").hidden = true;

  cs = document.getElementsByClassName("caption")
  for(var i = 0; i < cs.length; i++){
    cs[i].hidden = false;
  }
}


</script>

<script type="text/x-mathjax-config">
  MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$']]}});
</script>
<script type="text/javascript"
  src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>


<style>
.plot
  {
    width: 29%;
    display: inline-block;
    text-align: center;
    //border: 2px solid gray;
    background-color: white;
    padding: 5px;
    margin: 5px;
    vertical-align: top
  }
</style>



'''

header2 = '''
<div style="position:fixed;right:0;top:0">
  <button type="button" title="Hide" onclick="Hide()" id="hidebutton">Hide captions</button>
  <button type="button" title="Show" onclick="Show()" hidden id="showbutton">Show captions</button>
</div>
'''

def footer():
    footer = '\n\n<hr>\nLast updated '+strftime('%Y-%m-%d %H:%M:%S %Z') + '''
<!--//***********************************************************
************ DO NOT REMOVE CODE BELOW *************************** 
*************************************************************//-->

<!--//========== Last Modifed ==========//-->
<div class="last-modified">
    <div class="last-modified-inner">
        <ul>
                <li class="first title">Last modified</li>
                        <li class="date"><!-- #BeginDate format:Am3 --><!--#config timefmt="%m/%d/%Y" --><!--#echo var="LAST_MODIFIED"--><!-- #EndDate --></li>
                <li class="last email"><a href="http://www.fnal.gov/pub/contact/email.html">email Fermilab</a></li>
        </ul>
    </div><!-- /.last-modified-inner -->
</div><!-- /.last-modified -->
<!--//========== END: Last Modifed ==========//-->

<!--#include virtual="/fnalincludes/page-bottom.html"-->
'''
    return footer


def AddFile(fout, deets, f):
    thumb = 'plots/'+str(deets['id'])+'/thumbs/'+f['base']+'_thumb.png'

    fout.write('\n')

    with Tag(fout, 'div', {'class': 'plot'}):
        with Tag(fout, 'div', {'class': 'thumbnail'}):
            fout.write('<img src="'+thumb+'" width="100%"><br>\n')
            with Tag(fout, 'center'):
                for ext in f['exts']:
                    with Tag(fout, 'a', {'href': 'plots/'+str(deets['id'])+'/'+f['base']+'.'+ext}):
                        fout.write('['+ext+']')
                    fout.write('\n')
                if config.SHOW_CAPTION:  
                    with Tag(fout, 'p', {'class': 'caption'}):
                        fout.write(f['caption'])

    fout.write('\n\n')


page_cfg = json.load(file(config.BLESSED_PLOTS))
doc_deets = json.load(file(config.WEB_PATH + config.JSON_FILENAME))

allNos = [d['id'] for d in doc_deets]
allCatNos = [[n for n in page['docs']] for page in page_cfg]
allCatNos = sum(allCatNos, []) # flatten
new = [n for n in allNos if n not in allCatNos]

# Synthesize a "New" page at the top
if len(new) > 0:
    page_cfg = [{'category': 'New / uncategorized',
                 'docs': new,
                 'caption': 'Plots that have not yet been categorized. Please edit BlessedPlots.json to do so.'}] + page_cfg


fout_main = open(config.WEB_PATH + '/index.html', 'w')
fout_main.write(header)

with Tag(fout_main, 'h1'):
    fout_main.write('MicroBooNE Approved Plots')

with Tag(fout_main, 'h4'):
    fout_main.write('This page shows MicroBooNE plots that have been approved by the MicroBooNE collaboration to be shown publicly.<br><br>')

for page in page_cfg:
    cat = page['category']
    safe_cat = cat.replace(' ', '_').replace('/', 'and')

    with Tag(fout_main, 'div', {'class': 'plot'}):
        with Tag(fout_main, 'div', {'class': 'thumbnail'}):
            with Tag(fout_main, 'h2'):
                fout_main.write(cat)
            if 'thumb' in page:
                fout_main.write('<img src="plots/'+page['thumb']+'" width="100%">')
            with Tag(fout_main, 'p', {'class': 'test'}):
                if 'caption' in page:
                    fout_main.write(page['caption'])
            with Tag(fout_main, 'p', {'class': 'test'}):
                with Tag(fout_main, 'a', {'class': 'btn btn-default', 'href': safe_cat+'.html', 'role': 'button'}):
                    fout_main.write('View plots &raquo;')
                

        fout_main.write('\n')

    # Now write pages for each category
    fout_sub = open(config.WEB_PATH + '/' + safe_cat+'.html', 'w')
    fout_sub.write(header)
    fout_sub.write(header2)
    with Tag(fout_sub, 'h1'): fout_sub.write(cat)

    for docNo in page['docs']:
        deets = [d for d in doc_deets if d['id'] == docNo]
        if len(deets) == 0:
            print 'No info for doc', docNo, 'skipping'
            continue
        assert len(deets) == 1
        deets = deets[0]

        with Tag(fout_sub, 'h2'):
            with Tag(fout_sub, 'a', {'href': deets['url']}):
                fout_sub.write('docdb '+str(docNo))
                fout_sub.write(' - '+deets['title'])

        fout_sub.write('\n')

        with Tag(fout_sub, 'div'):
            for f in deets['files']:
                AddFile(fout_sub, deets, f)
            with Tag(fout_sub, 'div', {'class': 'clearfix'}): # a clear way to go to newline
                fout_sub.write(' ')

    fout_sub.write(footer())

fout_main.write(footer())

# Now copy the css style 
os.system('cp ./offcanvas.css ' + config.WEB_PATH)


