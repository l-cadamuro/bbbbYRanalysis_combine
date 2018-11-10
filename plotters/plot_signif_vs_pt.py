import ROOT
ROOT.gROOT.SetBatch(True)

plot_loss = True
do_y_in_percent=True ## only  if plotting loss
fIn_proto = '../cards/higgsCombineBDTG_nomasscut_{}.Significance.mH120.root'

sels = [
    ('baseline_SR' , 45), 
    ('baseline50_SR' , 50), 
    ('baseline55_SR' , 55), 
    ('baseline60_SR' , 60), 
    ('baseline65_SR' , 65), 
    ('baseline70_SR' , 70), 
    # ('baseline75_SR' , 75), 
    ('baseline80_SR' , 80), 
]

sigs = []

for idx in range(len(sels)):
    sel   = sels[idx][0]
    pt    = sels[idx][1]
    fname = fIn_proto.format(sel)
    print ">> opening file", fname
    fIn   = ROOT.TFile.Open(fname)
    tIn   = fIn.Get('limit')
    tIn.GetEntry(0)
    sig   = tIn.GetLeaf('limit').GetValue()
    sigs.append(sig)
    fIn.Close()

print sigs

## make the plot
c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)
c1.SetBottomMargin(0.13)
c1.SetLeftMargin(0.13)

gr = ROOT.TGraph()
for idx in range(len(sigs)):
    x = sels[idx][1]
    if plot_loss:
        y = 1. - sigs[idx]/sigs[0]
        if do_y_in_percent:
            y = 100.*y
    else: # plot directly signif
        y = sigs[idx]
    gr.SetPoint(idx, x, y)
gr.SetMarkerStyle(8)
gr.SetMarkerSize(1.2)
gr.SetMarkerColor(ROOT.kBlue)
gr.SetLineColor(ROOT.kBlue)
gr.Draw('APL')
gr.GetXaxis().SetTitle("Minimum jet p_{T} threshold [GeV]")
if plot_loss:
    gr.GetYaxis().SetTitle("Loss in signal significance")
    if do_y_in_percent:
        gr.GetYaxis().SetTitle("Loss in signal significance [%]")
else:
    gr.GetYaxis().SetTitle("Signal significance")
gr.GetXaxis().SetTitleSize(0.05)
gr.GetYaxis().SetTitleSize(0.05)
gr.GetXaxis().SetTitleOffset(1.25)
gr.GetYaxis().SetTitleOffset(1.25)
gr.Draw('APL')

### extra text
cmstextfont   = 61  # font of the "CMS" label
cmstextsize   = 0.05  # font size of the "CMS" label
chantextsize = 18
extratextfont = 52     # for the "preliminary"
extratextsize = 0.76 * cmstextsize # for the "preliminary"
lumitextfont  = 42
cmstextinframe = False

yoffset = -0.046

lumibox = ROOT.TLatex  (0.9, 0.964+yoffset, "3000 fb^{-1} (14 TeV)")
lumibox.SetNDC()
lumibox.SetTextAlign(31)
lumibox.SetTextSize(extratextsize)
lumibox.SetTextFont(lumitextfont)
lumibox.SetTextColor(ROOT.kBlack)

# xpos  = 0.177
xpos  = 0.137
if cmstextinframe:
    ypos  = 0.94 ## inside the frame
else:
    ypos  = 0.995  ## ouside the frame
CMSbox = ROOT.TLatex  (xpos, ypos+yoffset+0.01, "CMS")       
CMSbox.SetNDC()
CMSbox.SetTextSize(cmstextsize)
CMSbox.SetTextFont(cmstextfont)
CMSbox.SetTextColor(ROOT.kBlack)
CMSbox.SetTextAlign(13) ## inside the frame

# simBox = ROOT.TLatex  (xpos, ypos - 0.05+yoffset, "Simulation")
simBox = ROOT.TLatex  (xpos + 0.12, ypos+yoffset, "HL-LHC projection")
simBox.SetNDC()
simBox.SetTextSize(extratextsize)
simBox.SetTextFont(extratextfont)
simBox.SetTextColor(ROOT.kBlack)
simBox.SetTextAlign(13)


channelLabel = ROOT.TLatex  (0.2, 0.8, "HH #rightarrow b#bar{b}b#bar{b}")
channelLabel.SetNDC()
# channelLabel.SetTextAlign(31)
channelLabel.SetTextSize(1.15*extratextsize)
channelLabel.SetTextFont(lumitextfont)
channelLabel.SetTextColor(ROOT.kBlack)


lumibox.Draw()
CMSbox.Draw()
simBox.Draw()
channelLabel.Draw()

c1.Print('sig_vs_pt.pdf', 'pdf')

# c1.Update()
# raw_input()