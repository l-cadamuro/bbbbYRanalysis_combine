INPUT_FILE="/afs/cern.ch/work/l/lcadamur/private/YR_bbbb_analysis/CMSSW_9_3_2/src/bbbbYRanalysis/histofiller/bbbbAnalysis/various_plots_BDTallBkg/analysedOutPlotter.root"
for var in BDTG_6_masscut; do
    for sel in finalsel_SR; do
        for qcdsyst in 0.0000000001 0.1 0.25 0.5 1.0 2.0 5.0 10.0; do ### uncertainty will be unc = 1/n [%] because the histo bin unc. is 1% and combine expresses this in terms of sigmas 
            cardname=card_${var}_${sel}_syst${qcdsyst}.txt
            wsname=card_${var}_${sel}_syst${qcdsyst}.root
            oname=${var}_${sel}_syst${qcdsyst}
            echo ""
            echo ""
            echo ".... making card for var: $var, sel: $sel, qcdsyst: $qcdsyst"
            python make_datacard.py --var $var --sel $sel --cardOut cards/${cardname} --fileIn ${INPUT_FILE} --QCDsyst ${qcdsyst}
            echo ".... making workspace"
            cd cards/
            text2workspace.py ${cardname}
            combine -M Significance  -t -1 --expectSignal 1 -n ${oname} ${wsname}
            cd ..
        done
    done
done
