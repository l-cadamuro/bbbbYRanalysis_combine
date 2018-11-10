import ROOT
import numpy as np

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

A14tev = [2.100318379, 10.2, 0.287259045, 0.098882779, 1.321736614, -8.42431259, -1.388017366, 2.8, 0.518124457, -2.163473227, -0.550668596, 5.871490593, 0.296671491, -1.172793054, 0.653429812]
xsSM = 12.33 ### SM x BR in bbbb in fb

def functionGF(kl,kt,c2,cg,c2g,A):
    return A[0]*kt**4 + A[1]*c2**2 + (A[2]*kt**2 + A[3]*cg**2)*kl**2  + A[4]*c2g**2 + ( A[5]*c2 + A[6]*kt*kl )*kt**2  + (A[7]*kt*kl + A[8]*cg*kl )*c2 + A[9]*c2*c2g  + (A[10]*cg*kl + A[11]*c2g)*kt**2+ (A[12]*kl*cg + A[13]*c2g )*kt*kl + A[14]*cg*c2g*kl

def get_lim(tree, klambda):
    tree.GetEntry(2) ## entry for the 50% quantile
    lim = tree.limit
    qe = tree.quantileExpected
    if qe != 0.5:
        print " >> what is this quantile? ", qe, 'kl = ', klambda
        raise RuntimeError("cannot get limit")
    ## since histograms where scaled to the expected xs, I have to deconvolve the scaling to get the excluded xs
    xsr  = functionGF(klambda, 1, 0, 0, 0, A14tev)
    xs   = xsSM*xsr
    lim_xs = lim * xs

    return lim_xs

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
    channelLabel = ROOT.TLatex  (0.65, 0.8, "HH #rightarrow b#bar{b}b#bar{b}")
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
root_proto = '../cards/klscan/higgsCombinebbbb_result_{}.AsymptoticLimits.mH120.root'

points = list(np.arange(-5, 10, 0.25)) + [10.] ### and endpoint by hand
print points

lims = []
lims_valid = [] ### just to get the minimum
goodfit = []

# HH_kl_p_5d75
for kl in points:
    name = '{:g}'.format(kl).replace('.', 'd')
    if '-' in name: name = name.replace('-', 'm_')
    else: name = 'p_' + name
    name = 'HH_kl_' + name
    # print name

    rootfile = ROOT.TFile.Open(root_proto.format(name))
    tree     = rootfile.Get('limit')

    tree.GetEntry(0)

    # dll_r0 = tree_r0.deltaNLL
    # dll_r1 = tree_r1.deltaNLL

    lim = get_lim(tree, kl)

    # if not dll_r0 or not dll_r1:
    #     print "*** point ", kl, ' has an invalid fit, r=0 -> ', dll_r0, 'r=1 -> ', dll_r1, ' ... skipping'
    #     print "    >>> file r0 is", root_proto.format(0, name)
    #     print "    >>> file r1 is", root_proto.format(1, name)
    #     deltaLL.append(None)
    #     goodfit.append(False)
    # else:
    # dll = dll_r1 - dll_r0
    lims.append(lim)
    lims_valid.append(lim)
    goodfit.append(True)

    
### now make the plot
c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)
c1.SetBottomMargin(0.13)
c1.SetLeftMargin(0.13)

gr = ROOT.TGraph()
for ipt in range(0, len(points)):
    if not goodfit[ipt]: continue
    gr.SetPoint(gr.GetN(), points[ipt], lims[ipt])
gr.SetMarkerStyle(8)
gr.SetMarkerSize(0.8)

xmin = -5
xmax = 10
# frame = ROOT.TH1D('frame', ';k_{#lambda};95% CL u.l. on #sigma #times #bf{#it{#Beta}} (gg#rightarrowHH#rightarrowbbbb)', 100, xmin, xmax)
frame = ROOT.TH1D('frame', ';k_{#lambda};#sigma (gg#rightarrowHH) #times #bf{#it{#Beta}}(HH#rightarrowb#bar{b}b#bar{b}) [fb]', 100, xmin, xmax)
frame.SetMinimum(0)
frame.SetMaximum(300)
frame.GetXaxis().SetTitleSize(0.05)
frame.GetYaxis().SetTitleSize(0.05)
frame.GetXaxis().SetTitleOffset(1.25)
frame.GetYaxis().SetTitleOffset(1.25)
frame.Draw()
gr.Draw('PLsame')

### now draw the expected xs
theo_points  = list(np.arange(-5, 10, 0.25/5.)) + [10.] ### finer grid, and endpoint by hand
theo_cent    = [xsSM*functionGF(kl,1,0,0,0, A14tev) for kl in theo_points]
theo_up      = [(1.+2.1/100.)*xsSM*functionGF(kl,1,0,0,0, A14tev) for kl in theo_points]
theo_down    = [(1.-4.9/100.)*xsSM*functionGF(kl,1,0,0,0, A14tev) for kl in theo_points]

gr_cent = ROOT.TGraph()
gr_band = ROOT.TGraphAsymmErrors()
for ipt in range(0, len(theo_points)):
    x = theo_points[ipt]
    y = theo_cent[ipt]
    yup   = theo_up[ipt]
    ydown = theo_down[ipt]
    gr_cent.SetPoint(ipt, x, y)
    gr_band.SetPoint(ipt, x, y)
    gr_band.SetPointError(ipt, 0,0, y-ydown,yup-y)

gr_band.SetFillStyle(3001)
gr_band.SetFillColor(ROOT.kRed)
gr_cent.SetLineColor(ROOT.kRed+1)
gr_band.SetLineColor(ROOT.kRed+1)

gr_band.Draw('e3 same')
gr_cent.Draw('l same')

### now the legend
leg = ROOT.TLegend(0.15, 0.7, 0.65, 0.88)
# leg.SetFillColor(ROOT.kWhite)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.SetHeader('95% CL upper limits')
leg.AddEntry(gr, "Median expected", "pl")
leg.AddEntry(None, '', '')
leg.AddEntry(gr_band, "Theoretical prediction", "lf")
leg.Draw()

# ### lines
# sigmas = [1,2]
# lines = []
# for s in sigmas:
#     l = ROOT.TLine(xmin, s*s, xmax, s*s)
#     l.SetLineStyle(7)
#     l.SetLineWidth(1)
#     l.SetLineColor(ROOT.kGray)
#     lines.append(l)
# for l in lines: l.Draw()

# ## text for sigmas
# labels = []
# for s in sigmas:
#     lab = ROOT.TLatex(xmax + 0.03*(xmax-xmin), s*s, "%.0f#sigma" % s)
#     lab.SetTextFont(42)
#     lab.SetTextColor(lines[0].GetLineColor())
#     lab.SetTextSize(0.04)
#     labels.append(lab)
# for l in labels: l.Draw()

et = extra_texts()
for t in et: t.Draw()


c1.Print('klambda_limit_scan.pdf', 'pdf')