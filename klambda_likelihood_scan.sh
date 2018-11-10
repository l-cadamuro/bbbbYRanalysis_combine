INPUT_FILE="/afs/cern.ch/work/l/lcadamur/private/YR_bbbb_analysis/CMSSW_9_3_2/src/bbbbYRanalysis/histofiller/bbbbAnalysis/various_plots_BDTallBkg_klscan/analysedOutPlotter.root"
var="BDTG_6_masscut"
sel="finalsel_SR"
QCDsyst="0.5"
CARDDIR="cards/klscan"
# cardname="bbbb_datacard.txt"

echo "doing the cards for the lambda scan"
echo "INPUT_FILE: $INPUT_FILE"
echo "var: $var"
echo "sel: $sel"
echo "QCDsyst: $QCDsyst"
echo "CARD DIR: $CARDDIR"
# echo "cardname: $cardname"

if [ ! -d "$CARDDIR" ]; then
    mkdir -p $CARDDIR;
fi

######
# 1) build the cards

# echo "... making cards"

# ### the first lines will convert numbers into the plot conventions: - -> m, . -> d, positive numbers have a leading p
# for i in `seq -f %g -5 0.25 10`; do
#     kl=$i
#     kl=${kl/./d}
#     if [[ $kl == *-* ]]; then
#         kl=${kl/-/m_};
#     else
#         kl=p_${kl}
#     fi
#     kl="HH_kl_${kl}"
#     echo $kl
#     python make_datacard.py --var $var --sel $sel --cardOut ${CARDDIR}/bbbb_datacard_${kl}.txt --fileIn ${INPUT_FILE} --QCDsyst ${QCDsyst} --sigs $kl
# done

#####
# 2) generate an Asimov distribution for the SM expectation of sig (klambda = 1) + bkg
echo "... generating SM expectation"
SM_NAME="HH_kl_p_1"
cd ${CARDDIR}
# text2workspace.py bbbb_datacard_${SM_NAME}.txt
combine -M GenerateOnly -t -1 \
--setParameters r=1.0 \
--saveToys \
-n SM_toys \
bbbb_datacard_${SM_NAME}.txt

cd -


######
# 3) run the cross section upper limits

echo "... running points"

### need to go in the card folder, because I don't know how to tell combine to put its output in a specific folder
cd ${CARDDIR}

for i in `seq -f %g -5 0.25 10`; do
    kl=$i
    kl=${kl/./d}
    if [[ $kl == *-* ]]; then
        kl=${kl/-/m_};
    else
        kl=p_${kl}
    fi
    kl="HH_kl_${kl}"
    echo $kl

    combine -M MultiDimFit --algo fixed --fixedPointPOIs r=0 --saveNLL -t -1 --toysFile higgsCombineSM_toys.GenerateOnly.mH120.123456.root -n bbbb_result_r0_${kl} bbbb_datacard_${kl}.txt
    combine -M MultiDimFit --algo fixed --fixedPointPOIs r=1 --saveNLL -t -1 --toysFile higgsCombineSM_toys.GenerateOnly.mH120.123456.root -n bbbb_result_r1_${kl} bbbb_datacard_${kl}.txt
done

cd -

