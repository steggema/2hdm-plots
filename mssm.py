import ROOT
from tdrstyle import setTDRStyle
style = setTDRStyle()
style.SetPalette(ROOT.kFuchsia)
ROOT.TColor.InvertPalette()
style.SetNumberContours(256)

# br_file = '/Users/jan/Downloads/hMSSM_13TeV.root'
# mssm = 'hMSSM'
br_file = '/Users/jan/Downloads/mh125EFT_13.root'
mssm = 'mH125EFT'


br = 'A_Zh'
f = ROOT.TFile.Open(br_file)
h = f.Get(f'br_{br}')

style.cd()
cv = ROOT.TCanvas()

h.UseCurrentStyle()
h.GetXaxis().SetTitle('m_{A} [GeV]')
h.GetXaxis().SetNdivisions(505)
h.GetYaxis().SetTitle('tan #beta')
h.GetYaxis().SetRangeUser(1., 20.)
h.GetXaxis().SetRangeUser(200., 1000.)
h.SetContour(40)
h.Draw('COLZ')


latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextAlign(11)
latex.SetNDC()

l = cv.GetLeftMargin()
t = cv.GetTopMargin()

latex.DrawLatex(l + 0.02, 1-t + 0.02, f'{mssm}')

cv.SaveAs(f'B_{br}_{mssm}.pdf')
cv.SaveAs(f'B_{br}_{mssm}.root')
