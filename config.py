import os         #/// Interact with OS

#///////////////////////////////////////////////////////////////////////////////
# User Configuration
WEB_PATH      = '/web/sites/m/microboone-exp.fnal.gov/htdocs/public/approved_plots/'
JSON_FILENAME = 'BlessedPlotsMeta.json'
PLOT_SUBDIR   = 'plots/'
BLESSED_PLOTS = './BlessedPlots.json'
DOCDB_URL     = 'http://microboone-docdb.fnal.gov:8080/cgi-bin/'
REGENERATE    = False
PWD           = open(os.environ['UBDOCPWDFILE'], 'r').readlines()[0].strip()
SHOW_CAPTION  = False

EXTS          = ['.txt', '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.eps', '.ps', '.C', '.tar.gz', '.zip']
