INPUT_FILE="/afs/cern.ch/work/l/lcadamur/private/YR_bbbb_analysis/CMSSW_9_3_2/src/bbbbYRanalysis/histofiller/bbbbAnalysis/various_plots_BDTallBkg_lepveto2/analysedOutPlotter.root"
var="BDTG_6_masscut"
sel="finalsel_SR"
cardname="bbbb_datacard.txt"
QCDsyst="0.5"

echo "doing the final card"
echo "INPUT_FILE: $INPUT_FILE"
echo "var: $var"
echo "sel: $sel"
echo "cardname: $cardname"
echo "QCDsyst: $QCDsyst"

python make_datacard.py --var $var --sel $sel --cardOut cards/${cardname} --fileIn ${INPUT_FILE} --QCDsyst ${QCDsyst}