#!/usr/bin/env python3

import struct
import grf
import generate
import filters
from lib import BadgeFlags
from pathlib import Path

g = grf.NewGRF(
    format_version=8,
    grfid=b"PNS\xFF",
    name="Default Badge Set",
    description="A set of badges for common country flags, power types and operator logos",
)

b = generate.Badges()

BADGE_CLASS_FLAG = "flag"
BADGE_CLASS_ROLE = "role"
BADGE_CLASS_OPERATOR = "operator"
BADGE_CLASS_POWER = "power"
BADGE_CLASS_LIVERY = "livery"

# Classes
b.add(BADGE_CLASS_FLAG, None, "STR_CLASS_FLAG")
b.add(BADGE_CLASS_ROLE, None, "STR_CLASS_ROLE")
b.add(BADGE_CLASS_OPERATOR, None, "STR_CLASS_OPERATOR")
b.add(BADGE_CLASS_POWER, None, "STR_CLASS_PROPULSION")
b.add(BADGE_CLASS_LIVERY, None, "STR_CLASS_LIVERY")

# Modes
b.add(BADGE_CLASS_ROLE + "/passenger", None, "STR_ROLE_PASSENGER")
b.add(BADGE_CLASS_ROLE + "/freight", None, "STR_ROLE_FREIGHT")
b.add(BADGE_CLASS_ROLE + "/mixed", None, "STR_ROLE_MIXED")
b.add(BADGE_CLASS_ROLE + "/express_passenger", None, "STR_ROLE_EXPRESS_PASSENGER")
b.add(BADGE_CLASS_ROLE + "/express_freight", None, "STR_ROLE_EXPRESS_FREIGHT")
b.add(BADGE_CLASS_ROLE + "/heavy_freight", None, "STR_ROLE_HEAVY_FREIGHT")
b.add(BADGE_CLASS_ROLE + "/restaurant_car", None, "STR_ROLE_RESTAURANT_CAR")

# Country flags
b.add(BADGE_CLASS_FLAG + "/AD", "flag-icons/ad.svg", "STR_FLAG_AD")
b.add(BADGE_CLASS_FLAG + "/AE", "flag-icons/ae.svg", "STR_FLAG_AE")
b.add(BADGE_CLASS_FLAG + "/AF", "flag-icons/af.svg", "STR_FLAG_AF")
b.add(BADGE_CLASS_FLAG + "/AG", "flag-icons/ag.svg", "STR_FLAG_AG")
b.add(BADGE_CLASS_FLAG + "/AI", "flag-icons/ai.svg", "STR_FLAG_AI")
b.add(BADGE_CLASS_FLAG + "/AL", "flag-icons/al.svg", "STR_FLAG_AL")
b.add(BADGE_CLASS_FLAG + "/AM", "flag-icons/am.svg", "STR_FLAG_AM")
b.add(BADGE_CLASS_FLAG + "/AO", "flag-icons/ao.svg", "STR_FLAG_AO")
b.add(BADGE_CLASS_FLAG + "/AQ", "flag-icons/aq.svg", "STR_FLAG_AQ")
# b.add(BADGE_CLASS_FLAG + "/ARAB", "flag-icons/arab.svg", "STR_FLAG_ARA")
b.add(BADGE_CLASS_FLAG + "/AR", "flag-icons/ar.svg", "STR_FLAG_AR")
b.add(BADGE_CLASS_FLAG + "/AS", "flag-icons/as.svg", "STR_FLAG_AS")
b.add(BADGE_CLASS_FLAG + "/AT", "flag-icons/at.svg", "STR_FLAG_AT")
b.add(BADGE_CLASS_FLAG + "/AU", "flag-icons/au.svg", "STR_FLAG_AU")
b.add(BADGE_CLASS_FLAG + "/AW", "flag-icons/aw.svg", "STR_FLAG_AW")
b.add(BADGE_CLASS_FLAG + "/AX", "flag-icons/ax.svg", "STR_FLAG_AX")
b.add(BADGE_CLASS_FLAG + "/AZ", "flag-icons/az.svg", "STR_FLAG_AZ")
b.add(BADGE_CLASS_FLAG + "/BA", "flag-icons/ba.svg", "STR_FLAG_BA")
b.add(BADGE_CLASS_FLAG + "/BB", "flag-icons/bb.svg", "STR_FLAG_BB")
b.add(BADGE_CLASS_FLAG + "/BD", "flag-icons/bd.svg", "STR_FLAG_BD")
b.add(BADGE_CLASS_FLAG + "/BE", "flag-icons/be.svg", "STR_FLAG_BE")
b.add(BADGE_CLASS_FLAG + "/BF", "flag-icons/bf.svg", "STR_FLAG_BF")
b.add(BADGE_CLASS_FLAG + "/BG", "flag-icons/bg.svg", "STR_FLAG_BG")
b.add(BADGE_CLASS_FLAG + "/BH", "flag-icons/bh.svg", "STR_FLAG_BH")
b.add(BADGE_CLASS_FLAG + "/BI", "flag-icons/bi.svg", "STR_FLAG_BI")
b.add(BADGE_CLASS_FLAG + "/BJ", "flag-icons/bj.svg", "STR_FLAG_BJ")
b.add(BADGE_CLASS_FLAG + "/BL", "flag-icons/bl.svg", "STR_FLAG_BL")
b.add(BADGE_CLASS_FLAG + "/BM", "flag-icons/bm.svg", "STR_FLAG_BM")
b.add(BADGE_CLASS_FLAG + "/BN", "flag-icons/bn.svg", "STR_FLAG_BN")
b.add(BADGE_CLASS_FLAG + "/BO", "flag-icons/bo.svg", "STR_FLAG_BO")
b.add(BADGE_CLASS_FLAG + "/BQ", "flag-icons/bq.svg", "STR_FLAG_BQ")
b.add(BADGE_CLASS_FLAG + "/BR", "flag-icons/br.svg", "STR_FLAG_BR")
b.add(BADGE_CLASS_FLAG + "/BS", "flag-icons/bs.svg", "STR_FLAG_BS")
b.add(BADGE_CLASS_FLAG + "/BT", "flag-icons/bt.svg", "STR_FLAG_BT")
b.add(BADGE_CLASS_FLAG + "/BV", "flag-icons/bv.svg", "STR_FLAG_BV")
b.add(BADGE_CLASS_FLAG + "/BW", "flag-icons/bw.svg", "STR_FLAG_BW")
b.add(BADGE_CLASS_FLAG + "/BY", "flag-icons/by.svg", "STR_FLAG_BY")
b.add(BADGE_CLASS_FLAG + "/BZ", "flag-icons/bz.svg", "STR_FLAG_BZ")
b.add(BADGE_CLASS_FLAG + "/CA", "flag-icons/ca.svg", "STR_FLAG_CA")
b.add(BADGE_CLASS_FLAG + "/CC", "flag-icons/cc.svg", "STR_FLAG_CC")
b.add(BADGE_CLASS_FLAG + "/CD", "flag-icons/cd.svg", "STR_FLAG_CD")
# b.add(BADGE_CLASS_FLAG + "/CEFTA", "flag-icons/cefta.svg", "STR_FLAG_CEF")
b.add(BADGE_CLASS_FLAG + "/CF", "flag-icons/cf.svg", "STR_FLAG_CF")
b.add(BADGE_CLASS_FLAG + "/CG", "flag-icons/cg.svg", "STR_FLAG_CG")
b.add(BADGE_CLASS_FLAG + "/CH", "flag-icons/ch.svg", "STR_FLAG_CH")
b.add(BADGE_CLASS_FLAG + "/CI", "flag-icons/ci.svg", "STR_FLAG_CI")
b.add(BADGE_CLASS_FLAG + "/CK", "flag-icons/ck.svg", "STR_FLAG_CK")
b.add(BADGE_CLASS_FLAG + "/CL", "flag-icons/cl.svg", "STR_FLAG_CL")
b.add(BADGE_CLASS_FLAG + "/CM", "flag-icons/cm.svg", "STR_FLAG_CM")
b.add(BADGE_CLASS_FLAG + "/CN", "flag-icons/cn.svg", "STR_FLAG_CN")
b.add(BADGE_CLASS_FLAG + "/CO", "flag-icons/co.svg", "STR_FLAG_CO")
# b.add(BADGE_CLASS_FLAG + "/CP", "flag-icons/cp.svg", "STR_FLAG_CP")
b.add(BADGE_CLASS_FLAG + "/CR", "flag-icons/cr.svg", "STR_FLAG_CR")
b.add(BADGE_CLASS_FLAG + "/CU", "flag-icons/cu.svg", "STR_FLAG_CU")
b.add(BADGE_CLASS_FLAG + "/CV", "flag-icons/cv.svg", "STR_FLAG_CV")
b.add(BADGE_CLASS_FLAG + "/CW", "flag-icons/cw.svg", "STR_FLAG_CW")
b.add(BADGE_CLASS_FLAG + "/CX", "flag-icons/cx.svg", "STR_FLAG_CX")
b.add(BADGE_CLASS_FLAG + "/CY", "flag-icons/cy.svg", "STR_FLAG_CY")
b.add(BADGE_CLASS_FLAG + "/CZ", "flag-icons/cz.svg", "STR_FLAG_CZ")
b.add(BADGE_CLASS_FLAG + "/DE", "flag-icons/de.svg", "STR_FLAG_DE")
# b.add(BADGE_CLASS_FLAG + "/DG", "flag-icons/dg.svg", "STR_FLAG_DG")
b.add(BADGE_CLASS_FLAG + "/DJ", "flag-icons/dj.svg", "STR_FLAG_DJ")
b.add(BADGE_CLASS_FLAG + "/DK", "flag-icons/dk.svg", "STR_FLAG_DK")
b.add(BADGE_CLASS_FLAG + "/DM", "flag-icons/dm.svg", "STR_FLAG_DM")
b.add(BADGE_CLASS_FLAG + "/DO", "flag-icons/do.svg", "STR_FLAG_DO")
b.add(BADGE_CLASS_FLAG + "/DZ", "flag-icons/dz.svg", "STR_FLAG_DZ")
# b.add(BADGE_CLASS_FLAG + "/EAC", "flag-icons/eac.svg", "STR_FLAG_EAC")
b.add(BADGE_CLASS_FLAG + "/EC", "flag-icons/ec.svg", "STR_FLAG_EC")
b.add(BADGE_CLASS_FLAG + "/EE", "flag-icons/ee.svg", "STR_FLAG_EE")
b.add(BADGE_CLASS_FLAG + "/EG", "flag-icons/eg.svg", "STR_FLAG_EG")
b.add(BADGE_CLASS_FLAG + "/EH", "flag-icons/eh.svg", "STR_FLAG_EH")
b.add(BADGE_CLASS_FLAG + "/ER", "flag-icons/er.svg", "STR_FLAG_ER")
# b.add(BADGE_CLASS_FLAG + "/ES/CT", "flag-icons/es-ct.svg", "STR_FLAG_ESC")
# b.add(BADGE_CLASS_FLAG + "/ES/GA", "flag-icons/es-ga.svg", "STR_FLAG_ESG")
# b.add(BADGE_CLASS_FLAG + "/ES/PV", "flag-icons/es-pv.svg", "STR_FLAG_ESP")
b.add(BADGE_CLASS_FLAG + "/ES", "flag-icons/es.svg", "STR_FLAG_ES")
b.add(BADGE_CLASS_FLAG + "/ET", "flag-icons/et.svg", "STR_FLAG_ET")
# b.add(BADGE_CLASS_FLAG + "/EU", "flag-icons/eu.svg", "STR_FLAG_EU")
b.add(BADGE_CLASS_FLAG + "/FI", "flag-icons/fi.svg", "STR_FLAG_FI")
b.add(BADGE_CLASS_FLAG + "/FJ", "flag-icons/fj.svg", "STR_FLAG_FJ")
b.add(BADGE_CLASS_FLAG + "/FK", "flag-icons/fk.svg", "STR_FLAG_FK")
b.add(BADGE_CLASS_FLAG + "/FM", "flag-icons/fm.svg", "STR_FLAG_FM")
b.add(BADGE_CLASS_FLAG + "/FO", "flag-icons/fo.svg", "STR_FLAG_FO")
b.add(BADGE_CLASS_FLAG + "/FR", "flag-icons/fr.svg", "STR_FLAG_FR")
b.add(BADGE_CLASS_FLAG + "/GA", "flag-icons/ga.svg", "STR_FLAG_GA")
# b.add(BADGE_CLASS_FLAG + "/GB/england", "flag-icons/gb-eng.svg", "STR_FLAG_GBE")
# b.add(BADGE_CLASS_FLAG + "/GB/northern ireland", "flag-icons/gb-nir.svg", "STR_FLAG_GBN")
# b.add(BADGE_CLASS_FLAG + "/GB/scotland", "flag-icons/gb-sct.svg", "STR_FLAG_GBS")
b.add(BADGE_CLASS_FLAG + "/GB", "flag-icons/gb.svg", "STR_FLAG_GB")
# b.add(BADGE_CLASS_FLAG + "/GB/wales", "flag-icons/gb-wls.svg", "STR_FLAG_GBW")
b.add(BADGE_CLASS_FLAG + "/GD", "flag-icons/gd.svg", "STR_FLAG_GD")
b.add(BADGE_CLASS_FLAG + "/GE", "flag-icons/ge.svg", "STR_FLAG_GE")
b.add(BADGE_CLASS_FLAG + "/GF", "flag-icons/gf.svg", "STR_FLAG_GF")
b.add(BADGE_CLASS_FLAG + "/GG", "flag-icons/gg.svg", "STR_FLAG_GG")
b.add(BADGE_CLASS_FLAG + "/GH", "flag-icons/gh.svg", "STR_FLAG_GH")
b.add(BADGE_CLASS_FLAG + "/GI", "flag-icons/gi.svg", "STR_FLAG_GI")
b.add(BADGE_CLASS_FLAG + "/GL", "flag-icons/gl.svg", "STR_FLAG_GL")
b.add(BADGE_CLASS_FLAG + "/GM", "flag-icons/gm.svg", "STR_FLAG_GM")
b.add(BADGE_CLASS_FLAG + "/GN", "flag-icons/gn.svg", "STR_FLAG_GN")
b.add(BADGE_CLASS_FLAG + "/GP", "flag-icons/gp.svg", "STR_FLAG_GP")
b.add(BADGE_CLASS_FLAG + "/GQ", "flag-icons/gq.svg", "STR_FLAG_GQ")
b.add(BADGE_CLASS_FLAG + "/GR", "flag-icons/gr.svg", "STR_FLAG_GR")
b.add(BADGE_CLASS_FLAG + "/GS", "flag-icons/gs.svg", "STR_FLAG_GS")
b.add(BADGE_CLASS_FLAG + "/GT", "flag-icons/gt.svg", "STR_FLAG_GT")
b.add(BADGE_CLASS_FLAG + "/GU", "flag-icons/gu.svg", "STR_FLAG_GU")
b.add(BADGE_CLASS_FLAG + "/GW", "flag-icons/gw.svg", "STR_FLAG_GW")
b.add(BADGE_CLASS_FLAG + "/GY", "flag-icons/gy.svg", "STR_FLAG_GY")
b.add(BADGE_CLASS_FLAG + "/HK", "flag-icons/hk.svg", "STR_FLAG_HK")
b.add(BADGE_CLASS_FLAG + "/HM", "flag-icons/hm.svg", "STR_FLAG_HM")
b.add(BADGE_CLASS_FLAG + "/HN", "flag-icons/hn.svg", "STR_FLAG_HN")
b.add(BADGE_CLASS_FLAG + "/HR", "flag-icons/hr.svg", "STR_FLAG_HR")
b.add(BADGE_CLASS_FLAG + "/HT", "flag-icons/ht.svg", "STR_FLAG_HT")
b.add(BADGE_CLASS_FLAG + "/HU", "flag-icons/hu.svg", "STR_FLAG_HU")
# b.add(BADGE_CLASS_FLAG + "/IC", "flag-icons/ic.svg", "STR_FLAG_IC")
b.add(BADGE_CLASS_FLAG + "/ID", "flag-icons/id.svg", "STR_FLAG_ID")
b.add(BADGE_CLASS_FLAG + "/IE", "flag-icons/ie.svg", "STR_FLAG_IE")
b.add(BADGE_CLASS_FLAG + "/IL", "flag-icons/il.svg", "STR_FLAG_IL")
b.add(BADGE_CLASS_FLAG + "/IM", "flag-icons/im.svg", "STR_FLAG_IM")
b.add(BADGE_CLASS_FLAG + "/IN", "flag-icons/in.svg", "STR_FLAG_IN")
b.add(BADGE_CLASS_FLAG + "/IO", "flag-icons/io.svg", "STR_FLAG_IO")
b.add(BADGE_CLASS_FLAG + "/IQ", "flag-icons/iq.svg", "STR_FLAG_IQ")
b.add(BADGE_CLASS_FLAG + "/IR", "flag-icons/ir.svg", "STR_FLAG_IR")
b.add(BADGE_CLASS_FLAG + "/IS", "flag-icons/is.svg", "STR_FLAG_IS")
b.add(BADGE_CLASS_FLAG + "/IT", "flag-icons/it.svg", "STR_FLAG_IT")
b.add(BADGE_CLASS_FLAG + "/JE", "flag-icons/je.svg", "STR_FLAG_JE")
b.add(BADGE_CLASS_FLAG + "/JM", "flag-icons/jm.svg", "STR_FLAG_JM")
b.add(BADGE_CLASS_FLAG + "/JO", "flag-icons/jo.svg", "STR_FLAG_JO")
b.add(BADGE_CLASS_FLAG + "/JP", "flag-icons/jp.svg", "STR_FLAG_JP")
b.add(BADGE_CLASS_FLAG + "/KE", "flag-icons/ke.svg", "STR_FLAG_KE")
b.add(BADGE_CLASS_FLAG + "/KG", "flag-icons/kg.svg", "STR_FLAG_KG")
b.add(BADGE_CLASS_FLAG + "/KH", "flag-icons/kh.svg", "STR_FLAG_KH")
b.add(BADGE_CLASS_FLAG + "/KI", "flag-icons/ki.svg", "STR_FLAG_KI")
b.add(BADGE_CLASS_FLAG + "/KM", "flag-icons/km.svg", "STR_FLAG_KM")
b.add(BADGE_CLASS_FLAG + "/KN", "flag-icons/kn.svg", "STR_FLAG_KN")
b.add(BADGE_CLASS_FLAG + "/KP", "flag-icons/kp.svg", "STR_FLAG_KP")
b.add(BADGE_CLASS_FLAG + "/KR", "flag-icons/kr.svg", "STR_FLAG_KR")
b.add(BADGE_CLASS_FLAG + "/KW", "flag-icons/kw.svg", "STR_FLAG_KW")
b.add(BADGE_CLASS_FLAG + "/KY", "flag-icons/ky.svg", "STR_FLAG_KY")
b.add(BADGE_CLASS_FLAG + "/KZ", "flag-icons/kz.svg", "STR_FLAG_KZ")
b.add(BADGE_CLASS_FLAG + "/LA", "flag-icons/la.svg", "STR_FLAG_LA")
b.add(BADGE_CLASS_FLAG + "/LB", "flag-icons/lb.svg", "STR_FLAG_LB")
b.add(BADGE_CLASS_FLAG + "/LC", "flag-icons/lc.svg", "STR_FLAG_LC")
b.add(BADGE_CLASS_FLAG + "/LI", "flag-icons/li.svg", "STR_FLAG_LI")
b.add(BADGE_CLASS_FLAG + "/LK", "flag-icons/lk.svg", "STR_FLAG_LK")
b.add(BADGE_CLASS_FLAG + "/LR", "flag-icons/lr.svg", "STR_FLAG_LR")
b.add(BADGE_CLASS_FLAG + "/LS", "flag-icons/ls.svg", "STR_FLAG_LS")
b.add(BADGE_CLASS_FLAG + "/LT", "flag-icons/lt.svg", "STR_FLAG_LT")
b.add(BADGE_CLASS_FLAG + "/LU", "flag-icons/lu.svg", "STR_FLAG_LU")
b.add(BADGE_CLASS_FLAG + "/LV", "flag-icons/lv.svg", "STR_FLAG_LV")
b.add(BADGE_CLASS_FLAG + "/LY", "flag-icons/ly.svg", "STR_FLAG_LY")
b.add(BADGE_CLASS_FLAG + "/MA", "flag-icons/ma.svg", "STR_FLAG_MA")
b.add(BADGE_CLASS_FLAG + "/MC", "flag-icons/mc.svg", "STR_FLAG_MC")
b.add(BADGE_CLASS_FLAG + "/MD", "flag-icons/md.svg", "STR_FLAG_MD")
b.add(BADGE_CLASS_FLAG + "/ME", "flag-icons/me.svg", "STR_FLAG_ME")
b.add(BADGE_CLASS_FLAG + "/MF", "flag-icons/mf.svg", "STR_FLAG_MF")
b.add(BADGE_CLASS_FLAG + "/MG", "flag-icons/mg.svg", "STR_FLAG_MG")
b.add(BADGE_CLASS_FLAG + "/MH", "flag-icons/mh.svg", "STR_FLAG_MH")
b.add(BADGE_CLASS_FLAG + "/MK", "flag-icons/mk.svg", "STR_FLAG_MK")
b.add(BADGE_CLASS_FLAG + "/ML", "flag-icons/ml.svg", "STR_FLAG_ML")
b.add(BADGE_CLASS_FLAG + "/MM", "flag-icons/mm.svg", "STR_FLAG_MM")
b.add(BADGE_CLASS_FLAG + "/MN", "flag-icons/mn.svg", "STR_FLAG_MN")
b.add(BADGE_CLASS_FLAG + "/MO", "flag-icons/mo.svg", "STR_FLAG_MO")
b.add(BADGE_CLASS_FLAG + "/MP", "flag-icons/mp.svg", "STR_FLAG_MP")
b.add(BADGE_CLASS_FLAG + "/MQ", "flag-icons/mq.svg", "STR_FLAG_MQ")
b.add(BADGE_CLASS_FLAG + "/MR", "flag-icons/mr.svg", "STR_FLAG_MR")
b.add(BADGE_CLASS_FLAG + "/MS", "flag-icons/ms.svg", "STR_FLAG_MS")
b.add(BADGE_CLASS_FLAG + "/MT", "flag-icons/mt.svg", "STR_FLAG_MT")
b.add(BADGE_CLASS_FLAG + "/MU", "flag-icons/mu.svg", "STR_FLAG_MU")
b.add(BADGE_CLASS_FLAG + "/MV", "flag-icons/mv.svg", "STR_FLAG_MV")
b.add(BADGE_CLASS_FLAG + "/MW", "flag-icons/mw.svg", "STR_FLAG_MW")
b.add(BADGE_CLASS_FLAG + "/MX", "flag-icons/mx.svg", "STR_FLAG_MX")
b.add(BADGE_CLASS_FLAG + "/MY", "flag-icons/my.svg", "STR_FLAG_MY")
b.add(BADGE_CLASS_FLAG + "/MZ", "flag-icons/mz.svg", "STR_FLAG_MZ")
b.add(BADGE_CLASS_FLAG + "/NA", "flag-icons/na.svg", "STR_FLAG_NA")
b.add(BADGE_CLASS_FLAG + "/NC", "flag-icons/nc.svg", "STR_FLAG_NC")
b.add(BADGE_CLASS_FLAG + "/NE", "flag-icons/ne.svg", "STR_FLAG_NE")
b.add(BADGE_CLASS_FLAG + "/NF", "flag-icons/nf.svg", "STR_FLAG_NF")
b.add(BADGE_CLASS_FLAG + "/NG", "flag-icons/ng.svg", "STR_FLAG_NG")
b.add(BADGE_CLASS_FLAG + "/NI", "flag-icons/ni.svg", "STR_FLAG_NI")
b.add(BADGE_CLASS_FLAG + "/NL", "flag-icons/nl.svg", "STR_FLAG_NL")
b.add(BADGE_CLASS_FLAG + "/NO", "flag-icons/no.svg", "STR_FLAG_NO")
b.add(BADGE_CLASS_FLAG + "/NP", "flag-icons/np.svg", "STR_FLAG_NP")
b.add(BADGE_CLASS_FLAG + "/NR", "flag-icons/nr.svg", "STR_FLAG_NR")
b.add(BADGE_CLASS_FLAG + "/NU", "flag-icons/nu.svg", "STR_FLAG_NU")
b.add(BADGE_CLASS_FLAG + "/NZ", "flag-icons/nz.svg", "STR_FLAG_NZ")
b.add(BADGE_CLASS_FLAG + "/OM", "flag-icons/om.svg", "STR_FLAG_OM")
b.add(BADGE_CLASS_FLAG + "/PA", "flag-icons/pa.svg", "STR_FLAG_PA")
# b.add(BADGE_CLASS_FLAG + "/PC", "flag-icons/pc.svg", "STR_FLAG_PC")
b.add(BADGE_CLASS_FLAG + "/PE", "flag-icons/pe.svg", "STR_FLAG_PE")
b.add(BADGE_CLASS_FLAG + "/PF", "flag-icons/pf.svg", "STR_FLAG_PF")
b.add(BADGE_CLASS_FLAG + "/PG", "flag-icons/pg.svg", "STR_FLAG_PG")
b.add(BADGE_CLASS_FLAG + "/PH", "flag-icons/ph.svg", "STR_FLAG_PH")
b.add(BADGE_CLASS_FLAG + "/PK", "flag-icons/pk.svg", "STR_FLAG_PK")
b.add(BADGE_CLASS_FLAG + "/PL", "flag-icons/pl.svg", "STR_FLAG_PL")
b.add(BADGE_CLASS_FLAG + "/PM", "flag-icons/pm.svg", "STR_FLAG_PM")
b.add(BADGE_CLASS_FLAG + "/PN", "flag-icons/pn.svg", "STR_FLAG_PN")
b.add(BADGE_CLASS_FLAG + "/PR", "flag-icons/pr.svg", "STR_FLAG_PR")
b.add(BADGE_CLASS_FLAG + "/PS", "flag-icons/ps.svg", "STR_FLAG_PS")
b.add(BADGE_CLASS_FLAG + "/PT", "flag-icons/pt.svg", "STR_FLAG_PT")
b.add(BADGE_CLASS_FLAG + "/PW", "flag-icons/pw.svg", "STR_FLAG_PW")
b.add(BADGE_CLASS_FLAG + "/PY", "flag-icons/py.svg", "STR_FLAG_PY")
b.add(BADGE_CLASS_FLAG + "/QA", "flag-icons/qa.svg", "STR_FLAG_QA")
b.add(BADGE_CLASS_FLAG + "/RE", "flag-icons/re.svg", "STR_FLAG_RE")
b.add(BADGE_CLASS_FLAG + "/RO", "flag-icons/ro.svg", "STR_FLAG_RO")
b.add(BADGE_CLASS_FLAG + "/RS", "flag-icons/rs.svg", "STR_FLAG_RS")
b.add(BADGE_CLASS_FLAG + "/RU", "flag-icons/ru.svg", "STR_FLAG_RU")
b.add(BADGE_CLASS_FLAG + "/RW", "flag-icons/rw.svg", "STR_FLAG_RW")
b.add(BADGE_CLASS_FLAG + "/SA", "flag-icons/sa.svg", "STR_FLAG_SA")
b.add(BADGE_CLASS_FLAG + "/SB", "flag-icons/sb.svg", "STR_FLAG_SB")
b.add(BADGE_CLASS_FLAG + "/SC", "flag-icons/sc.svg", "STR_FLAG_SC")
b.add(BADGE_CLASS_FLAG + "/SD", "flag-icons/sd.svg", "STR_FLAG_SD")
b.add(BADGE_CLASS_FLAG + "/SE", "flag-icons/se.svg", "STR_FLAG_SE")
b.add(BADGE_CLASS_FLAG + "/SG", "flag-icons/sg.svg", "STR_FLAG_SG")
# b.add(BADGE_CLASS_FLAG + "/SH/AC", "flag-icons/sh-ac.svg", "STR_FLAG_SHA")
# b.add(BADGE_CLASS_FLAG + "/SH/HL", "flag-icons/sh-hl.svg", "STR_FLAG_SHH")
b.add(BADGE_CLASS_FLAG + "/SH", "flag-icons/sh.svg", "STR_FLAG_SH")
# b.add(BADGE_CLASS_FLAG + "/SH/TA", "flag-icons/sh-ta.svg", "STR_FLAG_SHT")
b.add(BADGE_CLASS_FLAG + "/SI", "flag-icons/si.svg", "STR_FLAG_SI")
b.add(BADGE_CLASS_FLAG + "/SJ", "flag-icons/sj.svg", "STR_FLAG_SJ")
b.add(BADGE_CLASS_FLAG + "/SK", "flag-icons/sk.svg", "STR_FLAG_SK")
b.add(BADGE_CLASS_FLAG + "/SL", "flag-icons/sl.svg", "STR_FLAG_SL")
b.add(BADGE_CLASS_FLAG + "/SM", "flag-icons/sm.svg", "STR_FLAG_SM")
b.add(BADGE_CLASS_FLAG + "/SN", "flag-icons/sn.svg", "STR_FLAG_SN")
b.add(BADGE_CLASS_FLAG + "/SO", "flag-icons/so.svg", "STR_FLAG_SO")
b.add(BADGE_CLASS_FLAG + "/SR", "flag-icons/sr.svg", "STR_FLAG_SR")
b.add(BADGE_CLASS_FLAG + "/SS", "flag-icons/ss.svg", "STR_FLAG_SS")
b.add(BADGE_CLASS_FLAG + "/ST", "flag-icons/st.svg", "STR_FLAG_ST")
b.add(BADGE_CLASS_FLAG + "/SV", "flag-icons/sv.svg", "STR_FLAG_SV")
b.add(BADGE_CLASS_FLAG + "/SX", "flag-icons/sx.svg", "STR_FLAG_SX")
b.add(BADGE_CLASS_FLAG + "/SY", "flag-icons/sy.svg", "STR_FLAG_SY")
b.add(BADGE_CLASS_FLAG + "/SZ", "flag-icons/sz.svg", "STR_FLAG_SZ")
b.add(BADGE_CLASS_FLAG + "/TC", "flag-icons/tc.svg", "STR_FLAG_TC")
b.add(BADGE_CLASS_FLAG + "/TD", "flag-icons/td.svg", "STR_FLAG_TD")
b.add(BADGE_CLASS_FLAG + "/TF", "flag-icons/tf.svg", "STR_FLAG_TF")
b.add(BADGE_CLASS_FLAG + "/TG", "flag-icons/tg.svg", "STR_FLAG_TG")
b.add(BADGE_CLASS_FLAG + "/TH", "flag-icons/th.svg", "STR_FLAG_TH")
b.add(BADGE_CLASS_FLAG + "/TJ", "flag-icons/tj.svg", "STR_FLAG_TJ")
b.add(BADGE_CLASS_FLAG + "/TK", "flag-icons/tk.svg", "STR_FLAG_TK")
b.add(BADGE_CLASS_FLAG + "/TL", "flag-icons/tl.svg", "STR_FLAG_TL")
b.add(BADGE_CLASS_FLAG + "/TM", "flag-icons/tm.svg", "STR_FLAG_TM")
b.add(BADGE_CLASS_FLAG + "/TN", "flag-icons/tn.svg", "STR_FLAG_TN")
b.add(BADGE_CLASS_FLAG + "/TO", "flag-icons/to.svg", "STR_FLAG_TO")
b.add(BADGE_CLASS_FLAG + "/TR", "flag-icons/tr.svg", "STR_FLAG_TR")
b.add(BADGE_CLASS_FLAG + "/TT", "flag-icons/tt.svg", "STR_FLAG_TT")
b.add(BADGE_CLASS_FLAG + "/TV", "flag-icons/tv.svg", "STR_FLAG_TV")
b.add(BADGE_CLASS_FLAG + "/TW", "flag-icons/tw.svg", "STR_FLAG_TW")
b.add(BADGE_CLASS_FLAG + "/TZ", "flag-icons/tz.svg", "STR_FLAG_TZ")
b.add(BADGE_CLASS_FLAG + "/UA", "flag-icons/ua.svg", "STR_FLAG_UA")
b.add(BADGE_CLASS_FLAG + "/UG", "flag-icons/ug.svg", "STR_FLAG_UG")
b.add(BADGE_CLASS_FLAG + "/UM", "flag-icons/um.svg", "STR_FLAG_UM")
# b.add(BADGE_CLASS_FLAG + "/UN", "flag-icons/un.svg", "STR_FLAG_UN")
b.add(BADGE_CLASS_FLAG + "/US", "flag-icons/us.svg", "STR_FLAG_US")
b.add(BADGE_CLASS_FLAG + "/UY", "flag-icons/uy.svg", "STR_FLAG_UY")
b.add(BADGE_CLASS_FLAG + "/UZ", "flag-icons/uz.svg", "STR_FLAG_UZ")
b.add(BADGE_CLASS_FLAG + "/VA", "flag-icons/va.svg", "STR_FLAG_VA")
b.add(BADGE_CLASS_FLAG + "/VC", "flag-icons/vc.svg", "STR_FLAG_VC")
b.add(BADGE_CLASS_FLAG + "/VE", "flag-icons/ve.svg", "STR_FLAG_VE")
b.add(BADGE_CLASS_FLAG + "/VG", "flag-icons/vg.svg", "STR_FLAG_VG")
b.add(BADGE_CLASS_FLAG + "/VI", "flag-icons/vi.svg", "STR_FLAG_VI")
b.add(BADGE_CLASS_FLAG + "/VN", "flag-icons/vn.svg", "STR_FLAG_VN")
b.add(BADGE_CLASS_FLAG + "/VU", "flag-icons/vu.svg", "STR_FLAG_VU")
b.add(BADGE_CLASS_FLAG + "/WF", "flag-icons/wf.svg", "STR_FLAG_WF")
b.add(BADGE_CLASS_FLAG + "/WS", "flag-icons/ws.svg", "STR_FLAG_WS")
# b.add(BADGE_CLASS_FLAG + "/XK", "flag-icons/xk.svg", "STR_FLAG_XK")
# b.add(BADGE_CLASS_FLAG + "/XX", "flag-icons/xx.svg", "STR_FLAG_XX")
b.add(BADGE_CLASS_FLAG + "/YE", "flag-icons/ye.svg", "STR_FLAG_YE")
b.add(BADGE_CLASS_FLAG + "/YT", "flag-icons/yt.svg", "STR_FLAG_YT")
b.add(BADGE_CLASS_FLAG + "/ZA", "flag-icons/za.svg", "STR_FLAG_ZA")
b.add(BADGE_CLASS_FLAG + "/ZM", "flag-icons/zm.svg", "STR_FLAG_ZM")
b.add(BADGE_CLASS_FLAG + "/ZW", "flag-icons/zw.svg", "STR_FLAG_ZW")

# Historical flags or non-ISO flags
b.add(BADGE_CLASS_FLAG + "/yugoslavia", "Civil_Ensign_of_Yugoslavia_(1950–1992).svg", "STR_FLAG__YU")
b.add(BADGE_CLASS_FLAG + "/east_germany", "Flag_of_East_Germany.svg", "STR_FLAG_GDR")
b.add(BADGE_CLASS_FLAG + "/soviet_union", "Flag_of_the_Soviet_Union.svg", "STR_FLAG__SU")
b.add(BADGE_CLASS_FLAG + "/europe", "flag-icons/eu.svg", "STR_FLAG_EUROPE")

# Power types
b.add(BADGE_CLASS_POWER + "/steam", "steam.png", "STR_PROPULSION_STEAM")
b.add(BADGE_CLASS_POWER + "/diesel", "diesel.png", "STR_PROPULSION_DIESEL")
b.add(BADGE_CLASS_POWER + "/electric", "electric.svg", "STR_PROPULSION_ELECTRIC")
b.add(BADGE_CLASS_POWER + "/turbine", "turbine.svg", "STR_PROPULSION_GAS_TURBINE")

b.add(BADGE_CLASS_LIVERY + "/random/1cc", "dice.svg", "STR_LIVERY_COMPANY_RANDOM_1CC", flags=BadgeFlags.USE_COMPANY_PALETTE, filters=[filters.MakeCCFilter(filters.HueMasker(0), None)])
b.add(BADGE_CLASS_LIVERY + "/random/2cc", "dice.svg", "STR_LIVERY_COMPANY_RANDOM_2CC", flags=BadgeFlags.USE_COMPANY_PALETTE, filters=[filters.MakeCCFilter(None, filters.HueMasker(0))])
b.add(BADGE_CLASS_LIVERY + "/2cc", "2cc.svg", "STR_LIVERY_COMPANY_2CC", flags=BadgeFlags.USE_COMPANY_PALETTE, filters=[filters.MakeCCFilter(filters.HueMasker(300), filters.HueMasker(120))], overlay=True)

g.add(grf.Comment("Default Badges"))
g.add(b)

grf.main(g, "badges.grf")

b.generate_docs(Path("docs/badges"), "GRF Badges", grf.BPP_32, grf.ZOOM_2X)
