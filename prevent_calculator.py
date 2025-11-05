"""
PREVENT Calculator - AHA Cardiovascular Disease Risk Calculator
Based on the American Heart Association's PREVENT equations

This file contains the faithful implementation of the PREVENT equations
ported from the original R code, as validated in the CalculadorasMed repository.
"""
import numpy as np
import math

class PREVENTCalculator:
    """
    PREVENT Calculator implementing the original validated formulas.
    """

    def _mmol_conversion(self, cholesterol):
        if cholesterol is None or np.isnan(cholesterol): return np.nan
        return 0.02586 * cholesterol

    def _adjust_uacr(self, uacr):
        if uacr is None or np.isnan(uacr): return np.nan
        if uacr >= 0.1: return uacr
        elif 0 <= uacr < 0.1: return 0.1
        return np.nan

    def _calculate_prevent_base(self, sex, age, tc, hdl, sbp, dm, smoking, bmi, egfr, bptreat, statin, **kwargs):
        logor_10yr_CVD = logor_10yr_ASCVD = logor_10yr_HF = np.nan
        if sex == 1: # Feminino
            logor_10yr_CVD = -3.307728 + 0.7939329*(age - 55)/10 + 0.0305239*(self._mmol_conversion(tc - hdl) - 3.5) - 0.1606857*(self._mmol_conversion(hdl) - 1.3)/(0.3) - 0.2394003*(min(sbp, 110) - 110)/20 + 0.2974913*(max(sbp, 110) - 130)/20 + 0.8173409*(dm) + 0.6846152*(smoking) + 0.0469145*(min(bmi, 20) - 20)/5 + 0.0076847*(max(bmi, 20) - 25)/5 - 0.2458428*(min(egfr, 60) - 60)/30 + 0.428678*(max(egfr, 60) - 90)/30 + 0.1463162*(bptreat) + 0.1804508*(0)
            logor_10yr_ASCVD = -3.819975 + 0.719883*(age - 55)/10 + 0.1176967*((self._mmol_conversion(tc) - self._mmol_conversion(hdl)) - 3.5) - 0.151185*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.0835358*(min(sbp, 110) - 110)/20 + 0.2796979*(max(sbp, 110) - 130)/20 + 0.7674992*(dm) + 0.6405786*(smoking) - 0.0064547*(min(bmi, 20) - 20)/5 - 0.0304664*(max(bmi, 20) - 25)/5 - 0.2345511*(min(egfr, 60) - 60)/30 + 0.3540822*(max(egfr, 60) - 90)/30 + 0.1167448*(bptreat) + 0.1588908*(0)
            logor_10yr_HF = -4.310409 + 0.8998235*(age - 55)/10 - 0.4559771*(min(sbp, 110) - 110)/20 + 0.3576505*(max(sbp, 110) - 130)/20 + 1.038346*(dm) + 0.583916*(smoking) - 0.0072294*(min(bmi, 30) - 30)/5 + 0.0933182*(max(bmi, 30) - 30)/5 - 0.2974911*(min(egfr, 60) - 60)/30 + 0.4497556*(max(egfr, 60) - 90)/30 + 0.1983057*(bptreat) + 0.1819138*(0)
        else: # Masculino
            logor_10yr_CVD = -3.031168 + 0.7688528*(age - 55)/10 + 0.0736174*(self._mmol_conversion(tc - hdl) - 3.5) - 0.0954431*(self._mmol_conversion(hdl) - 1.3)/(0.3) - 0.4347345*(min(sbp, 110) - 110)/20 + 0.301594*(max(sbp, 110) - 130)/20 + 0.730386*(dm) + 0.5786835*(smoking) - 0.0478951*(min(bmi, 20) - 20)/5 - 0.063851*(max(bmi, 20) - 25)/5 - 0.3344068*(min(egfr, 60) - 60)/30 + 0.4578502*(max(egfr, 60) - 90)/30 + 0.1782299*(bptreat) + 0.144759*(0)
            logor_10yr_ASCVD = -3.500655 + 0.7099847*(age - 55)/10 + 0.1658663*((self._mmol_conversion(tc) - self._mmol_conversion(hdl)) - 3.5) - 0.1144285*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.2837212*(min(sbp, 110) - 110)/20 + 0.2941589*(max(sbp, 110) - 130)/20 + 0.6558448*(dm) + 0.5801383*(smoking) - 0.0520614*(min(bmi, 20) - 20)/5 - 0.063383*(max(bmi, 20) - 25)/5 - 0.3370335*(min(egfr, 60) - 60)/30 + 0.428519*(max(egfr, 60) - 90)/30 + 0.1643663*(bptreat) + 0.1388492*(0)
            logor_10yr_HF = -3.946391 + 0.8972642*(age - 55)/10 - 0.6811466*(min(sbp, 110) - 110)/20 + 0.3634461*(max(sbp, 110) - 130)/20 + 0.923776*(dm) + 0.5023736*(smoking) - 0.0485841*(min(bmi, 30) - 30)/5 + 0.0494492*(max(bmi, 30) - 30)/5 - 0.3364421*(min(egfr, 60) - 60)/30 + 0.5367803*(max(egfr, 60) - 90)/30 + 0.2223455*(bptreat) + 0.1694628*(0)
        return logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF

    def _calculate_prevent_uacr(self, sex, age, tc, hdl, sbp, dm, smoking, bmi, egfr, bptreat, statin, uacr, **kwargs):
        logor_10yr_CVD = logor_10yr_ASCVD = logor_10yr_HF = np.nan
        adj_uacr = self._adjust_uacr(uacr)
        log_uacr = math.log(adj_uacr) if not math.isnan(adj_uacr) else np.nan
        
        if sex == 1: # Feminino
            uacr_term_cvd = 0.0132073 if math.isnan(log_uacr) else 0.1793037*log_uacr
            logor_10yr_CVD = -3.738341 + 0.7969249*((age - 55)/10) + 0.0256635*((self._mmol_conversion(tc) - self._mmol_conversion(hdl)) - 3.5) - 0.1588107*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.2255701*(min(sbp, 110) - 110)/20 + 0.2818907*(max(sbp, 110) - 130)/20 + 0.7712399*(dm) + 0.6775618*(smoking) + 0.0490715*(min(bmi, 20) - 20)/5 + 0.004128*(max(bmi, 20) - 25)/5 - 0.2396347*(min(egfr, 60) - 60)/30 + 0.4072225*(max(egfr, 60) - 90)/30 + 0.128795*(bptreat) + uacr_term_cvd + 0.1804508*(0)
            uacr_term_ascvd = 0.0050257 if math.isnan(log_uacr) else 0.1501217*log_uacr
            logor_10yr_ASCVD = -4.174614 + 0.7201999*((age - 55)/10) + 0.1135771*((self._mmol_conversion(tc) - self._mmol_conversion(hdl)) - 3.5) - 0.1493506*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.0726677*(min(sbp, 110) - 110)/20 + 0.2642197*(max(sbp, 110) - 130)/20 + 0.7270928*(dm) + 0.6322883*(smoking) - 0.003426*(min(bmi, 20) - 20)/5 - 0.0335017*(max(bmi, 20) - 25)/5 - 0.2285145*(min(egfr, 60) - 60)/30 + 0.3340579*(max(egfr, 60) - 90)/30 + 0.1017387*(bptreat) + uacr_term_ascvd + 0.1588908*(0)
            uacr_term_hf = 0.0326667 if math.isnan(log_uacr) else 0.2197281*log_uacr
            logor_10yr_HF = -4.841506 + 0.9145975*((age - 55)/10) - 0.4441346*(min(sbp, 110) - 110)/20 + 0.3260323*(max(sbp, 110) - 130)/20 + 0.9611365*(dm) + 0.5755787*(smoking) + 0.0008831*(min(bmi, 30) - 30)/5 + 0.0903823*(max(bmi, 30) - 30)/5 - 0.286221*(min(egfr, 60) - 60)/30 + 0.4284566*(max(egfr, 60) - 90)/30 + 0.1783427*(bptreat) + uacr_term_hf + 0.1819138*(0)
        else: # Masculino
            uacr_term_cvd = 0.0916979 if math.isnan(log_uacr) else 0.1887974*log_uacr
            logor_10yr_CVD = -3.510705 + 0.7768655*((age - 55)/10) + 0.0659949*((self._mmol_conversion(tc) - self._mmol_conversion(hdl)) - 3.5) - 0.0951111*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.420667*(min(sbp, 110) - 110)/20 + 0.2829285*(max(sbp, 110) - 130)/20 + 0.6724395*(dm) + 0.5714781*(smoking) - 0.047514*(min(bmi, 20) - 20)/5 - 0.068995*(max(bmi, 20) - 25)/5 - 0.3235372*(min(egfr, 60) - 60)/30 + 0.4357321*(max(egfr, 60) - 90)/30 + 0.1610996*(bptreat) + uacr_term_cvd + 0.144759*(0)
            uacr_term_ascvd = 0.0556 if math.isnan(log_uacr) else 0.1510073*log_uacr
            logor_10yr_ASCVD = -3.85146 + 0.7141718*((age - 55)/10) + 0.1602194*((self._mmol_conversion(tc) - self._mmol_conversion(hdl)) - 3.5) - 0.1139086*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.2719456*(min(sbp, 110) - 110)/20 + 0.276412*(max(sbp, 110) - 130)/20 + 0.6015949*(dm) + 0.5710928*(smoking) - 0.0519398*(min(bmi, 20) - 20)/5 - 0.0673413*(max(bmi, 20) - 25)/5 - 0.3255152*(min(egfr, 60) - 60)/30 + 0.407289*(max(egfr, 60) - 90)/30 + 0.1466033*(bptreat) + uacr_term_ascvd + 0.1388492*(0)
            uacr_term_hf = 0.1472194 if math.isnan(log_uacr) else 0.2306299*log_uacr
            logor_10yr_HF = -4.556907 + 0.9111795*((age - 55)/10) - 0.6693649*(min(sbp, 110) - 110)/20 + 0.3290082*(max(sbp, 110) - 130)/20 + 0.8377655*(dm) + 0.4978917*(smoking) - 0.042749*(min(bmi, 30) - 30)/5 + 0.0437435*(max(bmi, 30) - 30)/5 - 0.3256034*(min(egfr, 60) - 60)/30 + 0.5133316*(max(egfr, 60) - 90)/30 + 0.201777*(bptreat) + uacr_term_hf + 0.1694628*(0)
        return logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF

    def _calculate_prevent_hba1c(self, sex, age, tc, hdl, sbp, dm, smoking, bmi, egfr, bptreat, statin, hba1c, **kwargs):
        logor_10yr_CVD = logor_10yr_ASCVD = logor_10yr_HF = np.nan
        hba1c_val = hba1c if (hba1c is not None and not np.isnan(hba1c)) else np.nan

        if sex == 1: # Feminino
            hba1c_term_cvd = -0.0142496 if math.isnan(hba1c_val) else (0.1338348*(hba1c_val-5.3)*(dm) + 0.1622409*(hba1c_val-5.3)*(1-dm))
            logor_10yr_CVD = -3.306162 + 0.7858178*((age - 55)/10) + 0.0194438*((self._mmol_conversion(tc) - self._mmol_conversion(hdl)) - 3.5) - 0.1521964*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.2296681*(min(sbp, 110) - 110)/20 + 0.2869972*(max(sbp, 110) - 130)/20 + 0.5483256*(dm) + 0.6904135*(smoking) + 0.0494494*(min(bmi, 20) - 20)/5 + 0.0091391*(max(bmi, 20) - 25)/5 - 0.2452252*(min(egfr, 60) - 60)/30 + 0.428784*(max(egfr, 60) - 90)/30 + 0.1444106*(bptreat) + hba1c_term_cvd + 0.1804508*(0)
            hba1c_term_ascvd = 0.0015678 if math.isnan(hba1c_val) else (0.1339055*(hba1c_val-5.3)*(dm) + 0.1596461*(hba1c_val-5.3)*(1-dm))
            logor_10yr_ASCVD = -3.838746 + 0.7111831*((age - 55)/10) + 0.106797*((self._mmol_conversion(tc) - self._mmol_conversion(hdl)) - 3.5) - 0.1425745*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.0736824*(min(sbp, 110) - 110)/20 + 0.2707297*(max(sbp, 110) - 130)/20 + 0.521233*(dm) + 0.6457316*(smoking) - 0.003923*(min(bmi, 20) - 20)/5 - 0.028989*(max(bmi, 20) - 25)/5 - 0.2339832*(min(egfr, 60) - 60)/30 + 0.3541738*(max(egfr, 60) - 90)/30 + 0.1147746*(bptreat) + hba1c_term_ascvd + 0.1588908*(0)
            hba1c_term_hf = -0.0143112 if math.isnan(hba1c_val) else (0.1856442*(hba1c_val-5.3)*(dm) + 0.1833083*(hba1c_val-5.3)*(1-dm))
            logor_10yr_HF = -4.288225 + 0.8997391*((age - 55)/10) - 0.4422749*(min(sbp, 110) - 110)/20 + 0.3378691*(max(sbp, 110) - 130)/20 + 0.681284*(dm) + 0.5886005*(smoking) - 0.0148657*(min(bmi, 30) - 30)/5 + 0.0886532*(max(bmi, 30) - 30)/5 - 0.2965825*(min(egfr, 60) - 60)/30 + 0.4497911*(max(egfr, 60) - 90)/30 + 0.1947231*(bptreat) + hba1c_term_hf + 0.1819138*(0)
        else: # Masculino
            hba1c_term_cvd = -0.0128373 if math.isnan(hba1c_val) else (0.13159*(hba1c_val-5.3)*(dm) + 0.1295185*(hba1c_val-5.3)*(1-dm))
            logor_10yr_CVD = -3.040901 + 0.7699177*((age - 55)/10) + 0.0605093*((self._mmol_conversion(tc) - self._mmol_conversion(hdl)) - 3.5) - 0.0888525*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.417713*(min(sbp, 110) - 110)/20 + 0.2933934*(max(sbp, 110) - 130)/20 + 0.4851084*(dm) + 0.5833418*(smoking) - 0.0487059*(min(bmi, 20) - 20)/5 - 0.0664975*(max(bmi, 20) - 25)/5 - 0.3338575*(min(egfr, 60) - 60)/30 + 0.4578135*(max(egfr, 60) - 90)/30 + 0.17604*(bptreat) + hba1c_term_cvd + 0.144759*(0)
            hba1c_term_ascvd = -0.0010001 if math.isnan(hba1c_val) else (0.1157161*(hba1c_val-5.3)*(dm) + 0.1288303*(hba1c_val-5.3)*(1-dm))
            logor_10yr_ASCVD = -3.51835 + 0.7064146*((age - 55)/10) + 0.1532267*((self._mmol_conversion(tc) - self._mmol_conversion(hdl)) - 3.5) - 0.1082166*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.2675288*(min(sbp, 110) - 110)/20 + 0.2858597*(max(sbp, 110) - 130)/20 + 0.4439063*(dm) + 0.5843477*(smoking) - 0.052745*(min(bmi, 20) - 20)/5 - 0.0655866*(max(bmi, 20) - 25)/5 - 0.3366035*(min(egfr, 60) - 60)/30 + 0.428489*(max(egfr, 60) - 90)/30 + 0.162386*(bptreat) + hba1c_term_ascvd + 0.1388492*(0)
            hba1c_term_hf = -0.0113444 if math.isnan(hba1c_val) else (0.1652857*(hba1c_val-5.3)*(dm) + 0.1505859*(hba1c_val-5.3)*(1-dm))
            logor_10yr_HF = -3.961954 + 0.911787*((age - 55)/10) - 0.6568071*(min(sbp, 110) - 110)/20 + 0.3524645*(max(sbp, 110) - 130)/20 + 0.5849752*(dm) + 0.5014014*(smoking) - 0.0512352*(min(bmi, 30) - 30)/5 + 0.0463138*(max(bmi, 30) - 30)/5 - 0.335832*(min(egfr, 60) - 60)/30 + 0.5367676*(max(egfr, 60) - 90)/30 + 0.2198084*(bptreat) + hba1c_term_hf + 0.1694628*(0)
        return logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF

    def _calculate_prevent_full(self, sex, age, tc, hdl, sbp, dm, smoking, bmi, egfr, bptreat, statin, uacr, hba1c, **kwargs):
        logor_10yr_CVD = logor_10yr_ASCVD = logor_10yr_HF = np.nan
        adj_uacr = self._adjust_uacr(uacr)
        log_uacr = math.log(adj_uacr) if not math.isnan(adj_uacr) else np.nan
        hba1c_val = hba1c if (hba1c is not None and not np.isnan(hba1c)) else np.nan
        
        if sex == 1: # Feminino
            uacr_term_cvd = 0.0198413 if math.isnan(log_uacr) else 0.1645922*log_uacr
            hba1c_term_cvd = -0.0031658 if math.isnan(hba1c_val) else (0.1298513*(hba1c_val-5.3)*(dm) + 0.1412555*(hba1c_val-5.3)*(1 - dm))
            logor_10yr_CVD = -3.860385 + 0.7716794*((age - 55)/10) + 0.0062109*(self._mmol_conversion(tc - hdl) - 3.5) - 0.1547756*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.1933123*(min(sbp, 110) - 110)/20 + 0.2743841*(max(sbp, 110) - 130)/20 + 0.5113942*(dm) + 0.6834614*(smoking) + 0.0528246*(min(bmi, 20) - 20)/5 + 0.0051663*(max(bmi, 20) - 25)/5 - 0.2407519*(min(egfr, 60) - 60)/30 + 0.407981*(max(egfr, 60) - 90)/30 + 0.127546*(bptreat) + uacr_term_cvd + hba1c_term_cvd + 0.1804508*(0)
            uacr_term_ascvd = 0.0061613 if math.isnan(log_uacr) else 0.1371824*log_uacr
            hba1c_term_ascvd = 0.005866 if math.isnan(hba1c_val) else (0.123192*(hba1c_val-5.3)*(dm) + 0.1410572*(hba1c_val-5.3)*(1-dm))
            logor_10yr_ASCVD = -4.291503 + 0.7023067*((age - 55)/10) + 0.0898765*((self._mmol_conversion(tc) - self._mmol_conversion(hdl)) - 3.5) - 0.1407316*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.0256648*(min(sbp, 110) - 110)/20 + 0.2583802*(max(sbp, 110) - 130)/20 + 0.4851213*(dm) + 0.6370487*(smoking) + 0.0003264*(min(bmi, 20) - 20)/5 - 0.0322301*(max(bmi, 20) - 25)/5 - 0.22998*(min(egfr, 60) - 60)/30 + 0.334752*(max(egfr, 60) - 90)/30 + 0.099905*(bptreat) + uacr_term_ascvd + hba1c_term_ascvd + 0.1588908*(0)
            uacr_term_hf = 0.0395368 if math.isnan(log_uacr) else 0.1948135*log_uacr
            hba1c_term_hf = -0.0010583 if math.isnan(hba1c_val) else (0.176668*(hba1c_val-5.3)*(dm) + 0.1614911*(hba1c_val-5.3)*(1-dm))
            logor_10yr_HF = -4.896524 + 0.884209*((age - 55)/10) - 0.421474*(min(sbp, 110) - 110)/20 + 0.3002919*(max(sbp, 110) - 130)/20 + 0.6170359*(dm) + 0.5380269*(smoking) - 0.0191335*(min(bmi, 30) - 30)/5 + 0.085891*(max(bmi, 30) - 30)/5 - 0.2863923*(min(egfr, 60) - 60)/30 + 0.4286161*(max(egfr, 60) - 90)/30 + 0.1761405*(bptreat) + uacr_term_hf + hba1c_term_hf + 0.1819138*(0)
        else: # Masculino
            uacr_term_cvd = 0.1095674 if math.isnan(log_uacr) else 0.1772853*log_uacr
            hba1c_term_cvd = -0.0230072 if math.isnan(log_uacr) else (0.1165698*(hba1c_val-5.3)*(dm) + 0.1048297*(hba1c_val-5.3)*(1 - dm))
            logor_10yr_CVD = -3.631387 + 0.7847578*((age - 55)/10) + 0.0534485*(self._mmol_conversion(tc - hdl) - 3.5) - 0.0911282*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.4921973*(min(sbp, 110) - 110)/20 + 0.2743513*(max(sbp, 110) - 130)/20 + 0.4398642*(dm) + 0.5348911*(smoking) - 0.054593*(min(bmi, 20) - 20)/5 - 0.0717278*(max(bmi, 20) - 25)/5 - 0.3242099*(min(egfr, 60) - 60)/30 + 0.4363297*(max(egfr, 60) - 90)/30 + 0.1587635*(bptreat) + uacr_term_cvd + hba1c_term_cvd + 0.144759*(0)
            uacr_term_ascvd = 0.0652944 if math.isnan(log_uacr) else 0.1375837*log_uacr
            hba1c_term_ascvd = -0.0112852 if math.isnan(hba1c_val) else (0.101282*(hba1c_val-5.3)*(dm) + 0.1092726*(hba1c_val-5.3)*(1-dm))
            logor_10yr_ASCVD = -3.969788 + 0.7128741*((age - 55)/10) + 0.1465201*((self._mmol_conversion(tc) - self._mmol_conversion(hdl)) - 3.5) - 0.1125794*(self._mmol_conversion(hdl) - 1.3)/0.3 - 0.3387216*(min(sbp, 110) - 110)/20 + 0.2676063*(max(sbp, 110) - 130)/20 + 0.3957261*(dm) + 0.533251*(smoking) - 0.0573981*(min(bmi, 20) - 20)/5 - 0.0699933*(max(bmi, 20) - 25)/5 - 0.3262602*(min(egfr, 60) - 60)/30 + 0.4079836*(max(egfr, 60) - 90)/30 + 0.1444101*(bptreat) + uacr_term_ascvd + hba1c_term_ascvd + 0.1388492*(0)
            uacr_term_hf = 0.1702805 if math.isnan(log_uacr) else 0.2164607*log_uacr
            hba1c_term_hf = -0.0234637 if math.isnan(hba1c_val) else (0.148297*(hba1c_val-5.3)*(dm) + 0.1234088*(hba1c_val-5.3)*(1-dm))
            logor_10yr_HF = -4.663513 + 0.9095703*((age - 55)/10) - 0.6765184*(min(sbp, 110) - 110)/20 + 0.3111651*(max(sbp, 110) - 130)/20 + 0.5535052*(dm) + 0.4326811*(smoking) - 0.0854286*(min(bmi, 30) - 30)/5 + 0.0401826*(max(bmi, 30) - 30)/5 - 0.3261645*(min(egfr, 60) - 60)/30 + 0.5138988*(max(egfr, 60) - 90)/30 + 0.1994191*(bptreat) + uacr_term_hf + hba1c_term_hf + 0.1694628*(0)
        return logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF

    def _calculate_final_risks(self, logors, age, tc, hdl, statin, bmi):
        logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = logors
        
        def inv_logit(logor):
            if np.isnan(logor): return np.nan
            return 100 * math.exp(logor) / (1 + math.exp(logor))

        risks = {
            'total_cvd_10yr': inv_logit(logor_10yr_CVD),
            'ascvd_10yr': inv_logit(logor_10yr_ASCVD),
            'hf_10yr': inv_logit(logor_10yr_HF)
        }

        # Apply validation rules
        if (tc is None or tc < 130 or tc > 320) or \
           (hdl is None or hdl < 20 or hdl > 100) or \
           (statin is None):
            risks['total_cvd_10yr'] = np.nan
            risks['ascvd_10yr'] = np.nan
            
        if (bmi is None or bmi < 18.5 or bmi >= 40):
            risks['hf_10yr'] = np.nan
            
        return risks

    def calculate_risk_score(self, age, sex, total_cholesterol, hdl_cholesterol, sbp, 
                             on_bp_meds, diabetes, smoker, egfr, weight, height, on_statins, 
                             uacr=None, hba1c=None, **kwargs):
        
        # --- Data Validation and Preparation ---
        if any(p is None for p in [age, sex, total_cholesterol, hdl_cholesterol, sbp, egfr, weight, height, on_statins]):
            raise ValueError("Parâmetros essenciais (idade, sexo, colesterol, PA, TFG, peso, altura, estatina) não podem ser nulos.")

        bmi = self._calculate_bmi(weight, height)
        
        params = {
            "sex": 1 if sex == "F" else 0,
            "age": age,
            "tc": total_cholesterol,
            "hdl": hdl_cholesterol,
            "sbp": sbp,
            "dm": 1 if diabetes else 0,
            "smoking": 1 if smoker else 0,
            "bmi": bmi,
            "egfr": egfr,
            "bptreat": 1 if on_bp_meds else 0,
            "statin": 1 if on_statins else 0,
            "uacr": uacr,
            "hba1c": hba1c
        }

        # --- Logic to select the correct model ---
        uacr_provided = uacr is not None
        hba1c_provided = hba1c is not None

        if uacr_provided and hba1c_provided:
            logors = self._calculate_prevent_full(**params)
        elif uacr_provided:
            logors = self._calculate_prevent_uacr(**params)
        elif hba1c_provided:
            logors = self._calculate_prevent_hba1c(**params)
        else:
            logors = self._calculate_prevent_base(**params)
            
        # --- Final Risk Calculation and Validation ---
        final_risks = self._calculate_final_risks(logors, age, params['tc'], params['hdl'], params['statin'], bmi)

        # Format final output
        results = {}
        for key, value in final_risks.items():
            if np.isnan(value):
                results[key] = 'N/A'
            else:
                results[key] = round(value, 2)
        
        results['risk_category'] = self._categorize_risk(final_risks['total_cvd_10yr'])
        return results

    def _categorize_risk(self, risk_pct):
        if np.isnan(risk_pct): return 'Indisponível'
        if risk_pct < 5: return 'Baixo'
        elif risk_pct < 7.5: return 'Limítrofe'
        elif risk_pct < 20: return 'Intermediário'
        else: return 'Alto'
