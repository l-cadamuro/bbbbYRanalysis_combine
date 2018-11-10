import ROOT
import numpy as np

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

### a bit euristhic, but I notice that
### r is also saved in the output -> need to ask that it matches
### if the fit fails, the points *may* miss -> return None
def get_NLL(tree, r):
    dll = None
    for i in range (0, tree.GetEntries()):
        tree.GetEntry(i)
        if tree.r == r:
            dll = tree.deltaNLL
            break
    return dll

def extra_texts():
    # print "... drawing extra texts"
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


    # channelLabel = ROOT.TLatex  (0.2, 0.8, "HH #rightarrow b#bar{b}b#bar{b}")
    channelLabel = ROOT.TLatex  (0.6, 0.8, "HH #rightarrow b#bar{b}b#bar{b}")
    channelLabel.SetNDC()
    # channelLabel.SetTextAlign(31)
    channelLabel.SetTextSize(1.15*extratextsize)
    channelLabel.SetTextFont(lumitextfont)
    channelLabel.SetTextColor(ROOT.kBlack)


    return [lumibox, CMSbox, simBox, channelLabel]
    # lumibox.Draw()
    # CMSbox.Draw()
    # simBox.Draw()
    # channelLabel.Draw()


###
root_proto = '../cards/klscan/higgsCombinebbbb_result_r{}_{}.MultiDimFit.mH120.root'

points = list(np.arange(-5, 10, 0.25)) + [10.] ### and endpoint by hand
print points

deltaLL = []
deltaLL_valid = [] ### just to get the minimum
goodfit = []

# HH_kl_p_5d75
for kl in points:
    name = '{:g}'.format(kl).replace('.', 'd')
    if '-' in name: name = name.replace('-', 'm_')
    else: name = 'p_' + name
    name = 'HH_kl_' + name
    # print name

    rootfile_r0 = ROOT.TFile.Open(root_proto.format(0, name))
    rootfile_r1 = ROOT.TFile.Open(root_proto.format(1, name))

    tree_r0 = rootfile_r0.Get('limit')
    tree_r1 = rootfile_r1.Get('limit')

    tree_r0.GetEntry(1) ## for some reason, entry 0 is for r = 20
    tree_r1.GetEntry(1) ## for some reason, entry 0 is for r = 20

    # dll_r0 = tree_r0.deltaNLL
    # dll_r1 = tree_r1.deltaNLL

    dll_r0 = get_NLL(tree_r0, 0)
    dll_r1 = get_NLL(tree_r1, 1)

    if not dll_r0 or not dll_r1:
        print "*** point ", kl, ' has an invalid fit, r=0 -> ', dll_r0, 'r=1 -> ', dll_r1, ' ... skipping'
        print "    >>> file r0 is", root_proto.format(0, name)
        print "    >>> file r1 is", root_proto.format(1, name)
        deltaLL.append(None)
        goodfit.append(False)
    else:
        dll = dll_r1 - dll_r0
        deltaLL.append(dll)
        deltaLL_valid.append(dll)
        goodfit.append(True)

### find the global minimun and scale everything
mmin = min(deltaLL_valid)
deltaLL = [x - mmin if x else x for x in deltaLL]
# now apply a factor of 2 -> 2 delta log(l)
deltaLL = [2.*x if x else x for x in deltaLL]
    
### now make the plot
c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)
c1.SetBottomMargin(0.13)
c1.SetLeftMargin(0.13)

gr = ROOT.TGraph()
for ipt in range(0, len(points)):
    if not goodfit[ipt]: continue
    gr.SetPoint(gr.GetN(), points[ipt], deltaLL[ipt])
gr.SetMarkerStyle(8)
gr.SetMarkerSize(0.8)

xmin = -5
xmax = 10
frame = ROOT.TH1D('frame', ';k_{#lambda};-2#Deltaln(L)', 100, xmin, xmax)
frame.SetMinimum(0)
frame.SetMaximum(10)
frame.GetXaxis().SetTitleSize(0.05)
frame.GetYaxis().SetTitleSize(0.05)
frame.GetXaxis().SetTitleOffset(1.25)
frame.GetYaxis().SetTitleOffset(1.25)
frame.Draw()
gr.Draw('PLsame')

### lines
sigmas = [1,2]
lines = []
for s in sigmas:
    l = ROOT.TLine(xmin, s*s, xmax, s*s)
    l.SetLineStyle(7)
    l.SetLineWidth(1)
    l.SetLineColor(ROOT.kGray)
    lines.append(l)
for l in lines: l.Draw()

## text for sigmas
labels = []
for s in sigmas:
    lab = ROOT.TLatex(xmax + 0.03*(xmax-xmin), s*s, "%.0f#sigma" % s)
    lab.SetTextFont(42)
    lab.SetTextColor(lines[0].GetLineColor())
    lab.SetTextSize(0.04)
    labels.append(lab)
for l in labels: l.Draw()

et = extra_texts()
for t in et: t.Draw()

c1.Print('klambda_scan.pdf', 'pdf')