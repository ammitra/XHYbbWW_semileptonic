import ROOT
from TIMBER.Analyzer import analyzer, HistGroup
from TIMBER.Tools.Plot import *
from collections import OrderedDict

ROOT.gROOT.SetBatch(True)

####################################
# Store some global variables here #
####################################
# For now, just look at 2018 (there won't be much variation between years)
year = 18
# store the file name and the LaTeX title in a dict
signals = {
	'XHY-300-125_{}'.format(year) : 'm_{X}=300, m_{Y}=125 (GeV)',
        'XHY-500-300_{}'.format(year) : 'm_{X}=500, m_{Y}=300 (GeV)',
        'XHY-1000-400_{}'.format(year) : 'm_{X}=1000, m_{Y}=400 (GeV)',
        'XHY-3000-500_{}'.format(year) : 'm_{X}=3000, m_{Y}=500 (GeV)',
        'XHY-3500-500_{}'.format(year) : 'm_{X}=3500, m_{Y}=500 (GeV)',
        'XHY-4000-1000_{}'.format(year) : 'm_{X}=4000, m_{Y}=1000 (GeV)'
}

# store the colors to plot them
colors = {
        'XHY-300-125_{}'.format(year) : ROOT.kRed,
        'XHY-500-300_{}'.format(year) : ROOT.kBlue,
        'XHY-1000-400_{}'.format(year) : ROOT.kBlack,
        'XHY-3000-500_{}'.format(year) : ROOT.kYellow,
        'XHY-3500-500_{}'.format(year) : ROOT.kGreen,
        'XHY-4000-1000_{}'.format(year) : ROOT.kOrange
}

# Store the variables you want to plot, along with their LaTeX titles
varnames = {
    	'nElectron':'nElectron',
	'nMuon':'nMuon',
	'Electron_pt':'Electron p_{T}',
	'Muon_pt':'Muon p_{T}',
        'FatJet_msoftdrop': 'FatJet m_{#text{SD}}',
        'FatJet_pt':'FatJet p_{T}',
        'DeltaPhi_jets':'#Delta #phi j_{0},j_{1}',
        'DeltaPhi_Electron_Higgs':'#Delta #phi e^{-}_{1},j_{0}',
        'DeltaPhi_Muon_Higgs':'#Delta #phi #mu^{-}_{1},j_{0}',
        'DeltaPhi_Electron_Wqq':'#Delta #phi e^{-}_{1},j_{0}',
        'DeltaPhi_Muon_Wqq':'#Delta #phi #mu^{-}_{1},j_{0}',
        'MET_pt':'p_{T}^{miss}',
	'MET_phi':'p_{T}^{miss} #phi'
}

if __name__=="__main__":
    # store the histograms we want to track
    histgroups = {}
    for s in signals.keys():
	inFile = ROOT.TFile.Open('{}.root'.format(s),'READ')
	# Put histograms into the HistGroups
	histgroups[s] = HistGroup(s)
	for key in inFile.GetListOfKeys():	# loop over histograms in the file
	    varname = key.GetName()		# gets the histogram name 
	    inhist = inFile.Get(key.GetName()) 	# get it from the file
	    inhist.SetDirectory(0) # set the directory so hist is stored in memory and not as reference to TFile (this way it doesn't get tossed by python garbage collection when infile changes)
	    histgroups[s].Add(varname,inhist) # add to our group
	    print('Added {} distribution for signal {}'.format(varname, s))
	inFile.Close()


    ''' 
    # You can treat the histgroup just like a nested dictionary, i.e. 
    for i in histgroups.keys():
	# this will print the signal name
	print(i)
        for j in histgroups[i].keys():
	    # this will print the variable name (e.g. lead_tau32)
	    print(j)
    '''	

    # Now plot the variables up in the global definitions above
    for varname in varnames.keys():
	plot_filename = '{}.png'.format(varname)
	signal_hists = {}
	for sig in signals.keys():
	    signal_hists[sig] = histgroups[sig][sig+'_'+varname] 

	# Plot everything together!
	CompareShapes(
	    outfilename = plot_filename,
	    year = 18,	# HARD CODED - CHANGE THIS 
	    prettyvarname = varnames[varname],
	    signals = signal_hists,
	    colors = colors,
	    names = signals,
	    scale = False,
	    logy = False, # Whether or not to plot with log y
	    doSoverB = False, # not plotting bkgs, so signal/background will be impossible
	)	
