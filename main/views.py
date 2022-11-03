from django.shortcuts import render

# Create your views here.
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import YourSerializer, PnLSerializer
from _lib import panda

# report PO


@api_view(['GET'])
def report_PoManagementCopy(request, search_refno):

    querystr = '''
    #Query 1
    SELECT groupno,a.itemcode,
    LEFT(CONCAT(IF(barcode=a.itemcode,'',barcode),IF(articleno='' OR articleno=a.itemcode,'',CONCAT(' ',articleno))),25) AS barcode,
    packsize,articleno,line,
    IF(openingqty>1000,ROUND(openingqty),ROUND(openingqty,1)) AS openingqty,
    IF(soldqty>1000,ROUND(soldqty),ROUND(soldqty,1)) AS soldqty,
    datestart,posdate,issuestamp,
    podate,
    IF(DATE(laststamp)>podate,IF(MONTH(laststamp)<>MONTH(podate),LAST_DAY(CONCAT(LEFT(podate,7),'-01')),DATE(laststamp)),podate) AS date_range,
    IF(lastqty=0,'',DATE_FORMAT(grdate,'%%d/%%m/%%y')) AS grdate,
    IF(grqty>1000,ROUND(grqty),ROUND(grqty,1)) AS grqty,
    IF(other>1000 OR other <=-1000,ROUND(other),ROUND(other,1)) AS other,
    IF(psoldqty=0,'',IF(psoldqty<1000,ROUND(psoldqty,1),ROUND(psoldqty))) AS psoldqty,
    IF(pgrqty=0,'',IF(pgrqty<1000,ROUND(pgrqty,1),ROUND(pgrqty))) AS pgrqty,
    IF(pother=0,'',IF(pother>1000 OR pother<=-1000,ROUND(pother),ROUND(pother,1))) AS pother,
    IF(pqty=0,'',IF(pbalance>1000 OR pbalance<=-1000,ROUND(pbalance),ROUND(pbalance,1))) AS pbalance,
    IF(balanceqty>1000,ROUND(balanceqty),ROUND(balanceqty,1)) AS balanceqty,
    CONCAT(packsize,'/',bulkqty) AS ps,
    IF(bulkqty=1,0,IF(MOD((SUM(qty)+SUM(foc))/bulkqty,1)=0,(SUM(qty)+SUM(foc))/bulkqty,ROUND((SUM(qty)+SUM(foc))/bulkqty,1))) AS bqty,
    description,netunitprice,invactcost,SUM(foc) AS foc,SUM(qty) AS qty,totalprice,sellingprice,
    (SUM(foc)+SUM(qty))*sellingprice AS retailext,deliverdate,CONCAT(supplier,'  ',term) AS supplier,
    refno,expiry_date,IF(ROUND(lastcost,4)=ROUND(invactcost,4),'',ROUND(lastcost,4)) AS lastcost,totalprice AS totalcost,
    IF(stockday_pos_qty_avg*30<1000,ROUND(stockday_pos_qty_avg*30,1),ROUND(stockday_pos_qty_avg*30)) AS ams,
    IF(stockday_pos_qty_avg=0 AND (balanceqty+SUM(qty)+SUM(foc)+commitqty)<>0,999,
    (balanceqty+SUM(qty)+SUM(foc)+commitqty)/stockday_pos_qty_avg) AS doh,term,
    IF(pqty=0,'',IF((stockday_pos_qty_avg+pads)*30<1000,ROUND((stockday_pos_qty_avg+pads)*30,1),ROUND((stockday_pos_qty_avg+pads)*30))) AS pams,
    IF(pqty=0,'',ROUND((pbalance+SUM(foc)+SUM(qty)+commitqty)/(stockday_pos_qty_avg+pads))) AS pdoh,
    issuedby,laststamp,days,
    IF(ROUND(lastcost,4)<>ROUND(invactcost,4) AND scode<>CODE,IF(LEFT(CODE,5)='4000/',MID(CODE,6,6),LEFT(CODE,6)),'') AS lastsupcode,
    IF(sellingprice<=invactcost,'-','') AS pricechk,IF(ROUND(lastcost,4)<ROUND(invactcost,4) OR sellingprice<=invactcost OR pqty+commitqty<>0 OR 
    (pbalance+SUM(qty)+SUM(foc)+commitqty)>stock_max OR
    (pbalance+SUM(qty)+SUM(foc)+commitqty)<stock_min OR
    margin<cat_min OR margin>cat_max OR (pbalance+SUM(qty)+SUM(foc)+commitqty<>0 AND stockday_pos_qty_avg=0) OR mrank NOT IN ('A','B'),'X','') AS chk,
    IF(lastqty>1000,ROUND(lastqty),ROUND(lastqty,1)) AS lastqty,
    IF(commitqty<=0,'','O/S PO->') AS commitdesc,IF(commitqty=0,'',CONCAT('OS PO: ',ROUND(commitunitcost,4),' x ',CONCAT(ROUND(commitqty)))) AS commitqty,
    IF(commitcost=0,'',ROUND(commitcost,2)) AS commitcost,IF(commitunitcost=0,'',ROUND(commitunitcost,4)) AS commitunitcost,
    IF((scode<>CODE AND ROUND(lastcost,4)<>ROUND(invactcost,4)) OR pqty+commitqty<>0 OR ROUND(netunitprice,4)<>ROUND(invactcost,4) OR 
    ROUND(price_future,2)<>ROUND(sellingprice,2) OR (pbalance+SUM(qty)+SUM(foc)+commitqty)<stock_min OR (pbalance+SUM(qty)+SUM(foc)+commitqty)>stock_max,'X','') AS chk2,
    IF(pqty=0,'','Pending:') AS pending,DATE_ADD(podate,INTERVAL -365 DAY) AS grstart,
    IF(openingqty=0 AND soldqty<>0,CONCAT('1st tran: ',DATE_FORMAT(posdate,'%%d/%%m/%%y'),'=',TO_DAYS(podate)-TO_DAYS(posdate),' day'),'') AS solddate,
    total,discount1*-1 AS discount1,discount2,
    IF(ROUND(netunitprice,4)=ROUND(invactcost,4) AND cost_manual=0,'',ROUND(invactcost,4)) AS nettcost,IF(ROUND(netunitprice,4)=ROUND(invactcost,4),'','Net') AS nettcostdesc,
    itemremark,remark,posdate1,
    IF(ROUND(price_future,2)=ROUND(price_posnet,2),'',ROUND(price_future,2)) AS price_future,
    IF(ROUND(price_future,2)=ROUND(price_posnet,2),'',ROUND(((price_future*100/(100+gst_tax_rate))-invactcost)/(price_future*100/(100+gst_tax_rate*100)),1)) AS margin_future,
    IF(ROUND(price_future,2)=ROUND(price_posnet,2),'','<- future') AS price_future_desc,

    IF(stock_min>1000,ROUND(stock_min),ROUND(stock_min,1)) AS stock_min,
    IF(stock_max>1000,ROUND(stock_max),ROUND(stock_max,1)) AS stock_max,
    IF((pbalance+SUM(qty)+SUM(foc)+commitqty)<stock_min OR (pbalance+SUM(qty)+SUM(foc)+commitqty)>stock_max,'.','') AS chk_min,
    IF((pbalance+SUM(qty)+SUM(foc)+commitqty)>=stock_min AND (pbalance+SUM(qty)+SUM(foc)+commitqty)<=stock_max,'',' (Sug)') AS sug_desc,
    IF((pbalance+SUM(qty)+SUM(foc)+commitqty)>=stock_min AND (pbalance+SUM(qty)+SUM(foc)+commitqty)<=stock_max,'',
    IF((pbalance+SUM(qty)+SUM(foc)+commitqty)>stock_max,
    IF(stock_max-(pbalance+commitqty)<0,0,ROUND(stock_max-(pbalance+commitqty))),
    IF((pbalance+SUM(qty)+SUM(foc)+commitqty)<stock_min,ROUND(stock_max-(pbalance+commitqty)),''))) AS qty_sug,

    CONCAT(gst_tax_type,ROUND(a.price_include_tax,2),
    IF(ROUND(price_future,2)=ROUND(a.price_include_tax,2),'',CONCAT(' F$ ',ROUND(price_future,2),' (',
    ROUND(((price_future*100/(100+gst_tax_rate))-invactcost)/(price_future*100/(100+gst_tax_rate))*100,1),'%%) ')),
    IF(margin BETWEEN cat_min AND cat_max,'',CONCAT(' GP ',IF(RIGHT(cat_min,2)='00',ROUND(cat_min),cat_min),'%%-',
    IF(RIGHT(cat_max,2)='00',ROUND(cat_max),cat_max),'%%')),
    IF(promo IS NULL,'',CONCAT(' ',promo,' (',ROUND((b.price_include_tax-(invactcost-bare_supplier))/b.price_include_tax*100,1),'%%) '))) AS promo,

    IF(hqcost_desc<>'',hqcost_desc,IF(SUM(groupcost)=1,'',IF(SUM(qty)=0 AND SUM(foc)<>0 AND invactcost<>0,'Avg Cost Dist->',
    IF(SUM(qty)<>0 AND SUM(foc)<>0,'Not Group Cost->','')))) AS hqcost_desc,margin,IF(margin BETWEEN cat_min AND cat_max,'','.') AS chk_margin,
    mrank,IF(mrank NOT IN ('A','B'),'.','') AS chk_rank,IF(SUM(rebate)=0,'',ROUND(SUM(rebate),2)) AS rebate,
    IF(SUM(rebate)=0,'','Rebate DN->') AS rebate_desc,
    invactcost,bare_supplier,a.price_include_tax
    FROM

    (SELECT groupno,a.itemcode,a.itemlink,packsize,stockday_openingqty AS openingqty,stockday_pos_qty_sum AS soldqty,stockday_recqty AS grqty,
    stockday_adjustqty+stockday_hamperqty+stockday_creditqty+stockday_debitqty AS other,stockday_pos_qty_avg,stockday_onhandqty,stockday_soqty,
    stockday_poqty,stockday_min_qty AS stock_min,
    stockday_max_qty AS stock_max,psoldqty,pgrqty,pother,articleno,line,psoldqty/stockday_interval_days AS pads,stockday_interval_days AS days,
    stockday_onhandqty AS balanceqty,stockday_onhandqty+pgrqty+pother-psoldqty AS pbalance,pgrqty+pother+psoldqty AS pqty,
    stockday_first_grn_date AS datestart1,
    stockday_first_grn_date AS posdate,
    stockday_first_grn_date AS posdate1,
    IF(stockday_first_grn_date IS NULL,'',DATE_FORMAT(stockday_first_grn_date,'%%d/%%m')) AS posdate2,podate,last_grndate AS grdate,a.description,
    barcode,netunitprice,IF(cost_manual=0,invactcost,cost_manual_value) AS invactcost,
    IF(cost_manual=0,'','HQ Manual Cost->') AS hqcost_desc,groupcost,a.refno,
    IF(pricetype='foc',a.qty,0) AS foc,IF(pricetype<>'foc',a.qty,0) AS qty,totalprice,sellingprice,onhandqty,CONCAT(scode,' - ',sname) AS supplier,
    deliverdate,expiry_date,issuedby,laststamp,location,CONCAT('(Term: ',sterm,'  Min DOH: ',stockday_min,'  Max DOH: ',stockday_max,')') AS term,
    lastcost,scode,last_supcode AS CODE,last_qty AS lastqty,IF(stockday_poqty<=0,0,stockday_poqty) AS commitqty,
    ROUND(stockday_poamount/stockday_poqty,4) AS commitunitcost,stockday_poamount AS commitcost,total-(rebate_amt+dn_amt) AS total,
    discount1+rebate_amt+dn_amt AS discount1,discount2,
    IF(discount1=0,'',CONCAT(discount1,IF(discount1type=0,' $',' %%'))) AS discount1_old,
    IF(discount2=0,'',CONCAT(discount2,IF(discount2type=0,' $',' %%'))) discount2_old,
    IF(itemremark IS NULL,'',itemremark) AS itemremark,IF(b.remark IS NULL,'',b.remark) AS remark,price_posnet,price_future,stockday_min,
    stockday_max,stockday_first_grn_date AS datestart,bulkqty,cat_min,cat_max,
    ROUND((sellingprice-IF(cost_manual=0,invactcost,cost_manual_value))/sellingprice*100,1) AS margin,loc_group AS locgroup,mrank,
    costaftdisc AS rebate,cost_manual,a.gst_tax_rate,IF(a.gst_tax_rate=0,'z','s') AS gst_code,
    a.price_include_tax,
    CAST(CONCAT(LEFT(gst_tax_type,1),'$') AS CHAR) AS gst_tax_type,
    issuestamp

    FROM backend.pochild a

    INNER JOIN backend.pomain b ON a.refno=b.refno

    WHERE a.refno=%s
    ORDER BY groupno,pricetype DESC,description

    LIMIT 18446744073709551615) a

    LEFT JOIN

    (SELECT loc_group,itemcode,price_net,bare_supplier_1,bare_supplier_2,bare_supplier_type,promo_by_tragetprice,
    CONCAT(DATE_FORMAT(datefrom,'%%d/%%m'),' - ',DATE_FORMAT(dateto,'%%d/%%m'),' P$',ROUND(price_net,2),
    IF(bare_supplier+bare_supplier_2=0,'',CONCAT(' + claim $',ROUND(bare_supplier,2)))) AS promo,
    bare_supplier,price_include_tax FROM

    (SELECT e.loc_group,location,datefrom,dateto,c.itemcode,c.cardtype,
    price_net AS price_net_1,sellingprice,IF(cost_manual=0,invactcost,cost_manual_value) AS invactcost,
    bare_supplier_type,bare_supplier AS bare_supplier_1,bare_supplier_2,promo_by_tragetprice,
    c.disc1type,c.disc1value,c.disc2type,c.disc2value,
    IF(promo_by_tragetprice=1,price_net,sellingprice-IF(c.disc1type='$',c.disc1value,ROUND(sellingprice*c.disc1value/100,2))-
    IF(c.disc2type='$',c.disc2value,ROUND((sellingprice-ROUND(sellingprice*c.disc1value/100,2))*c.disc2value/100,2))) AS price_net,

    IF(promo_by_tragetprice=1,price_target-price_net,IF(c.disc1type='$',c.disc1value,
    ROUND(sellingprice*c.disc1value/100,2))+
    IF(c.disc2type='$',c.disc2value,ROUND((sellingprice-ROUND(sellingprice*c.disc1value/100,2))*c.disc2value/100,2))) AS disc_value,

    IF(supplier_claim=0,0,IF(bare_supplier_type='$',bare_supplier+bare_supplier_2,
    IF(LEFT(bare_supplier_type,6)='%% Cost',
    ROUND((IF(cost_manual=0,invactcost,cost_manual_value)*bare_supplier/100)+
    ((IF(cost_manual=0,invactcost,cost_manual_value)-(IF(cost_manual=0,invactcost,cost_manual_value)*bare_supplier/100))*bare_supplier_2/100),2),
    IF(LEFT(bare_supplier_type,6)='%% Pric',
    ROUND((IF(promo_by_tragetprice=1,price_target,sellingprice)*bare_supplier/100)+
    ((IF(promo_by_tragetprice=1,price_target,sellingprice)-(IF(promo_by_tragetprice=1,price_target,sellingprice)*bare_supplier/100))*bare_supplier_2/100),2),
    ROUND(((IF(promo_by_tragetprice=1,price_target-price_net,IF(c.disc1type='$',c.disc1value,
    ROUND(sellingprice*c.disc1value/100,2))+
    IF(c.disc2type='$',c.disc2value,ROUND((sellingprice-ROUND(sellingprice*c.disc1value/100,2))*c.disc2value/100,2))))*bare_supplier/100)+
    (((IF(promo_by_tragetprice=1,price_target-price_net,IF(c.disc1type='$',c.disc1value,
    ROUND(sellingprice*c.disc1value/100,2))+
    IF(c.disc2type='$',c.disc2value,ROUND((sellingprice-ROUND(sellingprice*c.disc1value/100,2))*c.disc2value/100,2))))-
    ((IF(promo_by_tragetprice=1,price_target-price_net,IF(c.disc1type='$',c.disc1value,
    ROUND(sellingprice*c.disc1value/100,2))+
    IF(c.disc2type='$',c.disc2value,ROUND((sellingprice-ROUND(sellingprice*c.disc1value/100,2))*c.disc2value/100,2))))*bare_supplier/100))*bare_supplier_2/100),2))))) AS bare_supplier,
    c.price_include_tax

    FROM backend.pochild a
    INNER JOIN backend.pomain b
    ON a.refno=b.refno
    INNER JOIN backend.promo_supplier_c c
    ON a.itemcode=c.itemcode
    INNER JOIN backend.promo_supplier d
    ON c.pvc_guid=d.pvc_guid
    INNER JOIN backend.promo_supplier_loc e
    ON b.loc_group=e.loc_group AND d.pvc_guid=e.pvc_guid
    WHERE a.refno=%s AND cancelpromo=0 AND d.posted=1 AND (podate BETWEEN datefrom AND dateto) AND trans_type IN ('pgl','psc')
    AND c.cardtype='NA'
    ORDER BY itemcode,posted_at DESC

    LIMIT 18446744073709551615) a
    GROUP BY itemcode,loc_group) b
    ON a.locgroup=b.loc_group AND a.itemcode=b.itemcode

    GROUP BY groupno,itemcode
    ORDER BY groupno,description
    '''

    result = panda.raw_query(querystr, [search_refno, search_refno])
    result = {"query1": result}

    querystr = """
    SELECT refno,sequence,CONCAT(IF(build_into_cost=0,'NS-','S-'),IF(dn=0,CODE,'DN'),' (',surcharge_disc_type,')') AS code_grn,surcharge_disc_value*Value_Factor AS value_grn
    FROM backend.trans_surcharge_discount 
    WHERE refno=%s

    UNION ALL

    SELECT refno,'99' AS sequence,'S-Rebate DN' AS code_grn,SUM(rebate_value)*-1 AS value_grn FROM backend.pochild
    WHERE refno=%s AND rebate_value<>0
    HAVING SUM(rebate_value) IS NOT NULL

    ORDER BY sequence;
    """
    result2 = panda.raw_query(querystr, [search_refno, search_refno])
    result["query2"] = result2

    querystr = """
    #Query 3
    SELECT dbtype,itemcode,refno,description,packsize,lastcost,SUM(qty) AS qty,SUM(totalcost) AS totalcost,reason,scan_barcode,created_at,
    created_by FROM

    (SELECT 'Goods To Be Returned' AS dbtype,itemcode,'GR Basket' AS refno,a.description,packsize,lastcost,qty,lastcost*qty AS totalcost,
    reason,scan_barcode,created_at,created_by 
    FROM backend.dbnote_basket a
    INNER JOIN backend.pomain b
    ON a.sup_code=b.scode
    WHERE converted=0 AND b.refno=%s

    UNION ALL

    SELECT 'Goods To Be Returned' AS dbtype,itemcode,'GR Basket' AS refno,c.description,packsize,lastcost,qty,lastcost*qty AS totalcost,
    reason,scan_barcode,a.created_at,a.created_by 
    FROM backend.dbnote_batch a

    INNER JOIN backend.dbnote_batch_c c
    ON a.dbnote_guid=c.dbnote_guid

    INNER JOIN backend.pomain b
    ON a.sup_code=b.scode
    WHERE converted=0 AND canceled=0 AND b.refno=%s
    AND b.`loc_group` = a.`loc_group`

    UNION ALL

    SELECT 'DN Created But Not Posted' AS dbtype,itemcode,b.refno,a.description,packsize,unitprice AS lastcost,qty,totalprice AS totalcost,reason,barcode AS scan_barcode,b.issuestamp AS created_at,b.issuedby AS created_by FROM backend.dbnotechild a
    INNER JOIN backend.dbnotemain b
    ON a.refno=b.refno
    INNER JOIN backend.pomain c
    ON b.CODE=c.scode
    WHERE b.billstatus=0 AND c.refno=%s
    AND b.`locgroup` = c.loc_group

    ORDER BY dbtype,created_at

    LIMIT 18446744073709551615) a

    GROUP BY dbtype,refno,itemcode,lastcost
    """
    result3 = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno])
    result["query3"] = result3

    querystr = """
    SELECT IF(a.remark IS NULL OR a.remark='',(SELECT CONCAT(companyname,' @ ',IF(c.description='' OR c.description IS NULL,loc_group,c.description)) 
    FROM backend.companyprofile a
    INNER JOIN backend.pomain b
    INNER JOIN backend.locationgroup c
    ON b.loc_group=c.CODE
    WHERE refno=%s),(SELECT remark FROM backend.location WHERE CODE=(SELECT location FROM backend.pomain WHERE refno=%s))) AS companyname,
    IF(consign=1,'CONSIGNMENT ORDER NOTE',IF(in_kind=1,'IN-KIND PURCHASE ORDER',
    IF(stock_returnable=0,'PURCHASE ORDER - OUTRIGHT NON-RETURNABLE','PURCHASE ORDER - OUTRIGHT RETURNABLE'))) AS title,location,
    CONCAT(b.scode,' - ',b.sname) AS supplier ,b.refno AS refno
    FROM backend.location a
    INNER JOIN backend.pomain b
    ON a.CODE=b.location
    INNER JOIN backend.supcus c
    ON b.scode=c.CODE
    WHERE refno=%s AND TYPE='s'
    """
    result4 = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno])
    result["query4"] = result4

    return Response(result, status=status.HTTP_200_OK)

# report PO


@api_view(['GET'])
def report_PoSupplierCopy(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT a.*,b.* FROM

    (SELECT CONCAT(IF(ibt='1','Branch Code  ','Supplier Code  '),scode,' - ',sname) AS supplier,stel,sfax,sterm,location,refno,podate,deliverdate,expiry_date,
    IF(in_kind=0,subtotal1,0) AS subtotal1,discount1 * -1 AS discount1,subtotal2,discount2,total,DATE_FORMAT(issuestamp,'%%d-%%m-%%Y %%H:%%i:%%s') AS issuestamp,issuedby,DATE_FORMAT(postdatetime,'%%d-%%m-%%Y %%H:%%i:%%s') AS postdatetime,postby,approvedby,DATE_FORMAT(a.laststamp,'%%d-%%m-%%Y %%H:%%i:%%s') AS laststamp,
    a.remark,
    IF(discount1type=1,'%%','$') AS discount1type,IF(discount2type=1,'%%','$') AS discount2type,
    contact,add1,add2,add3,city,state,postcode,country,
    CONCAT('PO Date ',DATE_FORMAT(podate,'%%Y-%%m-%%d %%a'),'    Deliver on ',
    DATE_FORMAT(deliverdate,'%%Y-%%m-%%d %%a'),'    Expiry ',DATE_FORMAT(expiry_date,'%%Y-%%m-%%d %%a')) AS date_po,

    IF(consign=1,'CONSIGNMENT           ORDER NOTE',IF(in_kind=1,'PURCHASE ORDER           STOCK IN-KIND',
    IF(stock_returnable=0,'PURCHASE ORDER   OUTRIGHT NON RETURNABLE','PURCHASE ORDER   OUTRIGHT RETURNABLE'))) AS title,

    IF(consign=1,'Consignment','Purchase Order') AS title_1,
    IF(consign=1,'Order Note',IF(in_kind=1,'Stock In-Kind',IF(stock_returnable=0,'Outright Non Returnable','Outright Returnable'))) AS title_2,

    IF(ibt=1,IF(ibt_gst=0,'PO - Inter Branch Transfer Inwards','PO - Inter Branch Transfer Inwards'),
    IF(ibt=2,IF(consign=0,IF(ibt_gst=0,'Purchase Order','Purchase Order'),
    IF(ibt_gst=0,'Consignment Note','Consignment Note')),
    IF(consign=1,'Consignment Order Note',IF(in_kind=1,'Purchase Order Stock In-Kind',
    IF(stock_returnable=0,'Purchase Order','Purchase Order'))))) AS title_3,

    IF(ibt=1,IF(ibt_gst=0,'Inter Branch Stock Transfer Inwards from','Inter Branch Stock Transfer Inwards from'),
    IF(ibt=2,IF(ibt_gst=0,'Purcahse from Inter Company Supplier','Purcahse from Inter Company Supplier'),
    IF(a.tax_code_purchase='NR','Purchase from Supplier',IF(e.gst_tax_rate=0,
    'Purchase from Supplier','Purchase from Supplier')))) AS title_gst,

    IF(ibt=1,'Inter Branch Stock Transfer Request by',
    IF(ibt=2,'Inter Company Purchase Order Issued by',
    'Purchase Order Issued by')) AS title_po,
    IF(ibt=1,'Branch Code','Supplier Code') AS title_sup,

    IF(ibt=1,'IBT Branch Copy',IF(ibt=2,'Inter Co Supplier Co','Supplier Copy')) AS title_supcopy,
    doc_name_reg,
    IF(in_kind=1,'Stock In-Kind Net','PO Net Amount') AS total_net_desc,approved_by,DATE_FORMAT(approved_at,'%%d-%%m-%%Y %%H:%%i:%%s') AS approved_at,
    CONCAT('Tel: ',stel,'    Fax: ',sfax) AS contact_sup,
    CONCAT(a.location,' - ',d.description) AS loc_desc,
    CONCAT('Co Reg No: ',reg_no,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no,
    IF((SELECT COUNT(DISTINCT(gst_tax_code)) AS gst_count 
    FROM backend.pochild a
    INNER JOIN backend.pomain b
    ON a.refno=b.refno
    WHERE a.refno=%s
    GROUP BY a.refno)=1,CONCAT('    Tax Code: ',tax_code_purchase),'')))) reg_sup,
    IF(c.b2b_registration=1,'B2B','') AS watermark,
    IF((SELECT set_enable FROM backend.`set_module_features` WHERE module_feature = 'Display "No Signature Is Required" @ Docoument')=1,
    '***This document is computer generated. No signature is required.***','') AS no_signature

    FROM backend.pomain a
    INNER JOIN backend.supcus c
    ON a.scode=c.CODE
    INNER JOIN backend.location d
    ON a.location=d.CODE
    LEFT JOIN backend.set_gst_table e
    ON a.tax_code_purchase=e.gst_tax_code
    WHERE refno=%s AND billstatus=1 AND TYPE='s') a

    INNER JOIN

    (SELECT /*IF(remark IS NULL OR remark='',IF(branch_name ='' OR branch_name IS NULL,companyname,branch_name),remark)*/
    IF(branch_name='' OR branch_name IS NULL,companyname,branch_name) AS companyname,
    (SELECT poremark1 FROM backend.xsetup) AS poremark1,
    (SELECT poremark2 FROM backend.xsetup) AS poremark2,
    (SELECT poremark3 FROM backend.xsetup) AS poremark3,
    IF(branch_add='' OR branch_add IS NULL,address1,'') AS address1,
    IF(branch_add='' OR branch_add IS NULL,address2,'') AS address2,
    IF(branch_add='' OR branch_add IS NULL,address3,'') AS address3,
    IF(branch_add='' OR branch_add IS NULL,CONCAT('Tel: ',tel,'    Fax: ',fax),CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax)) AS contactnumber,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,
    CONCAT('Co Reg No: ',IF(reg_no='' OR reg_no IS NULL,comp_reg_no,reg_no),IF(branch_gst='' OR branch_gst IS NULL,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no)),
    CONCAT('    GST Reg No: ',branch_gst))) reg_no,
    a.refno 
    FROM backend.pomain a

    INNER JOIN backend.companyprofile

    LEFT JOIN 
    (SELECT reg_no,gst_no AS branch_gst,name_reg,scode,
    IF(loc_address='' OR loc_address IS NULL,branch_add,loc_address) AS branch_add,
    branch_name,
    IF(loc_tel='' OR loc_tel IS NULL,branch_tel,loc_tel) AS branch_tel,
    IF(loc_fax='' OR loc_fax IS NULL,branch_fax,loc_fax) AS branch_fax
    FROM backend.pomain a
    INNER JOIN backend.cp_set_branch b
    ON a.loc_group=b.branch_code
    INNER JOIN backend.supcus c
    ON b.set_supplier_code=c.CODE

    LEFT JOIN backend.location d
    ON a.location=d.code

    WHERE refno=%s) b

    ON a.scode=b.scode

    WHERE a.refno=%s) b

    ON a.refno=b.refno
    """

    result = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno])
    result = {"query1": result}

    querystr = """
    #Query 2
    SELECT a.*, IF(balanceqty>1000,ROUND(balanceqty),ROUND(balanceqty,1)) AS balanceqty,
    IF(stockday_pos_qty_avg=0 AND (balanceqty+SUM(a_qty)+SUM(foc)+commitqty)<>0,999,
    (balanceqty+SUM(a_qty)+SUM(foc)+commitqty)/stockday_pos_qty_avg) AS doh,
    IF(stockday_pos_qty_avg*30<1000,ROUND(stockday_pos_qty_avg*30,1),ROUND(stockday_pos_qty_avg*30)) AS ams FROM
    (
    SELECT line,barcode,itemcode,itemlink,description,qty,netunitprice,packsize,poitemavgcost,receivedqty,totalprice,
    mrank,lastpesalesqty,sales_current,onhandqty,lastcost,sellingprice,itemremark,a.refno,groupno,
    IF(purtolerance_std_plus=0 AND purtolerance_std_minus=0,'','Tolerance:') AS tolerance_desc,
    IF(purtolerance_std_plus=0 AND purtolerance_std_minus=0,'',CONCAT('Target: ',purtolerance_std_minus,' /',um)) AS tolerance_desc1,
    IF(purtolerance_std_plus=0,'',purtolerance_std_plus) AS tolerance_plus,
    IF(purtolerance_std_minus=0,'',purtolerance_std_minus) AS tolerance_minus,
    disc1type,disc2type,IF(pricetype<>'FOC','','foc') AS pricetype,LOWER(um) AS um,
    discamt,
    IF(qty<bulkqty OR bulkqty=1,'',CONCAT('= ',IF(MOD(qty/bulkqty,1)=0,qty/bulkqty,ROUND(qty/bulkqty,1)),' ',umbulk)) AS ctn,
    IF(disc1value=0,'',IF(disc1type='%%',CONCAT(ROUND(disc1value,2),disc1type),CONCAT(disc1type,ROUND(disc1value,2)))) AS disc1value,
    IF(disc2value=0,'',IF(disc2type='%%',CONCAT(ROUND(disc2value,2),disc2type),CONCAT(disc2type,ROUND(disc2value,2)))) AS disc2value,

    CONCAT(IF(disc1value=0,'',IF(disc1type='%%',CONCAT(IF(MOD(disc1value,1)=0,ROUND(disc1value),ROUND(disc1value,2)),disc1type),
    CONCAT(disc1type,ROUND(disc1value,2)))),IF(disc2value=0,'',IF(disc2type='%%',CONCAT(' + ',IF(MOD(disc1value,2)=0,
    ROUND(disc2value),ROUND(disc2value,2)),disc2type),CONCAT(disc2type,ROUND(disc2value,2))))) AS disc_desc,
    IF(a.gst_tax_rate=0,'Z','S') AS gst_unit_code,
    ROUND(gst_tax_amount/qty,4) AS gst_unit_tax,

    /*ROUND(IF(hcost_po=0,netunitprice+(gst_tax_amount/qty),((totalprice-(hcost_po))+gst_tax_amount)/qty),4) AS gst_unit_cost,*/
    ROUND(IF(discvalue=0 AND surchgvalue=0,netunitprice+(gst_tax_amount/qty),((totalprice-(discvalue+surchgvalue))+gst_tax_amount)/qty),4) AS gst_unit_cost,

    gst_tax_amount AS gst_child_tax,

    /*ROUND(((totalprice-(hcost_po))+gst_tax_amount),2) AS gst_unit_total,*/
    ROUND(((totalprice-(discvalue+surchgvalue))+gst_tax_amount),2) AS gst_unit_total,


    gst_tax_sum AS gst_main_tax,
    ROUND(total+gst_tax_sum,2) AS gst_main_total,
    CONCAT(packsize,IF(bulkqty=1,'',CONCAT('/',bulkqty))) AS ps,

    unitprice,bulkqty,articleno,
    IF(in_kind=1,'Total Stock In-Kind','Total Before Tax') AS total_desc,
    gst_tax_code,a.gst_tax_rate,

    IF(LENGTH(MID(gst_tax_amount,POSITION('.' IN gst_tax_amount)+1,10))<=2,FORMAT(gst_tax_amount,2),
    FORMAT(gst_tax_amount,4)) AS gst_tax_amount,

    LENGTH(MID(gst_tax_amount,POSITION('.' IN gst_tax_amount)+1,10)) AS test,

    /*ROUND((hcost_po)/qty,4) AS unit_disc_prorate,
    ROUND(IF(hcost_po=0,netunitprice,(totalprice-(hcost_po))/qty),4) AS unit_price_bfr_tax,
    ROUND((totalprice-(hcost_po)),2) AS total_price_bfr_tax,*/

    IF(bqty=0 OR bqty=qty,'',IF(bulkqty=packsize,'',CONCAT('[',Bqty,' ',LOWER(umbulk),IF(pqty=0,'',CONCAT(' ',Pqty)),']'))) AS b_qty,
    CONCAT(itemcode,'  ',IF(articleno IS NULL,'',IF(articleno=itemcode,'',articleno))) AS sku_article,


    ROUND((discvalue+surchgvalue)/qty,4) AS unit_disc_prorate,
    ROUND(IF(discvalue=0 AND surchgvalue=0,netunitprice,(totalprice-(discvalue+surchgvalue))/qty),4) AS unit_price_bfr_tax,
    ROUND((totalprice-(discvalue+surchgvalue)),2) AS total_price_bfr_tax,
    stockday_onhandqty AS balanceqty,
    IF(pricetype='foc',a.qty,0) AS foc,
    IF(pricetype<>'foc',a.qty,0) AS a_qty,
    IF(stockday_poqty<=0,0,stockday_poqty) AS commitqty,
    stockday_pos_qty_avg


    FROM backend.pochild a
    INNER JOIN backend.pomain b
    ON a.refno=b.refno
    WHERE a.refno=%s AND billstatus=1) a

    GROUP BY line

    ORDER BY groupno,pricetype,line;
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["query2"] = result2

    querystr = """
    #Query3
    SELECT b.*,
    CONCAT('Important Note :  Below is the list of item to be returned to you.  Kindly arrange your transport team to collect from us within ',d.`stk_rtn_collect_day`,' days from the date hereof.') AS note 
    FROM 

    (SELECT dbtype,itemcode,refno,description,packsize,lastcost,SUM(qty) AS qty,SUM(totalcost) AS totalcost,reason,scan_barcode,created_at,
    created_by,porefno FROM

    (SELECT 'Goods To Be Returned' AS dbtype,itemcode,'GR Basket' AS refno,a.description,packsize,lastcost,qty,lastcost*qty AS totalcost,
    reason,scan_barcode,created_at,created_by,b.refno AS porefno
    FROM backend.dbnote_basket a
    INNER JOIN backend.pomain b
    ON a.sup_code=b.scode
    WHERE converted=0 AND b.refno=%s

    UNION ALL

    SELECT 'Goods To Be Returned' AS dbtype,itemcode,'GR Basket' AS refno,c.description,packsize,lastcost,qty,lastcost*qty AS totalcost,
    reason,scan_barcode,a.created_at,a.created_by,b.refno AS porefno
    FROM backend.dbnote_batch a

    INNER JOIN backend.dbnote_batch_c c
    ON a.dbnote_guid=c.dbnote_guid

    INNER JOIN backend.pomain b
    ON a.sup_code=b.scode
    WHERE converted=0 AND b.refno=%s
    AND b.`loc_group` = a.`loc_group`

    UNION ALL

    SELECT 'DN Created But Not Posted' AS dbtype,itemcode,b.refno,a.description,packsize,unitprice AS lastcost,qty,totalprice AS totalcost,
    reason,barcode AS scan_barcode,b.issuestamp AS created_at,b.issuedby AS created_by,c.refno AS porefno
    FROM backend.dbnotechild a
    INNER JOIN backend.dbnotemain b
    ON a.refno=b.refno
    INNER JOIN backend.pomain c
    ON b.CODE=c.scode
    WHERE b.billstatus=0 AND c.refno=%s
    AND b.`locgroup` = c.loc_group

    ORDER BY dbtype,created_at

    LIMIT 18446744073709551615) a

    GROUP BY itemcode) b

    INNER JOIN backend.pomain c
    ON b.porefno = c.`RefNo`
    INNER JOIN backend.`supcus` d
    ON c.`SCode` = d.`Code`
    WHERE c.`RefNo` = %s;
    """
    result3 = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno])
    result["query3"] = result3

    querystr = """
    SELECT a.*,b.* FROM

    (SELECT 'A' AS sort,refno,sequence,CONCAT(CODE,' (',surcharge_disc_type,')') AS code_grn,surcharge_disc_value*Value_Factor AS value_grn,
    ROUND(value_calculated,2) AS value_calculated
    FROM backend.trans_surcharge_discount 
    WHERE refno=%s AND dn=0 /*AND Value_Factor=-1*/

    /*UNION ALL

    SELECT 'B' AS sort,refno,'1' AS sequence,'Total After Discount' AS code_grn,0 AS value_grn,
    subtotal2 AS value_calculated FROM backend.pomain
    WHERE refno=%s AND discount1<>0

    UNION ALL

    SELECT 'C' AS sort,refno,sequence,
    CONCAT(CODE,' (',surcharge_disc_type,')') AS code_grn,
    surcharge_disc_value*Value_Factor AS value_grn,
    ROUND(value_calculated,2) AS value_calculated
    FROM backend.trans_surcharge_discount 
    WHERE refno=%s AND dn=0 AND Value_Factor=1*/

    UNION ALL

    SELECT 'D' AS sort,refno,'1' AS sequence,'Total After Surcharge/Discount' AS code_grn,0 AS value_grn,
    total AS value_calculated FROM backend.pomain
    WHERE refno=%s AND discount2<>0

    UNION ALL

    SELECT 'E1' AS sort,refno,'1' AS sequence,'Item Tax Amount' AS code_grn,0 AS value_grn,
    ROUND(gst_tax_sum,2) AS value_calculated FROM backend.pomain
    WHERE refno=%s

    UNION ALL

    SELECT 'E2' AS sort,refno,'1' AS sequence,'Surcharge Tax Amount' AS code_grn,0 AS value_grn,
    ROUND(surchg_tax_sum,2) AS value_calculated FROM backend.pomain
    WHERE refno=%s /*AND discount2<>0*/

    UNION ALL

    SELECT 'F' AS sort,refno,'1' AS sequence,'Total Amount Include Tax' AS code_grn,0 AS value_grn,
    ROUND(total+gst_tax_sum+surchg_tax_sum,2) AS value_calculated FROM backend.pomain
    WHERE refno=%s

    ORDER BY sort,sequence

    LIMIT 18446744073709551615) a

    INNER JOIN

    (SELECT refno,SUM(gst_zero) AS gst_zero,SUM(gst_std) AS gst_std FROM 

    (SELECT a.refno,ROUND(SUM(totalprice-(discvalue+surchgvalue)),2) AS gst_zero,0 AS gst_std FROM backend.pochild a
    INNER JOIN backend.pomain b
    ON a.refno=b.refno
    WHERE gst_tax_amount=0 AND a.refno=%s
    GROUP BY refno

    UNION ALL

    SELECT a.refno,0 AS gst_zero,ROUND(SUM(totalprice-(discvalue+surchgvalue)),2) AS gst_std FROM backend.pochild a
    INNER JOIN backend.pomain b
    ON a.refno=b.refno
    WHERE gst_tax_amount<>0 AND a.refno=%s
    GROUP BY refno) a

    GROUP BY refno) b

    ON a.refno=b.refno
    """

    result4 = panda.raw_query(querystr, [search_refno, search_refno, search_refno,
                              search_refno, search_refno, search_refno, search_refno, search_refno, search_refno])
    result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)

# report GRN


@api_view(['GET'])
def report_GrManagementCopy(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT a.refno,location,grdate,CONCAT(invno,' / ',dono) AS inv_do,
    invno AS invno,
    dono AS dono,
    loc_group AS outlet,
    a.CODE,a.NAME,a.term,
    cross_ref,
    CONCAT(DATE_FORMAT(duedate,'%%Y-%%m-%%d'),' (',a.term,')') AS duedate,
    total,receivedby,subtotal1,subtotal2-IF(pay_by_invoice=0,0,(rebate_amt+dn_amt)) AS subtotal2,
    discount1,discount2,CONCAT(a.refno,' - ',IF(billstatus=0,'UNPOST','POSTED')) AS refno1,
    IF(pay_by_invoice=1,discount1,0) AS inv_discount1,
    IF(pay_by_invoice=1,discount2,0) AS inv_discount2,
    IF(pay_by_invoice=1,invamount_vendor,0) AS invamount_vendor,a.remark,
    CONCAT(a.CODE,' ',a.NAME) AS supplier,docdate,IF(discount1type=1,'%%','$') AS discount1type,
    IF(discount2type=1,'%%','$') AS discount2type,
    invamount_vendor-IF(discount1type=1,ROUND(invamount_vendor*discount1/100,2),discount1)
    AS invamount_vendor_sub1,discount1*-1 AS grn_adj,
    IF(pay_by_invoice=1,invsurchargedisc_vendor*-1,0) AS inv_adj,
    IF(pay_by_invoice=1,invamount_vendor-invsurchargedisc_vendor,0) AS invamount_vendor_sub2,
    IF(pay_by_invoice=1,'','Vendor accepts Pay by GRN Method.  Invoice details are being omitted intentionally.') AS title_pay,
    IF(pay_by_invoice=1,'Inv Net','') AS title_pay1,IF(varianceamt IS NULL,0,varianceamt) AS varianceamt,
    IF(pay_by_invoice=1,0,IF(rebate_var IS NULL,0,rebate_var)) AS rebate_var,
    issuestamp,
    IF(billstatus=1,'','Document Not Posted') AS post_status,
    IF(billstatus=1,DATE_FORMAT(postdatetime,'Posted %%Y-%%m-%%d %%h:%%i:%%s'),'') AS postdatetime,

    ROUND(total+ROUND(gst_tax_sum+surchg_tax_sum+gst_adj,2)+IF(inv_gst IS NULL,0,inv_gst)
    -IF(rebate_dn_gst IS NULL,0,rebate_dn_gst)+IF(rounding_adj IS NULL,0,rounding_adj),2) AS total_aft_gst,

    IF(pay_by_invoice=1,ROUND(invnetamt_vendor+ROUND(gst_tax_sum_inv+surchg_tax_sum_inv+gst_adj+
    IF(inv_gst IS NULL,0,inv_gst)+IF(rounding_adj IS NULL,0,rounding_adj),2),2),0) AS total_inv_aft_gst,

    IF(gst_dncn IS NULL,0,gst_dncn) AS gst_dncn,
    IF(gst_dncn IS NULL OR gst_dncn=0,'','GST for DN') AS title_gst_dncn,
    ROUND(IF(pay_by_invoice=1,gst_tax_sum_inv+surchg_tax_sum_inv+gst_adj,gst_tax_sum+surchg_tax_sum+gst_adj)+IF(gst_inv IS NULL,0,gst_inv)-IF(gst_dncn IS NULL,0,gst_dncn),2) AS gst_net,
    ROUND(surchg_tax_sum,2) AS surchg_tax_sum,
    ROUND(surchg_tax_sum_inv,2) AS surchg_tax_sum_inv,
    rounding_dncn,
    input_amt_exc_tax,input_amt_inc_tax,
    input_gst+rounding_adj AS input_gst

    FROM backend.grmain a

    LEFT JOIN 
    (SELECT refno,
    SUM(IF(transtype IN ('ghv','grv','gdv','gds'),varianceamt+rounding_adj,0)) AS varianceamt,
    SUM(IF(transtype IN ('grv','gdv','gds'),varianceamt+rounding_adj,0)) AS rebate_var,
    ROUND(SUM(IF(transtype IN ('ivs','ivn'),0,gst_tax_sum+gst_adjust)),2) AS gst_dncn,
    ROUND(SUM(IF(transtype IN ('ghv','grv','gdv','gds'),(varianceamt+rounding_adj+ROUND(gst_tax_sum,2)+gst_adjust),0)),2) AS rebate_dn_gst,
    ROUND(SUM(IF(transtype IN ('ivs','ivn'),(varianceamt+ROUND(gst_tax_sum,2)),0)),2) AS inv_gst,
    ROUND(SUM(IF(transtype IN ('ivs','ivn'),gst_tax_sum+rounding_adj,0)),2) AS gst_inv,
    ROUND(SUM(IF(transtype IN ('GQV','IAV'),rounding_adj,0)),2) AS rounding_dncn
    FROM backend.grmain_dncn WHERE refno=%s

    GROUP BY refno
    ) b
    ON a.refno=b.refno

    WHERE a.refno=%s


    """

    result = panda.raw_query(querystr, [search_refno, search_refno])
    result = {"query1": result}

    querystr = """
    SELECT grp,a.itemcode,pricetype,description,itemremark,qty,netunitprice,totalprice,porefno,um,bulkqty,gractcost,
    #IF(a.qty=0,0,IF(cost_manual=0 AND ROUND(a.netunitprice,4)=ROUND(gractcost,4),0,ROUND(gractcost,4))) AS gractcost1,
    IF(a.qty=0,0,IF(cost_manual=0 AND ABS(ROUND(a.netunitprice,4)-ROUND(gractcost,4))<=0.0001,0,ROUND(gractcost,4))) AS gractcost1,
    grtotcost,poactcost,diff,diff_total,line,
    IF(pricetype='RTV','',barcode) AS barcode,
    packsize,bqty,umbulk,groupno,
    poprice,poqty,pototalprice,qtyvar,costvar,costqty,porefno AS refno_po,
    IF(qty=0,0,sellingprice) AS sellingprice,sysqoh,sysavgcost*packsize AS sysavgcost,IF(poqty_expected=a.qty OR (vartotal=0 AND pricetype<>'foc'),0,poqty_expected) AS poqty_expected,
    IF(vartotal=0 AND pricetype<>'foc',0,qtyvar) AS qtyvar1,IF(vartotal=0,0,costvar) AS costvar1,IF(vartotal=0,0,costqty) AS costqty1,
    IF(vartotal=0,0,ROUND(variance_qty/qtyvar,4)) AS poactcost1,
    weightavgcost*packsize AS weightavgcost,retailext,IF(grn_method=0 AND pricetype<>'FOC',0,vartotal) AS vartotal_1,vartotal,tolerance,poweighttrace,grnweighttrace,
    grnweighttraceuom,price_future,pricechange,future_margin,future_retail,
    IF(grn_method=0,'',IF(pricetype IN ('foc','vfoc') AND inv_qty<>0 AND inv_netunitprice=0,'foc','')) AS pricetype_inv,
    IF(pricetype IN ('foc','vfoc') AND a.qty<>0 AND netunitprice=0,'foc','') AS pricetype_grn,
    IF(pricetype IN ('foc','vfoc') AND ROUND(poactcost,4)<>ROUND(gractcost,4),ROUND(poactcost,4),'') AS pricetype_po,
    IF(pricetype IN ('foc','vfoc') AND ROUND(poactcost,4)<ROUND(gractcost,4),'.','') AS chk_pricetype_po,
    IF(pricetype IN ('foc','vfoc') AND (poqty<>inv_qty OR poqty<>qty OR ROUND(poactcost,4)<>ROUND(gractcost,4)),'foc','') AS pricetype_po1,
    IF(grn_method=1,invitemtotal,0) AS invitemtotal,IF(grn_method=1=1,inv_qty,0) AS inv_qty,
    IF(grn_method=1,inv_netunitprice,0) AS inv_netunitprice,IF(grn_method=1=1,actcost_vendor,0) AS actcost_vendor,
    IF(grn_method=1,ROUND(invactcostvendor,4)-ROUND(actcost_po,4),ROUND(gractcost,4)-ROUND(actcost_po,4)) AS actcost_diff,
    inv_variance,invitemvar,qohafter,IF(qty=0,0,actcost_po) AS actcost_po,qohchk,grn_method,articleno,
    stockday_min_qty,stockday_first_grn_date AS datestart,stockday_max_qty,IF(soldqty>100,ROUND(soldqty),ROUND(soldqty,1)) AS soldqty,
    IF(openingqty>100,ROUND(openingqty),ROUND(openingqty,1)) AS openingqty,stockday_onhandqty,
    stockday_possalesqty,stockday_invsalesqty,stockday_soqty,stockday_poqty,IF(grqty>100,ROUND(grqty),ROUND(grqty,1)) AS grqty,stockday_interval_days,
    IF(other>100,ROUND(other),ROUND(other,1)) AS other,
    IF(openingqty-soldqty+grqty+other>100,ROUND(openingqty-soldqty+grqty+other),ROUND(openingqty-soldqty+grqty+other,1)) AS balanceqty,IF(ams<100,ROUND(ams,1),ROUND(ams)) AS ams,
    IF((openingqty-soldqty+grqty+other+qty_po+stockday_poqty)/ROUND(ams,1)*30 IS NULL,0,(openingqty-soldqty+grqty+other+qty_po+stockday_poqty)/ROUND(ams,1)*30) AS doh,
    IF(grp=1,ROUND(poprice,4),IF(grn_method=0,IF(poqty<>qty OR ROUND(poprice,4)<>ROUND(netunitprice,4) OR ROUND(poactcost,4)<>ROUND(gractcost,4),poprice,0),
    IF(poqty<>inv_qty OR qty<>inv_qty OR ROUND(poprice,4)<>ROUND(inv_netunitprice,4) OR ROUND(inv_netunitprice,4)<>ROUND(netunitprice,4)
    OR ROUND(poactcost,4)<>ROUND(gractcost,4),poprice,0))) AS poprice1,
    IF(grp=1,poqty,IF(grn_method=0,IF(poqty<>qty OR ROUND(poprice,4)<>ROUND(netunitprice,4) OR ROUND(poactcost,4)<>ROUND(gractcost,4),poqty,0),
    IF(poqty<>inv_qty OR qty<>inv_qty OR ROUND(poprice,4)<>ROUND(inv_netunitprice,4) OR ROUND(inv_netunitprice,4)<>ROUND(netunitprice,4)
    OR ROUND(poactcost,4)<>ROUND(gractcost,4),poqty,0))) AS poqty1,
    IF(grp=1,ROUND(pototalprice,2),IF(grn_method=0,IF(poqty<>qty OR ROUND(poprice,4)<>ROUND(netunitprice,4),pototalprice,0),
    IF(poqty<>inv_qty OR qty<>inv_qty OR ROUND(poprice,4)<>ROUND(inv_netunitprice,4) OR ROUND(inv_netunitprice,4)<>ROUND(netunitprice,4),pototalprice,0))) AS pototalprice1,
    IF(a.qty=0,'',ROUND(sellingprice,2)) AS sellingprice1,IF(a.qty=0,'',CONCAT(ROUND((ROUND(sellingprice,2)-gractcost)/ROUND(sellingprice,2)*100,1),'%%')) AS margin,
    IF(a.qty=0,'',ROUND(ROUND(sellingprice,2)*a.qty,2)) AS retailext1,IF(a.qty=0,'',ROUND(sysqoh/packsize,1)) AS sysqoh1,
    IF(a.qty=0,'',ROUND(sysavgcost*packsize,4)) AS sysavgcost1,IF(a.qty=0,'',ROUND(ROUND(sysqoh/packsize,1)+a.linkqty_rec,1)) AS qohafter1,
    IF(a.qty=0,'',IF(cost_manual=0,ROUND(weightavgcost*packsize,4),ROUND(((sysavgcost*sysqoh)+(cost_manual_value*linkqty_rec))/((linkqty_rec*packsize)+sysqoh)*packsize,4))) AS weightavgcost1,
    qty_po+stockday_poqty AS poqty_total,

    IF(qty=0,'',CONCAT(gst_tax_type,ROUND(price_posnet,2),
    IF(ROUND(price_future1,2)=ROUND(a.price_posnet,2),'',CONCAT(' F$',ROUND(price_future1,2),' (',
    ROUND(((price_future1*100/(100+gst_tax_rate))-gractcost)/(price_future1*100/(100+gst_tax_rate))*100,1),'%%) ')),
    IF(margin BETWEEN cat_min AND cat_max,'',CONCAT(' GP ',IF(RIGHT(cat_min,2)='00',ROUND(cat_min),cat_min),'%%-',
    IF(RIGHT(cat_max,2)='00',ROUND(cat_max),cat_max),'%%')),
    IF(promo IS NULL,'',CONCAT(' ',promo,' (',ROUND((b.price_include_tax-(gractcost-bare_supplier))/b.price_include_tax*100,1),'%%) ')))) AS pricechange1,


    /*IF(a.qty=0,'',CONCAT(IF(promo IS NULL,'',CONCAT(promo,' (',ROUND((price_net-(gractcost-bare_supplier))/price_net*100,1),'%% ')),IF(pricechange1 IS NULL,'',pricechange1),
    IF(ROUND(sellingprice,2) BETWEEN price_min AND price_max AND ROUND(price_future1,2) BETWEEN price_min AND price_max,'',
    CONCAT(' GP ',cat_min,'%%-',cat_max,'%%'))))) AS pricechange1,*/

    locgroup,promo,
    IF(vartotal<>0 OR price_future1<>sellingprice OR qty<>poqty OR netunitprice<>poprice OR poprice<>inv_netunitprice 
    OR (weightavgcost-sysavgcost)/sysavgcost*100>20 OR (weightavgcost-sysavgcost)/sysavgcost*100<-20 OR (ROUND(sellingprice,2) NOT BETWEEN price_min AND price_max)
    OR (ROUND(price_net,2) NOT BETWEEN price_min AND price_max),'X','') AS chk,
    IF(pricetype IN ('RTV','VFOC'),'',IF(grn_method=0,IF(qty<>poqty,'.',''),IF(poqty<>inv_qty OR qty<>inv_qty,'.',''))) AS chk_poqty,

    IF(pricetype IN ('RTV','VFOC'),'',IF(grn_method=0,IF(((ROUND(poprice,4)<>ROUND(netunitprice,4)) OR ((pricetype IN ('foc','vfoc') AND ROUND(poactcost,4)<ROUND(gractcost,4))) AND (qty<>0 OR vartotal)<>0),'.',''),
    IF((ROUND(poprice,4)<>ROUND(inv_netunitprice,4) OR ROUND(netunitprice,4)<>ROUND(inv_netunitprice,4) OR ((pricetype IN ('foc','vfoc') AND ROUND(poactcost,4)<ROUND(gractcost,4)))) 
    AND (qty<>0 OR vartotal<>0),'.',''))) AS chk_poprice,

    IF(vartotal<>0,'.','') AS chk_var,
    IF(a.qty=0,'',IF(sellingprice<IF(inv_qty=0 AND a.qty=0,0,gractcost) OR ROUND(sellingprice,2) NOT BETWEEN price_min AND price_max,'.','')) AS chk_margin,group_code,
    IF(a.qty=0 OR ROUND(weightavgcost,4)=ROUND(sysavgcost,4),'',IF((weightavgcost-sysavgcost)/sysavgcost*100>20 OR (weightavgcost-sysavgcost)/sysavgcost*100<-20,'.','')) AS chk_system,
    price_min,price_max,mrank,hqcost_desc,IF(cost_dist='',IF(rebate_value='','',rebate_value),cost_dist) AS cost_dist,
    IF(rebate_value='','',IF(cost_dist='','',rebate_value)) AS rebate_value,
    IF(cost_dist_title='',IF(rebate_value='','','Rebate Amount for Distribution ->'),IF(rebate_value='',cost_dist_title,'PO Cost & Rebate Amt for Distribution ->')) AS cost_dist_title,
    IF(qty=0 AND inv_qty=0,'Item Not In Invoice',IF(inv_qty<>0 AND qty=0,'Item In Inv But Not Received','')) AS grn_remark,
    IF(rebate_var IS NULL,'',rebate_var) AS rebate_var,IF(po_rebate IS NULL,'',po_rebate) AS po_rebate,IF(rebate_var IS NULL,'','Warning ->') AS rebate_warning,
    gst_code,docdate,
    IF(pricetype='norm','1','2') AS pricetype_sort,
    expiry_date,poline

    FROM

    (SELECT IF(f.groupno IS NULL,0,1) AS grp,a.itemcode,a.pricetype,a.description,a.itemremark,a.qty,IF(qty=0,0,netunitprice) AS netunitprice,a.totalprice,
    IF(pricetype='RTV','Item Not in PO',IF(pricetype='VFOC','FOC Not in PO',a.porefno)) AS porefno,
    IF(a.qty=0,'',a.um) AS um,a.bulkqty,
    IF(cost_manual=0,ROUND(a.invactcost /* removed on 180506 due to VG vkggr18040552 a.billitemavgcost*/,4),ROUND(cost_manual_value,4)) AS gractcost,

    ROUND(a.invactcost*a.qty,2) AS grtotcost,
    IF(poqty_expected>a.qty,IF(poactcost<IF(invactcostvendor IS NULL,0,invactcostvendor),poactcost,IF(invactcostvendor IS NULL,poactcost,invactcostvendor)),0) AS poactcost_1,
    ROUND(a.invactcost,4)-ROUND(poactcost,4) AS diff,(ROUND(a.invactcost,4)-ROUND(poactcost,4))*a.qty AS diff_total,poqty_expected,invactcostvendor,
    a.line,a.barcode,a.packsize,IF(a.bqty=a.qty,0,a.bqty) AS bqty,IF(a.bqty=a.qty OR a.bqty=0,'',a.umbulk) AS umbulk,
    IF(pricetype='RTV',9999,a.groupno) AS groupno,
    pounitprice AS poprice,poqty,pototalprice,
    IF(poqty_expected>a.qty,IF(MOD(poqty_expected-a.qty,1)=0,poqty_expected-a.qty,ROUND(poqty_expected-a.qty,2)),0) AS qtyvar,
    IF(inv_netunitprice<pounitprice,0,inv_netunitprice-pounitprice) AS costvar_1,IF(inv_netunitprice>pounitprice,inv_qty,0) AS costqty_1,
    IF(variance_cost<>0,inv_qty,0) AS costqty,IF(variance_cost<>0,ROUND(variance_cost/inv_qty,4),0) AS costvar,
    IF(variance_qty<>0,ROUND(variance_qty/IF(poqty_expected>a.qty,IF(MOD(poqty_expected-a.qty,1)=0,poqty_expected-a.qty,ROUND(poqty_expected-a.qty,2)),0),4),0) AS poactcost_2,
    poactcost,a.sellingprice,a.sysqoh,a.sysavgcost,a.weightavgcost,a.sellingprice*a.qty AS retailext,
    IF(a.entrytype='amt',ROUND(inv_totalprice-a.totalprice,2),ROUND(((IF(poqty_expected-a.qty>0,poqty_expected-a.qty,0))*IF(poactcost<IF(invactcostvendor IS NULL,0,invactcostvendor),
    poactcost,IF(invactcostvendor IS NULL,poactcost,invactcostvendor)))+((IF(inv_netunitprice-pounitprice>0,inv_netunitprice-pounitprice,0))*inv_qty),2)) AS vartotal_1,
    variance_qty+variance_cost AS vartotal,variance_qty,variance_cost,
    IF(a.purtolerance_std_plus-a.purtolerance_std_minus=0,'',a.purtolerance_std_plus-a.purtolerance_std_minus) AS tolerance,
    IF(a.weighttraceqty=0,'',CONCAT(a.weighttraceqty,' ',a.weighttraceqtyuom)) AS poweighttrace,
    IF(a.weighttraceqtycount=0,'',a.weighttraceqtycount) AS grnweighttrace,a.weighttraceqtyuom AS grnweighttraceuom,
    inv_totalprice AS invitemtotal,IF(a.price_future=a.sellingprice,'',ROUND(a.price_future,2)) AS price_future,price_future AS price_future1,
    IF(a.price_future=a.sellingprice,'','Raise Price Change ->') AS pricechange,
    IF(a.price_future=a.sellingprice,'',ROUND((a.price_future-a.invactcost)/a.price_future*100,1)) AS future_margin,
    IF(a.price_future=a.sellingprice,'',ROUND(a.price_future*a.qty,2)) AS future_retail,
    inv_qty,IF(inv_qty=0,0,inv_netunitprice) AS inv_netunitprice,inv_variance,(a.netunitprice*a.qty)-(inv_qty*inv_netunitprice) AS invitemvar,
    a.qty+a.sysqoh AS qohafter,poactcost AS actcost_po,invactcostvendor AS actcost_vendor,
    IF(a.sellingprice<a.invactcost,'-','') AS pricechk,IF(a.sysqoh<0,'-','') AS qohchk,
    pay_by_invoice AS grn_method,
    a.articleno,stockday_min_qty,stockday_first_grn_date,stockday_max_qty,soldqty,openingqty,
    stockday_onhandqty,stockday_possalesqty,stockday_invsalesqty,stockday_soqty,stockday_poqty,grqty,stockday_interval_days,
    other,ams,qty_po,loc_group AS locgroup,

    IF(ROUND(a.price_future,2)=ROUND(a.sellingprice,2),'',CONCAT(' $ Chg ',ROUND(price_future,2),'=',
    ROUND((price_future-IF(cost_manual=0,ROUND(a.invactcost /* removed on 180506 due to VG vkggr18040552 a.billitemavgcost*/,4),
    ROUND(cost_manual_value,4)))/price_future*100,1),'%% ')) AS pricechange1,

    cat_min,cat_max,
    ROUND((sellingprice-IF(cost_manual=0,invactcost,cost_manual_value))/sellingprice*100,1) AS margin,

    ROUND(IF(cost_manual=0,ROUND(a.invactcost /* removed on 180506 due to VG vkggr18040552 a.billitemavgcost*/,4),ROUND(cost_manual_value,4))/((100-cat_min)/100),2) AS price_min,
    ROUND(IF(cost_manual=0,ROUND(a.invactcost /* removed on 180506 due to VG vkggr18040552 a.billitemavgcost*/,4),ROUND(cost_manual_value,4))/((100-cat_max)/100),2) AS price_max,mrank,group_code,linkqty_rec/a.packsize AS linkqty_rec,
    IF(cost_manual=0,'',IF(qty<>0,'HQ ->','')) AS hqcost_desc,cost_manual,cost_manual_value,


    /* amend cost_dist on 2020-10-19 to display invactcost due to to doremon case SRPGR20090084 where 
    1. group 1 buy item 114499 400 free item 114499 20 (groupcost=1) 
    2. group 2 buy item 114500 200 free item 114499 20 (groupcost=0) 
    system use the grn cost instead of itemmaster avgcost to update the foc item where groupcost=0 */

    IF(pricetype IN ('foc','vfoc') AND groupcost=0 AND 
    (qty<>0 OR variance_qty<>0) AND a.groupno<>0,
    IF(invactcost=0,IF(poactcost=0,ROUND(sysavgcost,4),ROUND(poactcost,4)),ROUND(invactcost,4)),'') AS cost_dist,

    IF(pricetype IN ('foc','vfoc') AND groupcost=0 AND (qty<>0 OR variance_qty<>0) AND a.groupno<>0,IF(poactcost=0,'System Avg Cost for Distribution ->','System Avg Cost for Distribution ->'),'') AS cost_dist_title,
    IF(rebate_value=0,'',ROUND(rebate_value,2)) AS rebate_value,rebate_var,CONCAT('PO Item Rebate Amt: ',po_rebate) AS po_rebate,
    LEFT(gst_tax_code,2) AS gst_code,price_posnet,docdate,
    CAST(CONCAT(LEFT(gst_tax_type,1),'$') AS CHAR) AS gst_tax_type,
    IF(expiry_date IS NULL OR expiry_date<=grdate,'',CONCAT('Exp ',DATE_FORMAT(expiry_date,'%%Y.%%m.%%d'))) AS expiry_date,
    poline,a.gst_tax_rate
    FROM backend.grchild a

    INNER JOIN backend.grmain d
    ON a.refno=d.refno

    LEFT JOIN
    (SELECT b.refno,itemlink,SUM(qty*packsize) AS linkqty_rec 
    FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE b.refno=%s
    GROUP BY b.refno,itemlink) c
    ON a.refno=c.refno AND a.itemlink=c.itemlink

    LEFT JOIN
    (SELECT a.itemcode,a.refno,SUM(a.qty) AS qty_po,stockday_min_qty,stockday_first_grn_date,stockday_max_qty,stockday_pos_qty_sum AS soldqty,
    stockday_openingqty AS openingqty,stockday_onhandqty,stockday_possalesqty,stockday_invsalesqty,stockday_soqty,stockday_poqty,
    stockday_recqty AS grqty,stockday_interval_days,stockday_adjustqty+stockday_hamperqty+stockday_creditqty+stockday_debitqty AS other,
    stockday_pos_qty_sum/stockday_interval_days*30 AS ams,mrank
    FROM backend.pochild a
    INNER JOIN backend.grchild b
    ON a.refno=b.porefno AND a.itemcode=b.itemcode AND a.line=b.poline
    WHERE b.refno=%s
    GROUP BY a.refno,itemcode) b
    ON a.porefno=b.refno AND a.itemcode=b.itemcode

    LEFT JOIN 
    backend.set_group_dept e
    ON a.dept=e.dept_code

    LEFT JOIN
    (SELECT b.refno,groupno FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE b.refno=%s AND pricetype IN ('foc','vfoc') AND poqty_expected<>qty
    GROUP BY b.refno,groupno) f
    ON a.groupno=f.groupno

    LEFT JOIN
    (SELECT b.refno,b.groupno,b.line,b.itemcode,a.rebate_value AS po_rebate,b.rebate_value AS gr_rebate,
    CONCAT('Item Rebate Var: ',a.rebate_value-b.rebate_value) AS rebate_var
    FROM backend.pochild a

    INNER JOIN 
    (SELECT b.refno,porefno,itemcode,poline,groupno,line,
    rebate_value 
    FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE b.refno=%s AND rebate_value<>0) b
    ON a.refno=b.porefno AND a.itemcode=b.itemcode AND a.line=b.poline

    WHERE a.groupno=0 AND a.rebate_value<>0
    GROUP BY b.refno,b.line

    UNION ALL

    SELECT a.refno,b.groupno,b.line,b.itemcode,a.rebate_value AS po_rebate,b.rebate_value AS gr_rebate,rebate_var
    FROM backend.pochild a
    INNER JOIN backend.grchild b
    ON a.refno=b.porefno AND a.itemcode=b.itemcode AND a.line=b.poline

    INNER JOIN 
    (SELECT b.refno,b.groupno,b.line,SUM(a.rebate_value) AS po_rebate,SUM(b.rebate_value) AS gr_rebate,
    CONCAT('Group Rebate Var: ',ROUND(SUM(a.rebate_value)-SUM(b.rebate_value),2)) rebate_var
    FROM backend.pochild a
    INNER JOIN backend.grchild b
    ON a.refno=b.porefno AND a.itemcode=b.itemcode AND a.line=b.poline
    WHERE b.refno=%s AND a.groupno<>0
    GROUP BY b.refno,groupno
    HAVING po_rebate>gr_rebate) c
    ON b.refno=c.refno AND b.groupno=c.groupno
    WHERE a.rebate_value<>0 OR b.rebate_value<>0) g
    ON a.line=g.line 

    WHERE a.refno=%s 
    /* remove on 18-05-06 AND ROUND(subtotal1,2)=(SELECT ROUND(SUM(totalprice)+0.000001,2) FROM backend.grchild WHERE refno=%s)*/) a

    LEFT JOIN
    (SELECT loc_group,itemcode,price_net,bare_supplier,
    CONCAT(DATE_FORMAT(datefrom,'%%d/%%m'),' - ',DATE_FORMAT(dateto,'%%d/%%m'),' P$',ROUND(price_net,2),
    IF(bare_supplier+bare_supplier_2=0,'',CONCAT(' + claim $',ROUND(bare_supplier,2)))) AS promo,
    price_include_tax
    /*CONCAT(DATE_FORMAT(datefrom,'%%d/%%m'),'-',DATE_FORMAT(dateto,'%%d/%%m'),' $',price_net,
    IF(bare_supplier=0,'',CONCAT(' + Claim $',ROUND(bare_supplier,2)))) AS promo*/ FROM

    (SELECT b.refno,b.loc_group,location,datefrom,dateto,c.itemcode,c.cardtype,price_net,bare_supplier_2,

    IF(supplier_claim=0,0,IF(bare_supplier_type='$',bare_supplier+bare_supplier_2,
    IF(LEFT(bare_supplier_type,6)='%% Cost',
    ROUND((IF(cost_manual=0,invactcost,cost_manual_value)*bare_supplier/100)+
    ((IF(cost_manual=0,invactcost,cost_manual_value)-(IF(cost_manual=0,invactcost,cost_manual_value)*bare_supplier/100))*bare_supplier_2/100),2),
    IF(LEFT(bare_supplier_type,6)='%% Pric',
    ROUND((IF(promo_by_tragetprice=1,price_target,sellingprice)*bare_supplier/100)+
    ((IF(promo_by_tragetprice=1,price_target,sellingprice)-(IF(promo_by_tragetprice=1,price_target,sellingprice)*bare_supplier/100))*bare_supplier_2/100),2),
    ROUND(((IF(promo_by_tragetprice=1,price_target-price_net,IF(c.disc1type='$',c.disc1value,
    ROUND(sellingprice*c.disc1value/100,2))+
    IF(c.disc2type='$',c.disc2value,ROUND((sellingprice-ROUND(sellingprice*c.disc1value/100,2))*c.disc2value/100,2))))*bare_supplier/100)+
    (((IF(promo_by_tragetprice=1,price_target-price_net,IF(c.disc1type='$',c.disc1value,
    ROUND(sellingprice*c.disc1value/100,2))+
    IF(c.disc2type='$',c.disc2value,ROUND((sellingprice-ROUND(sellingprice*c.disc1value/100,2))*c.disc2value/100,2))))-
    ((IF(promo_by_tragetprice=1,price_target-price_net,IF(c.disc1type='$',c.disc1value,
    ROUND(sellingprice*c.disc1value/100,2))+
    IF(c.disc2type='$',c.disc2value,ROUND((sellingprice-ROUND(sellingprice*c.disc1value/100,2))*c.disc2value/100,2))))*bare_supplier/100))*bare_supplier_2/100),2))))) AS bare_supplier,
    c.price_include_tax

    FROM backend.promo_supplier_c c

    INNER JOIN
    (SELECT b.refno,itemcode,loc_group,grdate,location,
    cost_manual,invactcost,cost_manual_value,sellingprice 
    FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE b.refno=%s
    GROUP BY b.refno,itemcode) b
    ON c.itemcode=b.itemcode

    INNER JOIN backend.promo_supplier d
    ON c.pvc_guid=d.pvc_guid 

    INNER JOIN backend.promo_supplier_loc e
    ON d.pvc_guid=e.pvc_guid AND b.loc_group=e.loc_group

    WHERE b.refno=%s AND cancelpromo=0 AND d.posted=1 
    AND (grdate BETWEEN datefrom AND dateto) AND trans_type IN ('pgl','psc')
    AND c.cardtype='NA' 
    ORDER BY itemcode,posted_at DESC

    LIMIT 18446744073709551615) a
    GROUP BY refno,itemcode,loc_group) b
    ON a.locgroup=b.loc_group AND a.itemcode=b.itemcode

    ORDER BY groupno,pricetype_sort,description






    """
    result2 = panda.raw_query(querystr, [search_refno, search_refno, search_refno,
                              search_refno, search_refno, search_refno, search_refno, search_refno, search_refno])
    result["query2"] = result2

    querystr = """
    SELECT a.*,
    IF(b.pay_by_invoice=1,'GRN Total','GRN Payable') AS title_grn,
    IF(b.pay_by_invoice=1,'Inv Payable','') AS title_inv 

    FROM backend.grmain b
    LEFT JOIN 
    (SELECT refno,sequence,SUM(value_grn) AS value_grn,SUM(value_inv) AS value_inv,
    GROUP_CONCAT(code_inv SEPARATOR '') AS code_inv,
    GROUP_CONCAT(code_grn SEPARATOR '') AS code_grn,pay_by_invoice,sort FROM

    (SELECT a.refno,sequence,CONCAT(IF(build_into_cost=1,'S-','NS-'),IF(dn=0,'','DN'),a.CODE,' (',surcharge_disc_type,')') AS code_grn,surcharge_disc_value*value_factor AS value_grn,
    '' AS code_inv,0 AS value_inv,pay_by_invoice,
    IF(value_factor=-1,'A1','C1') AS sort
    FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE a.refno=%s AND trans_type='grn' AND dn=0



    UNION ALL

    SELECT a.refno,sequence,'' AS code_grn,0 AS factor_grn,CONCAT(IF(build_into_cost=1,'S-','NS-'),a.CODE,' (',surcharge_disc_type,')') AS code_inv,
    surcharge_disc_value*value_factor AS value_inv,pay_by_invoice,
    IF(value_factor=-1,'A1','C1') AS sort
    FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE a.refno=%s AND trans_type='grninv' AND pay_by_invoice=1 AND dn=0

    UNION ALL

    SELECT a.refno,'999A' AS sequence,IF(share_cost=1,'S-DN','NS-DN') AS code_grn,
    ROUND((varianceamt+a.rounding_adj+ROUND(a.gst_tax_sum+gst_adjust,2)),2)*-1 AS value_grn,'' AS code_inv,0 AS value_inv,
    pay_by_invoice,'G1' AS sort FROM backend.grmain_dncn a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE a.refno=%s AND transtype IN ('GDS','GDV')

    UNION ALL

    SELECT a.refno,CONCAT('999B',sequence) AS sequence,
    c.code AS code_grn,
    #IF(share_cost=1,'S-IV','NS-IV') AS code_grn,
    ROUND((varianceamt+ROUND(a.gst_tax_sum,2)),2) AS value_grn,
    c.code AS code_inv,
    #IF(share_cost=1,'S-IV','NS-IV') AS code_inv,
    ROUND((varianceamt+ROUND(a.gst_tax_sum,2)),2) AS value_inv,
    pay_by_invoice,'G1' AS sort FROM backend.grmain_dncn a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno

    INNER JOIN backend.trans_surcharge_discount c
    ON b.refno=c.refno AND a.trans_seq=c.sequence
    WHERE a.refno=%s AND transtype IN ('IVS','IVN')
    AND c.trans_type='GRN'




    UNION ALL

    SELECT refno,'1' AS sequence,'Total After Disc' AS code_grn,total-discount2 AS value_grn,
    IF(pay_by_invoice=1,'Total After Disc','') AS code_inv,
    IF(pay_by_invoice=0,0,invnetamt_vendor-invsurcharge) AS value_inv,
    pay_by_invoice,'B1' AS sort FROM backend.grmain
    WHERE refno=%s AND discount1<>0

    UNION ALL

    SELECT refno,'1' AS sequence,'GRN GST Amt' AS code_grn,ROUND(gst_tax_sum+surchg_tax_sum,2) AS value_grn,
    IF(pay_by_invoice=0,'','Inv GST Amt') AS code_inv,
    IF(pay_by_invoice=0,0,ROUND(gst_tax_sum_inv+surchg_tax_sum_inv,2)) AS value_inv,
    pay_by_invoice,'D1' AS sort FROM backend.grmain
    WHERE refno=%s
    AND grdate BETWEEN (SELECT gst_start_date FROM backend.companyprofile) AND 
    (SELECT gst_end_date FROM backend.companyprofile)

    UNION ALL

    SELECT refno,'1' AS sequence,'GRN Rounding' AS code_grn,
    ROUND(rounding_adj,2) AS value_grn,
    'Inv Rounding' AS code_inv,
    ROUND(rounding_adj,2) AS value_inv,
    pay_by_invoice,'G1' AS sort FROM backend.grmain
    WHERE refno=%s AND pay_by_invoice=1 AND rounding_adj<>0

    UNION ALL

    SELECT refno,'1' AS sequence,'GRN GST Adj' AS code_grn,ROUND(gst_adj,2) AS value_grn,
    'Inv GST Adj' AS code_inv,
    ROUND(gst_adj,2) AS value_inv,
    pay_by_invoice,'D2' AS sort FROM backend.grmain
    WHERE refno=%s AND gst_adj<>0



    UNION ALL

    SELECT refno,'1' AS sequence,'S-Rebate DN' AS code_grn,
    ROUND(SUM((varianceamt+rounding_adj+ROUND(b.gst_tax_sum+gst_adjust,2))),2)*-1 AS value_grn,
    '' AS code_inv,0 AS value_inv,'1' AS pay_by_invoice,'H1' AS sort
    FROM backend.grmain_dncn b
    WHERE refno=%s AND transtype='GRV' AND varianceamt<>0
    GROUP BY refno) a

    GROUP BY refno,sort,sequence

    ORDER BY sort,sequence) a

    ON b.refno=a.refno

    WHERE b.refno=%s;
    """
    result3 = panda.raw_query(querystr, [search_refno, search_refno, search_refno, search_refno,
                              search_refno, search_refno, search_refno, search_refno, search_refno, search_refno])
    result["query3"] = result3

    querystr = """
    SELECT a.CODE AS location,b.CODE AS locgroup,CONCAT(locgroup,IF(b.description IS NULL,'',CONCAT(' - ',b.description))) AS outlet,
    IF(a.remark IS NULL OR a.remark='',IF((SELECT ashq FROM backend.companyprofile)=0,companyname,IF(c.branch_name IS NULL,'',c.branch_name)),a.remark) AS companyname,
    IF((SELECT ashq FROM backend.companyprofile)=0,CONCAT(address1,' ',address2),IF(c.branch_add IS NULL,'',c.branch_add)) AS address,
    IF((SELECT ashq FROM backend.companyprofile)=0,address1,'') AS address1,
    IF((SELECT ashq FROM backend.companyprofile)=0,address2,'') AS address2,
    IF((SELECT ashq FROM backend.companyprofile)=0,CONCAT('Tel : ',IF(d.tel IS NULL,'',d.tel),'  Fax : ',IF(d.fax IS NULL,'',d.fax)),
    CONCAT('Tel : ',IF(branch_tel IS NULL,'',branch_tel),'  Fax : ',IF(branch_fax IS NULL,'',branch_fax))) AS contact,

    IF(e.ibt=1,'IBT Stock Tranfer Inwards - Mgmt Copy (by Desc)',
    IF(e.ibt=2,'Inter Company Goods Received Note - Mgmt Copy (by Desc)',
    IF(e.consign=1,'Consigned Goods Received Note - Mgmt Copy (by Desc)',IF(in_kind=1,'In-Kind Goods Received Note - Mgmt Copy (by Desc)',
    IF(stock_returnable=0,'Outright Goods Received Note - Mgmt Copy (by Desc)','Outright Goods Received Note - Mgmt Copy (by Desc)'))))) AS title,

    IF(e.ibt=1,'IBT Stock Tranfer Inwards - Mgmt Copy (by Desc)',
    IF(e.ibt=2,'Inter Company Goods Received Note - Mgmt Copy (by Desc)',
    IF(e.consign=1,'Consigned Goods Received Note - Mgmt Copy (by Desc)',IF(in_kind=1,'In-Kind Goods Received Note - Mgmt Copy (by Desc)',
    IF(stock_returnable=0,'Outright Goods Received Note - Mgmt Copy (by Desc)','GRN by Desc'))))) AS title_old,

    grnremark1,grnremark2,grnremark3,in_kind,IF(in_kind=1,'In-Kind GRN - Not Valid for Payment','') AS in_kind_desc,
    grn_amt+IF(pay_by_invoice=1,IF(trans_disc_inv IS NULL,0,trans_disc_inv),IF(trans_disc IS NULL,0,trans_disc)) AS grn_amt,

    trans_disc_inv,

    gst_tax_code,
    gst_tax_amt,

    IF(IF(pay_by_invoice=1,IF(h.surchg_inv IS NULL,0,h.surchg_inv),
    IF(h.surchg IS NULL,0,h.surchg))=0,'',IF(pay_by_invoice=1,IF(h.gst_surchg_inv IS NULL,0,h.gst_surchg_inv),
    IF(h.gst_surchg IS NULL,0,h.gst_surchg))) AS gst_schg_amt,

    IF(pay_by_invoice=1,IF(h.surchg_inv IS NULL,0,h.surchg_inv),
    IF(h.surchg IS NULL,0,h.surchg)) AS schg_amt,


    title_gst_inv,title_gst_amt,title_gst_code,
    title_dn,title_gst_dn,
    title_dn_1,title_gst_dn_1,
    title_schg,title_gst_schg,
    IF(in_kind=1,0,IF(c.dncn_amt IS NULL,0,dncn_amt)+IF(rounding_dncn IS NULL,0,rounding_dncn)) AS dn_amt,
    IF(in_kind=1,0,gst_dn_amt+IF(c.gst_dncn_amt IS NULL,0,gst_dncn_amt)) AS gst_dn_amt,

    IF(IF(in_kind=1,0,IF(c.dncn_amt IS NULL,0,dncn_amt))=0,'',
    IF(in_kind=1,0,IF(c.gst_dncn_amt IS NULL,0,gst_dncn_amt)+
    IF(c.rounding_dncn_gst IS NULL,0,rounding_dncn_gst))) AS gst_dn_amt1



    FROM backend.location a

    INNER JOIN
    (SELECT CODE,location,consign,in_kind,a.refno,pay_by_invoice,
    gst_tax_code,
    grn_amt+IF(diff IS NULL,0,IF(gst_tax_amt=0,diff,0)) AS grn_amt,
    gst_tax_amt,title_gst_inv,title_gst_amt,title_gst_code,title_dn,title_gst_dn,
    title_dn_1,title_gst_dn_1,title_schg,title_gst_schg,dn_amt,gst_dn_amt,ibt FROM

    (SELECT CODE,location,consign,in_kind,a.refno,pay_by_invoice,
    IF(in_kind=1,'',gst_tax_code) AS gst_tax_code,

    IF(in_kind=1,0,
    ROUND(SUM(IF(pay_by_invoice=1,inv_totalprice/*remove on 2020-08-31 -hcost_iv*/,a.totalprice/* remove on 2020-08-31 -hcost_gr*/))+
    IF(ROUND(SUM(IF(pay_by_invoice=1,gst_tax_amt_inv,a.gst_tax_amount))+0.000001,2)=0,0,0.000001),2)) AS grn_amt,

    IF(in_kind=1,0,ROUND(SUM(IF(pay_by_invoice=0,gst_tax_amount,gst_tax_amt_inv))+0.000001,2)) AS gst_tax_amt,
    IF(in_kind=1,'',IF(pay_by_invoice=0,'GRN Amt','Inv Amt')) AS title_gst_inv,
    IF(in_kind=1,'','GST') AS title_gst_amt,
    IF(in_kind=1,'','Code') AS title_gst_code,
    IF(in_kind=1,'',IF(SUM(variance_qty+variance_cost+rebate_value)=0,'','DN Amt')) AS title_dn,
    IF(in_kind=1,'',IF(SUM(variance_qty+variance_cost+rebate_value)=0,'','GST')) AS title_gst_dn,
    IF(in_kind=1,'','DN Amt') AS title_dn_1,
    IF(in_kind=1,'','GST') AS title_gst_dn_1,
    IF(in_kind=1,'','S/CHG') AS title_schg,
    IF(in_kind=1,'','GST') AS title_gst_schg,


    IF(in_kind=1,0,IF(SUM(variance_qty+variance_cost+rebate_value)=0,0,
    ROUND(SUM(variance_qty+variance_cost+rebate_value),2))) AS dn_amt,

    IF(in_kind=1,0,IF(SUM(gst_var_qty+gst_var_cost+gst_rebate_amt)=0,0,
    ROUND(SUM(gst_var_qty+gst_var_cost+gst_rebate_amt)+0.000001,2))) AS gst_dn_amt,
    ibt

    FROM backend.grchild a

    INNER JOIN backend.grmain b
    ON a.refno=b.refno

    WHERE a.refno=%s
    GROUP BY gst_tax_code) a

    LEFT JOIN

    (SELECT refno,ROUND(total-SUM(taxableamt),2) AS diff FROM

    (SELECT a.refno,total,
    ROUND(SUM(IF(pay_by_invoice=1,inv_totalprice-hcost_iv,b.totalprice-hcost_gr))+
    IF(ROUND(SUM(IF(pay_by_invoice=1,gst_tax_amt_inv,b.gst_tax_amount))+0.000001,2)=0,0,0.000001),2) AS TaxableAmt

    FROM backend.grmain a

    INNER JOIN backend.grchild b
    ON a.refno=b.refno

    WHERE 
    IF(pay_by_invoice=1,ROUND(invnetamt_vendor,2),ROUND(a.total,2))>0 AND a.refno=%s

    GROUP BY a.refno,b.gst_tax_rate) a

    GROUP BY refno

    HAVING diff BETWEEN -0.01 AND 0.01) b

    ON a.refno=b.refno ) e
    ON a.CODE=e.location

    LEFT JOIN
    (SELECT a.refno,tax_code_purchase,
    ROUND(SUM(IF(transtype IN ('GDS','GDV','GRV','GQV','IAV'),a.gst_tax_sum,0)),2) AS gst_dncn_amt,
    ROUND(SUM(IF(transtype IN ('GDS','GDV','GRV','GQV','IAV'),varianceamt,0)),2) AS dncn_amt,
    ROUND(SUM(a.rounding_adj),2) AS rounding_dncn,
    ROUND(SUM(a.gst_adjust),2) AS rounding_dncn_gst
    FROM backend.grmain_dncn a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE a.refno=%s 
    GROUP BY tax_code_purchase) c
    ON e.refno=c.refno AND e.gst_tax_code=c.tax_code_purchase

    LEFT JOIN 
    (SELECT a.refno,gst_tax_code AS surchg_tax_code,
    ROUND(SUM(IF(trans_type='grn' AND value_factor>0,gst_amt,0)),2) AS gst_surchg,
    ROUND(SUM(IF(trans_type='grninv' AND value_factor>0,gst_amt,0)),2) AS gst_surchg_inv,
    ROUND(SUM(IF(trans_type='grn' AND value_factor>0,value_calculated,0)),2) AS surchg,
    ROUND(SUM(IF(trans_type='grninv' AND value_factor>0,value_calculated,0)),2) AS surchg_inv,

    ROUND(SUM(IF(trans_type='grn' AND value_factor<0 AND a.gst_tax_rate=0 AND dn=0,value_calculated,0)),2) AS trans_disc,
    ROUND(SUM(IF(trans_type='grninv' AND value_factor<0 AND a.gst_tax_rate=0 AND dn=0,value_calculated,0)),2) AS trans_disc_inv
    
    FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE a.refno=%s /*AND value_factor>0*/
    GROUP BY gst_tax_code) h
    ON e.refno=h.refno AND e.gst_tax_code=h.surchg_tax_code

    INNER JOIN backend.supcus f
    ON e.CODE=f.CODE

    LEFT JOIN backend.locationgroup b ON a.locgroup=b.CODE
    LEFT JOIN backend.cp_set_branch c ON a.locgroup=c.branch_code
    INNER JOIN backend.companyprofile d
    INNER JOIN backend.xsetup

    WHERE e.refno=%s AND f.TYPE='s' AND a.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)

    ORDER BY gst_tax_code DESC
    """

    result4 = panda.raw_query(querystr, [
                              search_refno, search_refno, search_refno, search_refno, search_refno, search_refno])
    result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)


# report GRN


@api_view(['GET'])
def report_GrSupplierCopy(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT a.*,b.* FROM

    (SELECT CONCAT(a.CODE,' - ',a.NAME) AS supplier,tel,fax,a.term,location,refno,grdate,cross_ref,
    IF(in_kind=0,subtotal1,0) AS subtotal1,discount1 * -1 AS discount1,subtotal2,discount2,total,DATE_FORMAT(issuestamp,'%%d-%%m-%%Y %%H:%%i:%%s') AS issuestamp,receivedby AS issuedby,
    DATE_FORMAT(postdatetime,'%%d-%%m-%%Y %%H:%%i:%%s') AS postdatetime,postby,postby AS approvedby,DATE_FORMAT(a.laststamp,'%%d-%%m-%%Y %%H:%%i:%%s') AS laststamp,
    a.remark,
    IF(discount1type=1,'%%','$') AS discount1type,IF(discount2type=1,'%%','$') AS discount2type,
    contact,add1,add2,add3,city,state,postcode,country,
    IF(a.consign=1,'CONSIGNMENT           RECEIVED NOTE',IF(in_kind=1,'GOODS RECEIVED NOTE           STOCK IN-KIND',
    IF(stock_returnable=0,'GOODS RECEIVED NOTE   OUTRIGHT NON RETURNABLE','GOODS RECEIVED NOTE   OUTRIGHT RETURNABLE'))) AS title,

    IF(a.consign=1,'Consignment','Goodes Received Note') AS title_1,
    IF(a.consign=1,'Received Note',IF(in_kind=1,'Stock In-Kind',IF(stock_returnable=0,'Outright Non Returnable','Outright Returnable'))) AS title_2,

    IF(ibt=1,IF(ibt_gst=0,'GRN - Inter Branch Transfer Inwards','GRN - Inter Branch Transfer Inwards'),
    IF(ibt=2,IF(ibt_gst=0,'Goods Received Note - Inter Company','Goods Received Note - Inter Company'),
    IF(a.consign=1,'Consignment Received Note',IF(in_kind=1,'Goods Received Note Stock In-Kind',
    IF(stock_returnable=0,'Goods Received Note Outright Non Returnable','Goods Received Note Outright Returnable'))))) AS title_3,

    IF(ibt=1,IF(ibt_gst=0,'Inter Branch Stock Transfer Inwards from','Inter Branch Stock Transfer Inwards from'),
    IF(ibt=2,IF(ibt_gst=0,'Purchase from Inter Company','Purchase from Inter Company'),
    IF(a.tax_code_purchase='NR','Purchase from Supplier',IF(e.gst_tax_rate=0,
    'Purchase from Supplier','Purchase from Supplier')))) AS title_gst,

    IF(ibt=1,'Transfer Note No','Tax Invoice No') AS title_invno,
    IF(ibt=1,'IBT Branch Copy',IF(ibt=2,'Inter Co Supplier Copy','Supplier Copy')) AS title_supcopy,

    doc_name_reg,docdate,
    IF(in_kind=1,'Stock In-Kind Net','GRN Net Amount') AS total_net_desc,postby AS approved_by,DATE_FORMAT(postdatetime,'%%d-%%m-%%Y %%H:%%i:%%s') AS approved_at,
    CONCAT('Tel: ',tel,'    Fax: ',fax) AS contact_sup,
    CONCAT(a.location,' - ',d.description) AS loc_desc,
    CONCAT('Co Reg No: ',reg_no,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no,
    IF((SELECT COUNT(DISTINCT(gst_tax_code)) AS gst_count FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE a.refno=%s
    GROUP BY a.refno)=1 AND ibt=0,CONCAT('    Tax Code: ',tax_code_purchase),'')))) reg_sup,
    invno,dono,
    CONCAT('Received Loc: ',CONCAT(a.location,' - ',d.description),'    Date: ',DATE_FORMAT(grdate,'%%d/%%m/%%y %%a'),'    Tax Invoice No: ',
    invno,'    DO No: ',dono,'    Inv Date: ',DATE_FORMAT(docdate,'%%d/%%m/%%y')) AS grn_desc,
    IF(a.billstatus=1,'','Document Not Posted') AS chk_1,
    IF((SELECT set_enable FROM backend.`set_module_features` WHERE module_feature = 'Display "No Signature Is Required" @ Docoument')=1,
    '***This document is computer generated. No signature is required.***','') AS no_signature

    FROM backend.grmain a
    INNER JOIN backend.supcus c
    ON a.CODE=c.CODE
    INNER JOIN backend.location d
    ON a.location=d.CODE
    LEFT JOIN backend.set_gst_table e
    ON a.tax_code_purchase=e.gst_tax_code
    WHERE refno=%s AND /*billstatus=1 AND*/ TYPE='s' /*AND pay_by_invoice=0*/) a

    INNER JOIN

    (SELECT /*IF(remark IS NULL OR remark='',IF(branch_name ='' OR branch_name IS NULL,companyname,branch_name),remark)*/
    IF(branch_name='' OR branch_name IS NULL,companyname,branch_name) AS companyname,
    (SELECT grnremark1 FROM backend.xsetup) AS poremark1,
    (SELECT grnremark2 FROM backend.xsetup) AS poremark2,
    (SELECT grnremark3 FROM backend.xsetup) AS poremark3,
    IF(branch_add='' OR branch_add IS NULL,address1,'') AS address1,
    IF(branch_add='' OR branch_add IS NULL,address2,'') AS address2,
    IF(branch_add='' OR branch_add IS NULL,address3,'') AS address3,
    IF(branch_add='' OR branch_add IS NULL,CONCAT('Tel: ',tel,'    Fax: ',fax),CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax)) AS contactnumber,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,
    CONCAT('Co Reg No: ',IF(reg_no='' OR reg_no IS NULL,comp_reg_no,reg_no),IF(branch_gst='' OR branch_gst IS NULL,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no)),
    CONCAT('    GST Reg No: ',branch_gst))) reg_no,
    a.refno 
    FROM backend.grmain a

    INNER JOIN backend.companyprofile

    LEFT JOIN 
    (SELECT reg_no,gst_no AS branch_gst,name_reg,a.CODE AS scode,branch_add,branch_name,branch_tel,branch_fax FROM backend.grmain a
    INNER JOIN backend.cp_set_branch b
    ON a.loc_group=b.branch_code
    INNER JOIN backend.supcus c
    ON b.set_supplier_code=c.CODE
    WHERE refno=%s) b
    ON a.CODE=b.scode

    WHERE a.refno=%s) b

    ON a.refno=b.refno

    """

    result = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno])
    result = {"query1": result}

    querystr = """
    SELECT line,
    IF(pricetype='RTV','Item Not in PO',barcode) AS barcode,
    itemcode,itemlink,description,qty,netunitprice,packsize,totalprice,
    itemremark,a.refno,groupno,
    IF(purtolerance_std_plus=0 AND purtolerance_std_minus=0,'','Tolerance:') AS tolerance_desc,
    IF(purtolerance_std_plus=0 AND purtolerance_std_minus=0,'',CONCAT('/',um)) AS tolerance_desc1,
    IF(purtolerance_std_plus=0,'',purtolerance_std_plus) AS tolerance_plus,IF(purtolerance_std_minus=0,'',purtolerance_std_minus) AS tolerance_minus,
    disc1type,disc2type,IF(pricetype<>'FOC','','foc') AS pricetype,LOWER(um) AS um,
    discamt,
    IF(qty<bulkqty OR bulkqty=1,'',CONCAT('= ',IF(MOD(qty/bulkqty,1)=0,qty/bulkqty,ROUND(qty/bulkqty,1)),' ',umbulk)) AS ctn,
    IF(disc1value=0,'',IF(disc1type='%%',CONCAT(ROUND(disc1value,2),disc1type),CONCAT(disc1type,ROUND(disc1value,2)))) AS disc1value,
    IF(disc2value=0,'',IF(disc2type='%%',CONCAT(ROUND(disc2value,2),disc2type),CONCAT(disc2type,ROUND(disc2value,2)))) AS disc2value,

    CONCAT(IF(disc1value=0,'',IF(disc1type='%%',CONCAT(IF(MOD(disc1value,1)=0,ROUND(disc1value),ROUND(disc1value,2)),disc1type),
    CONCAT(disc1type,ROUND(disc1value,2)))),IF(disc2value=0,'',IF(disc2type='%%',CONCAT(' + ',IF(MOD(disc1value,2)=0,
    ROUND(disc2value),ROUND(disc2value,2)),disc2type),CONCAT(disc2type,ROUND(disc2value,2))))) AS disc_desc,
    IF(a.gst_tax_rate=0,'Z','S') AS gst_unit_code,
    ROUND(gst_tax_amount/qty,4) AS gst_unit_tax,

    ROUND(IF(hcost_gr=0,netunitprice+ROUND(gst_tax_amount/qty,4),((totalprice-ROUND(hcost_gr,2))+gst_tax_amount)/qty),4) AS gst_unit_cost,
    /*ROUND(IF(discvalue=0 AND surchgvalue=0,netunitprice+ROUND(gst_tax_amount/qty,4),((totalprice-ROUND(discvalue+surchgvalue,2))+gst_tax_amount)/qty),4) AS gst_unit_cost,*/

    gst_tax_amount AS gst_child_tax,

    ROUND(((totalprice-ROUND((hcost_gr),2))+gst_tax_amount),2) AS gst_unit_total,
    /*ROUND(((totalprice-ROUND((discvalue+surchgvalue),2))+gst_tax_amount),2) AS gst_unit_total,*/

    gst_tax_sum AS gst_main_tax,
    ROUND(total+gst_tax_sum,2) AS gst_main_total,
    CONCAT(packsize,IF(bulkqty=1,'',CONCAT('/',bulkqty))) AS ps,

    unitprice,bulkqty,articleno,
    IF(in_kind=1,'Total Stock In-Kind','Total Before Tax') AS total_desc,
    gst_tax_code,a.gst_tax_rate,

    IF(LENGTH(MID(gst_tax_amount,POSITION('.' IN gst_tax_amount)+1,10))<=2,FORMAT(gst_tax_amount,2),
    FORMAT(gst_tax_amount,4)) AS gst_tax_amount,

    ROUND((hcost_gr)/qty,4) AS unit_disc_prorate,
    ROUND(IF(hcost_gr=0,netunitprice,(totalprice-(hcost_gr))/qty),4) AS unit_price_bfr_tax,
    /*ROUND((discvalue+surchgvalue)/qty,4) AS unit_disc_prorate,
    ROUND(IF(discvalue=0 AND surchgvalue=0,netunitprice,(totalprice-(discvalue+surchgvalue))/qty),4) AS unit_price_bfr_tax,*/

    porefno,poqty,pounitprice,pototalprice,poactcost

    FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE a.refno=%s AND qty<>0 /* if(pricetype='RTV',qty=0,qty<>0) AND billstatus=1 AND pay_by_invoice=0 */
    ORDER BY groupno,pricetype,line
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["query2"] = result2

    querystr = """
    SELECT dbtype,itemcode,refno,description,packsize,lastcost,SUM(qty) AS qty,SUM(totalcost) AS totalcost,reason,scan_barcode,created_at,
    created_by FROM

    (SELECT 'Goods To Be Returned' AS dbtype,itemcode,'GR Basket' AS refno,a.description,packsize,lastcost,qty,lastcost*qty AS totalcost,
    reason,scan_barcode,created_at,created_by 
    FROM backend.dbnote_basket a
    INNER JOIN backend.grmain b
    ON a.sup_code=b.CODE
    WHERE converted=0 AND b.refno=%s /*AND billstatus=1*/ AND pay_by_invoice=0

    UNION ALL

    SELECT 'DN Created But Not Posted' AS dbtype,itemcode,b.refno,a.description,packsize,unitprice AS lastcost,qty,totalprice AS totalcost,reason,barcode AS scan_barcode,b.issuestamp AS created_at,b.issuedby AS created_by FROM backend.dbnotechild a
    INNER JOIN backend.dbnotemain b
    ON a.refno=b.refno
    INNER JOIN backend.grmain c
    ON b.CODE=c.CODE
    WHERE b.billstatus=0 AND c.refno=%s /*AND c.billstatus=1*/ AND pay_by_invoice=0

    ORDER BY dbtype,created_at

    LIMIT 18446744073709551615) a

    GROUP BY itemcode;
    """
    result3 = panda.raw_query(querystr, [search_refno, search_refno])
    result["query3"] = result3

    querystr = """
    SELECT a.*,b.* FROM

    (SELECT 'A' AS sort,refno,sequence,CONCAT(CODE,' (',surcharge_disc_type,')') AS code_grn,surcharge_disc_value*value_factor AS value_grn,
    ROUND(value_calculated,2) AS value_calculated
    FROM backend.trans_surcharge_discount 
    WHERE refno=%s AND dn=0 AND trans_type='grn'/* AND value_factor=-1*/

    /*UNION ALL

    SELECT 'B' AS sort,refno,'1' AS sequence,'Total After Discount' AS code_grn,0 AS value_grn,
    subtotal2 AS value_calculated FROM backend.grmain
    WHERE refno=%s AND discount1<>0

    UNION ALL

    SELECT 'A' AS sort,refno,sequence,CONCAT(CODE,' (',surcharge_disc_type,')') AS code_grn,surcharge_disc_value*value_factor AS value_grn,
    ROUND(value_calculated,2) AS value_calculated
    FROM backend.trans_surcharge_discount 
    WHERE refno=%s AND dn=0 AND trans_type='grn' AND value_factor=1*/

    UNION ALL

    SELECT 'D' AS sort,refno,'1' AS sequence,'Total Include Surcharge/Discount' AS code_grn,0 AS value_grn,
    total AS value_calculated FROM backend.grmain
    WHERE refno=%s AND discount1<>0

    UNION ALL

    SELECT 'E1' AS sort,refno,'1' AS sequence,'Item Tax Amount' AS code_grn,0 AS value_grn,
    ROUND(gst_tax_sum,2) AS value_calculated FROM backend.grmain
    WHERE refno=%s

    UNION ALL

    SELECT 'E2' AS sort,refno,'1' AS sequence,'Surcharge Tax Amount' AS code_grn,0 AS value_grn,
    ROUND(surchg_tax_sum,2) AS value_calculated FROM backend.grmain
    WHERE refno=%s AND IF(pay_by_invoice=1,invsurcharge<>0,discount2<>0)

    UNION ALL

    SELECT 'F' AS sort,refno,'1' AS sequence,'GST Rounding Adjustment' AS code_grn,0 AS value_grn,
    ROUND(GST_adj,2) AS value_calculated FROM backend.grmain
    WHERE refno=%s AND gst_adj<>0

    UNION ALL

    SELECT 'G' AS sort,refno,'1' AS sequence,'Bill Rounding Adjustment' AS code_grn,0 AS value_grn,
    ROUND(rounding_adj,2) AS value_calculated FROM backend.grmain
    WHERE refno=%s AND rounding_adj<>0

    UNION ALL

    SELECT 'H' AS sort,refno,'1' AS sequence,'Total Amount Include Tax' AS code_grn,0 AS value_grn,
    ROUND(total+gst_tax_sum+surchg_tax_sum+gst_adj+rounding_adj,2) AS value_calculated FROM backend.grmain
    WHERE refno=%s

    ORDER BY sort,sequence

    LIMIT 18446744073709551615) a


    INNER JOIN

    (SELECT refno,SUM(gst_zero) AS gst_zero,SUM(gst_std) AS gst_std FROM 

    (SELECT a.refno,ROUND(SUM(totalprice-hcost_gr),2) AS gst_zero,0 AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_tax_amount=0 AND a.refno=%s
    GROUP BY refno

    UNION ALL

    SELECT a.refno,0 AS gst_zero,ROUND(SUM(totalprice-hcost_gr),2) AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_tax_amount<>0 AND a.refno=%s
    GROUP BY refno) a

    GROUP BY refno) b

    ON a.refno=b.refno
    """

    result4 = panda.raw_query(querystr, [search_refno, search_refno, search_refno, search_refno,
                              search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno])
    result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)

# report GRDA


@api_view(['GET'])
def report_Grda(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT a.*,b.* FROM

    (SELECT CONCAT(IF(transtype IN ('IVS','IVN'),ap_sup_code,a.CODE),' - ',
    IF(transtype IN ('IVS','IVN'),c.name,a.NAME)) AS supplier,
    tel,fax,a.term,location,a.refno,grdate,cross_ref,
    IF(in_kind=0,subtotal1,0) AS subtotal1,discount1 * -1 AS discount1,subtotal2,discount2,total,issuestamp,receivedby AS issuedby,
    DATE_FORMAT(postdatetime,'%%d-%%m-%%Y %%H:%%i:%%s') AS postdatetime,postby,postby AS approvedby,DATE_FORMAT(a.laststamp,'%%d-%%m-%%Y %%H:%%i:%%s') AS laststamp,
    a.remark,
    IF(discount1type=1,'%%','$') AS discount1type,IF(discount2type=1,'%%','$') AS discount2type,
    contact,add1,add2,add3,city,state,postcode,country,

    IF(ibt=1,IF(ibt_gst=0,'Issued to Inter Branch Outlet','Issued to Inter Branch Outlet'),
    IF(ibt=2,IF(ibt_gst=0,'Issued to Inter Company Supplier','Issued to Inter Company Supplier'),
    IF(a.tax_code_purchase='NR','Issued to Supplier',IF(e.gst_tax_rate=0,
    'Issued to Supplier','Issued to Supplier')))) AS title_gst,

    IF(in_kind=1,'Stock In-Kind Net','GRN Net Amount') AS total_net_desc,postby AS approved_by,DATE_FORMAT(postdatetime,'%%d-%%m-%%Y %%H:%%i:%%s') AS approved_at,
    CONCAT('Tel: ',tel,'    Fax: ',fax) AS contact_sup,
    CONCAT(a.location,' - ',d.description) AS loc_desc,
    CONCAT('Co Reg No: ',reg_no,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no,
    IF((SELECT COUNT(DISTINCT(gst_tax_code)) AS gst_count FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE a.refno=%s
    GROUP BY a.refno)=1,CONCAT('    Tax Code: ',tax_code),'')))) reg_sup,
    invno,dono,
    CONCAT('Inv ',
    invno,'   DO ',dono,'   Date ',DATE_FORMAT(docdate,'%%d/%%m/%%y')) AS grdn_desc,
    IF(a.billstatus=1,'','Document Not Posted') AS chk_1,
    IF(transtype IN ('IVS','IVN'),c.name_reg,doc_name_reg) AS doc_name_reg,

    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Debit Note issued by'))) AS title_grda,

    IF(ibt=1,'IBT Branch Copy',IF(ibt=2,'Inter Co Supplier Copy','Supplier Copy')) AS title_supcopy

    FROM backend.grmain a

    INNER JOIN backend.grmain_dncn b
    ON a.refno=b.refno

    INNER JOIN backend.supcus c
    ON IF(transtype IN ('IVS','IVN'),b.ap_sup_code,a.CODE)=c.CODE

    INNER JOIN backend.location d
    ON a.location=d.CODE

    LEFT JOIN backend.set_gst_table e
    ON a.tax_code_purchase=e.gst_tax_code

    WHERE a.refno=%sAND /*billstatus=1 AND*/ TYPE='s') a

    INNER JOIN

    (SELECT /*IF(remark IS NULL OR remark='',IF(branch_name ='' OR branch_name IS NULL,companyname,branch_name),remark)*/
    IF(branch_name='' OR branch_name IS NULL,companyname,branch_name) AS companyname,
    (SELECT grnremark1 FROM backend.xsetup) AS grnremark1,
    (SELECT grnremark2 FROM backend.xsetup) AS grnremark2,
    (SELECT grnremark3 FROM backend.xsetup) AS grnremark3,
    IF(branch_add='' OR branch_add IS NULL,address1,'') AS address1,
    IF(branch_add='' OR branch_add IS NULL,address2,'') AS address2,
    IF(branch_add='' OR branch_add IS NULL,address3,'') AS address3,
    IF(branch_add='' OR branch_add IS NULL,CONCAT('Tel: ',tel,'    Fax: ',fax),CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax)) AS contactnumber,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,
    CONCAT('Co Reg No: ',IF(reg_no='' OR reg_no IS NULL,comp_reg_no,reg_no),IF(branch_gst='' OR branch_gst IS NULL,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no)),
    CONCAT('    GST Reg No: ',branch_gst))) reg_no,
    a.refno 
    FROM backend.grmain a

    INNER JOIN backend.companyprofile

    LEFT JOIN 
    (SELECT reg_no,gst_no AS branch_gst,name_reg,a.CODE AS scode,branch_add,branch_name,branch_tel,branch_fax FROM backend.grmain a
    INNER JOIN backend.cp_set_branch b
    ON a.loc_group=b.branch_code
    INNER JOIN backend.supcus c
    ON b.set_supplier_code=c.CODE
    WHERE refno=%s) b
    ON a.CODE=b.scode

    WHERE a.refno=%s) b

    ON a.refno=b.refno

    """
    result = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno])
    result = {"query1": result}

    querystr = """
    SELECT a.*,b.gst_zero,gst_std,
    IF(pricetype='RTV','',barcode1) AS barcode,
    IF(LENGTH(MID(gst_tax_total,POSITION('.' IN gst_tax_total)+1,10))<=2,FORMAT(gst_tax_total,2),
    FORMAT(gst_tax_total,4)) AS gst_tax_total_1,
    'Total Amount Exclude Tax' AS title7,
    ROUND(variance_amt-var_total_disc+0.000001,2) AS total_gross,
    IF(a.transtype IN ('IVS','IVN'),name_reg,doc_name_reg) AS doc_name_reg1,
    CONCAT('Co Reg No: ',reg_no,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no,
    IF((SELECT COUNT(DISTINCT(gst_tax_code)) AS gst_count FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE a.refno=%s
    GROUP BY a.refno)=1,CONCAT('    Tax Code: ',tax_code),'')))) reg_sup,
    add1,add2,add3,contact_sup

    FROM

    (
    SELECT '1' AS sort,'1' AS sort1,a.refno,groupno,line,itemcode,description,description AS description_1,qty,inv_qty,inv_netunitprice,inv_totalprice,
    IF(pricetype='FOC' AND inv_netunitprice=0,CONCAT('PO Qty: ',IF(MOD(poqty_expected,1)=0,ROUND(poqty_expected),ROUND(poqty_expected,1))),'') AS pricetype_vendor,
    grdate,#CONCAT(b.CODE,'-',b.NAME) AS supplier,
    CONCAT(IF(transtype IN ('IVS','IVN'),ap_sup_code,b.CODE),' - ',
    IF(transtype IN ('IVS','IVN'),sc.name,b.NAME)) AS supplier,
    ROUND(pounitprice,4) AS pounitprice,totalprice AS invactcost,
    netunitprice,

    ROUND(ROUND(variance_qty,2)/ROUND(inv_qty - qty,4),4) AS factor,

    /* amend on 2020-10-23 and change to above due to target case TBPGR20100305 
    ROUND(variance_qty/(poqty_expected-qty),4) AS factor,*/
    pototalprice AS pototal,
    invno,dono,
    IF(pricetype='RTV','Item Not in PO',porefno) AS porefno,

    poqty,barcode AS barcode1,articleno,packsize,b.remark,loc_desc AS location,
    #IF(MOD(poqty_expected-qty,1)=0,poqty_expected-qty,ROUND(poqty_expected-qty,2)) AS qtyvar,
    IF(pay_by_invoice = 0,
    IF(MOD(poqty_expected-qty,1)=0,poqty_expected-qty,ROUND(poqty_expected-qty,2)),
    ROUND(inv_qty - qty,4))
    AS qtyvar,
    IF(variance_qty>0,'x','') AS chk1,'' AS chk2,
    ROUND(variance_qty,2) AS variance_amt,IF(pricetype='FOC','FOC','') AS pricetype,
    receivedby,
    IF(reason='' OR reason IS NULL,IF(pricetype='foc','FOC Short Supplied',
    IF(pricetype='RTV','Wrong Item','Qty Short Supplied')),reason) AS reason,
    group_code,postby,
    CONCAT(b.refno,'-',IF(transtype='ghv','IAV',transtype)) AS refno_dn,
    'Goods Received Difference Advice' AS title1,
    'Quantity Short Supplied' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Unit Price After Tax' AS title3,
    'Quantity' AS title4,
    'Unit Price After Discount' AS title5,
    # amended on 2020-10-23 'Unit Price Exclude Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(b.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',b.postby)) AS posted_on,
    CONCAT('Debit Note - Goods Received Difference Advice for ','Quantity Short Supplied') title_gst,
    CONCAT('Important Note : This Debit Advice is to notify your Company that qty received by us does not tallied with the qty specified in your Tax Invoice No ',invno,
    '.  Kindly issued us a credit note within 7 days from the date hereof failure which we will not proceed with payment of this invoice.') AS grdn_note,
    IF(a.gst_tax_rate=0,'Z','S') AS gst_unit_code,
    ROUND(gst_var_qty/IF(MOD(poqty_expected-qty,1)=0,poqty_expected-qty,ROUND(poqty_expected-qty,2)),4) AS gst_unit_tax,
    ROUND((variance_qty+gst_var_qty)/IF(MOD(poqty_expected-qty,1)=0,poqty_expected-qty,ROUND(poqty_expected-qty,2)),4) AS gst_unit_cost,
    ROUND((variance_qty+gst_var_qty),2) AS gst_unit_total,
    gst_var_qty AS gst_tax_total,
    ROUND(variance_qty+ROUND(gst_var_qty,4),2) AS gst_amt_total,
    transtype,'' AS title_inv,
    'GRDA Refno' AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',b.refno) AS refno_barcode,
    IF(tax_invoice=1,c.refno2,'') AS refno_2,

    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Debit Note issued by')))) AS title_grda,

    CONCAT('Supplier CN No: ',IF(c.sup_cn_no IS NULL,'',c.sup_cn_no)) AS sup_cn_no,
    CONCAT('CN Date: ',IF(c.sup_cn_date IS NULL,'',DATE_FORMAT(c.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    c.rounding_adj AS rounding_dncn,
    c.gst_adjust AS rounding_dncn_gst,
    a.gst_tax_code,
    ROUND(hcost_iv-hcost_gr+0.000001,2)*-1 AS var_total_disc,
    name_reg,doc_name_reg,reg_no,gst_no,tax_code,add1,add2,add3,
    IF(in_kind=1,'Stock In-Kind Net','GRN Net Amount') AS total_net_desc,postby AS approved_by,a.postdatetime AS approved_at,
    CONCAT('Tel: ',tel,'    Fax: ',fax) AS contact_sup

    FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    INNER JOIN backend.grmain_dncn c
    ON a.refno=c.refno
    INNER JOIN backend.supcus sc
    ON IF(transtype IN ('IVS','IVN'),c.ap_sup_code,b.CODE)=sc.CODE
    LEFT JOIN backend.set_group_dept e
    ON a.dept=e.dept_code
    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON b.location=d.CODE
    WHERE a.refno=%s AND transtype='gqv'
    AND IF(pricetype='foc',qty<>poqty_expected,inv_qty<>qty)
    /* amend on 180421 due to everrise case 4mg1841343 IF(pricetype<>'foc',variance_qty<>0,qty<>poqty_expected) */


    UNION ALL

    SELECT '2' AS sort,'2' AS sort1,a.refno,groupno,line,itemcode,description,description AS description_1,qty,inv_qty,inv_netunitprice,inv_totalprice,
    IF(pricetype='FOC' AND inv_netunitprice=0,pricetype,'') AS pricetype_vendor,grdate,#CONCAT(b.CODE,'-',b.NAME) AS supplier,
    CONCAT(IF(transtype IN ('IVS','IVN'),ap_sup_code,b.CODE),' - ',
    IF(transtype IN ('IVS','IVN'),sc.name,b.NAME)) AS supplier,
    ROUND(pounitprice,4) AS pounitprice,totalprice AS invactcost,
    netunitprice,ROUND(variance_cost/inv_qty,4) AS factor,pototalprice AS pototal,
    invno,dono,porefno,poqty,barcode AS barcode1,articleno,packsize,b.remark,loc_desc AS location,inv_qty AS qtyvar,
    '' AS chk1,IF(variance_cost>0,'x','') AS chk2,
    ROUND(variance_cost,2) AS variance_amt,IF(pricetype='FOC','FOC','') AS pricetype,
    receivedby,'Price Overcharged' AS reason,group_code,postby,
    CONCAT(b.refno,'-','IAV') AS refno_dn,'Goods Received Difference Advice' AS title1,'Price Overcharged' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Unit Price After Tax' AS title3,'Quantity' AS title4,'Unit Price Before Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(b.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',b.postby)) AS posted_on,
    CONCAT('Debit Note - Goods Received Difference Advice for ','Price Overcharged') title_gst,
    CONCAT('Important Note : This Debit Advice is to notify your Company that the price charged in your Tax Invoice No ',invno,
    ' is higher than our PO Price.  Kindly issued us a credit note within 7 days from the date hereof failure which we will not proceed with payment of this invoice.') AS grdn_note,
    IF(a.gst_tax_rate=0,'Z','S') AS gst_unit_code,
    ROUND(gst_var_cost/inv_qty,4) AS gst_unit_tax,
    ROUND((variance_cost+gst_var_cost)/inv_qty,4) AS gst_unit_cost,
    ROUND((variance_cost+gst_var_cost),2) AS gst_unit_total,
    gst_var_cost AS gst_tax_total,
    ROUND(variance_cost+ROUND(gst_var_cost,4),2) AS gst_amt_total,
    transtype,'' AS title_inv,
    'GRDA Refno' AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',b.refno) AS refno_barcode,
    IF(tax_invoice=1,c.refno2,'') AS refno_2,
    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Debit Note issued by')))) AS title_grda,
    CONCAT('Supplier CN No: ',IF(c.sup_cn_no IS NULL,'',c.sup_cn_no)) AS sup_cn_no,
    CONCAT('CN Date: ',IF(c.sup_cn_date IS NULL,'',DATE_FORMAT(c.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    c.rounding_adj AS rounding_dncn,
    c.gst_adjust AS rounding_dncn_gst,
    a.gst_tax_code,
    ROUND(hcost_iv+0.000001,2)*-1 AS var_total_disc,
    name_reg,doc_name_reg,reg_no,gst_no,tax_code,add1,add2,add3,
    IF(in_kind=1,'Stock In-Kind Net','GRN Net Amount') AS total_net_desc,postby AS approved_by,a.postdatetime AS approved_at,
    CONCAT('Tel: ',tel,'    Fax: ',fax) AS contact_sup


    FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    INNER JOIN backend.grmain_dncn c
    ON a.refno=c.refno
    INNER JOIN backend.supcus sc
    ON IF(transtype IN ('IVS','IVN'),c.ap_sup_code,b.CODE)=sc.CODE
    LEFT JOIN backend.set_group_dept e
    ON a.dept=e.dept_code
    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON b.location=d.CODE
    WHERE a.refno=%s AND variance_cost<>0 AND transtype='iav'


    UNION ALL 

    SELECT '3' AS sort,IF(rebate_value=0,'4','3') AS sort1,a.refno,a.groupno,a.line,itemcode,description,description AS description_1,qty,inv_qty,inv_netunitprice,inv_totalprice,
    IF(pricetype='FOC' AND inv_netunitprice=0,pricetype,'') AS pricetype_vendor,grdate,#CONCAT(b.CODE,'-',b.NAME) AS supplier,
    CONCAT(IF(transtype IN ('IVS','IVN'),ap_sup_code,b.CODE),' - ',
    IF(transtype IN ('IVS','IVN'),sc.name,b.NAME)) AS supplier,
    ROUND(pounitprice,4) AS pounitprice,totalprice AS invactcost,
    netunitprice,rebate_value AS factor,pototalprice AS pototal,
    invno,dono,porefno,poqty,barcode AS barcode1,articleno,packsize,b.remark,loc_desc AS location,1 AS qtyvar,
    '' AS chk1,'' AS chk2,
    ROUND(rebate_value,2) AS variance_amt,IF(pricetype='FOC','FOC','') AS pricetype,
    receivedby,IF(rebate_value=0,'','Rebate Incentive') AS reason,group_code,postby,
    CONCAT(b.refno,'-','GRV') AS refno_dn,'PO/GRN Debit Advice' AS title1,'By Invoice Item' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Rebate Amt After Tax' AS title3,'Quantity' AS title4,'Rebate Amt Before Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(b.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',b.postby)) AS posted_on,

    IF(tax_invoice=1,'Tax Invoice',
    CONCAT('PO/GRN Debit Note for ','Rebate Incentive')) title_gst,

    IF(tax_invoice=1,'',
    CONCAT('Important Note : This Debit Advice is to notify your Company that your company has agreed to issue a Rebate CN for the above item purchased.  Kindly issued us a credit note within 7 days from the date hereof failure which we will not proceed with payment of this invoice.'))
    AS grdn_note,

    IF(a.gst_tax_rate=0,'Z','S') AS gst_unit_code,
    ROUND(gst_rebate_amt,2) AS gst_unit_tax,
    ROUND((rebate_value+gst_rebate_amt),2) AS gst_unit_cost,
    ROUND((rebate_value+gst_rebate_amt),2) AS gst_unit_total,
    gst_rebate_amt AS gst_tax_total,
    ROUND(rebate_value+ROUND(gst_rebate_amt,4),2) AS gst_amt_total,
    transtype,
    IF(tax_invoice=1,'Rebate Incentive','') AS title_inv,
    IF(tax_invoice=1,'Refno #1','GRDN Refno') AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',b.refno) AS refno_barcode,
    IF(tax_invoice=1,h.refno2,'') AS refno_2,
    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Debit Note issued by')))) AS title_grda,
    CONCAT('Supplier CN No: ',IF(h.sup_cn_no IS NULL,'',h.sup_cn_no)) AS sup_cn_no,
    CONCAT('CN Date: ',IF(h.sup_cn_date IS NULL,'',DATE_FORMAT(h.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    h.rounding_adj AS rounding_dncn,
    h.gst_adjust AS rounding_dncn_gst,
    a.gst_tax_code,
    ROUND(hcost_iv+0.000001,2)*-1 AS var_total_disc,
    name_reg,doc_name_reg,reg_no,gst_no,tax_code,add1,add2,add3,
    IF(in_kind=1,'Stock In-Kind Net','GRN Net Amount') AS total_net_desc,postby AS approved_by,a.postdatetime AS approved_at,
    CONCAT('Tel: ',tel,'    Fax: ',fax) AS contact_sup

    FROM backend.grchild a

    INNER JOIN backend.grmain b
    ON a.refno=b.refno

    INNER JOIN backend.grmain_dncn h
    ON b.refno=h.refno

    INNER JOIN backend.supcus sc
    ON IF(transtype IN ('IVS','IVN'),h.ap_sup_code,b.CODE)=sc.CODE

    INNER JOIN 
    (SELECT a.refno,a.groupno,IF(a.groupno=0,a.line,b.line) AS line1,b.line AS line FROM 
    (SELECT refno,groupno,line FROM backend.grchild 
    WHERE rebate_value<>0 AND refno=%s
    GROUP BY groupno) a
    INNER JOIN backend.grchild b
    ON a.refno=b.refno AND a.groupno=b.groupno
    WHERE IF(b.groupno=0,rebate_value<>0,rebate_value>=0)
    GROUP BY groupno,line) c
    ON a.refno=c.refno AND a.line=c.line

    LEFT JOIN backend.set_group_dept e
    ON a.dept=e.dept_code

    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON b.location=d.CODE

    WHERE a.refno=%s AND transtype='GRV'

    UNION ALL

    SELECT '6' AS sort,'5' AS sort1,a.refno,0 AS groupno,0 AS line,'' AS itemcode,
    CONCAT(code_type,' ',
    IF(surcharge_disc_type='%%',CONCAT(surcharge_disc_value,surcharge_disc_type),
    CONCAT(surcharge_disc_type,surcharge_disc_value)),' - by Debit Note') AS description,
    CONCAT(b.code,' - ',code_type,' ',
    IF(surcharge_disc_type='%%',CONCAT(surcharge_disc_value,surcharge_disc_type),
    CONCAT(surcharge_disc_type,surcharge_disc_value)),' - by Debit Note') AS description_1,
    0 AS qty,0 AS inv_qty,0 AS inv_netunitprice,invnetamt_vendor AS inv_totalprice,
    '' AS pricetype_vendor,grdate,#CONCAT(a.CODE,' - ',a.NAME) AS supplier,
    CONCAT(IF(transtype IN ('IVS','IVN'),ap_sup_code,a.CODE),' - ',
    IF(transtype IN ('IVS','IVN'),sc.name,a.NAME)) AS supplier,
    0 AS pounitprice,a.total AS invactcost,
    0 AS netunitprice,ROUND(ABS(value_calculated)/**value_factor*/,2) AS factor,pototal,
    invno,dono,porefno,0 AS poqty,'' AS barcode1,'' AS articleno,0 AS packsize,a.remark,
    loc_desc AS location,1 AS qtyvar,
    '' AS chk1,'' AS chk2,ROUND(ABS(value_calculated)/**value_factor*/,2) AS variance_amt,'' AS pricetype,
    receivedby,IF(share_cost=0,'Discount Income','Reduce Purchase Cost') AS reason,group_code,postby,
    CONCAT(a.refno,'-','GDV') AS refno_dn,'PO/GRN Debit Note' AS title1,'By Total Invoice' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Amount After Tax' AS title3,'Quantity' AS title4,'Amount Debit Before Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(a.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',a.postby)) AS posted_on,

    IF(tax_invoice=1,'Tax Invoice',
    CONCAT('PO/GRN Debit Note for ','Total Invoice (Discount Income)')) title_gst,

    IF(tax_invoice=1,'',
    CONCAT('Important Note : This Debit Advice is to notify your Company that your company has agreed to issue a Credit Note for our PO refno ',
    porefno,'.  Kindly issued us a credit note within 7 days from the date hereof failure which we will not proceed with payment of this invoice.'))
    AS grdn_note,

    IF(b.gst_amt=0,'Z','S') AS gst_unit_code,
    ROUND(b.gst_amt,2) AS gst_unit_tax,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_unit_cost,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_unit_total,
    ROUND(b.gst_amt,4) AS gst_tax_total,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_amt_total,
    transtype,
    IF(tax_invoice=1,'GRDN Discount Income','') AS title_inv,
    IF(tax_invoice=1,'Refno #1','GRDN Refno') AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',a.refno) AS refno_barcode,
    IF(tax_invoice=1,e.refno2,'') AS refno_2,
    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Debit Note issued by')))) AS title_grda,
    CONCAT('Supplier CN No: ',IF(e.sup_cn_no IS NULL,'',e.sup_cn_no)) AS sup_cn_no,
    CONCAT('CN Date: ',IF(e.sup_cn_date IS NULL,'',DATE_FORMAT(e.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    e.rounding_adj AS rounding_dncn,
    e.gst_adjust AS rounding_dncn_gst,
    b.gst_tax_code,
    0 AS var_total_disc,
    name_reg,doc_name_reg,reg_no,gst_no,tax_code,add1,add2,add3,
    IF(in_kind=1,'Stock In-Kind Net','GRN Net Amount') AS total_net_desc,postby AS approved_by,a.postdatetime AS approved_at,
    CONCAT('Tel: ',tel,'    Fax: ',fax) AS contact_sup

    FROM backend.grmain a

    INNER JOIN backend.trans_surcharge_discount b
    ON a.refno=b.refno

    INNER JOIN backend.grmain_dncn e
    ON a.refno=e.refno

    INNER JOIN backend.supcus sc
    ON IF(transtype IN ('IVS','IVN'),e.ap_sup_code,a.CODE)=sc.CODE

    INNER JOIN
    (SELECT a.refno,group_code,b.total AS pototal,porefno FROM backend.grchild a

    INNER JOIN backend.pomain b
    ON a.porefno=b.refno

    LEFT JOIN 
    backend.set_group_dept e
    ON a.dept=e.dept_code
    WHERE a.refno=%s
    GROUP BY refno) c
    ON a.refno=c.refno

    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON a.location=d.CODE

    WHERE a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND transtype='gdv' AND build_into_cost=0 AND value_factor<0


    UNION ALL

    SELECT '5' AS sort,'6' AS sort1,a.refno,0 AS groupno,0 AS line,'' AS itemcode,
    CONCAT(code_type,' ',
    IF(surcharge_disc_type='%%',CONCAT(surcharge_disc_value,surcharge_disc_type),
    CONCAT(surcharge_disc_type,surcharge_disc_value)),' - by Debit Note') AS description,
    CONCAT(b.code,' - ',code_type,' ',
    IF(surcharge_disc_type='%%',CONCAT(surcharge_disc_value,surcharge_disc_type),
    CONCAT(surcharge_disc_type,surcharge_disc_value)),' - by Debit Note') AS description_1,
    0 AS qty,0 AS inv_qty,0 AS inv_netunitprice,invnetamt_vendor AS inv_totalprice,
    '' AS pricetype_vendor,grdate,#CONCAT(a.CODE,' - ',a.NAME) AS supplier,
    CONCAT(IF(transtype IN ('IVS','IVN'),ap_sup_code,a.CODE),' - ',
    IF(transtype IN ('IVS','IVN'),sc.name,a.NAME)) AS supplier,
    0 AS pounitprice,a.total AS invactcost,
    0 AS netunitprice,
    ROUND(ABS(value_calculated),2) AS factor,

    /*ROUND(value_calculated/* amended on 16-08-03 due to tf bergr16061826 *value_factor,2) AS factor, - amended on 16-08-17 due to KMNGR16080234*/
    pototal,
    invno,dono,porefno,0 AS poqty,'' AS barcode1,'' AS articleno,0 AS packsize,a.remark,
    loc_desc AS location,1 AS qtyvar,
    '' AS chk1,'' AS chk2,ROUND(ABS(value_calculated)/**value_factor*/,2) AS variance_amt,'' AS pricetype,
    receivedby,IF(share_cost=0,'Discount Income','Reduce Purchase Cost') AS reason,group_code,postby,
    CONCAT(a.refno,'-','GDS') AS refno_dn,'PO/GRN Debit Note' AS title1,'By Total Invoice' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Amount After Tax' AS title3,'Quantity' AS title4,'Amount Debit Before Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(a.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',a.postby)) AS posted_on,

    IF(tax_invoice=1,'Tax Invoice',
    CONCAT('PO/GRN Debit Note for ','Total Invoice (Reduce Purchase Cost)')) title_gst,

    IF(tax_invoice=1,'',
    CONCAT('Important Note : This Debit Advice is to notify your Company that your company has agreed to issue a Credit Note for our PO refno ',
    porefno,'.  Kindly issued us a credit note within 7 days from the date hereof failure which we will not proceed with payment of this invoice.'))
    AS grdn_note,

    IF(b.gst_amt=0,'Z','S') AS gst_unit_code,
    ROUND(b.gst_amt,2) AS gst_unit_tax,
    ROUND((ABS(value_calculated)+ROUND(b.gst_amt,2)),2) AS gst_unit_cost,
    ROUND((ABS(value_calculated)+ROUND(b.gst_amt,2)),2) AS gst_unit_total,
    ROUND(b.gst_amt,4) AS gst_tax_total,
    ROUND((ABS(value_calculated)+ROUND(b.gst_amt,2)),2) AS gst_amt_total,
    transtype,
    IF(tax_invoice=1,'GRDN Purchase Cost Reduction','') AS title_inv,
    IF(tax_invoice=1,'Refno #1','GRDA Refno') AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',a.refno) AS refno_barcode,
    IF(tax_invoice=1,e.refno2,'') AS refno_2,
    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Debit Note issued by')))) AS title_grda,
    CONCAT('Supplier CN No: ',IF(e.sup_cn_no IS NULL,'',e.sup_cn_no)) AS sup_cn_no,
    CONCAT('CN Date: ',IF(e.sup_cn_date IS NULL,'',DATE_FORMAT(e.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    e.rounding_adj AS rounding_dncn,
    e.gst_adjust AS rounding_dncn_gst,
    b.gst_tax_code,
    0 AS var_total_disc,
    name_reg,doc_name_reg,reg_no,gst_no,tax_code,add1,add2,add3,
    IF(in_kind=1,'Stock In-Kind Net','GRN Net Amount') AS total_net_desc,postby AS approved_by,a.postdatetime AS approved_at,
    CONCAT('Tel: ',tel,'    Fax: ',fax) AS contact_sup

    FROM backend.grmain a

    INNER JOIN backend.trans_surcharge_discount b
    ON a.refno=b.refno

    INNER JOIN backend.grmain_dncn e
    ON a.refno=e.refno

    INNER JOIN backend.supcus sc
    ON IF(transtype IN ('IVS','IVN'),e.ap_sup_code,a.CODE)=sc.CODE

    INNER JOIN
    (SELECT a.refno,group_code,b.total AS pototal,porefno FROM backend.grchild a

    INNER JOIN backend.pomain b
    ON a.porefno=b.refno

    LEFT JOIN 
    backend.set_group_dept e
    ON a.dept=e.dept_code
    WHERE a.refno=%s
    GROUP BY refno) c
    ON a.refno=c.refno

    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON a.location=d.CODE

    WHERE a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND transtype='gds' AND build_into_cost=1 AND value_factor<0

    UNION ALL

    SELECT '7' AS sort,'7' AS sort1,a.refno,0 AS groupno,0 AS line,'' AS itemcode,
    CONCAT(code_type,' ',
    IF(surcharge_disc_type='%%',CONCAT(surcharge_disc_value,surcharge_disc_type),
    CONCAT(surcharge_disc_type,surcharge_disc_value)),' - by Credit Note') AS description,
    CONCAT(b.code,' - ',code_type,' ',
    IF(surcharge_disc_type='%%',CONCAT(surcharge_disc_value,surcharge_disc_type),
    CONCAT(surcharge_disc_type,surcharge_disc_value)),' - by Credit Note') AS description_1,
    0 AS qty,0 AS inv_qty,0 AS inv_netunitprice,invnetamt_vendor AS inv_totalprice,
    '' AS pricetype_vendor,grdate,#CONCAT(a.CODE,' - ',a.NAME) AS supplier,
    CONCAT(IF(transtype IN ('IVS','IVN'),ap_sup_code,a.CODE),' - ',
    IF(transtype IN ('IVS','IVN'),sc.name,a.NAME)) AS supplier,
    0 AS pounitprice,a.total AS invactcost,
    0 AS netunitprice,
    ROUND(ABS(value_calculated)/**value_factor*/,2) AS factor,
    pototal,
    invno,dono,porefno,0 AS poqty,'' AS barcode1,'' AS articleno,0 AS packsize,a.remark,
    loc_desc AS location,1 AS qtyvar,
    '' AS chk1,'' AS chk2,ROUND(ABS(value_calculated)/**value_factor*/,2) AS variance_amt,'' AS pricetype,
    receivedby,IF(share_cost=0,'Other Expenses','Purchase Cost') AS reason,group_code,postby,
    CONCAT(a.refno,'-','IVS') AS refno_dn,'PO/GRN Credit Note' AS title1,'By Total Invoice' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Amount After Tax' AS title3,'Quantity' AS title4,'Amount Credit Before Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(a.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',a.postby)) AS posted_on,

    IF(tax_invoice=1,'Tax Invoice',
    CONCAT('GRN Surcharge Credit Note for ','Debit Note or Invoice Received')) title_gst,

    IF(tax_invoice=1,'',
    CONCAT('Important Note : This Credit Advice is to notify your Company to issue a Tax Invoice or Debit Note for our Purchase ',
    porefno,'.  Kindly issued us a Tax Invoice or Debit Note note within 7 days from the date hereof failure which we will not proceed with payment.'))
    AS grdn_note,

    IF(b.gst_amt=0,'Z','S') AS gst_unit_code,
    ROUND(b.gst_amt,2) AS gst_unit_tax,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_unit_cost,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_unit_total,
    ROUND(b.gst_amt,4) AS gst_tax_total,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_amt_total,
    transtype,
    IF(tax_invoice=1,'GRCN Purchase Cost','') AS title_inv,
    IF(tax_invoice=1,'Refno #1','GRCN Refno') AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',a.refno) AS refno_barcode,
    IF(tax_invoice=1,e.refno2,'') AS refno_2,
    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Credit Note issued by')))) AS title_grda,
    CONCAT('Supplier DN/Inv No: ',IF(e.sup_cn_no IS NULL,'',e.sup_cn_no)) AS sup_cn_no,
    CONCAT('DN/Inv Date: ',IF(e.sup_cn_date IS NULL,'',DATE_FORMAT(e.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    e.rounding_adj AS rounding_dncn,
    e.gst_adjust AS rounding_dncn_gst,
    b.gst_tax_code,
    0 AS var_total_disc,
    name_reg,doc_name_reg,reg_no,gst_no,tax_code,add1,add2,add3,
    IF(in_kind=1,'Stock In-Kind Net','GRN Net Amount') AS total_net_desc,postby AS approved_by,a.postdatetime AS approved_at,
    CONCAT('Tel: ',tel,'    Fax: ',fax) AS contact_sup

    FROM backend.grmain a

    INNER JOIN backend.trans_surcharge_discount b
    ON a.refno=b.refno

    INNER JOIN backend.grmain_dncn e
    ON a.refno=e.refno AND b.sequence=e.trans_seq

    INNER JOIN backend.supcus sc
    ON IF(transtype IN ('IVS','IVN'),e.ap_sup_code,a.CODE)=sc.CODE

    INNER JOIN
    (SELECT a.refno,group_code,b.total AS pototal,porefno FROM backend.grchild a

    INNER JOIN backend.pomain b
    ON a.porefno=b.refno

    LEFT JOIN 
    backend.set_group_dept e
    ON a.dept=e.dept_code
    WHERE a.refno=%s
    GROUP BY refno) c
    ON a.refno=c.refno

    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON a.location=d.CODE

    WHERE a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 
    AND transtype='ivs' AND build_into_cost=1 AND value_factor>0

    UNION ALL

    SELECT '8' AS sort,'8' AS sort1,a.refno,0 AS groupno,0 AS line,'' AS itemcode,
    CONCAT(code_type,' ',
    IF(surcharge_disc_type='%%',CONCAT(surcharge_disc_value,surcharge_disc_type),
    CONCAT(surcharge_disc_type,surcharge_disc_value)),' - by Credit Note') AS description,
    CONCAT(b.code,' - ',code_type,' ',
    IF(surcharge_disc_type='%%',CONCAT(surcharge_disc_value,surcharge_disc_type),
    CONCAT(surcharge_disc_type,surcharge_disc_value)),' - by Credit Note') AS description_1,
    0 AS qty,0 AS inv_qty,0 AS inv_netunitprice,invnetamt_vendor AS inv_totalprice,
    '' AS pricetype_vendor,grdate,#CONCAT(a.CODE,' - ',a.NAME) AS supplier,
    CONCAT(IF(transtype IN ('IVS','IVN'),ap_sup_code,a.CODE),' - ',
    IF(transtype IN ('IVS','IVN'),sc.name,a.NAME)) AS supplier,
    0 AS pounitprice,a.total AS invactcost,
    0 AS netunitprice,
    ROUND(ABS(value_calculated)/**value_factor*/,2) AS factor,
    pototal,
    invno,dono,porefno,0 AS poqty,'' AS barcode1,'' AS articleno,0 AS packsize,a.remark,
    loc_desc AS location,1 AS qtyvar,
    '' AS chk1,'' AS chk2,ROUND(ABS(value_calculated)/**value_factor*/,2) AS variance_amt,'' AS pricetype,
    receivedby,IF(share_cost=0,'Other Expenses','Purchase Cost') AS reason,group_code,postby,
    CONCAT(a.refno,'-','IVN') AS refno_dn,'PO/GRN Credit Note' AS title1,'By Total Invoice' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Amount After Tax' AS title3,'Quantity' AS title4,'Amount Credit Before Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(a.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',a.postby)) AS posted_on,

    IF(tax_invoice=1,'Tax Invoice',
    CONCAT('GRN Surcharge Credit Note for ','Debit Note or Invoice Received')) title_gst,

    IF(tax_invoice=1,'',
    CONCAT('Important Note : This Credit Advice is to notify your Company to issue a Tax Invoice or Debit Note for our Purchase ',
    porefno,'.  Kindly issued us a Tax Invoice or Debit Note note within 7 days from the date hereof failure which we will not proceed with payment.'))
    AS grdn_note,

    IF(b.gst_amt=0,'Z','S') AS gst_unit_code,
    ROUND(b.gst_amt,2) AS gst_unit_tax,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_unit_cost,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_unit_total,
    ROUND(b.gst_amt,4) AS gst_tax_total,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_amt_total,
    transtype,
    IF(tax_invoice=1,'GRCN Purchase Cost','') AS title_inv,
    IF(tax_invoice=1,'Refno #1','GRCN Refno') AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',a.refno) AS refno_barcode,
    IF(tax_invoice=1,e.refno2,'') AS refno_2,
    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Credit Note issued by')))) AS title_grda,
    CONCAT('Supplier DN/Inv No: ',IF(e.sup_cn_no IS NULL,'',e.sup_cn_no)) AS sup_cn_no,
    CONCAT('DN/Inv Date: ',IF(e.sup_cn_date IS NULL,'',DATE_FORMAT(e.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    e.rounding_adj AS rounding_dncn,
    e.gst_adjust AS rounding_dncn_gst,
    b.gst_tax_code,
    0 AS var_total_disc,
    name_reg,doc_name_reg,reg_no,gst_no,tax_code,add1,add2,add3,
    IF(in_kind=1,'Stock In-Kind Net','GRN Net Amount') AS total_net_desc,postby AS approved_by,a.postdatetime AS approved_at,
    CONCAT('Tel: ',tel,'    Fax: ',fax) AS contact_sup

    FROM backend.grmain a

    INNER JOIN backend.trans_surcharge_discount b
    ON a.refno=b.refno

    INNER JOIN backend.grmain_dncn e
    ON a.refno=e.refno

    INNER JOIN backend.supcus sc
    ON IF(transtype IN ('IVS','IVN'),e.ap_sup_code,a.CODE)=sc.CODE

    INNER JOIN
    (SELECT a.refno,group_code,b.total AS pototal,porefno FROM backend.grchild a

    INNER JOIN backend.pomain b
    ON a.porefno=b.refno

    LEFT JOIN 
    backend.set_group_dept e
    ON a.dept=e.dept_code
    WHERE a.refno=%s
    GROUP BY refno) c
    ON a.refno=c.refno

    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON a.location=d.CODE

    WHERE a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND transtype='IVN' AND build_into_cost=0 AND value_factor>0) a

    LEFT JOIN

    (SELECT sort,refno,SUM(gst_zero) AS gst_zero,SUM(gst_std) AS gst_std FROM 

    (SELECT '3' AS sort,a.refno,ROUND(SUM(rebate_value),2) AS gst_zero,0 AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_rebate_amt=0 AND a.refno=%s AND rebate_value<>0
    GROUP BY refno

    UNION ALL

    SELECT '3' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(rebate_value),2) AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_rebate_amt<>0 AND a.refno=%s AND rebate_value<>0
    GROUP BY refno

    UNION ALL

    SELECT '1' AS sort,a.refno,ROUND(SUM(variance_qty),2) AS gst_zero,0 AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_var_qty=0 AND a.refno=%s AND variance_qty<>0
    GROUP BY refno

    UNION ALL

    SELECT '1' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(variance_qty),2) AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_var_qty<>0 AND a.refno=%s AND variance_qty<>0
    GROUP BY refno

    UNION ALL

    SELECT '2' AS sort,a.refno,ROUND(SUM(variance_cost),2) AS gst_zero,0 AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_var_cost=0 AND a.refno=%s AND variance_cost<>0
    GROUP BY refno

    UNION ALL

    SELECT '2' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(variance_cost),2) AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_var_cost<>0 AND a.refno=%s AND variance_cost<>0
    GROUP BY refno

    UNION ALL

    SELECT '6' AS sort,a.refno,ROUND(SUM(ABS(value_calculated)/**value_factor*/),2) AS gst_zero,0 AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt=0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=0 AND value_factor<0
    GROUP BY refno

    UNION ALL

    SELECT '6' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(ABS(value_calculated)/**value_factor*/),2) AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt<>0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=0 AND value_factor<0
    GROUP BY refno
    /**value_factor*/
    UNION ALL

    SELECT '5' AS sort,a.refno,ROUND(SUM(ABS(value_calculated)/**value_factor*/),2) AS gst_zero,0 AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt=0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=1 AND value_factor<0
    GROUP BY refno

    UNION ALL/**value_factor*/

    SELECT '5' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(ABS(value_calculated)/**value_factor*/),2) AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt<>0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=1 AND value_factor<0
    GROUP BY refno

    UNION ALL

    SELECT '7' AS sort,a.refno,ROUND(SUM(value_calculated/**value_factor*/),2) AS gst_zero,0 AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt=0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=1 AND value_factor>0
    GROUP BY refno

    UNION ALL

    SELECT '7' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(value_calculated/**value_factor*/),2) AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt<>0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=1 AND value_factor>0
    GROUP BY refno

    UNION ALL

    SELECT '8' AS sort,a.refno,ROUND(SUM(value_calculated/**value_factor*/),2) AS gst_zero,0 AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt=0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=0 AND value_factor>0
    GROUP BY refno

    UNION ALL

    SELECT '8' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(value_calculated/**value_factor*/),2) AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt<>0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=0 AND value_factor>0
    GROUP BY refno) a

    GROUP BY sort) b

    ON a.refno=b.refno AND a.sort=b.sort

    ORDER BY sort,sort1,groupno,pricetype,description,description_1,reason
    """
    result2 = panda.raw_query(querystr, [
        search_refno, search_refno, search_refno, search_refno, search_refno,
        search_refno, search_refno, search_refno, search_refno, search_refno,
        search_refno, search_refno, search_refno, search_refno, search_refno,
        search_refno, search_refno, search_refno, search_refno, search_refno,
        search_refno, search_refno, search_refno, search_refno, search_refno,
        search_refno, search_refno, search_refno, search_refno, search_refno,
        search_refno, search_refno, search_refno, search_refno
    ])
    result["query2"] = result2

    querystr = """
    SELECT varianceamt,CONCAT(a.refno,'-',transtype) AS refno_grda,
    CONCAT(a.refno,IF(b.refno2='' OR b.refno2 IS NULL,'',CONCAT(' / ',b.refno2))) AS refno2,
    IF(transtype='GQV','1','9') AS sort 
    FROM backend.grmain a
    LEFT JOIN backend.grmain_dncn b
    ON a.refno=b.refno
    WHERE a.refno=%s
    ORDER BY sort,refno_grda
    """
    result3 = panda.raw_query(querystr, [search_refno])
    result["query3"] = result3

    # querystr="""

    # """

    # result4=panda.raw_query(querystr,[search_refno,search_refno,search_refno,search_refno,search_refno,search_refno,search_refno,search_refno,search_refno])
    # result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)


# report GRN


@api_view(['GET'])
def report_GrSupplierGQV(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT a.*,b.* FROM

    (SELECT CONCAT(IF(transtype IN ('IVS','IVN'),ap_sup_code,a.CODE),' - ',
    IF(transtype IN ('IVS','IVN'),c.name,a.NAME)) AS supplier,
    tel,fax,a.term,location,a.refno,grdate,cross_ref,
    IF(in_kind=0,subtotal1,0) AS subtotal1,discount1 * -1 AS discount1,subtotal2,discount2,total,issuestamp,receivedby AS issuedby,
    postdatetime,postby,postby AS approvedby,a.laststamp,
    a.remark,
    IF(discount1type=1,'%%','$') AS discount1type,IF(discount2type=1,'%%','$') AS discount2type,
    contact,add1,add2,add3,city,state,postcode,country,

    IF(ibt=1,IF(ibt_gst=0,'Issued to Inter Branch Outlet','Issued to Inter Branch Outlet'),
    IF(ibt=2,IF(ibt_gst=0,'Issued to Inter Company Supplier','Issued to Inter Company Supplier'),
    IF(a.tax_code_purchase='NR','Issued to Supplier',IF(e.gst_tax_rate=0,
    'Issued to Supplier','Issued to Supplier')))) AS title_gst,

    IF(in_kind=1,'Stock In-Kind Net','GRN Net Amount') AS total_net_desc,postby AS approved_by,postdatetime AS approved_at,
    CONCAT('Tel: ',tel,'    Fax: ',fax) AS contact_sup,
    CONCAT(a.location,' - ',d.description) AS loc_desc,
    CONCAT('Co Reg No: ',reg_no,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no,
    IF((SELECT COUNT(DISTINCT(gst_tax_code)) AS gst_count FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE a.refno=%s
    GROUP BY a.refno)=1,CONCAT('    Tax Code: ',tax_code),'')))) reg_sup,
    invno,dono,
    CONCAT('Inv ',
    invno,'   DO ',dono,'   Date ',DATE_FORMAT(docdate,'%%d/%%m/%%y')) AS grdn_desc,
    IF(a.billstatus=1,'','Document Not Posted') AS chk_1,
    IF(transtype IN ('IVS','IVN'),c.name_reg,doc_name_reg) AS doc_name_reg,

    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Debit Note issued by'))) AS title_grda,

    IF(ibt=1,'IBT Branch Copy',IF(ibt=2,'Inter Co Supplier Copy','Supplier Copy')) AS title_supcopy

    FROM backend.grmain a

    INNER JOIN backend.grmain_dncn b
    ON a.refno=b.refno

    INNER JOIN backend.supcus c
    ON IF(transtype IN ('IVS','IVN'),b.ap_sup_code,a.CODE)=c.CODE

    INNER JOIN backend.location d
    ON a.location=d.CODE

    LEFT JOIN backend.set_gst_table e
    ON a.tax_code_purchase=e.gst_tax_code

    WHERE a.refno=%s AND /*billstatus=1 AND*/ TYPE='s') a

    INNER JOIN

    (SELECT /*IF(remark IS NULL OR remark='',IF(branch_name ='' OR branch_name IS NULL,companyname,branch_name),remark)*/
    IF(branch_name='' OR branch_name IS NULL,companyname,branch_name) AS companyname,
    (SELECT grnremark1 FROM backend.xsetup) AS grnremark1,
    (SELECT grnremark2 FROM backend.xsetup) AS grnremark2,
    (SELECT grnremark3 FROM backend.xsetup) AS grnremark3,
    IF(branch_add='' OR branch_add IS NULL,address1,'') AS address1,
    IF(branch_add='' OR branch_add IS NULL,address2,'') AS address2,
    IF(branch_add='' OR branch_add IS NULL,address3,'') AS address3,
    IF(branch_add='' OR branch_add IS NULL,CONCAT('Tel: ',tel,'    Fax: ',fax),CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax)) AS contactnumber,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,
    CONCAT('Co Reg No: ',IF(reg_no='' OR reg_no IS NULL,comp_reg_no,reg_no),IF(branch_gst='' OR branch_gst IS NULL,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no)),
    CONCAT('    GST Reg No: ',branch_gst))) reg_no,
    a.refno 
    FROM backend.grmain a

    INNER JOIN backend.companyprofile

    LEFT JOIN 
    (SELECT reg_no,gst_no AS branch_gst,name_reg,a.CODE AS scode,branch_add,branch_name,branch_tel,branch_fax FROM backend.grmain a
    INNER JOIN backend.cp_set_branch b
    ON a.loc_group=b.branch_code
    INNER JOIN backend.supcus c
    ON b.set_supplier_code=c.CODE
    WHERE refno=%s) b
    ON a.CODE=b.scode

    WHERE a.refno=%s) b

    ON a.refno=b.refno
    group by a.refno

    """

    result = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno])
    result = {"query1": result}

    querystr = """
    SELECT a.*,b.gst_zero,gst_std,
    IF(pricetype='RTV','',barcode1) AS barcode,
    IF(LENGTH(MID(gst_tax_total,POSITION('.' IN gst_tax_total)+1,10))<=2,FORMAT(gst_tax_total,2),
    FORMAT(gst_tax_total,4)) AS gst_tax_total_1,
    'Total Amount Exclude Tax' AS title7,
    ROUND(variance_amt-var_total_disc+0.000001,2) AS total_gross

    FROM

    (
    SELECT '1' AS sort,'1' AS sort1,a.refno,groupno,line,itemcode,description,qty,inv_qty,inv_netunitprice,inv_totalprice,
    IF(pricetype='FOC' AND inv_netunitprice=0,CONCAT('PO Qty: ',IF(MOD(poqty_expected,1)=0,ROUND(poqty_expected),ROUND(poqty_expected,1))),'') AS pricetype_vendor,
    grdate,CONCAT(b.CODE,'-',b.NAME) AS supplier,
    ROUND(pounitprice,4) AS pounitprice,totalprice AS invactcost,
    netunitprice,

    ROUND(ROUND(variance_qty,2)/ROUND(inv_qty - qty,4),4) AS factor,

    /* amend on 2020-10-23 and change to above due to target case TBPGR20100305 
    ROUND(variance_qty/(poqty_expected-qty),4) AS factor,*/
    pototalprice AS pototal,
    invno,dono,
    IF(pricetype='RTV','Item Not in PO',porefno) AS porefno,

    poqty,barcode AS barcode1,articleno,packsize,b.remark,loc_desc AS location,
    #IF(MOD(poqty_expected-qty,1)=0,poqty_expected-qty,ROUND(poqty_expected-qty,2)) AS qtyvar,
    IF(pay_by_invoice = 0,
    IF(MOD(poqty_expected-qty,1)=0,poqty_expected-qty,ROUND(poqty_expected-qty,2)),
    ROUND(inv_qty - qty,4))
    AS qtyvar,
    IF(variance_qty>0,'x','') AS chk1,'' AS chk2,
    ROUND(variance_qty,2) AS variance_amt,IF(pricetype='FOC','FOC','') AS pricetype,
    receivedby,
    IF(reason='' OR reason IS NULL,IF(pricetype='foc','FOC Short Supplied',
    IF(pricetype='RTV','Wrong Item','Qty Short Supplied')),reason) AS reason,
    group_code,postby,
    CONCAT(b.refno,'-',IF(transtype='ghv','IAV',transtype)) AS refno_dn,
    'Goods Received Difference Advice' AS title1,
    'Quantity Short Supplied' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Unit Price After Tax' AS title3,
    'Quantity' AS title4,
    'Unit Price After Discount' AS title5,
    # amended on 2020-10-23 'Unit Price Exclude Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(b.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',b.postby)) AS posted_on,
    CONCAT('Debit Note - Goods Received Difference Advice for ','Quantity Short Supplied') title_gst,
    CONCAT('Important Note : This Debit Advice is to notify your Company that qty received by us does not tallied with the qty specified in your Tax Invoice No ',invno,
    '.  Kindly issued us a credit note within 7 days from the date hereof failure which we will not proceed with payment of this invoice.') AS grdn_note,
    IF(a.gst_tax_rate=0,'Z','S') AS gst_unit_code,
    ROUND(gst_var_qty/IF(MOD(poqty_expected-qty,1)=0,poqty_expected-qty,ROUND(poqty_expected-qty,2)),4) AS gst_unit_tax,
    ROUND((variance_qty+gst_var_qty)/IF(MOD(poqty_expected-qty,1)=0,poqty_expected-qty,ROUND(poqty_expected-qty,2)),4) AS gst_unit_cost,
    ROUND((variance_qty+gst_var_qty),2) AS gst_unit_total,
    gst_var_qty AS gst_tax_total,
    ROUND(variance_qty+ROUND(gst_var_qty,4),2) AS gst_amt_total,
    transtype,'' AS title_inv,
    'GRDA Refno' AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',b.refno) AS refno_barcode,
    IF(tax_invoice=1,c.refno2,'') AS refno_2,

    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Debit Note issued by')))) AS title_grda,

    CONCAT('Supplier CN No: ',IF(c.sup_cn_no IS NULL,'',c.sup_cn_no)) AS sup_cn_no,
    CONCAT('CN Date: ',IF(c.sup_cn_date IS NULL,'',DATE_FORMAT(c.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    c.rounding_adj AS rounding_dncn,
    c.gst_adjust AS rounding_dncn_gst,
    a.gst_tax_code,
    ROUND(hcost_iv-hcost_gr+0.000001,2)*-1 AS var_total_disc

    FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    INNER JOIN backend.grmain_dncn c
    ON a.refno=c.refno
    LEFT JOIN backend.set_group_dept e
    ON a.dept=e.dept_code
    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON b.location=d.CODE
    WHERE a.refno=%s AND transtype='gqv'
    AND IF(pricetype='foc',qty<>poqty_expected,inv_qty<>qty)
    /* amend on 180421 due to everrise case 4mg1841343 IF(pricetype<>'foc',variance_qty<>0,qty<>poqty_expected) */


    UNION ALL

    SELECT '2' AS sort,'2' AS sort1,a.refno,groupno,line,itemcode,description,qty,inv_qty,inv_netunitprice,inv_totalprice,
    IF(pricetype='FOC' AND inv_netunitprice=0,pricetype,'') AS pricetype_vendor,grdate,CONCAT(b.CODE,'-',b.NAME) AS supplier,
    ROUND(pounitprice,4) AS pounitprice,totalprice AS invactcost,
    netunitprice,ROUND(variance_cost/inv_qty,4) AS factor,pototalprice AS pototal,
    invno,dono,porefno,poqty,barcode AS barcode1,articleno,packsize,b.remark,loc_desc AS location,inv_qty AS qtyvar,
    '' AS chk1,IF(variance_cost>0,'x','') AS chk2,
    ROUND(variance_cost,2) AS variance_amt,IF(pricetype='FOC','FOC','') AS pricetype,
    receivedby,'Price Overcharged' AS reason,group_code,postby,
    CONCAT(b.refno,'-','IAV') AS refno_dn,'Goods Received Difference Advice' AS title1,'Price Overcharged' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Unit Price After Tax' AS title3,'Quantity' AS title4,'Unit Price Before Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(b.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',b.postby)) AS posted_on,
    CONCAT('Debit Note - Goods Received Difference Advice for ','Price Overcharged') title_gst,
    CONCAT('Important Note : This Debit Advice is to notify your Company that the price charged in your Tax Invoice No ',invno,
    ' is higher than our PO Price.  Kindly issued us a credit note within 7 days from the date hereof failure which we will not proceed with payment of this invoice.') AS grdn_note,
    IF(a.gst_tax_rate=0,'Z','S') AS gst_unit_code,
    ROUND(gst_var_cost/inv_qty,4) AS gst_unit_tax,
    ROUND((variance_cost+gst_var_cost)/inv_qty,4) AS gst_unit_cost,
    ROUND((variance_cost+gst_var_cost),2) AS gst_unit_total,
    gst_var_cost AS gst_tax_total,
    ROUND(variance_cost+ROUND(gst_var_cost,4),2) AS gst_amt_total,
    transtype,'' AS title_inv,
    'GRDA Refno' AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',b.refno) AS refno_barcode,
    IF(tax_invoice=1,c.refno2,'') AS refno_2,
    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Debit Note issued by')))) AS title_grda,
    CONCAT('Supplier CN No: ',IF(c.sup_cn_no IS NULL,'',c.sup_cn_no)) AS sup_cn_no,
    CONCAT('CN Date: ',IF(c.sup_cn_date IS NULL,'',DATE_FORMAT(c.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    c.rounding_adj AS rounding_dncn,
    c.gst_adjust AS rounding_dncn_gst,
    a.gst_tax_code,
    ROUND(hcost_iv+0.000001,2)*-1 AS var_total_disc


    FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    INNER JOIN backend.grmain_dncn c
    ON a.refno=c.refno
    LEFT JOIN backend.set_group_dept e
    ON a.dept=e.dept_code
    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON b.location=d.CODE
    WHERE a.refno=%s AND variance_cost<>0 AND transtype='iav'


    UNION ALL 

    SELECT '3' AS sort,IF(rebate_value=0,'4','3') AS sort1,a.refno,a.groupno,a.line,itemcode,description,qty,inv_qty,inv_netunitprice,inv_totalprice,
    IF(pricetype='FOC' AND inv_netunitprice=0,pricetype,'') AS pricetype_vendor,grdate,CONCAT(b.CODE,'-',b.NAME) AS supplier,
    ROUND(pounitprice,4) AS pounitprice,totalprice AS invactcost,
    netunitprice,rebate_value AS factor,pototalprice AS pototal,
    invno,dono,porefno,poqty,barcode AS barcode1,articleno,packsize,b.remark,loc_desc AS location,1 AS qtyvar,
    '' AS chk1,'' AS chk2,
    ROUND(rebate_value,2) AS variance_amt,IF(pricetype='FOC','FOC','') AS pricetype,
    receivedby,IF(rebate_value=0,'','Rebate Incentive') AS reason,group_code,postby,
    CONCAT(b.refno,'-','GRV') AS refno_dn,'PO/GRN Debit Advice' AS title1,'By Invoice Item' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Rebate Amt After Tax' AS title3,'Quantity' AS title4,'Rebate Amt Before Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(b.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',b.postby)) AS posted_on,

    IF(tax_invoice=1,'Tax Invoice',
    CONCAT('PO/GRN Debit Note for ','Rebate Incentive')) title_gst,

    IF(tax_invoice=1,'',
    CONCAT('Important Note : This Debit Advice is to notify your Company that your company has agreed to issue a Rebate CN for the above item purchased.  Kindly issued us a credit note within 7 days from the date hereof failure which we will not proceed with payment of this invoice.'))
    AS grdn_note,

    IF(a.gst_tax_rate=0,'Z','S') AS gst_unit_code,
    ROUND(gst_rebate_amt,2) AS gst_unit_tax,
    ROUND((rebate_value+gst_rebate_amt),2) AS gst_unit_cost,
    ROUND((rebate_value+gst_rebate_amt),2) AS gst_unit_total,
    gst_rebate_amt AS gst_tax_total,
    ROUND(rebate_value+ROUND(gst_rebate_amt,4),2) AS gst_amt_total,
    transtype,
    IF(tax_invoice=1,'Rebate Incentive','') AS title_inv,
    IF(tax_invoice=1,'Refno #1','GRDN Refno') AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',b.refno) AS refno_barcode,
    IF(tax_invoice=1,h.refno2,'') AS refno_2,
    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Debit Note issued by')))) AS title_grda,
    CONCAT('Supplier CN No: ',IF(h.sup_cn_no IS NULL,'',h.sup_cn_no)) AS sup_cn_no,
    CONCAT('CN Date: ',IF(h.sup_cn_date IS NULL,'',DATE_FORMAT(h.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    h.rounding_adj AS rounding_dncn,
    h.gst_adjust AS rounding_dncn_gst,
    a.gst_tax_code,
    ROUND(hcost_iv+0.000001,2)*-1 AS var_total_disc

    FROM backend.grchild a

    INNER JOIN backend.grmain b
    ON a.refno=b.refno

    INNER JOIN backend.grmain_dncn h
    ON b.refno=h.refno

    INNER JOIN 
    (SELECT a.refno,a.groupno,IF(a.groupno=0,a.line,b.line) AS line1,b.line AS line FROM 
    (SELECT refno,groupno,line FROM backend.grchild 
    WHERE rebate_value<>0 AND refno=%s
    GROUP BY groupno) a
    INNER JOIN backend.grchild b
    ON a.refno=b.refno AND a.groupno=b.groupno
    WHERE IF(b.groupno=0,rebate_value<>0,rebate_value>=0)
    GROUP BY groupno,line) c
    ON a.refno=c.refno AND a.line=c.line

    LEFT JOIN backend.set_group_dept e
    ON a.dept=e.dept_code

    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON b.location=d.CODE

    WHERE a.refno=%s AND transtype='GRV'

    UNION ALL

    SELECT '6' AS sort,'5' AS sort1,a.refno,0 AS groupno,0 AS line,'' AS itemcode,
    CONCAT(code_type,' ',
    IF(surcharge_disc_type='%%',CONCAT(surcharge_disc_value,surcharge_disc_type),
    CONCAT(surcharge_disc_type,surcharge_disc_value)),' - by Debit Note') AS description,
    0 AS qty,0 AS inv_qty,0 AS inv_netunitprice,invnetamt_vendor AS inv_totalprice,
    '' AS pricetype_vendor,grdate,CONCAT(a.CODE,' - ',a.NAME) AS supplier,
    0 AS pounitprice,a.total AS invactcost,
    0 AS netunitprice,ROUND(ABS(value_calculated)/**value_factor*/,2) AS factor,pototal,
    invno,dono,porefno,0 AS poqty,'' AS barcode1,'' AS articleno,0 AS packsize,a.remark,
    loc_desc AS location,1 AS qtyvar,
    '' AS chk1,'' AS chk2,ROUND(ABS(value_calculated)/**value_factor*/,2) AS variance_amt,'' AS pricetype,
    receivedby,IF(share_cost=0,'Discount Income','Reduce Purchase Cost') AS reason,group_code,postby,
    CONCAT(a.refno,'-','GDV') AS refno_dn,'PO/GRN Debit Note' AS title1,'By Total Invoice' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Amount After Tax' AS title3,'Quantity' AS title4,'Amount Debit Before Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(a.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',a.postby)) AS posted_on,

    IF(tax_invoice=1,'Tax Invoice',
    CONCAT('PO/GRN Debit Note for ','Total Invoice (Discount Income)')) title_gst,

    IF(tax_invoice=1,'',
    CONCAT('Important Note : This Debit Advice is to notify your Company that your company has agreed to issue a Credit Note for our PO refno ',
    porefno,'.  Kindly issued us a credit note within 7 days from the date hereof failure which we will not proceed with payment of this invoice.'))
    AS grdn_note,

    IF(b.gst_amt=0,'Z','S') AS gst_unit_code,
    ROUND(b.gst_amt,2) AS gst_unit_tax,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_unit_cost,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_unit_total,
    ROUND(b.gst_amt,4) AS gst_tax_total,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_amt_total,
    transtype,
    IF(tax_invoice=1,'GRDN Discount Income','') AS title_inv,
    IF(tax_invoice=1,'Refno #1','GRDN Refno') AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',a.refno) AS refno_barcode,
    IF(tax_invoice=1,e.refno2,'') AS refno_2,
    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Debit Note issued by')))) AS title_grda,
    CONCAT('Supplier CN No: ',IF(e.sup_cn_no IS NULL,'',e.sup_cn_no)) AS sup_cn_no,
    CONCAT('CN Date: ',IF(e.sup_cn_date IS NULL,'',DATE_FORMAT(e.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    e.rounding_adj AS rounding_dncn,
    e.gst_adjust AS rounding_dncn_gst,
    b.gst_tax_code,
    0 AS var_total_disc

    FROM backend.grmain a

    INNER JOIN backend.trans_surcharge_discount b
    ON a.refno=b.refno

    INNER JOIN backend.grmain_dncn e
    ON a.refno=e.refno

    INNER JOIN
    (SELECT a.refno,group_code,b.total AS pototal,porefno FROM backend.grchild a

    INNER JOIN backend.pomain b
    ON a.porefno=b.refno

    LEFT JOIN 
    backend.set_group_dept e
    ON a.dept=e.dept_code
    WHERE a.refno=%s
    GROUP BY refno) c
    ON a.refno=c.refno

    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON a.location=d.CODE

    WHERE a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND transtype='gdv' AND build_into_cost=0 AND value_factor<0


    UNION ALL

    SELECT '5' AS sort,'6' AS sort1,a.refno,0 AS groupno,0 AS line,'' AS itemcode,
    CONCAT(code_type,' ',
    IF(surcharge_disc_type='%%',CONCAT(surcharge_disc_value,surcharge_disc_type),
    CONCAT(surcharge_disc_type,surcharge_disc_value)),' - by Debit Note') AS description,
    0 AS qty,0 AS inv_qty,0 AS inv_netunitprice,invnetamt_vendor AS inv_totalprice,
    '' AS pricetype_vendor,grdate,CONCAT(a.CODE,' - ',a.NAME) AS supplier,
    0 AS pounitprice,a.total AS invactcost,
    0 AS netunitprice,
    ROUND(ABS(value_calculated),2) AS factor,

    /*ROUND(value_calculated/* amended on 16-08-03 due to tf bergr16061826 *value_factor,2) AS factor, - amended on 16-08-17 due to KMNGR16080234*/
    pototal,
    invno,dono,porefno,0 AS poqty,'' AS barcode1,'' AS articleno,0 AS packsize,a.remark,
    loc_desc AS location,1 AS qtyvar,
    '' AS chk1,'' AS chk2,ROUND(ABS(value_calculated)/**value_factor*/,2) AS variance_amt,'' AS pricetype,
    receivedby,IF(share_cost=0,'Discount Income','Reduce Purchase Cost') AS reason,group_code,postby,
    CONCAT(a.refno,'-','GDS') AS refno_dn,'PO/GRN Debit Note' AS title1,'By Total Invoice' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Amount After Tax' AS title3,'Quantity' AS title4,'Amount Debit Before Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(a.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',a.postby)) AS posted_on,

    IF(tax_invoice=1,'Tax Invoice',
    CONCAT('PO/GRN Debit Note for ','Total Invoice (Reduce Purchase Cost)')) title_gst,

    IF(tax_invoice=1,'',
    CONCAT('Important Note : This Debit Advice is to notify your Company that your company has agreed to issue a Credit Note for our PO refno ',
    porefno,'.  Kindly issued us a credit note within 7 days from the date hereof failure which we will not proceed with payment of this invoice.'))
    AS grdn_note,

    IF(b.gst_amt=0,'Z','S') AS gst_unit_code,
    ROUND(b.gst_amt,2) AS gst_unit_tax,
    ROUND((ABS(value_calculated)+ROUND(b.gst_amt,2)),2) AS gst_unit_cost,
    ROUND((ABS(value_calculated)+ROUND(b.gst_amt,2)),2) AS gst_unit_total,
    ROUND(b.gst_amt,4) AS gst_tax_total,
    ROUND((ABS(value_calculated)+ROUND(b.gst_amt,2)),2) AS gst_amt_total,
    transtype,
    IF(tax_invoice=1,'GRDN Purchase Cost Reduction','') AS title_inv,
    IF(tax_invoice=1,'Refno #1','GRDA Refno') AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',a.refno) AS refno_barcode,
    IF(tax_invoice=1,e.refno2,'') AS refno_2,
    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Debit Note issued by')))) AS title_grda,
    CONCAT('Supplier CN No: ',IF(e.sup_cn_no IS NULL,'',e.sup_cn_no)) AS sup_cn_no,
    CONCAT('CN Date: ',IF(e.sup_cn_date IS NULL,'',DATE_FORMAT(e.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    e.rounding_adj AS rounding_dncn,
    e.gst_adjust AS rounding_dncn_gst,
    b.gst_tax_code,
    0 AS var_total_disc

    FROM backend.grmain a

    INNER JOIN backend.trans_surcharge_discount b
    ON a.refno=b.refno

    INNER JOIN backend.grmain_dncn e
    ON a.refno=e.refno

    INNER JOIN
    (SELECT a.refno,group_code,b.total AS pototal,porefno FROM backend.grchild a

    INNER JOIN backend.pomain b
    ON a.porefno=b.refno

    LEFT JOIN 
    backend.set_group_dept e
    ON a.dept=e.dept_code
    WHERE a.refno=%s
    GROUP BY refno) c
    ON a.refno=c.refno

    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON a.location=d.CODE

    WHERE a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND transtype='gds' AND build_into_cost=1 AND value_factor<0

    UNION ALL

    SELECT '7' AS sort,'7' AS sort1,a.refno,0 AS groupno,0 AS line,'' AS itemcode,
    CONCAT(code_type,' ',
    IF(surcharge_disc_type='%%',CONCAT(surcharge_disc_value,surcharge_disc_type),
    CONCAT(surcharge_disc_type,surcharge_disc_value)),' - by Credit Note') AS description,
    0 AS qty,0 AS inv_qty,0 AS inv_netunitprice,invnetamt_vendor AS inv_totalprice,
    '' AS pricetype_vendor,grdate,CONCAT(a.CODE,' - ',a.NAME) AS supplier,
    0 AS pounitprice,a.total AS invactcost,
    0 AS netunitprice,
    ROUND(ABS(value_calculated)/**value_factor*/,2) AS factor,
    pototal,
    invno,dono,porefno,0 AS poqty,'' AS barcode1,'' AS articleno,0 AS packsize,a.remark,
    loc_desc AS location,1 AS qtyvar,
    '' AS chk1,'' AS chk2,ROUND(ABS(value_calculated)/**value_factor*/,2) AS variance_amt,'' AS pricetype,
    receivedby,IF(share_cost=0,'Other Expenses','Purchase Cost') AS reason,group_code,postby,
    CONCAT(a.refno,'-','IVS') AS refno_dn,'PO/GRN Credit Note' AS title1,'By Total Invoice' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Amount After Tax' AS title3,'Quantity' AS title4,'Amount Credit Before Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(a.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',a.postby)) AS posted_on,

    IF(tax_invoice=1,'Tax Invoice',
    CONCAT('GRN Surcharge Credit Note for ','Debit Note or Invoice Received')) title_gst,

    IF(tax_invoice=1,'',
    CONCAT('Important Note : This Credit Advice is to notify your Company to issue a Tax Invoice or Debit Note for our Purchase ',
    porefno,'.  Kindly issued us a Tax Invoice or Debit Note note within 7 days from the date hereof failure which we will not proceed with payment.'))
    AS grdn_note,

    IF(b.gst_amt=0,'Z','S') AS gst_unit_code,
    ROUND(b.gst_amt,2) AS gst_unit_tax,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_unit_cost,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_unit_total,
    ROUND(b.gst_amt,4) AS gst_tax_total,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_amt_total,
    transtype,
    IF(tax_invoice=1,'GRCN Purchase Cost','') AS title_inv,
    IF(tax_invoice=1,'Refno #1','GRCN Refno') AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',a.refno) AS refno_barcode,
    IF(tax_invoice=1,e.refno2,'') AS refno_2,
    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Credit Note issued by')))) AS title_grda,
    CONCAT('Supplier DN/Inv No: ',IF(e.sup_cn_no IS NULL,'',e.sup_cn_no)) AS sup_cn_no,
    CONCAT('DN/Inv Date: ',IF(e.sup_cn_date IS NULL,'',DATE_FORMAT(e.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    e.rounding_adj AS rounding_dncn,
    e.gst_adjust AS rounding_dncn_gst,
    b.gst_tax_code,
    0 AS var_total_disc

    FROM backend.grmain a

    INNER JOIN backend.trans_surcharge_discount b
    ON a.refno=b.refno

    INNER JOIN backend.grmain_dncn e
    ON a.refno=e.refno

    INNER JOIN
    (SELECT a.refno,group_code,b.total AS pototal,porefno FROM backend.grchild a

    INNER JOIN backend.pomain b
    ON a.porefno=b.refno

    LEFT JOIN 
    backend.set_group_dept e
    ON a.dept=e.dept_code
    WHERE a.refno=%s
    GROUP BY refno) c
    ON a.refno=c.refno

    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON a.location=d.CODE

    WHERE a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 
    AND transtype='ivs' AND build_into_cost=1 AND value_factor>0

    UNION ALL

    SELECT '8' AS sort,'8' AS sort1,a.refno,0 AS groupno,0 AS line,'' AS itemcode,
    CONCAT(code_type,' ',
    IF(surcharge_disc_type='%%',CONCAT(surcharge_disc_value,surcharge_disc_type),
    CONCAT(surcharge_disc_type,surcharge_disc_value)),' - by Credit Note') AS description,
    0 AS qty,0 AS inv_qty,0 AS inv_netunitprice,invnetamt_vendor AS inv_totalprice,
    '' AS pricetype_vendor,grdate,CONCAT(a.CODE,' - ',a.NAME) AS supplier,
    0 AS pounitprice,a.total AS invactcost,
    0 AS netunitprice,
    ROUND(ABS(value_calculated)/**value_factor*/,2) AS factor,
    pototal,
    invno,dono,porefno,0 AS poqty,'' AS barcode1,'' AS articleno,0 AS packsize,a.remark,
    loc_desc AS location,1 AS qtyvar,
    '' AS chk1,'' AS chk2,ROUND(ABS(value_calculated)/**value_factor*/,2) AS variance_amt,'' AS pricetype,
    receivedby,IF(share_cost=0,'Other Expenses','Purchase Cost') AS reason,group_code,postby,
    CONCAT(a.refno,'-','IVN') AS refno_dn,'PO/GRN Credit Note' AS title1,'By Total Invoice' AS title2,
    IF(billstatus=0,'Document Not Posted','Document Posted') AS doc_status,
    'Amount After Tax' AS title3,'Quantity' AS title4,'Amount Credit Before Tax' AS title5,
    IF(billstatus=0,'',CONCAT('Document posted on ',DATE_FORMAT(a.postdatetime,'%%d/%%m/%%y %%h:%%i:%%s'),' by ',a.postby)) AS posted_on,

    IF(tax_invoice=1,'Tax Invoice',
    CONCAT('GRN Surcharge Credit Note for ','Debit Note or Invoice Received')) title_gst,

    IF(tax_invoice=1,'',
    CONCAT('Important Note : This Credit Advice is to notify your Company to issue a Tax Invoice or Debit Note for our Purchase ',
    porefno,'.  Kindly issued us a Tax Invoice or Debit Note note within 7 days from the date hereof failure which we will not proceed with payment.'))
    AS grdn_note,

    IF(b.gst_amt=0,'Z','S') AS gst_unit_code,
    ROUND(b.gst_amt,2) AS gst_unit_tax,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_unit_cost,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_unit_total,
    ROUND(b.gst_amt,4) AS gst_tax_total,
    ROUND((ABS(value_calculated)/**value_factor*/+ROUND(b.gst_amt,2)),2) AS gst_amt_total,
    transtype,
    IF(tax_invoice=1,'GRCN Purchase Cost','') AS title_inv,
    IF(tax_invoice=1,'Refno #1','GRCN Refno') AS title_refno,
    IF(tax_invoice=1,'Refno #2','') AS title_refno_2,
    IF(tax_invoice=1,'',a.refno) AS refno_barcode,
    IF(tax_invoice=1,e.refno2,'') AS refno_2,
    IF(tax_invoice=1,'Tax Invoice issued by',
    IF(transtype IN ('GQV','IAV'),'Goods Received Difference Advice issued by',
    IF(transtype='GRV','Purchase Rebate Incentive Debit Advice issued by',
    IF(transtype IN ('IVS','IVN'),'Surcharge Credit Note issued by',
    'Goods Received Credit Note issued by')))) AS title_grda,
    CONCAT('Supplier DN/Inv No: ',IF(e.sup_cn_no IS NULL,'',e.sup_cn_no)) AS sup_cn_no,
    CONCAT('DN/Inv Date: ',IF(e.sup_cn_date IS NULL,'',DATE_FORMAT(e.sup_cn_date,'%%d/%%m/%%y'))) AS sup_cn_date,
    e.rounding_adj AS rounding_dncn,
    e.gst_adjust AS rounding_dncn_gst,
    b.gst_tax_code,
    0 AS var_total_disc


    FROM backend.grmain a

    INNER JOIN backend.trans_surcharge_discount b
    ON a.refno=b.refno

    INNER JOIN backend.grmain_dncn e
    ON a.refno=e.refno

    INNER JOIN
    (SELECT a.refno,group_code,b.total AS pototal,porefno FROM backend.grchild a

    INNER JOIN backend.pomain b
    ON a.porefno=b.refno

    LEFT JOIN 
    backend.set_group_dept e
    ON a.dept=e.dept_code
    WHERE a.refno=%s
    GROUP BY refno) c
    ON a.refno=c.refno

    LEFT JOIN 
    (SELECT b.CODE,CONCAT(b.CODE,' - ',c.description) AS loc_desc FROM backend.location b
    INNER JOIN backend.locationgroup c
    ON b.locgroup=c.CODE
    WHERE b.CODE=(SELECT location FROM backend.grmain WHERE refno=%s)
    GROUP BY b.CODE) d
    ON a.location=d.CODE

    WHERE a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND transtype='IVN' AND build_into_cost=0 AND value_factor>0) a

    LEFT JOIN

    (SELECT sort,refno,SUM(gst_zero) AS gst_zero,SUM(gst_std) AS gst_std FROM 

    (SELECT '3' AS sort,a.refno,ROUND(SUM(rebate_value),2) AS gst_zero,0 AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_rebate_amt=0 AND a.refno=%s AND rebate_value<>0
    GROUP BY refno

    UNION ALL

    SELECT '3' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(rebate_value),2) AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_rebate_amt<>0 AND a.refno=%s AND rebate_value<>0
    GROUP BY refno

    UNION ALL

    SELECT '1' AS sort,a.refno,ROUND(SUM(variance_qty),2) AS gst_zero,0 AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_var_qty=0 AND a.refno=%s AND variance_qty<>0
    GROUP BY refno

    UNION ALL

    SELECT '1' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(variance_qty),2) AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_var_qty<>0 AND a.refno=%s AND variance_qty<>0
    GROUP BY refno

    UNION ALL

    SELECT '2' AS sort,a.refno,ROUND(SUM(variance_cost),2) AS gst_zero,0 AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_var_cost=0 AND a.refno=%s AND variance_cost<>0
    GROUP BY refno

    UNION ALL

    SELECT '2' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(variance_cost),2) AS gst_std FROM backend.grchild a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_var_cost<>0 AND a.refno=%s AND variance_cost<>0
    GROUP BY refno

    UNION ALL

    SELECT '6' AS sort,a.refno,ROUND(SUM(ABS(value_calculated)/**value_factor*/),2) AS gst_zero,0 AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt=0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=0 AND value_factor<0
    GROUP BY refno

    UNION ALL

    SELECT '6' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(ABS(value_calculated)/**value_factor*/),2) AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt<>0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=0 AND value_factor<0
    GROUP BY refno
    /**value_factor*/
    UNION ALL

    SELECT '5' AS sort,a.refno,ROUND(SUM(ABS(value_calculated)/**value_factor*/),2) AS gst_zero,0 AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt=0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=1 AND value_factor<0
    GROUP BY refno

    UNION ALL/**value_factor*/

    SELECT '5' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(ABS(value_calculated)/**value_factor*/),2) AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt<>0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=1 AND value_factor<0
    GROUP BY refno

    UNION ALL

    SELECT '7' AS sort,a.refno,ROUND(SUM(value_calculated/**value_factor*/),2) AS gst_zero,0 AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt=0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=1 AND value_factor>0
    GROUP BY refno

    UNION ALL

    SELECT '7' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(value_calculated/**value_factor*/),2) AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt<>0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=1 AND value_factor>0
    GROUP BY refno

    UNION ALL

    SELECT '8' AS sort,a.refno,ROUND(SUM(value_calculated/**value_factor*/),2) AS gst_zero,0 AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt=0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=0 AND value_factor>0
    GROUP BY refno

    UNION ALL

    SELECT '8' AS sort,a.refno,0 AS gst_zero,ROUND(SUM(value_calculated/**value_factor*/),2) AS gst_std FROM backend.trans_surcharge_discount a
    INNER JOIN backend.grmain b
    ON a.refno=b.refno
    WHERE gst_amt<>0 AND a.refno=%s AND trans_type=IF(pay_by_invoice=0,'grn','grninv') AND dn=1 AND build_into_cost=0 AND value_factor>0
    GROUP BY refno) a

    GROUP BY sort) b

    ON a.refno=b.refno AND a.sort=b.sort

    ORDER BY sort,sort1,groupno,pricetype,description,reason;
    """
    result2 = panda.raw_query(querystr, [
        search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno,
        search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno,
        search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno])
    result["query2"] = result2

    querystr = """
    SELECT varianceamt,CONCAT(a.refno,'-',transtype) AS refno_grda,
    CONCAT(a.refno,IF(b.refno2='' OR b.refno2 IS NULL,'',CONCAT(' / ',b.refno2))) AS refno2,
    IF(transtype='GQV','1','9') AS sort 
    FROM backend.grmain a
    LEFT JOIN backend.grmain_dncn b
    ON a.refno=b.refno
    WHERE a.refno=%s 
    ORDER BY sort,refno_grda
    """
    result3 = panda.raw_query(querystr, [search_refno])
    result["query3"] = result3

    # querystr="""

    # """

    # result4=panda.raw_query(querystr,[search_refno,search_refno,search_refno,search_refno,search_refno,search_refno,search_refno,search_refno,search_refno])
    # result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)


# report PRDN
@api_view(['GET'])
def report_PurchaseReturnDN(request, search_refno):
    print(search_refno)

    querystr = """

    #5
    SELECT a.*,b.*,c.division FROM

    (SELECT /*CONCAT(a.CODE,' - ',a.NAME) AS supplier,*/
    CONCAT(a.CODE,IF(dn_doutlet_code='',CONCAT(' - ',a.NAME),CONCAT('    Customer Outlet  ',dn_doutlet_code))) AS supplier,
    location,
    refno,
    docdate,
    amount AS total,
    issuestamp,issuedby,
    IF(billstatus=0,'',DATE_FORMAT(postdatetime,'%%d/%%m/%%y %%H:%%i:%%s')) AS postdatetime,
    postby,a.laststamp,a.remark,
    c.add1,c.add2,c.add3,c.city,c.state,c.postcode,c.country,
    CONCAT(c.tel,IF(c.fax='' OR c.fax IS NULL,'',CONCAT('  Fax : ',c.fax))) AS contact,
    CONCAT('Doc Status : ',IF(billstatus=0,'Unpost','Posted')) AS doc_status,
    a.docno,a.pono,sup_cn_no,
    IF(sup_cn_no='' OR sup_cn_no IS NULL,'',DATE_FORMAT(sup_cn_date,'%%d/%%m/%%y %%a')) AS sup_cn_date,

    IF(ibt=1,'IBT CN No',
    IF(sctype='S','Supplier CN No','Customer CN No')) AS sup_cn_title,
    IF(ibt=1,'IBT CN Date',
    IF(sctype='S','Supplier CN Date','Customer CN Date')) AS sup_cn_date_title,

    IF(a.billstatus=1,'','XXX') AS chk,
    IF(a.billstatus=1,'','Document Not Posted') AS chk_1,


    IF(ibt=1,IF(sctype='s',CONCAT('Inter Branch Stock Return Outwards',IF(a.consign=0,' - Consignment','')),
    CONCAT('Inter Branch Stock Return Inwards',IF(a.consign=0,' - Consignment',''))),'') AS title_ibt,

    IF(ibt=0,IF(sctype='s',IF(a.consign=1,'Consignment Return Note to Supplier','Purchase Return Debit Note to Supplier'),
    IF(a.consign=1,'Debit Note to Customer - Consignment','Debit Note to Customer - Outright')),
    IF(ibt=2,IF(sctype='s',IF(a.consign=1,'Consignment Return Note to Supplier','Purchase Return Debit Note to Supplier'),
    IF(a.consign=1,'Debit Note to Customer - Consignment','Debit Note to Customer - Outright')),
    IF(a.consign=0,'DN - Inter Branch Transfer Outwards','Consignment Note DN - Inter Branch Tranfer Outwards'))) AS title,

    IF(billstatus=0,'Draft Copy','') AS draft,

    IF(ibt=0 AND sctype='s' AND a.consign=0,'Supplier Credit Note','') AS title_match_cn,

    /*IF(ibt=1,IF(ibt_gst=0,'Inter Branch Stock Transfer Outwards to','Inter Branch Stock Transfer Outwards with GST to'),
    IF(sctype='S',IF(ibt=2,IF(ibt_gst=0,'Debit to Inter Company Supplier','Debit to Inter Company Supplier with GST'),
    IF(a.Tax_code_purchase='NR','Debit to Non Registered GST Supplier',
    'Debit to Registered GST Supplier')),
    IF(ibt=2,IF(ibt_gst=0,'Debit to Inter Company Customer','Debit to Inter Company Customer with GST'),
    IF(a.tax_code_purchase='ES','Debit to Exempted Customer entitled to 0%% Tax',
    'Debit to Customer with GST')))) AS title_gst,*/

    IF(ibt=1,IF(ibt_gst=0,'Inter Branch Stock Transfer Outwards to','Inter Branch Stock Transfer Outwards to'),
    IF(sctype='S',IF(ibt=2,IF(ibt_gst=0,'Debit to Inter Company Supplier','Debit to Inter Company Supplier'),
    IF(a.Tax_code_purchase='NR','Debit to Supplier',
    'Debit to Supplier')),
    IF(ibt=2,IF(ibt_gst=0,'Debit to Inter Company Customer','Debit to Inter Company Customer'),
    IF(a.tax_code_purchase='ES','Debit to Customer',
    'Debit to Customer')))) AS title_gst,

    IF(ibt=1,'Inter Branch Transfer Outwards Note Issued By',
    IF(ibt=2,'Inter Company Debit Note Issued By',
    'Debit Note Issued Ny')) AS title_issue,

    CONCAT(a.location,' - ',f.description) AS loc_desc,

    CONCAT('Co Reg No: ',reg_no,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no,
    IF((SELECT COUNT(DISTINCT(gst_tax_code)) AS gst_count FROM backend.dbnotechild a
    INNER JOIN backend.dbnotemain b
    ON a.refno=b.refno
    WHERE a.refno=%s
    GROUP BY a.refno)=1,CONCAT('    Tax Code: ',tax_code_purchase),'')))) reg_sup,

    doc_name_reg,
    IF(ibt=1,'Transfer Note No','Debit Note No') AS title_invno,
    IF(ibt=1,'IBT Branch Copy',IF(sctype='s',IF(ibt=2,'Inter Co Supplier Copy','Suppier Copy'),IF(ibt='2','Inter Co Customer Copy','Customer Copy'))) AS title_supcopy,
    IF(sctype='S','Sup Code','Cus Code') AS title_supcode,
    subdeptcode



    FROM backend.dbnotemain a

    INNER JOIN 
    (SELECT * FROM backend.supcus WHERE
    TYPE=(SELECT sctype FROM backend.dbnotemain WHERE refno=%s)) c
    ON a.CODE=c.CODE

    INNER JOIN backend.location f
    ON a.location=f.CODE

    LEFT JOIN backend.set_gst_table g
    ON a.tax_code_purchase=g.gst_tax_code

    WHERE a.refno=%s) a

    INNER JOIN

    (SELECT /*IF(remark IS NULL OR remark='',IF(branch_name ='' OR branch_name IS NULL,companyname,branch_name),remark)*/
    IF(branch_name='' OR branch_name IS NULL,companyname,branch_name) AS companyname,
    (SELECT dnremark1 FROM backend.xsetup) AS dnremark1,
    (SELECT dnremark2 FROM backend.xsetup) AS dnremark2,
    (SELECT dnremark3 FROM backend.xsetup) AS dnremark3,
    IF(branch_add='' OR branch_add IS NULL,address1,'') AS address1,
    IF(branch_add='' OR branch_add IS NULL,address2,'') AS address2,
    IF(branch_add='' OR branch_add IS NULL,address3,'') AS address3,
    IF(branch_add='' OR branch_add IS NULL,CONCAT('Tel: ',tel,'    Fax: ',fax),CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax)) AS contactnumber,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,
    CONCAT('Co Reg No: ',IF(reg_no='' OR reg_no IS NULL,comp_reg_no,reg_no),IF(branch_gst='' OR branch_gst IS NULL,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no)),
    CONCAT('    GST Reg No: ',branch_gst))) reg_no,
    a.refno, 
    Branch_name
    FROM backend.dbnotemain a

    INNER JOIN backend.companyprofile

    LEFT JOIN 
    (SELECT a.refno,reg_no,gst_no AS branch_gst,name_reg,branch_add,branch_name,branch_tel,branch_fax 
    FROM backend.dbnotemain a
    INNER JOIN backend.cp_set_branch b
    ON a.locgroup=b.branch_code
    INNER JOIN backend.supcus c
    ON b.set_supplier_code=c.CODE
    WHERE refno=%s) b

    ON a.refno=b.refno

    WHERE a.refno=%s) b

    ON a.refno=b.refno

    LEFT JOIN
    (SELECT a.CODE,IF(c.group_code IS NULL,'Not Applicable',c.group_code) AS division FROM backend.subdept a
    INNER JOIN backend.department b
    ON a.mcode=b.CODE
    LEFT JOIN backend.set_group_dept c
    ON b.CODE=c.dept_code) c
    ON a.subdeptcode=c.CODE
    """

    result = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno, search_refno])
    result = {"query1": result}

    querystr = """
    #1

    SELECT itemcode,barcode,articleno,description,packsize,unitprice,
    unitprice AS netunitprice,qty,totalprice,IF(pricetype='foc','FOC','') AS pricetype,
    line,itemlink,a.refno,LOWER(um) AS um,subtotal1,

    IF(a.gst_tax_rate=0,'Z','S') AS gst_unit_code,
    ROUND(gst_tax_amount/qty,4) AS gst_unit_tax,

    ROUND(IF(surchg_disc_gst=0,unitprice+(gst_tax_amount/qty),((totalprice-surchg_disc_gst)+gst_tax_amount)/qty),4) AS gst_unit_cost,
    /*ROUND(IF(discvalue=0 AND surchg_value=0,unitprice+(gst_tax_amount/qty),((totalprice-discvalue)+gst_tax_amount)/qty),4) AS gst_unit_cost,*/
    gst_tax_amount AS gst_child_tax,
    ROUND((totalprice-surchg_disc_gst)+gst_tax_amount,2) AS gst_unit_total,
    /*ROUND((totalprice-discvalue)+gst_tax_amount,2) AS gst_unit_total,*/


    gst_tax_sum AS gst_main_tax,
    ROUND(amount+gst_tax_sum,2) AS gst_main_total,
    packsize AS ps,

    gst_tax_code,a.gst_tax_rate,gst_tax_amount,
    ROUND(surchg_disc_gst/qty,4) AS unit_disc_prorate,
    IF(surchg_disc_gst=0,unitprice,ROUND((totalprice-surchg_disc_gst)/qty,4)) AS unit_price_bfr_tax,
    ROUND(totalprice-surchg_disc_gst+0.000001,2) AS total_price_bfr_tax,

    /*ROUND(discvalue/qty,4) AS unit_disc_prorate,
    IF(discvalue=0 AND surchg_value=0,unitprice,ROUND((totalprice-discvalue)/qty,4)) AS unit_price_bfr_tax,
    ROUND(totalprice-discvalue+0.000001,2) AS total_price_bfr_tax,*/

    ori_inv_no,ori_inv_date,itemremark,reason

    FROM backend.dbnotechild a

    INNER JOIN backend.dbnotemain b
    ON a.refno=b.refno

    WHERE a.refno=%s
    ORDER BY line;


    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["query2"] = result2

    querystr = """
    #2
    SELECT refno,SUM(gst_zero) AS gst_zero,SUM(gst_std) AS gst_std FROM 

    (SELECT a.refno,SUM(totalprice-surchg_disc_gst) AS gst_zero,0 AS gst_std FROM backend.dbnotechild a
    INNER JOIN backend.dbnotemain b
    ON a.refno=b.refno
    WHERE gst_tax_amount=0 AND a.refno=%s
    GROUP BY refno

    UNION ALL

    SELECT a.refno,0 AS gst_zero,SUM(totalprice-surchg_disc_gst) AS gst_std FROM backend.dbnotechild a
    INNER JOIN backend.dbnotemain b
    ON a.refno=b.refno
    WHERE gst_tax_amount<>0 AND a.refno=%s
    GROUP BY refno) a

    GROUP BY refno;
    """
    result3 = panda.raw_query(querystr, [search_refno, search_refno])
    result["query3"] = result3

    querystr = """
    #7
    SELECT refno,sequence,
    CONCAT(CODE,' (',surcharge_disc_type,')') AS code_grn,surcharge_disc_value*value_factor AS value_grn,
    ROUND(value_calculated,2) AS value_calculated
    FROM backend.trans_surcharge_discount 
    WHERE refno=%s AND dn=0

    UNION ALL

    SELECT refno,'A1' AS sequence,'Total Include Surcharge/Disc' AS code_grn,0 AS value_grn,
    amount AS value_calculated FROM backend.dbnotemain
    WHERE refno=%s AND discount1<>0

    UNION ALL

    SELECT refno,'B1' AS sequence,'Item Tax Amount' AS code_grn,0 AS value_grn,
    ROUND(gst_tax_sum,2) AS value_calculated FROM backend.dbnotemain
    WHERE refno=%s AND gst_tax_sum<>0

    UNION ALL

    SELECT refno,'B2' AS sequence,'Surcharge Tax Amount' AS code_grn,0 AS value_grn,
    ROUND(surchg_tax_sum,2) AS value_calculated FROM backend.dbnotemain
    WHERE refno=%s AND surchg_tax_sum<>0

    UNION ALL

    SELECT refno,'C1' AS sequence,'GST Rounding Adjustment' AS code_grn,0 AS value_grn,
    ROUND(GST_adj,2) AS value_calculated FROM backend.dbnotemain
    WHERE refno=%s AND gst_adj<>0

    UNION ALL

    SELECT refno,'C2' AS sequence,'Bill Rounding Adjustment' AS code_grn,0 AS value_grn,
    ROUND(rounding_adj,2) AS value_calculated FROM backend.dbnotemain
    WHERE refno=%s AND rounding_adj<>0

    UNION ALL 

    SELECT refno,'D1' AS sequence,'Total Amount Include Tax' AS code_grn,0 AS value_grn,
    ROUND(amount+gst_tax_sum+surchg_tax_sum+gst_adj+rounding_adj,2) AS value_calculated FROM backend.dbnotemain
    WHERE refno=%s

    ORDER BY sequence    
    """

    result4 = panda.raw_query(querystr, [
                              search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno])
    result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)


# report PRCN


@api_view(['GET'])
def report_PurchaseReturnCN(request, search_refno):
    print(search_refno)

    querystr = """
    #5
    SELECT a.*,b.*,c.division FROM

    (SELECT /*CONCAT(a.CODE,' - ',a.NAME) AS supplier,*/
    CONCAT(a.CODE,IF(cn_doutlet_code='',CONCAT(' - ',a.NAME),CONCAT('    Customer Outlet  ',cn_doutlet_code))) AS supplier,
    CONCAT(a.CODE,IF(cn_doutlet_code='',CONCAT(' - ',a.NAME),CONCAT('    Customer Outlet  ',cn_doutlet_code))) AS customer,
    cn_salesman AS salesman,
    @euser AS USER,
    cn_amtasdesc AS Amtasdescription,
    location,
    refno,
    docdate,
    amount AS total,
    issuestamp,issuedby,
    IF(billstatus=0,'',DATE_FORMAT(postdatetime,'%%d/%%m/%%y %%H:%%i:%%s')) AS postdatetime,
    postby,a.laststamp,a.remark,
    IF(a.cn_dadd1='' OR a.cn_dadd1 IS NULL,a.cn_add1,a.cn_dadd1) AS add1,
    IF(a.cn_dadd1='' OR a.cn_dadd1 IS NULL,a.cn_add2,a.cn_dadd2) AS add2,
    IF(a.cn_dadd1='' OR a.cn_dadd1 IS NULL,a.cn_add3,a.cn_dadd3) AS add3,
    IF(a.cn_dadd1='' OR a.cn_dadd1 IS NULL,a.cn_add4,a.cn_dadd4) AS add4,
    c.city,c.state,c.postcode,c.country,
    CONCAT(c.tel,IF(c.fax='' OR c.fax IS NULL,'',CONCAT('  Fax : ',c.fax))) AS contact,
    CONCAT('Doc Status : ',IF(billstatus=0,'Unpost','Posted')) AS doc_status,
    a.docno,a.pono,sup_cn_no,
    IF(sup_cn_no='' OR sup_cn_no IS NULL,'',DATE_FORMAT(sup_cn_date,'%%d/%%m/%%y %%a')) AS sup_cn_date,

    IF(ibt=1,'IBT DN No',
    IF(sctype='S','Supplier DN No','Customer DN No')) AS sup_cn_title,
    IF(ibt=1,'IBT DN Date',IF(sctype='S','Supplier DN Date','Customer DN Date')) AS sup_cn_date_title,

    IF(a.billstatus=1,'','XXX') AS chk,
    IF(a.billstatus=1,'','Document Not Posted') AS chk_1,


    IF(ibt=0,IF(sctype='s',IF(a.consign=1,'Consignment Credit Note to Supplier','Purchase Return Credit Note to Supplier'),
    IF(a.consign=1,'Consignment Credit Note to Customer','Sales Return Credit Note to Customer')),
    IF(ibt=2,IF(sctype='s',IF(a.consign=1,'Consignment Credit Note to Supplier','Purchase Return Credit Note to Supplier'),
    IF(a.consign=1,'Consignment Credit Note to Customer','Sales Return Credit Note to Customer')),
    IF(a.consign=0,'CN - Inter Branch Transfer Inwards','Consignment Note CN - Inter Branch Tranfer Inwards'))) AS title,

    IF(billstatus=0,'Draft Copy','') AS draft,

    IF(ibt=0 AND sctype='s' AND a.consign=0,'Customer Debit Note','') AS title_match_cn,

    IF(ibt=1,IF(ibt_gst=0,'Inter Branch Stock Transfer Inwards from','Inter Branch Stock Transfer Inwards from'),
    IF(sctype='S',IF(ibt=2,IF(ibt_gst=0,'Credit to Inter Company Supplier','Credit to Inter Company Supplier'),
    IF(a.Tax_code_purchase='NR','Credit to Supplier',
    'Credit to Supplier')),
    IF(ibt=2,IF(ibt_gst=0,'Credit to Inter Company Customer','Credit to Inter Company Customer'),
    IF(a.tax_code_purchase='ES','Credit to Customer',
    'Credit to Customer')))) AS title_gst,

    IF(ibt=1,'Inter Branch Transfer Inwards Note Issued By',
    IF(ibt=2,'Inter Company Credit Note Issued By',
    'Credit Note Issued By')) AS title_issue,

    IF(ibt=1,'Inter Branch Transfer Inwards Note',
    IF(sctype='C','Sales Return Credit Note','Purchase Return Credit Note')) AS title_CN,

    CONCAT(a.location,' - ',f.description) AS loc_desc,

    CONCAT('Co Reg No: ',reg_no,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no,
    IF((SELECT COUNT(DISTINCT(gst_tax_code)) AS gst_count FROM backend.cnnotechild a
    INNER JOIN backend.cnnotemain b
    ON a.refno=b.refno
    WHERE a.refno=%s
    GROUP BY a.refno)=1,CONCAT('    Tax Code: ',tax_code_purchase),'')))) reg_sup,

    doc_name_reg,
    IF(ibt=1,'Transfer Note No','Credit Note No') AS title_invno,
    IF(ibt=1,'IBT Branch Copy',IF(sctype='s',IF(ibt=2,'Inter Co Supplier Copy','Suppier Copy'),IF(ibt='2','Inter Co Customer Copy','Customer Copy'))) AS title_supcopy,
    IF(sctype='S','Sup Code','Cus Code') AS title_supcode,
    subdeptcode,
    CONCAT(a.term, ' - ',b.description) AS termdesc,

    CONCAT(a.locgroup,IF(a.locgroup=a.location,'',CONCAT(' - ',a.location))) AS outlet_loc,

    IF(a.locgroup=a.location,'Outlet','Outlet (Location)') AS outlet_title


    FROM backend.cnnotemain a

    INNER JOIN 
    (SELECT * FROM backend.supcus WHERE
    TYPE=(SELECT sctype FROM backend.cnnotemain WHERE refno=%s)) c
    ON a.CODE=c.CODE

    INNER JOIN backend.location f
    ON a.location=f.CODE

    LEFT JOIN backend.set_gst_table g
    ON a.tax_code_purchase=g.gst_tax_code

    LEFT JOIN backend.pay_term b
    ON a.term=b.CODE

    WHERE a.refno=%s) a

    INNER JOIN

    (SELECT /*IF(remark IS NULL OR remark='',IF(branch_name ='' OR branch_name IS NULL,companyname,branch_name),remark)*/
    IF(branch_name='' OR branch_name IS NULL,companyname,branch_name) AS companyname,
    (SELECT cnremark1 FROM backend.xsetup) AS cnremark1,
    (SELECT cnremark2 FROM backend.xsetup) AS cnremark2,
    (SELECT cnremark3 FROM backend.xsetup) AS cnremark3,
    IF(branch_add='' OR branch_add IS NULL,address1,'') AS address1,
    IF(branch_add='' OR branch_add IS NULL,address2,'') AS address2,
    IF(branch_add='' OR branch_add IS NULL,address3,'') AS address3,
    IF(branch_add='' OR branch_add IS NULL,CONCAT('Tel: ',tel,'    Fax: ',fax),CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax)) AS contactnumber,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,
    CONCAT('Co Reg No: ',IF(reg_no='' OR reg_no IS NULL,comp_reg_no,reg_no),IF(branch_gst='' OR branch_gst IS NULL,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no)),
    CONCAT('    GST Reg No: ',branch_gst))) reg_no,
    a.refno, 
    Branch_name
    FROM backend.cnnotemain a

    INNER JOIN backend.companyprofile

    LEFT JOIN 
    (SELECT a.refno,reg_no,gst_no AS branch_gst,name_reg,branch_add,branch_name,branch_tel,branch_fax 
    FROM backend.cnnotemain a
    INNER JOIN backend.cp_set_branch b
    ON a.locgroup=b.branch_code
    INNER JOIN backend.supcus c
    ON b.set_supplier_code=c.CODE
    WHERE refno=%s) b

    ON a.refno=b.refno

    WHERE a.refno=%s) b

    ON a.refno=b.refno

    LEFT JOIN
    (SELECT a.CODE,IF(c.group_code IS NULL,'Not Applicable',c.group_code) AS division FROM backend.subdept a
    INNER JOIN backend.department b
    ON a.mcode=b.CODE
    LEFT JOIN backend.set_group_dept c
    ON b.CODE=c.dept_code) c
    ON a.subdeptcode=c.CODE

    """

    result = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno, search_refno])
    result = {"query1": result}

    querystr = """
    #1
    SELECT itemcode,barcode,articleno,description,packsize,unitprice,
    unitprice AS netunitprice,qty,totalprice,IF(pricetype='foc','FOC','') AS pricetype,
    line,itemlink,a.refno,LOWER(um) AS um,subtotal1,

    IF(a.gst_tax_rate=0,'Z','S') AS gst_unit_code,
    ROUND(gst_tax_amount/qty,4) AS gst_unit_tax,
    ROUND(IF(surchg_disc_gst=0,unitprice+(gst_tax_amount/qty),((totalprice-surchg_disc_gst)+gst_tax_amount)/qty),4) AS gst_unit_cost,
    gst_tax_amount AS gst_child_tax,
    ROUND((totalprice-surchg_disc_gst)+gst_tax_amount,2) AS gst_unit_total,
    gst_tax_sum AS gst_main_tax,
    ROUND(amount+gst_tax_sum,2) AS gst_main_total,
    packsize AS ps,

    gst_tax_code,a.gst_tax_rate,gst_tax_amount,
    ROUND(surchg_disc_gst/qty,4) AS unit_disc_prorate,
    IF(surchg_disc_gst=0,unitprice,ROUND((totalprice-surchg_disc_gst)/qty,4)) AS unit_price_bfr_tax,
    ROUND(totalprice-surchg_disc_gst+0.000001,2) AS total_price_bfr_tax,

    ori_inv_no,ori_inv_date,itemremark,reason

    FROM backend.cnnotechild a

    INNER JOIN backend.cnnotemain b
    ON a.refno=b.refno

    WHERE a.refno=%s
    ORDER BY line;
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["query2"] = result2

    querystr = """
    #2
    SELECT refno,SUM(gst_zero) AS gst_zero,SUM(gst_std) AS gst_std FROM 

    (SELECT a.refno,SUM(totalprice-surchg_disc_gst) AS gst_zero,0 AS gst_std FROM backend.cnnotechild a
    INNER JOIN backend.cnnotemain b
    ON a.refno=b.refno
    WHERE gst_tax_amount=0 AND a.refno=%s
    GROUP BY refno

    UNION ALL

    SELECT a.refno,0 AS gst_zero,SUM(totalprice-surchg_disc_gst) AS gst_std FROM backend.cnnotechild a
    INNER JOIN backend.cnnotemain b
    ON a.refno=b.refno
    WHERE gst_tax_amount<>0 AND a.refno=%s
    GROUP BY refno) a

    GROUP BY refno;
    """
    result3 = panda.raw_query(querystr, [search_refno, search_refno])
    result["query3"] = result3

    querystr = """
    #7
SELECT refno,sequence,
CONCAT(CODE,' (',surcharge_disc_type,')') AS code_grn,surcharge_disc_value*value_factor AS value_grn,
ROUND(value_calculated,2) AS value_calculated
FROM backend.trans_surcharge_discount 
WHERE refno=%s AND dn=0

UNION ALL

SELECT refno,'A1' AS sequence,'Total Include Surcharge/Disc' AS code_grn,0 AS value_grn,
amount AS value_calculated FROM backend.cnnotemain
WHERE refno=%s AND discount1<>0

UNION ALL

SELECT refno,'B1' AS sequence,'Item Tax Amount' AS code_grn,0 AS value_grn,
ROUND(gst_tax_sum,2) AS value_calculated FROM backend.cnnotemain
WHERE refno=%s AND gst_tax_sum<>0

UNION ALL

SELECT refno,'B2' AS sequence,'Surcharge Tax Amount' AS code_grn,0 AS value_grn,
ROUND(surchg_tax_sum,2) AS value_calculated FROM backend.cnnotemain
WHERE refno=%s AND surchg_tax_sum<>0

UNION ALL

SELECT refno,'C1' AS sequence,'GST Rounding Adjustment' AS code_grn,0 AS value_grn,
ROUND(GST_adj,2) AS value_calculated FROM backend.cnnotemain
WHERE refno=%s AND gst_adj<>0

UNION ALL

SELECT refno,'C2' AS sequence,'Bill Rounding Adjustment' AS code_grn,0 AS value_grn,
ROUND(rounding_adj,2) AS value_calculated FROM backend.cnnotemain
WHERE refno=%s AND rounding_adj<>0

UNION ALL

SELECT refno,'D1' AS sequence,'Total Amount Include Tax' AS code_grn,0 AS value_grn,
ROUND(amount+gst_tax_sum+surchg_tax_sum+gst_adj+rounding_adj,2) AS value_calculated FROM backend.cnnotemain
WHERE refno=%s

ORDER BY sequence
    """

    result4 = panda.raw_query(querystr, [
                              search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno])
    result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)


# report PDN
@api_view(['GET'])
def report_PurchaseDN(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT a.*,b.*,c.division FROM

    (SELECT CONCAT(a.CODE,' - ',a.NAME) AS supplier,
    location,
    refno,
    docdate,
    amount AS total,
    DATE_FORMAT(a.created_at,'%%d-%%m-%%Y %%H:%%i:%%s') AS issuestamp,
    a.created_by AS issuedby,
    IF(posted=0,'',DATE_FORMAT(posted_at,'%%d/%%m/%%y %%H:%%i:%%s')) AS postdatetime,
    posted_by AS postby,
    DATE_FORMAT(a.updated_at,'%%d-%%m-%%Y %%H:%%i:%%s') AS laststamp,a.remark,
    c.add1,c.add2,c.add3,c.city,c.state,c.postcode,c.country,
    CONCAT(c.tel,IF(c.fax='' OR c.fax IS NULL,'',CONCAT('  Fax : ',c.fax))) AS contact,
    CONCAT('Doc Status : ',IF(posted=0,'Unpost','Posted')) AS doc_status,
    a.docno,sup_cn_no,
    IF(sup_cn_no='' OR sup_cn_no IS NULL,'',DATE_FORMAT(sup_cn_date,'%%d/%%m/%%y %%a')) AS sup_cn_date,

    IF(ibt=1,IF(LEFT(trans_type,3) IN ('PCN','SCN'),'IBT DN No','IBT CN No'),
    IF(LEFT(trans_type,3)='PDN','Supplier CN No',
    IF(LEFT(trans_type,3)='PCN','Supplier DN No',
    IF(LEFT(trans_type,3)='SCN','Customer DN No','Customer CN No')))) AS sup_cn_title,

    IF(ibt=1,IF(LEFT(trans_type,3) IN ('PCN','SCN'),'IBT DN Date','IBT CN Date'),
    IF(LEFT(trans_type,3)='PDN','Supplier CN Date',
    IF(LEFT(trans_type,3)='PCN','Supplier DN Date',
    IF(LEFT(trans_type,3)='SCN','Customer DN Date','Customer CN Date')))) AS sup_cn_date_title,

    IF(a.posted=1,'','XXX') AS chk,
    IF(a.posted=1,'','Document Not Posted') AS chk_1,


    IF(ibt=0,IF(LEFT(trans_type,1)='P',IF(a.consign=1,CONCAT('Consignment ',IF(LEFT(trans_type,2)='PC','Credit Note','Debit Note'),'to Supplier'),
    CONCAT('Purchase ',IF(LEFT(trans_type,2)='PC','Credit Note','Debit Note'),' to Supplier')),
    IF(a.consign=1,CONCAT('Consignment ',IF(LEFT(trans_type,2)='SC','Credit Note','Debit Note'),' to Customer'),
    CONCAT('Sales ',IF(LEFT(trans_type,2)='SC','Credit Note','Debit Note'),' to Customer'))),
    IF(ibt=2,IF(LEFT(trans_type,1)='P',IF(a.consign=1,CONCAT('Consignment ',IF(LEFT(trans_type,2)='PC','Credit Note','Debit Note'),' to Inter Company Supplier'),
    CONCAT('Purchase ',IF(LEFT(trans_type,2)='PC','Credit Note','Debit Note'),' to Inter Company Supplier')),
    IF(a.consign=1,CONCAT(IF(LEFT(trans_type,2)='SC','Credit Note','Debit Note'),' to Inter Company Customer - Consignment'),
    CONCAT(IF(LEFT(trans_type,2)='SC','Credit Note','Debit Note'),' to Inter Company Customer - Outright'))),
    IF(a.consign=0,IF(LEFT(trans_type,2) IN ('SC','PC'),'CN - Inter Branch Transfer Inwards','DN - Inter Branch Transfer Outwards'),
    IF(LEFT(trans_type,2) IN ('SC','PC'),'Consignment Note CN - Inter Branch Tranfer Inwards','Consignment Note DN - Inter Branch Tranfer Outwards')))) AS title,

    IF(posted=0,'Draft Copy','') AS draft,

    IF(ibt=0 AND LEFT(trans_type,1)='P' AND a.consign=0,'Customer Debit Note','') AS title_match_cn,

    /* IF(ibt=1,IF(ibt_gst=0,'Inter Branch Stock Transfer Inwards from','Inter Branch Stock Transfer Inwards with GST from'),
    IF(sctype='S',IF(ibt=2,IF(ibt_gst=0,'Credit to Inter Company Supplier','Credit to Inter Company Supplier with GST'),
    IF(a.Tax_code_purchase='NR','Credit to Non Registered GST Supplier',
    'Credit to Registered GST Supplier')),
    IF(ibt=2,IF(ibt_gst=0,'Credit to Inter Company Customer','Credit to Inter Company Customer with GST'),
    IF(a.tax_code_purchase='ES','Credit to Exempted Customer entitled to 0%% Tax',
    'Credit to Customer with GST')))) AS title_gst, */

    IF(LEFT(trans_type,3) IN ('PCN','SCN'),'Credit Note Issued To','Debit Note Issued To') AS title_gst,

    IF(LEFT(trans_type,3) IN ('PCN','SCN'),'Credit Note Issued By','Debit Note Issued By') AS title_issue,

    CONCAT(a.location,' - ',f.description) AS loc_desc,

    CONCAT('Co Reg No: ',reg_no,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no,
    IF((SELECT COUNT(DISTINCT(gst_tax_code)) AS gst_count FROM backend.cndn_amt_c a
    INNER JOIN backend.cndn_amt b
    ON a.cndn_guid=b.cndn_guid
    WHERE a.cndn_guid=%s
    GROUP BY a.cndn_guid)=1,CONCAT('    Tax Code: ',a.tax_code),'')))) reg_sup,

    doc_name_reg,
    IF(ibt=1,'Transfer Note No',IF(LEFT(trans_type,3) IN ('PCN','SCN'),'Credit Note No','Debit Note No')) AS title_invno,
    IF(ibt=1,'IBT Branch Copy',IF(LEFT(trans_type,1)='P','Supplier Copy','Customer Copy')) AS title_supcopy,
    IF(LEFT(trans_type,1)='P','Sup Code','Cus Code') AS title_supcode,
    subdeptcode,cndn_guid,

    #IF(trans_type_acc='OI','Type: O',
    #if(trans_type_acc='EXP','Type: Expenses',
    IF(trans_type_acc='Sales','',CONCAT('Type: ',trans_type_acc)) AS trans_type_acc


    FROM backend.cndn_amt a

    INNER JOIN 
    (SELECT * FROM backend.supcus WHERE
    TYPE=(SELECT IF(LEFT(trans_type,1)='S','C','S') FROM backend.cndn_amt WHERE cndn_guid=%s)) c
    ON a.CODE=c.CODE

    INNER JOIN backend.location f
    ON a.location=f.CODE

    LEFT JOIN backend.set_gst_table g
    ON a.tax_code=g.gst_tax_code

    WHERE a.cndn_guid=%s) a

    INNER JOIN

    (SELECT /*IF(remark IS NULL OR remark='',IF(branch_name ='' OR branch_name IS NULL,companyname,branch_name),remark)*/
    IF(branch_name='' OR branch_name IS NULL,companyname,branch_name) AS companyname,
    IF(trans_type IN ('SCNAMT','PCNAMT'),(SELECT cnremark1 FROM backend.xsetup),(SELECT dnremark1 FROM backend.xsetup)) AS cnremark1,
    IF(trans_type IN ('SCNAMT','PCNAMT'),(SELECT cnremark2 FROM backend.xsetup),(SELECT dnremark2 FROM backend.xsetup)) AS cnremark2,
    IF(trans_type IN ('SCNAMT','PCNAMT'),(SELECT cnremark3 FROM backend.xsetup),(SELECT dnremark3 FROM backend.xsetup)) AS cnremark3,
    IF(branch_add='' OR branch_add IS NULL,address1,'') AS address1,
    IF(branch_add='' OR branch_add IS NULL,address2,'') AS address2,
    IF(branch_add='' OR branch_add IS NULL,address3,'') AS address3,
    IF(branch_add='' OR branch_add IS NULL,CONCAT('Tel: ',tel,'    Fax: ',fax),CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax)) AS contactnumber,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,
    CONCAT('Co Reg No: ',IF(reg_no='' OR reg_no IS NULL,comp_reg_no,reg_no),IF(branch_gst='' OR branch_gst IS NULL,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no)),
    CONCAT('    GST Reg No: ',branch_gst))) reg_no,
    a.cndn_guid, 
    Branch_name
    FROM backend.cndn_amt a

    INNER JOIN backend.companyprofile

    LEFT JOIN 
    (SELECT a.cndn_guid,reg_no,gst_no AS branch_gst,name_reg,branch_add,branch_name,branch_tel,branch_fax 
    FROM backend.cndn_amt a
    INNER JOIN backend.cp_set_branch b
    ON a.loc_group=b.branch_code
    INNER JOIN backend.supcus c
    ON b.set_supplier_code=c.CODE
    WHERE cndn_guid=%s) b

    ON a.cndn_guid=b.cndn_guid

    WHERE a.cndn_guid=%s) b

    ON a.cndn_guid=b.cndn_guid

    LEFT JOIN
    (SELECT a.CODE,IF(c.group_code IS NULL,'Not Applicable',c.group_code) AS division FROM backend.subdept a
    INNER JOIN backend.department b
    ON a.mcode=b.CODE
    LEFT JOIN backend.set_group_dept c
    ON b.CODE=c.dept_code) c
    ON a.subdeptcode=c.CODE

    """
    result = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno, search_refno])
    result = {"query1": result}

    querystr = """
    SELECT itemcode,barcode,
    articleno,
    description,
    packsize,
    unitprice,
    unitprice AS netunitprice,
    qty,
    amount_c AS totalprice,
    '' AS pricetype,
    seq AS line,itemlink,
    b.refno,
    LOWER(IF(um='' OR um IS NULL,'unit',um)) AS um,
    amount AS subtotal1,

    IF(a.gst_tax_rate=0,'Z','S') AS gst_unit_code,
    ROUND(gst_tax_amount/qty,4) AS gst_unit_tax,
    ROUND(unitprice+ROUND(gst_tax_amount/qty,4),4) AS gst_unit_cost,
    gst_tax_amount AS gst_child_tax,
    amount_c_include_tax AS gst_unit_total,
    gst_tax_sum AS gst_main_tax,
    ROUND(amount+gst_tax_sum,2) AS gst_main_total,
    packsize AS ps,

    gst_tax_code,a.gst_tax_rate,gst_tax_amount,
    0 AS unit_disc_prorate,
    unitprice AS unit_price_bfr_tax,
    amount_c AS total_price_bfr_tax,

    ori_inv_no,ori_inv_date,

    a.remark AS itemremark,reason

    FROM backend.cndn_amt_c a

    INNER JOIN backend.cndn_amt b
    ON a.cndn_guid=b.cndn_guid

    WHERE a.cndn_guid=%s
    ORDER BY seq;

    """
    result2 = panda.raw_query(querystr, [
        search_refno
    ])
    result["query2"] = result2

    querystr = """
    SELECT cndn_guid,SUM(gst_zero) AS gst_zero,SUM(gst_std) AS gst_std FROM 

    (SELECT a.cndn_guid,SUM(amount_c) AS gst_zero,0 AS gst_std FROM backend.cndn_amt_c a
    INNER JOIN backend.cndn_amt b
    ON a.cndn_guid=b.cndn_guid
    WHERE gst_tax_amount=0 AND a.cndn_guid=%s
    GROUP BY cndn_guid

    UNION ALL

    SELECT a.cndn_guid,0 AS gst_zero,SUM(amount_c) AS gst_std FROM backend.cndn_amt_c a
    INNER JOIN backend.cndn_amt b
    ON a.cndn_guid=b.cndn_guid
    WHERE gst_tax_amount<>0 AND a.cndn_guid=%s
    GROUP BY cndn_guid) a

    GROUP BY cndn_guid;
    """
    result3 = panda.raw_query(querystr, [search_refno, search_refno])
    result["query3"] = result3

    querystr = """
    SELECT refno,'B1' AS sequence,'Item Tax Amount' AS code_grn,0 AS value_grn,
    ROUND(gst_tax_sum,2) AS value_calculated FROM backend.cndn_amt
    WHERE cndn_guid=%s AND gst_tax_sum<>0

    UNION ALL

    SELECT refno,'C1' AS sequence,'GST Rounding Adjustment' AS code_grn,0 AS value_grn,
    ROUND(GST_adj,2) AS value_calculated FROM backend.cndn_amt
    WHERE cndn_guid=%s AND gst_adj<>0

    UNION ALL

    SELECT refno,'C2' AS sequence,'Bill Rounding Adjustment' AS code_grn,0 AS value_grn,
    ROUND(rounding_adj,2) AS value_calculated FROM backend.cndn_amt
    WHERE cndn_guid=%s AND rounding_adj<>0

    UNION ALL

    SELECT refno,'D1' AS sequence,'Total Amount Incude Tax' AS code_grn,0 AS value_grn,
    ROUND(amount+gst_tax_sum+gst_adj+rounding_adj,2) AS value_calculated FROM backend.cndn_amt
    WHERE cndn_guid=%s

    ORDER BY sequence
    """

    result4 = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno])
    result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)

# report PCN


@api_view(['GET'])
def report_PurchaseCN(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT a.*,b.*,c.division FROM

    (SELECT CONCAT(a.CODE,' - ',a.NAME) AS supplier,
    location,
    refno,
    docdate,
    amount AS total,
    DATE_FORMAT(a.created_at,'%%d/%%m/%%y %%H:%%i:%%s') AS issuestamp,
    a.created_by AS issuedby,
    IF(posted=0,'',DATE_FORMAT(posted_at,'%%d/%%m/%%y %%H:%%i:%%s')) AS postdatetime,
    posted_by AS postby,
    DATE_FORMAT(a.updated_at,'%%d/%%m/%%y %%H:%%i:%%s') AS laststamp,a.remark,
    c.add1,c.add2,c.add3,c.city,c.state,c.postcode,c.country,
    CONCAT(c.tel,IF(c.fax='' OR c.fax IS NULL,'',CONCAT('  Fax : ',c.fax))) AS contact,
    CONCAT('Doc Status : ',IF(posted=0,'Unpost','Posted')) AS doc_status,
    a.docno,sup_cn_no,
    IF(sup_cn_no='' OR sup_cn_no IS NULL,'',DATE_FORMAT(sup_cn_date,'%%d/%%m/%%y %%a')) AS sup_cn_date,

    IF(ibt=1,IF(LEFT(trans_type,3) IN ('PCN','SCN'),'IBT DN No','IBT CN No'),
    IF(LEFT(trans_type,3)='PDN','Supplier CN No',
    IF(LEFT(trans_type,3)='PCN','Supplier DN No',
    IF(LEFT(trans_type,3)='SCN','Customer DN No','Customer CN No')))) AS sup_cn_title,

    IF(ibt=1,IF(LEFT(trans_type,3) IN ('PCN','SCN'),'IBT DN Date','IBT CN Date'),
    IF(LEFT(trans_type,3)='PDN','Supplier CN Date',
    IF(LEFT(trans_type,3)='PCN','Supplier DN Date',
    IF(LEFT(trans_type,3)='SCN','Customer DN Date','Customer CN Date')))) AS sup_cn_date_title,

    IF(a.posted=1,'','XXX') AS chk,
    IF(a.posted=1,'','Document Not Posted') AS chk_1,


    IF(ibt=0,IF(LEFT(trans_type,1)='P',IF(a.consign=1,CONCAT('Consignment ',IF(LEFT(trans_type,2)='PC','Credit Note','Debit Note'),'to Supplier'),
    CONCAT('Purchase ',IF(LEFT(trans_type,2)='PC','Credit Note','Debit Note'),' to Supplier')),
    IF(a.consign=1,CONCAT('Consignment ',IF(LEFT(trans_type,2)='SC','Credit Note','Debit Note'),' to Customer'),
    CONCAT('Sales ',IF(LEFT(trans_type,2)='SC','Credit Note','Debit Note'),' to Customer'))),
    IF(ibt=2,IF(LEFT(trans_type,1)='P',IF(a.consign=1,CONCAT('Consignment ',IF(LEFT(trans_type,2)='PC','Credit Note','Debit Note'),' to Inter Company Supplier'),
    CONCAT('Purchase ',IF(LEFT(trans_type,2)='PC','Credit Note','Debit Note'),' to Inter Company Supplier')),
    IF(a.consign=1,CONCAT(IF(LEFT(trans_type,2)='SC','Credit Note','Debit Note'),' to Inter Company Customer - Consignment'),
    CONCAT(IF(LEFT(trans_type,2)='SC','Credit Note','Debit Note'),' to Inter Company Customer - Outright'))),
    IF(a.consign=0,IF(LEFT(trans_type,2) IN ('SC','PC'),'CN - Inter Branch Transfer Inwards','DN - Inter Branch Transfer Outwards'),
    IF(LEFT(trans_type,2) IN ('SC','PC'),'Consignment Note CN - Inter Branch Tranfer Inwards','Consignment Note DN - Inter Branch Tranfer Outwards')))) AS title,

    IF(posted=0,'Draft Copy','') AS draft,

    IF(ibt=0 AND LEFT(trans_type,1)='P' AND a.consign=0,'Customer Debit Note','') AS title_match_cn,

    /* IF(ibt=1,IF(ibt_gst=0,'Inter Branch Stock Transfer Inwards from','Inter Branch Stock Transfer Inwards with GST from'),
    IF(sctype='S',IF(ibt=2,IF(ibt_gst=0,'Credit to Inter Company Supplier','Credit to Inter Company Supplier with GST'),
    IF(a.Tax_code_purchase='NR','Credit to Non Registered GST Supplier',
    'Credit to Registered GST Supplier')),
    IF(ibt=2,IF(ibt_gst=0,'Credit to Inter Company Customer','Credit to Inter Company Customer with GST'),
    IF(a.tax_code_purchase='ES','Credit to Exempted Customer entitled to 0%% Tax',
    'Credit to Customer with GST')))) AS title_gst, */

    IF(LEFT(trans_type,3) IN ('PCN','SCN'),'Credit Note Issued To','Debit Note Issued To') AS title_gst,

    IF(LEFT(trans_type,3) IN ('PCN','SCN'),'Credit Note Issued By','Debit Note Issued By') AS title_issue,

    CONCAT(a.location,' - ',f.description) AS loc_desc,

    CONCAT('Co Reg No: ',reg_no,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no,
    IF((SELECT COUNT(DISTINCT(gst_tax_code)) AS gst_count FROM backend.cndn_amt_c a
    INNER JOIN backend.cndn_amt b
    ON a.cndn_guid=b.cndn_guid
    WHERE a.cndn_guid=%s
    GROUP BY a.cndn_guid)=1,CONCAT('    Tax Code: ',a.tax_code),'')))) reg_sup,

    doc_name_reg,
    IF(ibt=1,'Transfer Note No',IF(LEFT(trans_type,3) IN ('PCN','SCN'),'Credit Note No','Debit Note No')) AS title_invno,
    IF(ibt=1,'IBT Branch Copy',IF(LEFT(trans_type,1)='P','Supplier Copy','Customer Copy')) AS title_supcopy,
    IF(LEFT(trans_type,1)='P','Sup Code','Cus Code') AS title_supcode,
    subdeptcode,cndn_guid,
    IF(trans_type_acc='Sales','',CONCAT('Type: ',trans_type_acc)) AS trans_type_acc



    FROM backend.cndn_amt a

    INNER JOIN 
    (SELECT * FROM backend.supcus WHERE
    TYPE=(SELECT IF(LEFT(trans_type,1)='S','C','S') FROM backend.cndn_amt WHERE cndn_guid=%s)) c
    ON a.CODE=c.CODE

    INNER JOIN backend.location f
    ON a.location=f.CODE

    LEFT JOIN backend.set_gst_table g
    ON a.tax_code=g.gst_tax_code

    WHERE a.cndn_guid=%s) a

    INNER JOIN

    (SELECT /*IF(remark IS NULL OR remark='',IF(branch_name ='' OR branch_name IS NULL,companyname,branch_name),remark)*/
    IF(branch_name='' OR branch_name IS NULL,companyname,branch_name) AS companyname,
    IF(trans_type IN ('SCNAMT','PCNAMT'),(SELECT cnremark1 FROM backend.xsetup),(SELECT dnremark1 FROM backend.xsetup)) AS cnremark1,
    IF(trans_type IN ('SCNAMT','PCNAMT'),(SELECT cnremark2 FROM backend.xsetup),(SELECT dnremark2 FROM backend.xsetup)) AS cnremark2,
    IF(trans_type IN ('SCNAMT','PCNAMT'),(SELECT cnremark3 FROM backend.xsetup),(SELECT dnremark3 FROM backend.xsetup)) AS cnremark3,
    IF(branch_add='' OR branch_add IS NULL,address1,'') AS address1,
    IF(branch_add='' OR branch_add IS NULL,address2,'') AS address2,
    IF(branch_add='' OR branch_add IS NULL,address3,'') AS address3,
    IF(branch_add='' OR branch_add IS NULL,CONCAT('Tel: ',tel,'    Fax: ',fax),CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax)) AS contactnumber,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,
    CONCAT('Co Reg No: ',IF(reg_no='' OR reg_no IS NULL,comp_reg_no,reg_no),IF(branch_gst='' OR branch_gst IS NULL,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no)),
    CONCAT('    GST Reg No: ',branch_gst))) reg_no,
    a.cndn_guid, 
    Branch_name
    FROM backend.cndn_amt a

    INNER JOIN backend.companyprofile

    LEFT JOIN 
    (SELECT a.cndn_guid,reg_no,gst_no AS branch_gst,name_reg,branch_add,branch_name,branch_tel,branch_fax 
    FROM backend.cndn_amt a
    INNER JOIN backend.cp_set_branch b
    ON a.loc_group=b.branch_code
    INNER JOIN backend.supcus c
    ON b.set_supplier_code=c.CODE
    WHERE cndn_guid=%s) b

    ON a.cndn_guid=b.cndn_guid

    WHERE a.cndn_guid=%s) b

    ON a.cndn_guid=b.cndn_guid

    LEFT JOIN
    (SELECT a.CODE,IF(c.group_code IS NULL,'Not Applicable',c.group_code) AS division FROM backend.subdept a
    INNER JOIN backend.department b
    ON a.mcode=b.CODE
    LEFT JOIN backend.set_group_dept c
    ON b.CODE=c.dept_code) c
    ON a.subdeptcode=c.CODE

    """
    result = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno, search_refno])
    result = {"query1": result}

    querystr = """
    SELECT itemcode,barcode,
    articleno,
    description,
    packsize,
    unitprice,
    unitprice AS netunitprice,
    qty,
    amount_c AS totalprice,
    '' AS pricetype,
    seq AS line,itemlink,
    b.refno,
    LOWER(IF(um='' OR um IS NULL,'unit',um)) AS um,
    amount AS subtotal1,

    IF(a.gst_tax_rate=0,'Z','S') AS gst_unit_code,
    ROUND(gst_tax_amount/qty,4) AS gst_unit_tax,
    ROUND(unitprice+ROUND(gst_tax_amount/qty,4),4) AS gst_unit_cost,
    gst_tax_amount AS gst_child_tax,
    amount_c_include_tax AS gst_unit_total,
    gst_tax_sum AS gst_main_tax,
    ROUND(amount+gst_tax_sum,2) AS gst_main_total,
    packsize AS ps,

    gst_tax_code,a.gst_tax_rate,gst_tax_amount,
    0 AS unit_disc_prorate,
    unitprice AS unit_price_bfr_tax,
    amount_c AS total_price_bfr_tax,

    ori_inv_no,ori_inv_date,

    a.remark AS itemremark,reason

    FROM backend.cndn_amt_c a

    INNER JOIN backend.cndn_amt b
    ON a.cndn_guid=b.cndn_guid

    WHERE a.cndn_guid=%s
    ORDER BY seq;

    """
    result2 = panda.raw_query(querystr, [
        search_refno
    ])
    result["query2"] = result2

    querystr = """
    SELECT cndn_guid,SUM(gst_zero) AS gst_zero,SUM(gst_std) AS gst_std FROM 

    (SELECT a.cndn_guid,SUM(amount_c) AS gst_zero,0 AS gst_std FROM backend.cndn_amt_c a
    INNER JOIN backend.cndn_amt b
    ON a.cndn_guid=b.cndn_guid
    WHERE gst_tax_amount=0 AND a.cndn_guid=%s
    GROUP BY cndn_guid

    UNION ALL

    SELECT a.cndn_guid,0 AS gst_zero,SUM(amount_c) AS gst_std FROM backend.cndn_amt_c a
    INNER JOIN backend.cndn_amt b
    ON a.cndn_guid=b.cndn_guid
    WHERE gst_tax_amount<>0 AND a.cndn_guid=%s
    GROUP BY cndn_guid) a

    GROUP BY cndn_guid;
    """
    result3 = panda.raw_query(querystr, [search_refno, search_refno])
    result["query3"] = result3

    querystr = """
    SELECT refno,'B1' AS sequence,'Item Tax Amount' AS code_grn,0 AS value_grn,
    ROUND(gst_tax_sum,2) AS value_calculated FROM backend.cndn_amt
    WHERE cndn_guid=%s AND gst_tax_sum<>0

    UNION ALL

    SELECT refno,'C1' AS sequence,'GST Rounding Adjustment' AS code_grn,0 AS value_grn,
    ROUND(GST_adj,2) AS value_calculated FROM backend.cndn_amt
    WHERE cndn_guid=%s AND gst_adj<>0

    UNION ALL

    SELECT refno,'C2' AS sequence,'Bill Rounding Adjustment' AS code_grn,0 AS value_grn,
    ROUND(rounding_adj,2) AS value_calculated FROM backend.cndn_amt
    WHERE cndn_guid=%s AND rounding_adj<>0

    UNION ALL

    SELECT refno,'D1' AS sequence,'Total Amount Include Tax' AS code_grn,0 AS value_grn,
    ROUND(amount+gst_tax_sum+gst_adj+rounding_adj,2) AS value_calculated FROM backend.cndn_amt
    WHERE cndn_guid=%s

    ORDER BY sequence
    """

    result4 = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno])
    result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)


# report PCI


@api_view(['GET'])
def report_PromotionClaimInvoie(request, search_refno):
    print(search_refno)

    querystr = """
    #4

    SELECT c.*,a.loc_group,cardtype,itemcode,description,barcode,price_target,price_net,supplier,a.remark,
    bare_supplier_type,sys_average,a.trans_type,qtyclaim_manual,
    disc_value,sold_qty,datefrom,dateto,timefrom,timeto,DATE_FORMAT(a.posted_at,'%%d-%%m-%%Y %%H:%%i:%%s') AS posted_at,cancel_at,docno,promo_themes,
    /* amend on 2018-12-22 due to mydin generate inv from hq
    IF(a.issued_by_hq=1,CONCAT(a.refno,'-',a.loc_group),a.refno) AS refno,*/
    a.refno,
    convert_at,
    locdesc,warn_remark,(bear_supplier+bear_supplier_add) AS bear_supplier,sold_bare_supplier,
    CONCAT(DATE_FORMAT(datefrom,'%%d/%%m/%%y %%a'),' to ',DATE_FORMAT(dateto,'%%d/%%m/%%y %%a')) AS promo_date,
    ROUND(sold_bare_supplier+(qtyclaim_manual*bear_supplier)+(sold_qty*bear_add),2) AS sold_bear_sup,
    ROUND(gst_tax_amount,2) AS gst_tax_amount,a.gst_tax_rate,
    ROUND(ROUND(sold_bare_supplier+(qtyclaim_manual*bear_supplier)+(sold_qty*bear_add),2)+gst_tax_amount,2) AS total_bear_gst,
    discount,
    IF(docdate BETWEEN (SELECT gst_start_date FROM backend.companyprofile)
    AND (SELECT gst_end_date FROM backend.companyprofile) 
    AND (SELECT country FROM backend.companyprofile)='Malaysia',
    IF(LEFT(gst_tax_code,1) IN ('Z','S'),LEFT(gst_tax_code,1),gst_tax_code),'') AS gst_tax_code,

    tax_zero,tax_std,
    IF(convert_dn=0,'Ongoing Promotion','') AS chk_1,

    inv_refno,docdate AS inv_date,
    IF(inv_refno IS NULL OR inv_refno='','Please Generate Promo Tax Invoice via Housekeeping/Accounting Process','') AS inv_remark,

    /* amend on 2018-12-22 due to mydin generate from hq
    IF(inv_refno IS NULL OR inv_refno='',
    IF(docdate>=(SELECT gst_start_date FROM backend.companyprofile) AND docdate<=(SELECT gst_end_date FROM backend.companyprofile),
    'Tax Invoice - Draft Copy','Tax Invoice'),'Invoice') AS title_doc_2, */

    CONCAT(IF(docdate<'2015-04-01','Debit Advice',
    IF(docdate>=(SELECT gst_start_date FROM backend.companyprofile) AND docdate<=(SELECT gst_end_date FROM backend.companyprofile),
    'Tax Invoice','Invoice')),IF(posted=0,' - Draft Copy','')) AS title_doc_2


    FROM

    (SELECT IF(d.promo_refno IS NULL,a.loc_group,d.loc_group) AS loc_group,
    cardtype,itemcode,description,barcode,price_target,price_net,supplier,a.remark,
    bare_supplier_type,sys_average,a.trans_type,
    ROUND(SUM(qtyclaim_manual),2) AS qtyclaim_manual,
    ROUND(SUM(sold_bare_supplier),2) AS sold_bare_supplier,
    ROUND(SUM(bear_supplier_add),2) AS bear_add,
    ROUND(SUM(sold_qty),2) AS sold_qty,
    disc_value,datefrom,dateto,timefrom,timeto,a.posted_at,cancel_at,docno,promo_themes,a.refno,convert_at,
    locdesc,warn_remark,bear_supplier,gst_tax_code,gst_tax_amount,a.gst_tax_rate,discount,a.issued_by_hq,convert_dn,
    IF(d.promo_refno IS NULL,a.loc_group,d.taxinv_guid) AS taxinv_guid1,bear_supplier_add

    FROM

    (SELECT d.loc_group,
    IF(a.trans_type IN ('pgl','psc'),b.cardtype,a.cardtype) AS cardtype,
    b.itemcode,b.description,barcode,b.price_target,b.price_net,
    CONCAT(supcode,' - ',supname) AS supplier,
    CONCAT(a.remark,IF(a.remark='' OR a.remark IS NULL,'',IF(cancelpromo=0,'',CONCAT(' - Cancelled on ',DATE_FORMAT(a.cancel_at,'%%d/%%m/%%y %%H:%%i:%%s'))))) AS remark,
    bare_supplier_type,sys_average,a.trans_type,d.qtyclaim_manual,d.sold_bare_supplier,d.bear_supplier_add,
    d.bear_supplier,gst_tax_code,gst_tax_amount,gst_tax_rate,

    IF(a.trans_type='mix',IF(set_type='any',CONCAT('Buy any ',set_qty,' @ ',ROUND(set_target_price,2)),
    CONCAT('Qty=',qtylimit,' ->Buy 1 set @ ',ROUND(set_target_price,2))),
    CONCAT(IF(disc1value+disc2value=0,'',
    CONCAT(IF(disc1value=0,'',IF(disc1type='$',CONCAT(disc1type,disc1value,IF(disc2value=0,'','+')),CONCAT(disc1value,disc1type,IF(disc2value=0,'','+')))
    ),IF(disc2value=0,'',IF(disc2type='$',CONCAT(disc2type,disc2value),CONCAT(disc2value,disc2type))))))) AS discount,


    IF(promo_by_tragetprice=1,price_target-price_net,IF(disc1type='$',disc1value,
    ROUND(price_target*disc1value/100,2))+
    IF(disc2type='$',disc2value,ROUND((price_target-ROUND(price_target*disc1value/100,2))*disc2value/100,2))) AS disc_value,

    d.sold_qty+IF(d.qtyclaim_manual IS NULL,0,d.qtyclaim_manual) AS sold_qty,

    datefrom,dateto,timefrom,timeto,posted_at,a.cancel_at,docno,promo_themes,a.refno,
    dateto AS convert_at,
    CONCAT(c.loc_group,' - ',IF(e.description IS NULL,'',e.description)) AS locdesc,
    IF(cancelpromo=0,'','CANCELLED') AS cancelpromo,
    IF(set_disable=1,CONCAT('SKU Promo Cancelled on ',DATE_FORMAT(set_disable_at,'%%d/%%m/%%y %%H:%%i:%%s')),'') AS warn_remark,
    a.issued_by_hq,convert_dn

    FROM backend.promo_supplier a
    INNER JOIN backend.promo_supplier_c b
    ON a.pvc_guid=b.pvc_guid
    INNER JOIN backend.promo_supplier_loc c
    ON a.pvc_guid=c.pvc_guid
    INNER JOIN backend.promo_supplier_result d
    ON a.pvc_guid=d.pvc_guid AND b.pvc_guid_c=d.pvc_guid_c AND c.loc_group = d.loc_group

    INNER JOIN backend.locationgroup e
    ON c.loc_group=e.CODE 

    WHERE a.pvc_guid=%s AND c.set_active=1 AND posted=1
    AND d.sold_qty+IF(d.qtyclaim_manual IS NULL,0,d.qtyclaim_manual)>0) a

    LEFT JOIN backend.`promo_taxinv` d
    ON a.refno=d.promo_refno AND a.loc_group=d.loc_group

    GROUP BY taxinv_guid1,itemcode,cardtype

    HAVING sold_qty<>0) a

    INNER JOIN
    (SELECT IF(d.promo_refno IS NULL,a.loc_group,d.loc_group) AS loc_group,
    SUM(tax_zero) AS tax_zero,SUM(tax_std) AS tax_std FROM

    (SELECT b.refno,sold_bare_supplier,
    qtyclaim_manual*bear_supplier AS sold_manual,
    gst_tax_rate,a.loc_group,
    IF(gst_tax_rate=0,ROUND(sold_bare_supplier+(qtyclaim_manual*bear_supplier),2),0) AS tax_zero,
    IF(gst_tax_rate=6,ROUND(sold_bare_supplier+(qtyclaim_manual*bear_supplier),2),0) AS tax_std
    FROM backend.promo_supplier_result a
    INNER JOIN backend.promo_supplier b
    ON a.pvc_guid=b.pvc_guid
    WHERE a.pvc_guid=%s AND posted=1) a

    LEFT JOIN backend.`promo_taxinv` d
    ON a.refno=d.promo_refno AND a.loc_group=d.loc_group

    GROUP BY loc_group) b
    ON a.loc_group=b.loc_group

    INNER JOIN 

    (SELECT b.loc_group AS loc,
    IF(branch_name ='' OR branch_name IS NULL,companyname,branch_name) AS companyname,
    IF(branch_add='' OR branch_add IS NULL,address1,'') AS address1,
    IF(branch_add='' OR branch_add IS NULL,address2,'') AS address2,
    IF(branch_add='' OR branch_add IS NULL,address3,'') AS address3,
    IF(branch_add='' OR branch_add IS NULL,CONCAT('Tel: ',d.tel,'    Fax: ',d.fax),CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax)) AS contactnumber,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,
    CONCAT('Co Reg No: ',IF(c.reg_no='' OR c.reg_no IS NULL,comp_reg_no,c.reg_no),IF(branch_gst='' OR branch_gst IS NULL,IF(d.gst_no='','',CONCAT('    GST Reg No: ',d.gst_no)),
    CONCAT('    GST Reg No: ',branch_gst))) reg_no,
    Branch_name,
    e.name_reg AS doc_name_reg,
    CONCAT('Co Reg No: ',e.reg_no,IF(e.gst_no='','',CONCAT('    GST Reg No: ',e.gst_no)),CONCAT('    Supplier Code: ',supcode)) AS reg_sup,
    add1,add2,add3,
    CONCAT(e.tel,IF(e.fax='' OR e.fax IS NULL,'',CONCAT('  Fax : ',e.fax))) AS contact,


    IF(dateto<'2015-04-01','Debit Advice',
    IF(dateto>=(SELECT gst_start_date FROM backend.companyprofile) AND dateto<=(SELECT gst_end_date FROM backend.companyprofile),
    'Tax Invoice for Promotion Claim issued by','Invoice for Promotion Claim issued by')) AS title_bene,

    IF(dateto<'2015-04-01','Debit Advice Issued To',
    IF(dateto>=(SELECT gst_start_date FROM backend.companyprofile) AND dateto<=(SELECT gst_end_date FROM backend.companyprofile),
    'Tax Invoice for Promotion Claim issued to','Tax Invoice for Promotion Claim issued to')) AS title_sup,

    CONCAT(IF(dateto<'2015-04-01','Debit Advice',
    IF(dateto>=(SELECT gst_start_date FROM backend.companyprofile) AND dateto<=(SELECT gst_end_date FROM backend.companyprofile),
    'Tax Invoice','Invoice')),IF(convert_dn=0,' - Draft Copy','')) AS title_doc,

    IF(convert_dn=0,'Promotion Still Valid','') AS chk_1,
    CONCAT(supcode,' - ',supname) AS sup_code


    FROM backend.promo_supplier a

    INNER JOIN backend.promo_supplier_loc b
    ON a.pvc_guid=b.pvc_guid

    INNER JOIN backend.supcus e
    ON a.supcode=e.CODE

    INNER JOIN backend.locationgroup f
    ON b.loc_group=f.CODE

    INNER JOIN backend.companyprofile d

    LEFT JOIN 
    (SELECT a.refno,reg_no,gst_no AS branch_gst,branch_add,branch_name,branch_tel,branch_fax,
    d.loc_group AS branch_code
    FROM backend.promo_supplier a
    INNER JOIN backend.promo_supplier_loc d
    ON a.pvc_guid=d.pvc_guid
    INNER JOIN backend.cp_set_branch b
    ON d.loc_group=b.branch_code
    INNER JOIN backend.supcus c
    ON b.set_supplier_code=c.CODE
    WHERE a.pvc_guid=%s AND d.set_active=1 AND supplier_claim=1) c

    ON b.loc_group=c.branch_code

    WHERE a.pvc_guid=%s AND b.set_active=1 AND supplier_claim=1


    GROUP BY b.loc_group

    ORDER BY b.loc_group)c

    ON b.loc_group = c.loc

    LEFT JOIN backend.`promo_taxinv` d
    ON a.refno=d.promo_refno AND a.loc_group=d.loc_group

    HAVING total_bear_gst<>0

    ORDER BY a.loc_group,itemcode,cardtype,bear_supplier

    """

    result = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno])
    result = {"query1": result}

    # querystr="""

    # """
    # result2=panda.raw_query(querystr,[search_refno])
    # result["query2"] = result2

    # querystr="""

    # """
    # result3=panda.raw_query(querystr,[search_refno,search_refno,search_refno,search_refno])
    # result["query3"] = result3

    querystr = """
    #@Epvc_guid 3
    SELECT a.refno,'0' AS sort,'0' AS sequence,
    CONCAT('Total Tax') AS code_grn,
    0 AS value_grn,
    FORMAT(ROUND(SUM(gst_tax_amount),2),2) AS value_calculated 

    FROM backend.promo_supplier a
    INNER JOIN backend.promo_supplier_c b
    ON a.pvc_guid=b.pvc_guid
    INNER JOIN backend.promo_supplier_loc c
    ON a.pvc_guid=c.pvc_guid
    INNER JOIN backend.promo_supplier_result d
    ON a.pvc_guid=d.pvc_guid AND b.pvc_guid_c=d.pvc_guid_c AND c.loc_group = d.loc_group

    INNER JOIN backend.locationgroup e
    ON c.loc_group=e.CODE

    WHERE a.pvc_guid=%s AND c.set_active=1 AND posted=1
    AND d.sold_qty+IF(d.qtyclaim_manual IS NULL,0,d.qtyclaim_manual)>0
    GROUP BY a.pvc_guid

    HAVING value_calculated<>0

    UNION ALL

    SELECT a.refno,'1' AS sort,'1' AS sequence,
    CONCAT('Total Include Tax') AS code_grn,
    0 AS value_grn,
    FORMAT(ROUND(ROUND(SUM(d.qtyclaim_manual*d.bear_supplier),2)
    +ROUND(SUM(d.sold_bare_supplier),2)
    +ROUND(SUM(gst_tax_amount),2),2),2) AS value_calculated

    FROM backend.promo_supplier a
    INNER JOIN backend.promo_supplier_c b
    ON a.pvc_guid=b.pvc_guid
    INNER JOIN backend.promo_supplier_loc c
    ON a.pvc_guid=c.pvc_guid
    INNER JOIN backend.promo_supplier_result d
    ON a.pvc_guid=d.pvc_guid AND b.pvc_guid_c=d.pvc_guid_c AND c.loc_group = d.loc_group

    INNER JOIN backend.locationgroup e
    ON c.loc_group=e.CODE

    WHERE a.pvc_guid=%s AND c.set_active=1 AND posted=1
    AND d.sold_qty+IF(d.qtyclaim_manual IS NULL,0,d.qtyclaim_manual)>0
    GROUP BY a.pvc_guid

    HAVING ROUND(SUM(gst_tax_amount),2)<>0

    UNION ALL

    SELECT a.refno,'2' AS sort,'2' AS sequence,
    CONCAT('Total Qty') AS code_grn,
    0 AS value_grn,
    SUM(d.sold_qty+IF(d.qtyclaim_manual IS NULL,0,d.qtyclaim_manual)) AS value_calculated

    FROM backend.promo_supplier a
    INNER JOIN backend.promo_supplier_c b
    ON a.pvc_guid=b.pvc_guid
    INNER JOIN backend.promo_supplier_loc c
    ON a.pvc_guid=c.pvc_guid
    INNER JOIN backend.promo_supplier_result d
    ON a.pvc_guid=d.pvc_guid AND b.pvc_guid_c=d.pvc_guid_c AND c.loc_group = d.loc_group

    INNER JOIN backend.locationgroup e
    ON c.loc_group=e.CODE

    WHERE a.pvc_guid=%s AND c.set_active=1 AND posted=1
    AND d.sold_qty+IF(d.qtyclaim_manual IS NULL,0,d.qtyclaim_manual)>0
    GROUP BY a.pvc_guid

    """

    result4 = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno])
    result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)


# report DI


@api_view(['GET'])
def report_DisplayIncentive_TaxInvoice(request, search_refno):
    print(search_refno)

    querystr = """
    #1
    SELECT a.refno,a.loc_group AS outlet,
    CONCAT(a.CODE,' - ',a.NAME) AS supplier,datefrom,dateto,freqofpayment,FORMAT(amountperpayment,2) AS amountperpayment,FORMAT(totalpayment,2) AS totalpayment,FORMAT(lastpayment,2) AS lastpayment ,firstpaymentdate,
    IF(e.created_by IS NULL,issuedby,IF(e.posted=0,issuedby,e.created_by)) AS issuedby,
    DATE_FORMAT(IF(e.created_at IS NULL,issuestamp,IF(e.posted=0,issuestamp,e.created_at)),'%%d/%%m/%%y %%H:%%i:%%s') AS issuestamp,
    a.docdate,
    a.remark AS remark,
    IF(e.remark IS NULL OR e.remark='',a.remark,IF(e.posted=0,a.remark,e.remark)) AS remark2,
    IF(e.posted_by IS NULL,a.postby,IF(e.posted=0,a.postby,e.posted_by)) AS post_by,
    IF(billstatus=0,'',DATE_FORMAT(IF(e.posted_at IS NULL,a.postdatetime,e.posted_at),'%%d/%%m/%%y %%H:%%i:%%s')) AS postdatetime,
    CONCAT(a.displaytype,IF(c.description IS NULL OR c.description='','',CONCAT(' - ',c.description))) AS displaytype,
    IF(e.docdate IS NULL,paymentdate,IF(e.posted=0,paymentdate,e.docdate)) AS paymentdate,
    FORMAT(paidamount, 2) AS paidamount,line,
    CONCAT(b.refno,'-',line) AS dnrefno,info_authorisedby,
    CONCAT(info_contactno,IF(info_ic='' OR info_ic IS NULL,'',CONCAT(' | ',info_ic))) AS contact,
    info_theme,
    IF(canceled=0,'',CONCAT('CANCELLED ON ',DATE_FORMAT(DATE(canceled_at),'%%d-%%m-%%Y'))) AS cancel,
    CONCAT(block_length,'x',block_width,' ',IF(block_size_unit IS NULL,'',block_size_unit)) AS info_blocksize,info_bincode,info_itemdisplay,
    a.displaytype AS dis_type,subdeptcode,
    gst_tax_code,b.gst_tax_rate,gst_tax_amt,
    FORMAT(ROUND(paidamount+gst_tax_amt,2),2) AS total_aft_gst,

    IF(e.inv_refno IS NULL,'Document Refno',
    IF(paymentdate<'2015-04-01','Debit Note Reference No',
    IF((SELECT gst_start_date FROM backend.companyprofile)<=paymentdate AND (SELECT gst_end_date FROM backend.companyprofile)>=paymentdate,
    'Tax Invoice Refno','Invoice Refno'))) AS title_inv,

    IF(e.inv_refno IS NULL,'Document Date',
    IF(paymentdate>='2015-04-01','Invoice Date','DN Date')) AS title_inv_date,

    IF(paymentdate>=(SELECT gst_start_date FROM backend.companyprofile) AND paymentdate<=(SELECT gst_end_date FROM backend.companyprofile),
    'Amount with GST','Total Amount') AS title_inv_amt,

    IF(a.billstatus=1,'','XXX') AS chk,
    IF(a.billstatus=1,'','Document Not Posted') AS chk_1,
    CONCAT(Line,' of ',freqofpayment) AS pmt_info,

    IF(a.refno2 IS NULL OR a.refno2='',CONCAT(a.refno,'-',line),CONCAT(a.refno2,'-',line)) AS dnrefno2,

    CONCAT(IF(c.description IS NULL OR c.description='',c.TYPE,c.description),
    IF(b.remark IS NULL OR b.remark='','',CONCAT(' for ',b.remark))) AS remark1,

    IF(a.refno2 IS NULL OR a.refno2='',CONCAT(a.refno,'-',line),IF(line='1',a.refno2,CONCAT(a.refno2,'-',line))) AS dnrefno3,

    IF(e.inv_refno IS NULL,'Document Issued By',
    IF(paymentdate<'2015-04-01','Debit Advice',
    IF(paymentdate>=(SELECT gst_start_date FROM backend.companyprofile) AND paymentdate<=(SELECT gst_end_date FROM backend.companyprofile),
    'Tax Invoice Issued By','Invoice Issued By'))) AS title_bene,

    IF(e.inv_refno IS NULL,'Document Issued To',
    IF(paymentdate<'2015-04-01','Debit Advice Issued To',
    IF(paymentdate>=(SELECT gst_start_date FROM backend.companyprofile) AND paymentdate<=(SELECT gst_end_date FROM backend.companyprofile),
    'Tax Invoice Issued To','Invoice Issued To'))) AS title_sup,

    IF(e.inv_refno IS NULL,'Display Incentive',
    IF(paymentdate<'2015-04-01','Debit Advice',
    IF(paymentdate>=(SELECT gst_start_date FROM backend.companyprofile) AND paymentdate<=(SELECT gst_end_date FROM backend.companyprofile),
    'Tax Invoice','Invoice'))) AS title_doc,

    IF(e.inv_refno IS NULL,CONCAT(b.refno,'-',line),IF(e.posted=0,'',e.inv_refno)) AS inv_refno,

    IF(e.inv_refno IS NULL OR e.posted=1,'',
    IF(e.posted=0,CONCAT('Invoice Not Posted  ',e.inv_refno),e.inv_refno)) AS inv_refno_1,

    ar_cuscode,

    branch_name AS companyname,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,
    CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax) AS contactnumber,

    name_reg AS doc_name_reg,
    CONCAT('Co Reg No: ',g.reg_no,IF(g.gst_no='','',CONCAT('    GST Reg No: ',g.gst_no))) AS reg_sup,
    g.add1 AS sup_add1,
    g.add2 AS sup_add2,
    g.add3 AS sup_add3,
    g.add4 AS sup_add4,
    CONCAT(g.tel,IF(g.fax='' OR g.fax IS NULL,'',CONCAT('  Fax : ',g.fax))) AS sup_contact,
    CONCAT(group_code,' | ',subdeptdesc) AS subdept

    FROM backend.dischememain a 

    INNER JOIN
    backend.dischemechild b
    ON a.refno=b.refno

    INNER JOIN backend.cp_set_branch f
    ON a.loc_group=f.branch_code

    INNER JOIN backend.supcus g
    ON a.CODE=g.CODE

    LEFT JOIN 
    backend.view_subdept_div m
    ON a.subdeptcode=m.subdept

    LEFT JOIN
    backend.discheme_taxinv e
    ON b.refno=e.refno AND b.line=e.refno_line

    LEFT JOIN
    backend.acc_code c
    ON a.displaytype=c.NAME

    WHERE a.refno=%s AND canceled=0

    GROUP BY b.refno,line,a.displaytype

    ORDER BY refno,paymentdate;

    """

    result = panda.raw_query(querystr, [search_refno])
    result = {"query1": result}

    querystr = """
    #2
    SELECT IF(branch_name ='' OR branch_name IS NULL,companyname,branch_name) AS companyname,
    IF(branch_add='' OR branch_add IS NULL,address1,'') AS address1,
    IF(branch_add='' OR branch_add IS NULL,address2,'') AS address2,
    IF(branch_add='' OR branch_add IS NULL,address3,'') AS address3,
    IF(branch_add='' OR branch_add IS NULL,CONCAT('Tel: ',d.tel,'    Fax: ',d.fax),CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax)) AS contactnumber,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,

    CONCAT('Co Reg No: ',IF(c.reg_no='' OR c.reg_no IS NULL,comp_reg_no,c.reg_no),
    IF(branch_gst='' OR branch_gst IS NULL,IF(d.gst_no='','',
    IF((SELECT gst_end_date FROM backend.companyprofile)>=paymentdate,CONCAT('    GST Reg No: ',d.gst_no),'')),
    IF((SELECT gst_end_date FROM backend.companyprofile)>=paymentdate,CONCAT('    GST Reg No: ',branch_gst),'')),
    IF((SELECT sst_start_date FROM backend.companyprofile)<=paymentdate,CONCAT('    SST Reg No: ',sst_no),'')) reg_no,


    Branch_name,name_reg AS doc_name_reg,
    CONCAT('Co Reg No: ',e.reg_no,IF(e.gst_no='','',CONCAT('    GST Reg No: ',e.gst_no))) AS reg_sup,
    add1,add2,add3,
    CONCAT(e.tel,IF(e.fax='' OR e.fax IS NULL,'',CONCAT('  Fax : ',e.fax))) AS contact,
    IF(paymentdate>='2015-04-01',IF(b.billstatus=0,'Tax Invoice','Tax Invoice - Draft Copy'),'Debit Advice') AS title_doc

    FROM backend.dischemechild a

    INNER JOIN backend.dischememain b
    ON a.refno=b.refno

    INNER JOIN backend.supcus e
    ON b.CODE=e.CODE

    INNER JOIN backend.companyprofile d

    LEFT JOIN 
    (SELECT a.refno,reg_no,gst_no AS branch_gst,branch_add,branch_name,branch_tel,branch_fax,
    a.loc_group AS branch_code
    FROM backend.dischememain a
    INNER JOIN backend.cp_set_branch b
    ON a.loc_group=b.branch_code
    INNER JOIN backend.supcus c
    ON b.set_supplier_code=c.CODE
    WHERE a.refno=%s AND TYPE='s') c
    ON b.refno=c.refno

    WHERE a.refno=%s AND TYPE='s'

    GROUP BY a.refno
    """
    result2 = panda.raw_query(querystr, [search_refno, search_refno])
    result["query2"] = result2

    querystr = """
    #3
    SELECT a.*,b.* FROM

    (SELECT a.refno,a.loc_group AS outlet,
    CONCAT(CODE,' - ',a.NAME) AS supplier,CONCAT(c.NAME,' - ',c.description) AS displaytype,
    CONCAT(info_authorisedby,IF(info_ic='' OR info_ic IS NULL,'',CONCAT(' (',info_ic,')'))) AS info_authorisedby,
    CONCAT(info_contactno,IF(info_ic='' OR info_ic IS NULL,'',CONCAT(' | ',info_ic))) AS contact,
    info_theme,info_itemdisplay,
    a.displaytype AS dis_type,subdeptcode,
    a.remark,
    IF(a.refno2 IS NULL OR a.refno2='',a.refno,a.refno2) AS refno2

    FROM backend.dischememain a 

    INNER JOIN
    backend.dischemechild b
    ON a.refno=b.refno

    INNER JOIN
    backend.acc_code c
    ON a.displaytype=c.NAME

    WHERE a.refno=%s

    GROUP BY b.refno) a

    LEFT JOIN

    (SELECT refno,info_bincode,
    CONCAT(IF(block_length=0,'',block_length),IF(block_width=0,'',CONCAT('x',block_width)),' ',IF(block_size_unit IS NULL,'',block_size_unit)) AS block 
    FROM backend.dischememain a 
    WHERE a.refno=%s AND info_bincode<>''

    UNION ALL

    SELECT refno,info_bincode,CONCAT(block_length,
    IF(block_width IS NULL,'',CONCAT(' x ',block_width,' = ',block_size,' ',block_size_unit))) AS block 
    FROM backend.dischememain_location a

    INNER JOIN backend.set_block_display b
    ON a.info_bincode=b.block_code

    WHERE refno=%s

    GROUP BY info_bincode) b

    ON a.refno=b.refno

    ORDER BY a.refno,info_bincode;
    """
    result3 = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno])
    result["query3"] = result3

    querystr = """
    #1
    SELECT IF(remark IS NULL OR remark='',IF(branch_name ='' OR branch_name IS NULL,companyname,branch_name),remark) AS companyname,
    IF(branch_add='' OR branch_add IS NULL,address1,'') AS address1,
    IF(branch_add='' OR branch_add IS NULL,address2,'') AS address2,
    IF(branch_add='' OR branch_add IS NULL,address3,'') AS address3,
    IF(branch_add='' OR branch_add IS NULL,CONCAT('Tel: ',tel,'    Fax: ',fax),CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax)) AS contactnumber,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,
    CONCAT('Co Reg No: ',comp_reg_no,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no))) reg_no
    FROM backend.location a
    LEFT JOIN backend.cp_set_branch b
    ON a.locgroup=b.branch_code
    INNER JOIN backend.companyprofile
    WHERE locgroup=(SELECT loc_group FROM backend.dischememain WHERE refno=%s)
    GROUP BY locgroup
    """

    result4 = panda.raw_query(querystr, [search_refno])
    result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def PnLCategory_old(request, date_from, date_to):
    # print(edate_from,'-',edate_to)

    querystr = """
    SELECT 
    a.loc_group,a.code,/*a.itemcode,*/
    any_value(group_code) AS group_code,
    any_value(group_desc) AS group_desc,
    any_value(dept) AS dept,
    any_value(deptdesc) AS deptdesc,
    any_value(subdept) AS subdept,
    any_value(subdeptdesc) AS subdeptdesc,
    any_value(c.category) AS category, 
    any_value(categorydesc) AS categorydesc,
    any_value(d.brand) AS brand,
    any_value(branddesc) AS branddesc,
    any_value(manufacturer) AS manufacturer,
    any_value(manudesc) AS manudesc,


    ROUND(SUM(IF(consign=0,IF(receivedamt IS NULL,0,receivedamt)/*-IF(grn_ibt_amt IS NULL,0,grn_ibt_amt)-IF(grn_inkind_amt IS NULL,0,grn_inkind_amt)*/,0)),2) AS receivedamt,

    ROUND(SUM(IF(consign=0,IF(debitamt IS NULL,0,debitamt)-
    (IF(cnamt_sup IS NULL,0,cnamt_sup)+
    (IF(dnamt_sup_ibt IS NULL,0,dnamt_sup_ibt)-IF(cnamt_sup_ibt IS NULL,0,cnamt_sup_ibt))+
    IF(dnamt_cus IS NULL,0,dnamt_cus)),0)),2) AS netreturnamt,

    ROUND(SUM(IF(consign=0,IF(markdownamt_dn IS NULL,0,markdownamt_dn),0)),2) AS markdown_dn,


    ROUND(SUM(IF(consign=0,IF(receivedamt IS NULL,0,receivedamt)/*-IF(grn_ibt_amt IS NULL,0,grn_ibt_amt)-IF(grn_inkind_amt IS NULL,0,grn_inkind_amt)*/,0))-
    (
    SUM(IF(consign=0,IF(debitamt IS NULL,0,debitamt)-
    (IF(cnamt_sup IS NULL,0,cnamt_sup)+
    (IF(dnamt_sup_ibt IS NULL,0,dnamt_sup_ibt)-IF(cnamt_sup_ibt IS NULL,0,cnamt_sup_ibt))+
    IF(dnamt_cus IS NULL,0,dnamt_cus)),0)) -
    SUM(IF(consign=0,IF(markdownamt_dn IS NULL,0,markdownamt_dn),0)) ),2) AS receivedamt_net


    FROM
    (
    SELECT 
    loc_group,CODE,Itemcode,
    #LEFT(Description,60) AS Description,
    #PeriodDays,
    ROUND(SUM(OpeningQty),4) AS OpenginQty,ROUND(SUM(OpeningAmt),4) AS OpeningAmt,
    ROUND(SUM(TransInQty),4) AS TransInQty, ROUND(SUM(TransInAmt),4) AS TransInAmt,
    ROUND(SUM(TransOutQty),4) AS TransOutQty, ROUND(SUM(TransOutAmt),4) AS TransOutAmt,
    ROUND(SUM(OnHandQty),4) AS OnHandQty, ROUND(SUM(OnHandAmt),4) AS OnHandAmt,
    ROUND(SUM(HamperInQty),4) AS HamperInQty, ROUND(SUM(HamperInAmt),4) AS HamperInAmt, 
    ROUND(SUM(HamperOutQty),4) AS HamperOutQty, ROUND(SUM(HamperOutAmt),4) AS HamperOutAmt,
    ROUND(SUM(AdjustInQty),4) AS AdjustInQty, ROUND(SUM(AdjustInAmt),4) AS AdjustInAmt, 
    ROUND(SUM(AdjustOutQty),4) AS AdjustOutQty, ROUND(SUM(AdjustOutAmt),4)  AS AdjustOutAmt,
    ROUND(SUM(DebitQty),4) AS DebitQty, ROUND(SUM(DebitAmt),4) AS DebitAmt, ROUND(SUM(CreditQty),4) AS CreditQty, ROUND(SUM(CreditAmt),4) AS CreditAmt,
    ROUND(SUM(ReceivedQty),4) AS ReceivedQty, ROUND(SUM(ReceivedAmt),4) AS ReceivedAmt,
    ROUND(SUM(ExchangeINQty),4) AS ExchangeINQty, ROUND(SUM(ExchangeOUTQty),4) AS ExchangeOUTQty,
    ROUND(SUM(SalesTempQty),4) AS SalesTempQty, ROUND(SUM(SalesTempAmt),4) AS SalesTempAmt, 
    ROUND(SUM(SalesQty),4) AS SalesQty, ROUND(SUM(SalesAmt),4) AS SalesAmt,
    ROUND(SUM(BalanceQty),4) AS BalanceQty, ROUND(SUM(BalanceAmt),4) AS BalanceAmt,
   

    SUM(SalesPOS) AS SalesPOS,
    SUM(SalesInvoice) AS SalesInvoice,
    @Elocation_group,SUM(Claim_Qty) AS Claim_Qty,SUM(Claim_Amt) AS Claim_Amt,
    SUM(SalesAmt_by_lastcost) AS SalesAmt_by_lastcost,
    SUM(markdownqty) AS markdownqty,SUM(markdownAmt) AS markdownamt,
    SUM(markdownamt_dn) AS markdownamt_dn,
    SUM(cnqty_sup) AS cnqty_sup,
    SUM(cnamt_sup) AS cnamt_sup,
    SUM(dnqty_cus)  AS DNQty_cus, 
    SUM(dnamt_cus) AS Dnamt_cus,
    SUM(dnqty_sup_ibt) AS dnqty_sup_ibt,
    SUM(dnamt_sup_ibt) AS dnamt_sup_ibt,
    SUM(dnqty_cus_ibt) AS dnqty_cus_ibt,
    SUM(dnamt_cus_ibt) AS dnamt_cus_ibt,
    SUM(cnqty_sup_ibt) AS cnqty_sup_ibt,
    SUM(cnamt_sup_ibt) AS cnamt_sup_ibt,
    SUM(cnqty_cus_ibt) AS cnqty_cus_ibt,
    SUM(cnamt_cus_ibt) AS cnamt_cus_ibt

    FROM
    (

    /* GRN */
    SELECT 

    a.loc_group ,a.code,
    b.Itemcode,
    #b.Description,

    
    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 0 AS DebitAmt, 0 AS CreditQty, 0 AS CreditAmt,
    SUM(IF(a.BillStatus=1,b.Qty,0)) AS ReceivedQty, 

    SUM(IF(entrytype='amt' AND pricetype='norm' AND groupno=0 AND inv_variance=0 AND rebate_value=0
    AND qty>=1000 AND grdate<='2018-10-31',
    totalprice,b.invactcost*b.qty)) AS ReceivedAmt,

    0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,0 AS Claim_Qty,0 AS Claim_Amt,0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,0 AS markdownAmt,0 AS markdownamt_dn,
    0 AS cnqty_sup,
    0 AS cnamt_sup,
    0  AS DNQty_cus, 
    0 AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    0 AS dnamt_cus_ibt,
    0 AS cnqty_sup_ibt,
    0 AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    0 AS cnamt_cus_ibt 
    FROM backend.grmain a
    INNER JOIN backend.grchild b
    ON a.refno=b.refno
    WHERE grdate BETWEEN %s AND %s AND billstatus=1 AND qty<>0 AND itemcode<>'' AND a.ibt<>1 AND a.in_kind=0
    AND billstatus=1
    GROUP BY a.code,b.Itemcode,a.loc_group  

    UNION ALL

    /* Mark Down By Item */
    SELECT 

    a.loc_group,a.code,
    b.Itemcode,
    #b.Description,

  
    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 0 AS DebitAmt, 0 AS CreditQty, 0 AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,
    0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,0 AS Claim_Qty,0 AS Claim_Amt,0 AS SalesAmt_by_lastcost,
    SUM(IF(a.BillStatus=1,b.Qty,0)) AS markdownqty,
    SUM(UnitPrice*(IF(a.BillStatus=1,b.Qty,0))) AS markdownAmt,
    0 AS markdownamt_dn,
    0 AS cnqty_sup,
    0 AS cnamt_sup,
    0  AS DNQty_cus, 
    0 AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    0 AS dnamt_cus_ibt,
    0 AS cnqty_sup_ibt,
    0 AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    0 AS cnamt_cus_ibt
    FROM backend.markdownrecmain a
    INNER JOIN backend.markdownrec_free b
    ON a.refno=b.refno
    WHERE grdate BETWEEN %s AND %s AND billstatus=1 
    GROUP BY a.code,b.Itemcode,a.loc_group

    UNION ALL

    /* Markdown Amt DN */

    SELECT 

    a.loc_group,a.code,
    b.Itemcode,
    #b.Description,

    
    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 0 AS DebitAmt, 0 AS CreditQty, 0 AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,
    0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,0 AS Claim_Qty,
    0 AS Claim_Amt,
    0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,
    0 AS markdownAmt,
    SUM(totalprice) AS markdownamt_dn,
    0 AS cnqty_sup,
    0 AS cnamt_sup,
    0  AS DNQty_cus, 
    0 AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    0 AS dnamt_cus_ibt,
    0 AS cnqty_sup_ibt,
    0 AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    0 AS cnamt_cus_ibt
    FROM backend.markdownamtmain a
    INNER JOIN backend.markdownamtchild b
    ON a.refno=b.refno
    WHERE docdate BETWEEN %s AND %s AND billstatus=1 AND a.ibt<>1
    GROUP BY a.code,b.Itemcode,a.loc_group

    UNION ALL

    /* SALES INVOICE */

    SELECT
    a.loc_group AS Location,
    a.code,
    b.Itemcode,
    #b.Description,


    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 0 AS DebitAmt, 0 AS CreditQty, 0 AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 
    SUM(IF(a.BillStatus=1,b.Qty,0)) AS SalesQty, SUM((SysAvgCost-claim_amt_unit)*(IF(a.BillStatus=1,b.Qty,0))) AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    SUM(b.TotalPrice-(discvalue+surchg_disc_gst)) AS SalesInvoice,0 AS Claim_Qty,0 AS Claim_Amt,0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,0 AS markdownAmt,0 AS markdownamt_dn,
    0 AS cnqty_sup,
    0 AS cnamt_sup,
    0  AS DNQty_cus, 
    0 AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    0 AS dnamt_cus_ibt,
    0 AS cnqty_sup_ibt,
    0 AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    0 AS cnamt_cus_ibt
    FROM backend.simain a
    INNER JOIN backend.sichild b
    ON a.refno=b.refno
    WHERE invoicedate BETWEEN %s AND %s AND billstatus=1 AND ibt<>1
    GROUP BY a.code,b.Itemcode,a.loc_group


    UNION ALL

    /* DEBIT NOTE - supplier & customer */
    SELECT 

    a.locgroup,a.code,
    b.Itemcode,
    #b.Description,


    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    SUM(IF(a.BillStatus=1,b.Qty,0))  AS DebitQty, 
    SUM(UnitPrice*(IF(a.BillStatus=1,b.Qty,0))) AS DebitAmt, 
    0 AS CreditQty, 0 AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,0 AS Claim_Qty,0 AS Claim_Amt,0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,0 AS markdownAmt,0 AS markdownamt_dn,
    0 AS cnqty_sup,
    0 AS cnamt_sup,
    SUM(IF(sctype='C',b.Qty,0)) AS DNQty_cus,
    SUM(IF(sctype='C',UnitPrice*b.Qty,0)) AS Dnamt_cus,

    SUM(IF(sctype='S' AND ibt=1,b.Qty,0)) AS dnqty_sup_ibt, 
    SUM(IF(sctype='S' AND ibt=1,UnitPrice*b.qty,0)) AS dnamt_sup_ibt, 
    SUM(IF(sctype='C' AND ibt=1,b.Qty,0)) AS dnqty_cus_ibt, 
    SUM(IF(sctype='C' AND ibt=1,UnitPrice*b.qty,0)) AS dnamt_cus_ibt, 
    0 AS cnqty_sup_ibt,
    0 AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    0 AS cnamt_cus_ibt
    FROM  backend.dbnotemain a
    INNER JOIN backend.dbnotechild b
    ON a.refno=b.refno
    WHERE docdate BETWEEN %s AND %s AND billstatus=1 AND ibt<>1
    GROUP BY a.code,b.Itemcode,a.locgroup

    UNION ALL

    /* SDNAMT & PDNAMT - customer & supplier*/
    SELECT 

    a.loc_group,a.code,
    b.Itemcode,
    #b.Description,


    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 
    SUM(amount_c) AS DebitAmt, 
    0 AS CreditQty, 
    0 AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,
    0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 
    0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,
    0 AS Claim_Qty,0 AS Claim_Amt,
    0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,
    SUM(IF(trans_type='SDNAMT' AND ibt<>1,amount_c*-1,0)) AS markdownAmt,
    SUM(IF(trans_type='PDNAMT' AND ibt<>1,amount_c,0)) AS markdownamt_dn,
    0 AS cnqty_sup,
    0 AS cnamt_sup,
    0 AS DNQty_cus, 
    SUM(IF(trans_type='SDNAMT',amount_c,0)) AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    SUM(IF(trans_type='SDNAMT' AND ibt=1,amount_c,0)) AS dnamt_cus_ibt,
    0 AS cnqty_sup_ibt,
    0 AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    0 AS cnamt_cus_ibt
    FROM backend.cndn_amt a
    INNER JOIN backend.cndn_amt_c b
    ON a.cndn_guid=b.cndn_guid
    WHERE docdate BETWEEN %s AND %s AND posted=1 AND a.ibt<>1
    AND (itemcode<>'' AND itemcode IS NOT NULL) AND trans_type IN ('PDNAMT','SDNAMT')
    GROUP BY a.code,b.Itemcode,a.loc_group

    UNION ALL

    /* CREDIT NOTE - customer & supplier*/
    SELECT 

    a.locgroup,a.code,
    b.Itemcode,
    #b.Description,


    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 0 AS DebitAmt, 
    SUM(b.Qty) AS CreditQty, 
    SUM(Unitprice*b.Qty) AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,0 AS Claim_Qty,0 AS Claim_Amt,0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,0 AS markdownAmt,0 AS markdownamt_dn,
    SUM(IF(sctype='S',b.Qty,0)) AS cnqty_sup,
    SUM(IF(sctype='S',UnitPrice*b.Qty,0)) AS cnamt_sup,
    0 AS DNQty_cus, 
    0 AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    0 AS dnamt_cus_ibt,
    SUM(IF(sctype='S' AND ibt=1,b.Qty,0)) AS cnqty_sup_ibt, 
    SUM(IF(sctype='S' AND ibt=1,UnitPrice*b.qty,0)) AS cnamt_sup_ibt, 
    SUM(IF(sctype='C' AND ibt=1,b.Qty,0)) AS cnqty_cus_ibt, 
    SUM(IF(sctype='C' AND ibt=1,UnitPrice*b.qty,0)) AS cnamt_cus_ibt 
    FROM backend.cnnotemain a
    INNER JOIN backend.cnnotechild b
    ON a.refno=b.refno
    WHERE docdate BETWEEN %s AND %s AND billstatus=1 AND a.ibt<>1
    GROUP BY a.code,b.Itemcode,a.locgroup

    UNION ALL

    /* SCNAMT & PCNAMT - customer & supplier*/
    SELECT 

    a.loc_group,a.code,
    b.Itemcode,
    #b.Description,


    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 0 AS DebitAmt, 
    0 AS CreditQty, 
    SUM(amount_c) AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,0 AS Claim_Qty,0 AS Claim_Amt,0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,
    SUM(IF(trans_type='SCNAMT' AND ibt<>1,amount_c,0)) AS markdownAmt,
    SUM(IF(trans_type='PCNAMT' AND ibt<>1,amount_c*-1,0)) AS markdownamt_dn,
    0 AS cnqty_sup,
    SUM(IF(trans_type='PCNAMT',amount_c,0)) AS cnamt_sup,
    0 AS DNQty_cus, 
    0 AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    0 AS dnamt_cus_ibt,
    0 AS cnqty_sup_ibt,
    SUM(IF(trans_type='PCNAMT' AND ibt=1,amount_c,0)) AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    SUM(IF(trans_type='SCNAMT' AND ibt=1,amount_c,0)) cnamt_cus_ibt
    FROM backend.cndn_amt a
    INNER JOIN backend.cndn_amt_c b
    ON a.cndn_guid=b.cndn_guid
    WHERE docdate BETWEEN %s AND %s AND posted=1 
    AND (itemcode<>'' AND itemcode IS NOT NULL) AND trans_type IN ('SCNAMT','PCNAMT')
    GROUP BY a.code,b.Itemcode,a.loc_group

    ) a

    WHERE loc_group<>'' AND itemcode<>''

    GROUP BY loc_group,a.code,Itemcode
    )a
    INNER JOIN 
    (
    SELECT location_group,itemcode,consign,category,brand
    FROM backend.locationstock_period
    WHERE periodcode=LEFT(CONVERT(%s USING latin1),7)
    )b
        ON a.itemcode=b.itemcode AND a.loc_group=b.location_group
    INNER JOIN backend.view_set_d_dept_s_c c
        ON b.category=c.category
    LEFT JOIN backend.view_brand d
        ON b.brand=d.brand

    GROUP BY a.loc_group,a.code,b.category

    """

    result = panda.raw_query(querystr, [
        date_from, date_to,
        date_from, date_to,
        date_from, date_to,
        date_from, date_to,
        date_from, date_to,
        date_from, date_to,
        date_from, date_to,
        date_from, date_to,
        date_from])

    result = {"query1": result}

    return Response(result, status=status.HTTP_200_OK)


# report PDNCN
@api_view(['POST'])
def report_PnLCategory(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        results = PnLSerializer(data, many=False).data
        date_from = data['date_from']
        date_to = data['date_to']
        print(results)
        print(data['date_from'], ' - ', data['date_to'])

    querystr = """
    SELECT 
    a.loc_group,a.code,/*a.itemcode,*/
    any_value(group_code) AS group_code,
    any_value(group_desc) AS group_desc,
    any_value(dept) AS dept,
    any_value(deptdesc) AS deptdesc,
    any_value(subdept) AS subdept,
    any_value(subdeptdesc) AS subdeptdesc,
    any_value(c.category) AS category, 
    any_value(categorydesc) AS categorydesc,
    any_value(d.brand) AS brand,
    any_value(branddesc) AS branddesc,
    any_value(manufacturer) AS manufacturer,
    any_value(manudesc) AS manudesc,


    ROUND(SUM(IF(consign=0,IF(receivedamt IS NULL,0,receivedamt)/*-IF(grn_ibt_amt IS NULL,0,grn_ibt_amt)-IF(grn_inkind_amt IS NULL,0,grn_inkind_amt)*/,0)),2) AS receivedamt,

    ROUND(SUM(IF(consign=0,IF(debitamt IS NULL,0,debitamt)-
    (IF(cnamt_sup IS NULL,0,cnamt_sup)+
    (IF(dnamt_sup_ibt IS NULL,0,dnamt_sup_ibt)-IF(cnamt_sup_ibt IS NULL,0,cnamt_sup_ibt))+
    IF(dnamt_cus IS NULL,0,dnamt_cus)),0)),2) AS netreturnamt,

    ROUND(SUM(IF(consign=0,IF(markdownamt_dn IS NULL,0,markdownamt_dn),0)),2) AS markdown_dn,


    ROUND(SUM(IF(consign=0,IF(receivedamt IS NULL,0,receivedamt)/*-IF(grn_ibt_amt IS NULL,0,grn_ibt_amt)-IF(grn_inkind_amt IS NULL,0,grn_inkind_amt)*/,0))-
    (
    SUM(IF(consign=0,IF(debitamt IS NULL,0,debitamt)-
    (IF(cnamt_sup IS NULL,0,cnamt_sup)+
    (IF(dnamt_sup_ibt IS NULL,0,dnamt_sup_ibt)-IF(cnamt_sup_ibt IS NULL,0,cnamt_sup_ibt))+
    IF(dnamt_cus IS NULL,0,dnamt_cus)),0)) -
    SUM(IF(consign=0,IF(markdownamt_dn IS NULL,0,markdownamt_dn),0)) ),2) AS receivedamt_net


    FROM
    (
    SELECT 
    loc_group,CODE,Itemcode,
    #LEFT(Description,60) AS Description,
    #PeriodDays,
    ROUND(SUM(OpeningQty),4) AS OpenginQty,ROUND(SUM(OpeningAmt),4) AS OpeningAmt,
    ROUND(SUM(TransInQty),4) AS TransInQty, ROUND(SUM(TransInAmt),4) AS TransInAmt,
    ROUND(SUM(TransOutQty),4) AS TransOutQty, ROUND(SUM(TransOutAmt),4) AS TransOutAmt,
    ROUND(SUM(OnHandQty),4) AS OnHandQty, ROUND(SUM(OnHandAmt),4) AS OnHandAmt,
    ROUND(SUM(HamperInQty),4) AS HamperInQty, ROUND(SUM(HamperInAmt),4) AS HamperInAmt, 
    ROUND(SUM(HamperOutQty),4) AS HamperOutQty, ROUND(SUM(HamperOutAmt),4) AS HamperOutAmt,
    ROUND(SUM(AdjustInQty),4) AS AdjustInQty, ROUND(SUM(AdjustInAmt),4) AS AdjustInAmt, 
    ROUND(SUM(AdjustOutQty),4) AS AdjustOutQty, ROUND(SUM(AdjustOutAmt),4)  AS AdjustOutAmt,
    ROUND(SUM(DebitQty),4) AS DebitQty, ROUND(SUM(DebitAmt),4) AS DebitAmt, ROUND(SUM(CreditQty),4) AS CreditQty, ROUND(SUM(CreditAmt),4) AS CreditAmt,
    ROUND(SUM(ReceivedQty),4) AS ReceivedQty, ROUND(SUM(ReceivedAmt),4) AS ReceivedAmt,
    ROUND(SUM(ExchangeINQty),4) AS ExchangeINQty, ROUND(SUM(ExchangeOUTQty),4) AS ExchangeOUTQty,
    ROUND(SUM(SalesTempQty),4) AS SalesTempQty, ROUND(SUM(SalesTempAmt),4) AS SalesTempAmt, 
    ROUND(SUM(SalesQty),4) AS SalesQty, ROUND(SUM(SalesAmt),4) AS SalesAmt,
    ROUND(SUM(BalanceQty),4) AS BalanceQty, ROUND(SUM(BalanceAmt),4) AS BalanceAmt,
   

    SUM(SalesPOS) AS SalesPOS,
    SUM(SalesInvoice) AS SalesInvoice,
    @Elocation_group,SUM(Claim_Qty) AS Claim_Qty,SUM(Claim_Amt) AS Claim_Amt,
    SUM(SalesAmt_by_lastcost) AS SalesAmt_by_lastcost,
    SUM(markdownqty) AS markdownqty,SUM(markdownAmt) AS markdownamt,
    SUM(markdownamt_dn) AS markdownamt_dn,
    SUM(cnqty_sup) AS cnqty_sup,
    SUM(cnamt_sup) AS cnamt_sup,
    SUM(dnqty_cus)  AS DNQty_cus, 
    SUM(dnamt_cus) AS Dnamt_cus,
    SUM(dnqty_sup_ibt) AS dnqty_sup_ibt,
    SUM(dnamt_sup_ibt) AS dnamt_sup_ibt,
    SUM(dnqty_cus_ibt) AS dnqty_cus_ibt,
    SUM(dnamt_cus_ibt) AS dnamt_cus_ibt,
    SUM(cnqty_sup_ibt) AS cnqty_sup_ibt,
    SUM(cnamt_sup_ibt) AS cnamt_sup_ibt,
    SUM(cnqty_cus_ibt) AS cnqty_cus_ibt,
    SUM(cnamt_cus_ibt) AS cnamt_cus_ibt

    FROM
    (

    /* GRN */
    SELECT 

    a.loc_group ,a.code,
    b.Itemcode,
    #b.Description,

    
    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 0 AS DebitAmt, 0 AS CreditQty, 0 AS CreditAmt,
    SUM(IF(a.BillStatus=1,b.Qty,0)) AS ReceivedQty, 

    SUM(IF(entrytype='amt' AND pricetype='norm' AND groupno=0 AND inv_variance=0 AND rebate_value=0
    AND qty>=1000 AND grdate<='2018-10-31',
    totalprice,b.invactcost*b.qty)) AS ReceivedAmt,

    0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,0 AS Claim_Qty,0 AS Claim_Amt,0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,0 AS markdownAmt,0 AS markdownamt_dn,
    0 AS cnqty_sup,
    0 AS cnamt_sup,
    0  AS DNQty_cus, 
    0 AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    0 AS dnamt_cus_ibt,
    0 AS cnqty_sup_ibt,
    0 AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    0 AS cnamt_cus_ibt 
    FROM backend.grmain a
    INNER JOIN backend.grchild b
    ON a.refno=b.refno
    WHERE grdate BETWEEN %s AND %s AND billstatus=1 AND qty<>0 AND itemcode<>'' AND a.ibt<>1 AND a.in_kind=0
    AND billstatus=1
    GROUP BY a.code,b.Itemcode,a.loc_group  

    UNION ALL

    /* Mark Down By Item */
    SELECT 

    a.loc_group,a.code,
    b.Itemcode,
    #b.Description,

  
    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 0 AS DebitAmt, 0 AS CreditQty, 0 AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,
    0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,0 AS Claim_Qty,0 AS Claim_Amt,0 AS SalesAmt_by_lastcost,
    SUM(IF(a.BillStatus=1,b.Qty,0)) AS markdownqty,
    SUM(UnitPrice*(IF(a.BillStatus=1,b.Qty,0))) AS markdownAmt,
    0 AS markdownamt_dn,
    0 AS cnqty_sup,
    0 AS cnamt_sup,
    0  AS DNQty_cus, 
    0 AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    0 AS dnamt_cus_ibt,
    0 AS cnqty_sup_ibt,
    0 AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    0 AS cnamt_cus_ibt
    FROM backend.markdownrecmain a
    INNER JOIN backend.markdownrec_free b
    ON a.refno=b.refno
    WHERE grdate BETWEEN %s AND %s AND billstatus=1 
    GROUP BY a.code,b.Itemcode,a.loc_group

    UNION ALL

    /* Markdown Amt DN */

    SELECT 

    a.loc_group,a.code,
    b.Itemcode,
    #b.Description,

    
    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 0 AS DebitAmt, 0 AS CreditQty, 0 AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,
    0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,0 AS Claim_Qty,
    0 AS Claim_Amt,
    0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,
    0 AS markdownAmt,
    SUM(totalprice) AS markdownamt_dn,
    0 AS cnqty_sup,
    0 AS cnamt_sup,
    0  AS DNQty_cus, 
    0 AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    0 AS dnamt_cus_ibt,
    0 AS cnqty_sup_ibt,
    0 AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    0 AS cnamt_cus_ibt
    FROM backend.markdownamtmain a
    INNER JOIN backend.markdownamtchild b
    ON a.refno=b.refno
    WHERE docdate BETWEEN %s AND %s AND billstatus=1 AND a.ibt<>1
    GROUP BY a.code,b.Itemcode,a.loc_group

    UNION ALL

    /* SALES INVOICE */

    SELECT
    a.loc_group AS Location,
    a.code,
    b.Itemcode,
    #b.Description,


    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 0 AS DebitAmt, 0 AS CreditQty, 0 AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 
    SUM(IF(a.BillStatus=1,b.Qty,0)) AS SalesQty, SUM((SysAvgCost-claim_amt_unit)*(IF(a.BillStatus=1,b.Qty,0))) AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    SUM(b.TotalPrice-(discvalue+surchg_disc_gst)) AS SalesInvoice,0 AS Claim_Qty,0 AS Claim_Amt,0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,0 AS markdownAmt,0 AS markdownamt_dn,
    0 AS cnqty_sup,
    0 AS cnamt_sup,
    0  AS DNQty_cus, 
    0 AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    0 AS dnamt_cus_ibt,
    0 AS cnqty_sup_ibt,
    0 AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    0 AS cnamt_cus_ibt
    FROM backend.simain a
    INNER JOIN backend.sichild b
    ON a.refno=b.refno
    WHERE invoicedate BETWEEN %s AND %s AND billstatus=1 AND ibt<>1
    GROUP BY a.code,b.Itemcode,a.loc_group


    UNION ALL

    /* DEBIT NOTE - supplier & customer */
    SELECT 

    a.locgroup,a.code,
    b.Itemcode,
    #b.Description,


    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    SUM(IF(a.BillStatus=1,b.Qty,0))  AS DebitQty, 
    SUM(UnitPrice*(IF(a.BillStatus=1,b.Qty,0))) AS DebitAmt, 
    0 AS CreditQty, 0 AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,0 AS Claim_Qty,0 AS Claim_Amt,0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,0 AS markdownAmt,0 AS markdownamt_dn,
    0 AS cnqty_sup,
    0 AS cnamt_sup,
    SUM(IF(sctype='C',b.Qty,0)) AS DNQty_cus,
    SUM(IF(sctype='C',UnitPrice*b.Qty,0)) AS Dnamt_cus,

    SUM(IF(sctype='S' AND ibt=1,b.Qty,0)) AS dnqty_sup_ibt, 
    SUM(IF(sctype='S' AND ibt=1,UnitPrice*b.qty,0)) AS dnamt_sup_ibt, 
    SUM(IF(sctype='C' AND ibt=1,b.Qty,0)) AS dnqty_cus_ibt, 
    SUM(IF(sctype='C' AND ibt=1,UnitPrice*b.qty,0)) AS dnamt_cus_ibt, 
    0 AS cnqty_sup_ibt,
    0 AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    0 AS cnamt_cus_ibt
    FROM  backend.dbnotemain a
    INNER JOIN backend.dbnotechild b
    ON a.refno=b.refno
    WHERE docdate BETWEEN %s AND %s AND billstatus=1 AND ibt<>1
    GROUP BY a.code,b.Itemcode,a.locgroup

    UNION ALL

    /* SDNAMT & PDNAMT - customer & supplier*/
    SELECT 

    a.loc_group,a.code,
    b.Itemcode,
    #b.Description,


    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 
    SUM(amount_c) AS DebitAmt, 
    0 AS CreditQty, 
    0 AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,
    0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 
    0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,
    0 AS Claim_Qty,0 AS Claim_Amt,
    0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,
    SUM(IF(trans_type='SDNAMT' AND ibt<>1,amount_c*-1,0)) AS markdownAmt,
    SUM(IF(trans_type='PDNAMT' AND ibt<>1,amount_c,0)) AS markdownamt_dn,
    0 AS cnqty_sup,
    0 AS cnamt_sup,
    0 AS DNQty_cus, 
    SUM(IF(trans_type='SDNAMT',amount_c,0)) AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    SUM(IF(trans_type='SDNAMT' AND ibt=1,amount_c,0)) AS dnamt_cus_ibt,
    0 AS cnqty_sup_ibt,
    0 AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    0 AS cnamt_cus_ibt
    FROM backend.cndn_amt a
    INNER JOIN backend.cndn_amt_c b
    ON a.cndn_guid=b.cndn_guid
    WHERE docdate BETWEEN %s AND %s AND posted=1 AND a.ibt<>1
    AND (itemcode<>'' AND itemcode IS NOT NULL) AND trans_type IN ('PDNAMT','SDNAMT')
    GROUP BY a.code,b.Itemcode,a.loc_group

    UNION ALL

    /* CREDIT NOTE - customer & supplier*/
    SELECT 

    a.locgroup,a.code,
    b.Itemcode,
    #b.Description,


    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 0 AS DebitAmt, 
    SUM(b.Qty) AS CreditQty, 
    SUM(Unitprice*b.Qty) AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,0 AS Claim_Qty,0 AS Claim_Amt,0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,0 AS markdownAmt,0 AS markdownamt_dn,
    SUM(IF(sctype='S',b.Qty,0)) AS cnqty_sup,
    SUM(IF(sctype='S',UnitPrice*b.Qty,0)) AS cnamt_sup,
    0 AS DNQty_cus, 
    0 AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    0 AS dnamt_cus_ibt,
    SUM(IF(sctype='S' AND ibt=1,b.Qty,0)) AS cnqty_sup_ibt, 
    SUM(IF(sctype='S' AND ibt=1,UnitPrice*b.qty,0)) AS cnamt_sup_ibt, 
    SUM(IF(sctype='C' AND ibt=1,b.Qty,0)) AS cnqty_cus_ibt, 
    SUM(IF(sctype='C' AND ibt=1,UnitPrice*b.qty,0)) AS cnamt_cus_ibt 
    FROM backend.cnnotemain a
    INNER JOIN backend.cnnotechild b
    ON a.refno=b.refno
    WHERE docdate BETWEEN %s AND %s AND billstatus=1 AND a.ibt<>1
    GROUP BY a.code,b.Itemcode,a.locgroup

    UNION ALL

    /* SCNAMT & PCNAMT - customer & supplier*/
    SELECT 

    a.loc_group,a.code,
    b.Itemcode,
    #b.Description,


    0 AS OpeningQty, 0 AS OpeningAmt, 0  AS TransInQty, 0 AS TransInAmt,
    0 AS TransOutQty, 0 AS TransOutAmt, 0 AS OnHandQty, 0 AS OnHandAmt,
    0 AS HamperInQty, 0 AS HamperInAmt, 0 AS HamperOutQty, 0 AS HamperOutAmt,
    0 AS AdjustInQty, 0 AS AdjustInAmt, 0 AS AdjustOutQty, 0  AS AdjustOutAmt,
    0 AS DebitQty, 0 AS DebitAmt, 
    0 AS CreditQty, 
    SUM(amount_c) AS CreditAmt,
    0 AS ReceivedQty, 0 AS ReceivedAmt,0 AS ExchangeINQty, 0 AS ExchangeOUTQty,
    0 AS SalesTempQty, 0 AS SalesTempAmt, 0 AS SalesQty, 0 AS SalesAmt,
    0 AS BalanceQty, 0 AS BalanceAmt,
    

    0 AS SalesPOS,
    0 AS SalesInvoice,0 AS Claim_Qty,0 AS Claim_Amt,0 AS SalesAmt_by_lastcost,
    0 AS markdownqty,
    SUM(IF(trans_type='SCNAMT' AND ibt<>1,amount_c,0)) AS markdownAmt,
    SUM(IF(trans_type='PCNAMT' AND ibt<>1,amount_c*-1,0)) AS markdownamt_dn,
    0 AS cnqty_sup,
    SUM(IF(trans_type='PCNAMT',amount_c,0)) AS cnamt_sup,
    0 AS DNQty_cus, 
    0 AS Dnamt_cus,

    0 AS dnqty_sup_ibt, 
    0 AS dnamt_sup_ibt,
    0 AS dnqty_cus_ibt,
    0 AS dnamt_cus_ibt,
    0 AS cnqty_sup_ibt,
    SUM(IF(trans_type='PCNAMT' AND ibt=1,amount_c,0)) AS cnamt_sup_ibt,
    0 AS cnqty_cus_ibt,
    SUM(IF(trans_type='SCNAMT' AND ibt=1,amount_c,0)) cnamt_cus_ibt
    FROM backend.cndn_amt a
    INNER JOIN backend.cndn_amt_c b
    ON a.cndn_guid=b.cndn_guid
    WHERE docdate BETWEEN %s AND %s AND posted=1 
    AND (itemcode<>'' AND itemcode IS NOT NULL) AND trans_type IN ('SCNAMT','PCNAMT')
    GROUP BY a.code,b.Itemcode,a.loc_group

    ) a

    WHERE loc_group<>'' AND itemcode<>''

    GROUP BY loc_group,a.code,Itemcode
    )a
    INNER JOIN 
    (
    SELECT location_group,itemcode,consign,category,brand
    FROM backend.locationstock_period
    WHERE periodcode=LEFT(CONVERT(%s USING latin1),7)
    )b
        ON a.itemcode=b.itemcode AND a.loc_group=b.location_group
    INNER JOIN backend.view_set_d_dept_s_c c
        ON b.category=c.category
    LEFT JOIN backend.view_brand d
        ON b.brand=d.brand

    GROUP BY a.loc_group,a.code,b.category

    """

    result = panda.raw_query(querystr, [
        date_from, date_to,
        date_from, date_to,
        date_from, date_to,
        date_from, date_to,
        date_from, date_to,
        date_from, date_to,
        date_from, date_to,
        date_from, date_to,
        date_from])

    #results = YourSerializer(yourdata, many=True).data
    return Response(result, status=status.HTTP_200_OK)


# report SI


@api_view(['GET'])
def report_SiManagementCopy(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT a.*,b.* FROM

    (SELECT CONCAT(a.CODE,' - ',a.NAME) AS customer,a.tel,a.fax,a.term,deflocation AS location,
    IF(d.refno IS NULL OR d.refno='',a.refno,d.refno) AS refno,invoicedate,a.deliverdate,
    a.subtotal1,discount1 * -1 AS discount1,a.subtotal2,discount2,a.total,issuestamp,issuedby,postdatetime,postby,a.laststamp,a.remark,
    IF(discount1type=1,'%%','$') AS discount1type,IF(discount2type=1,'%%','$') AS discount2type,
    IF(a.dadd1='' OR a.dadd1 IS NULL,a.add1,a.dadd1) AS add1,
    IF(a.dadd2='' OR a.dadd2 IS NULL,a.add2,a.dadd2) AS add2,
    IF(a.dadd3='' OR a.dadd3 IS NULL,a.add3,a.dadd3) AS add3,
    c.city,c.state,c.postcode,c.country,
    CONCAT(IF(a.dtel IS NULL OR a.dtel='',a.tel,a.dtel),IF(a.dfax='' OR a.dfax IS NULL,IF(a.fax='' OR a.fax IS NULL,'',CONCAT('  Fax : ',a.fax)),CONCAT('  Fax : ',a.dfax))) AS contact,

    IF(converted_from_module='dc_picklist','IBT SALES INVOICE CUM DELIVERY ORDER','SALES INVOICE CUM DELIVERY ORDER') AS title,
    CONCAT('Doc Status : ',IF(billstatus=0,'Unpost','Posted')) AS doc_status,
    CONCAT(a.term, ' - ',b.description) AS termdesc,a.deliverd_by,a.vehicle_no,a.doc_no,
    e.refno AS ibt_refno,
    IF(a.billstatus=1,'','XXX') AS chk,IF(a.billstatus=1,'','Document Not Posted') AS chk_1,
    a.refno AS refno_si,
    IF(a.docno='' OR a.docno IS NULL,d.refno,a.docno) AS refno_pick,
    IF(a.ibt=1,'IBT Request','Other Refno') AS docno_title,
    a.doc_name_reg,

    IF(a.ibt=1,'Inter Branch Stock Transfer Outwards Management Copy',
    IF(consign=1,'Consignment Note Management Copy','Sales Invoice Management Copy')) AS title_3,

    IF(billstatus=0,'Draft Copy','') AS draft,

    IF(a.ibt=1,'Refno','Refno') AS inv_title,

    IF(a.ibt=1,IF(a.ibt_gst=0,'Inter Branch Stock Transfer Outwards to','Inter Branch Stock Transfer Outwards with GST to'),
    IF(a.ibt=2,IF(a.ibt_gst=0,'Sales to Inter Company Customer','Sales to Inter Company Customer with GST'),
    IF(g.gst_tax_rate=0,
    'Sales to Registered GST Customer entitled to 0%% Tax','Sales to Customer with GST'))) AS title_gst,

    IF(a.ibt=1,'Inter Branch Stock Transfer Outwards Issued By',
    IF(a.ibt=2,'Inter Company Sales Invoice Issued By',
    'Sales Invoice Issued By')) AS title_issue,

    CONCAT(a.deflocation,' - ',f.description) AS loc_desc,
    CONCAT(loc_group,IF(loc_group=a.deflocation,'',CONCAT(' (',a.deflocation,')'))) AS outlet_loc,
    IF(loc_group=a.deflocation,'Outlet','Outlet (Location)') AS outlet_title,

    CONCAT('Co Reg No: ',reg_no,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no,
    IF((SELECT COUNT(DISTINCT(gst_tax_code)) AS gst_count FROM backend.sichild a
    INNER JOIN backend.simain b
    ON a.refno=b.refno
    WHERE a.refno=%s
    GROUP BY a.refno)=1 AND a.ibt=0,CONCAT('    Tax Code: ',tax_code_sales),'')))) reg_sup,

    IF(a.ibt=1,'IBT Branch Copy',
    IF(a.ibt=2,'Inter Company Copy',
    'Customer Copy')) AS title_supcopy,


    IF(a.billstatus=0,'Posted on',CONCAT('Posted on ',DATE_FORMAT(a.postdatetime,'%%d/%%m/%%y %%H:%%I:%%S'))) AS doc_posted,
    CONCAT('Issued on ',DATE_FORMAT(a.issuestamp,'%%d/%%m/%%y %%H:%%I:%%S')) AS doc_created,

    IF(d.docdate IS NULL,'',CONCAT('Picking List Date  ',DATE_FORMAT(d.docdate,'%%d/%%m/%%y'))) AS pick_date,
    a.refno AS si_refno,
    tran_weight,
    tran_volume


    FROM backend.simain a

    INNER JOIN backend.supcus c
    ON a.CODE=c.CODE

    INNER JOIN backend.location f
    ON a.deflocation=f.CODE

    LEFT JOIN backend.set_gst_table g
    ON a.tax_code_sales=g.gst_tax_code

    LEFT JOIN backend.pay_term b
    ON a.term=b.CODE

    LEFT JOIN backend.dc_pick d
    ON a.converted_from_guid=d.trans_guid

    LEFT JOIN backend.dc_req e
    ON d.trans_guid=e.converted_guid
    WHERE a.refno=%s AND TYPE='c') a

    INNER JOIN

    (SELECT /*IF(remark IS NULL OR remark='',IF(branch_name ='' OR branch_name IS NULL,companyname,branch_name),remark)*/
    IF(branch_name='' OR branch_name IS NULL,companyname,branch_name) AS companyname,
    (SELECT invremark1 FROM backend.xsetup) AS invremark1,
    (SELECT invremark2 FROM backend.xsetup) AS invremark2,
    (SELECT invremark3 FROM backend.xsetup) AS invremark3,
    IF(branch_add='' OR branch_add IS NULL,address1,'') AS address1,
    IF(branch_add='' OR branch_add IS NULL,address2,'') AS address2,
    IF(branch_add='' OR branch_add IS NULL,address3,'') AS address3,
    IF(branch_add='' OR branch_add IS NULL,CONCAT('Tel: ',c.tel,'    Fax: ',c.fax),CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax)) AS contactnumber,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,
    CONCAT('Co Reg No: ',IF(reg_no='' OR reg_no IS NULL,comp_reg_no,reg_no),IF(branch_gst='' OR branch_gst IS NULL,IF(gst_no='','',CONCAT('    GST Reg No: ',gst_no)),
    CONCAT('    GST Reg No: ',branch_gst))) reg_no,
    a.refno, 
    Branch_name
    FROM backend.simain a

    INNER JOIN backend.companyprofile c

    LEFT JOIN 
    (SELECT a.refno,reg_no,gst_no AS branch_gst,name_reg,branch_add,branch_name,branch_tel,branch_fax 
    FROM backend.simain a
    INNER JOIN backend.cp_set_branch b
    ON a.loc_group=b.branch_code
    INNER JOIN backend.supcus c
    ON b.set_supplier_code=c.CODE
    WHERE refno=%s) b

    ON a.refno=b.refno

    WHERE a.refno=%s) b

    ON a.si_refno=b.refno



    """

    result = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno])
    result = {"query1": result}

    querystr = """
    #Query 2
    SELECT a.itemcode,barcode,articleno,description,c.item_remark,packsize,bulkqty,unitprice,
    IF(disc1value=0,'',IF(disc1type='%%s',CONCAT(disc1value,disc1type),CONCAT(disc1type,disc1value))) AS disc1,
    IF(disc2value=0,'',IF(disc2type='%%s',CONCAT(disc2value,disc2type),CONCAT(disc2type,disc2value))) AS disc2,discamt,
    netunitprice,qty,totalprice,
    ROUND(sysavgcost*qty,2) AS total_cost,
    ROUND(totalprice-ROUND(sysavgcost*qty,2),2) AS profit,
    ROUND((totalprice-ROUND(sysavgcost*qty,2))/totalprice*100,1) AS margin,

    ROUND(IF(lastcost<>0,lastcost,sysavgcost)*qty,2) AS total_lastcost,
    ROUND(totalprice-ROUND(IF(lastcost<>0,lastcost,sysavgcost)*qty,2),2) AS profit_lastcost,
    ROUND((totalprice-ROUND(IF(lastcost<>0,lastcost,sysavgcost)*qty,2))/totalprice*100,1) AS margin_lastcost,

    ROUND(IF(fifocost<>0,fifocost,sysavgcost)*qty,2) AS total_fifocost,
    ROUND(totalprice-ROUND(IF(fifocost<>0,fifocost,sysavgcost)*qty,2),2) AS profit_fifocost,
    ROUND((totalprice-ROUND(IF(fifocost<>0,fifocost,sysavgcost)*qty,2))/totalprice*100,1) AS margin_fifocost,




    itemremark,IF(pricetype='foc','FOC','') AS pricetype,

    line,itemlink,a.refno,disc1type,disc2type,LOWER(um) AS um,
    IF(qty<bulkqty OR bulkqty=1,'',CONCAT('= ',IF(MOD(qty/bulkqty,1)=0,qty/bulkqty,ROUND(qty/bulkqty,1)),' ',umbulk)) AS ctn,
    IF(bqty=0,'',IF(bulkqty=packsize,'',CONCAT('[',Bqty,' ',LOWER(umbulk),IF(pqty=0,'',CONCAT(' ',Pqty)),']'))) AS b_qty,
    IF(disc1value=0,'',IF(disc1type='%%s',CONCAT(ROUND(disc1value,2),disc1type),CONCAT(disc1type,ROUND(disc1value,2)))) AS disc1value,
    IF(disc2value=0,'',IF(disc2type='%%s',CONCAT(ROUND(disc2value,2),disc2type),CONCAT(disc2type,ROUND(disc2value,2)))) AS disc2value,
    CONCAT(IF(disc1value=0,'',IF(disc1type='%%s',CONCAT(IF(MOD(disc1value,1)=0,ROUND(disc1value),ROUND(disc1value,2)),disc1type),
    CONCAT(disc1type,ROUND(disc1value,2)))),IF(disc2value=0,'',IF(disc2type='%%s',CONCAT(' + ',IF(MOD(disc2value,1)=0,
    ROUND(disc2value),ROUND(disc2value,2)),disc2type),CONCAT(disc2type,ROUND(disc2value,2))))) AS disc_desc,

    IF(a.gst_tax_code IN ('zrl','sr'),UPPER(LEFT(gst_tax_code,1)),UPPER(gst_tax_code)) AS gst_unit_code,
    ROUND(gst_tax_amount/qty,4) AS gst_unit_tax,
    ROUND(IF(discvalue=0,netunitprice+(gst_tax_amount/qty),((totalprice-discvalue)+gst_tax_amount)/qty),4) AS gst_unit_cost,
    gst_tax_amount AS gst_child_tax,
    ROUND((totalprice-discvalue)+gst_tax_amount,2) AS gst_unit_total,
    gst_tax_sum AS gst_main_tax,
    ROUND(total+gst_tax_sum,2) AS gst_main_total,
    CONCAT(packsize,IF(bulkqty=1,'',CONCAT('/',bulkqty))) AS ps,

    gst_tax_code,a.gst_tax_rate,

    IF(LENGTH(MID(gst_tax_amount,POSITION('.' IN gst_tax_amount)+1,10))<=2,FORMAT(gst_tax_amount,2),
    FORMAT(gst_tax_amount,4)) AS gst_tax_amount,

    ROUND(discvalue/qty,4) AS unit_disc_prorate,
    IF(discvalue=0,netunitprice,ROUND((totalprice-discvalue)/qty,4)) AS unit_price_bfr_tax,
    ROUND((totalprice-discvalue),4) AS total_price_bfr_tax

    FROM backend.sichild a

    INNER JOIN backend.simain b
    ON a.refno=b.refno

    LEFT JOIN (SELECT itemcode, remark AS item_remark FROM backend.itemmaster )c 
    ON a.`Itemcode` = c.`Itemcode`

    WHERE a.refno=%s
    ORDER BY line;
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["query2"] = result2

    querystr = """
    #Query3
    SELECT refno,SUM(gst_zero) AS gst_zero,SUM(gst_std) AS gst_std FROM 

    (SELECT a.refno,ROUND(SUM(totalprice-discvalue),2) AS gst_zero,0 AS gst_std FROM backend.sichild a
    INNER JOIN backend.simain b
    ON a.refno=b.refno
    WHERE gst_tax_amount=0 AND a.refno=%s
    GROUP BY refno

    UNION ALL

    SELECT a.refno,0 AS gst_zero,ROUND(SUM(totalprice-discvalue),2) AS gst_std FROM backend.sichild a
    INNER JOIN backend.simain b
    ON a.refno=b.refno
    WHERE gst_tax_amount<>0 AND a.refno=%s
    GROUP BY refno) a

    GROUP BY refno
    """
    result3 = panda.raw_query(querystr, [search_refno, search_refno])
    result["query3"] = result3

    querystr = """
        
    SELECT 
    a.refno,
    'B1' AS sequence,
    #ROUND(SUM(totalprice),2) AS TotalPrice,
    'Total Cost' AS code_grn,
    SUM(ROUND(sysavgcost*qty,2)) AS value_calculated,
    SUM(ROUND(IF(lastcost<>0,lastcost,sysavgcost)*qty,2)) AS value_calculated2,
    SUM(ROUND(IF(fifocost<>0,fifocost,sysavgcost)*qty,2)) AS value_calculated3
    #ROUND(SUM(totalprice)-SUM(ROUND(sysavgcost*qty,2)),2) AS profit
    FROM backend.sichild a
    INNER JOIN backend.simain b 
        ON a.refno=b.refno
    WHERE a.refno=%s
    GROUP BY a.refno

    UNION ALL
    SELECT 
    a.refno,
    'C1' AS sequence,
    #ROUND(SUM(totalprice),2) AS TotalPrice,
    #SUM(ROUND(sysavgcost*qty,2)) AS total_cost,
    'Total Profit' AS code_grn,
    ROUND(SUM(totalprice)-SUM(ROUND(sysavgcost*qty,2)),2) AS value_calculated,
    ROUND(SUM(totalprice)-SUM(ROUND(IF(lastcost<>0,lastcost,sysavgcost)*qty,2)),2) AS value_calculated2,
    ROUND(SUM(totalprice)-SUM(ROUND(IF(fifocost<>0,fifocost,sysavgcost)*qty,2)),2) AS value_calculated3
    FROM backend.sichild a
    INNER JOIN backend.simain b 
        ON a.refno=b.refno
    WHERE a.refno=%s
    GROUP BY a.refno


    UNION ALL
    SELECT 
    a.refno,
    'D1' AS sequence,
    #ROUND(SUM(totalprice),2) AS TotalPrice,
    #SUM(ROUND(sysavgcost*qty,2)) AS total_cost,
    'Profit Margin' AS code_grn,
    ROUND(ROUND(SUM(totalprice)-SUM(ROUND(sysavgcost*qty,2)),2)/SUM(ROUND(sysavgcost*qty,2))*100,1) AS valye_calculated,
    ROUND(ROUND(SUM(totalprice)-SUM(ROUND(IF(lastcost<>0,lastcost,sysavgcost)*qty,2)),2)/SUM(ROUND(IF(lastcost<>0,lastcost,sysavgcost)*qty,2))*100,1) AS valye_calculated2,
    ROUND(ROUND(SUM(totalprice)-SUM(ROUND(IF(fifocost<>0,fifocost,sysavgcost)*qty,2)),2)/SUM(ROUND(IF(fifocost<>0,fifocost,sysavgcost)*qty,2))*100,1) AS valye_calculated3
    FROM backend.sichild a
    INNER JOIN backend.simain b 
        ON a.refno=b.refno
    WHERE a.refno=%s
    GROUP BY a.refno

    ORDER BY sequence
    """

    result4 = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno])
    result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)

# report SI


@api_view(['GET'])
def report_SiSupplierCopy(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT a.*,b.* FROM

    (SELECT CONCAT(a.CODE,IF(doutlet_code='',CONCAT(' - ',a.NAME),CONCAT('    Customer Outlet  ',doutlet_code))) AS customer,salesman,
    @euser AS USER,
    CONCAT(a.deliverd_by,IF(a.deliverd_by='','','  '),a.vehicle_no) AS delivered_by,
    a.docno AS refno2,
    a.tel,a.fax,a.term,deflocation AS location,
    tran_weight,
    tran_volume,
    IF(tran_weight=0 AND tran_volume=0,'',
    IF(tran_weight<>0 AND tran_volume=0,CONCAT('Total kg ',ROUND(tran_weight,1)),
    IF(tran_weight=0 AND tran_volume<>0,CONCAT('Total m3 ',ROUND(tran_volume,1)),
    CONCAT('KG: ',ROUND(tran_weight,1),'   M3: ',ROUND(tran_volume,1))))) AS total_weight,
    Amtasdescription,
    IF(d.refno IS NULL OR d.refno='',a.refno,d.refno) AS refno,invoicedate,a.deliverdate,
    a.subtotal1,discount1 * -1 AS discount1,a.subtotal2,discount2,a.total,issuestamp,issuedby,postdatetime,postby,a.laststamp,a.remark,
    IF(discount1type=1,'%%','$') AS discount1type,IF(discount2type=1,'%%','$') AS discount2type,
    IF(a.dadd1='' OR a.dadd1 IS NULL,a.add1,a.dadd1) AS add1,
    IF(a.dadd1='' OR a.dadd1 IS NULL,a.add2,a.dadd2) AS add2,
    IF(a.dadd1='' OR a.dadd1 IS NULL,a.add3,a.dadd3) AS add3,
    IF(a.dadd1='' OR a.dadd1 IS NULL,a.add4,a.dadd4) AS add4,
    c.city,c.state,c.postcode,c.country,
    CONCAT('Tel : ',IF(a.dadd1 IS NULL OR a.dadd1='',a.tel,a.dtel),IF(a.dadd1='' OR a.dadd1 IS NULL,IF(a.fax='' OR a.fax IS NULL,'',
    CONCAT('  Fax : ',a.fax)),CONCAT('  Fax : ',a.dfax))) AS contact,

    IF(converted_from_module='dc_picklist','IBT SALES INVOICE CUM DELIVERY ORDER','SALES INVOICE CUM DELIVERY ORDER') AS title,
    CONCAT('Doc Status : ',IF(billstatus=0,'Unpost','Posted')) AS doc_status,
    CONCAT(a.term, ' - ',b.description) AS termdesc,
    a.deliverd_by,a.vehicle_no,a.doc_no,
    e.refno AS ibt_refno,
    IF(a.billstatus=1,'','XXX') AS chk,IF(a.billstatus=1,'','Document Not Posted') AS chk_1,
    a.refno AS refno_si,
    IF(a.docno='' OR a.docno IS NULL,d.refno,a.docno) AS refno_pick,
    IF(a.ibt=1,'IBT Request','Other Refno') AS docno_title,
    a.doc_name_reg,

    IF(a.ibt=1,'Inter Branch Stock Transfer Outwards',
    IF(consign=1,'Consignment Note',
    IF((SELECT gst_end_date FROM backend.companyprofile)>=invoicedate,'Tax Invoice','Invoice'))) AS title_3,

    IF(billstatus=0,'Draft Copy','') AS draft,

    IF(a.ibt=1,'Refno','Refno') AS inv_title,

    IF(a.ibt=1,IF(a.ibt_gst=0,'Inter Branch Stock Transfer Outwards to','Inter Branch Stock Transfer Outwards to'),
    IF(a.ibt=2,IF(a.ibt_gst=0,'Sales to Inter Company Customer','Sales to Inter Company Customer'),
    IF(g.gst_tax_rate=0,
    'Sales to Registered GST Customer entitled to 0%% Tax','Sales to Customer'))) AS title_gst,

    IF(a.ibt=1,'Inter Branch Stock Transfer Outwards Issued By',
    IF(a.ibt=2,'Inter Company Sales Invoice Issued By',
    'Sales Invoice Issued By')) AS title_issue,

    IF(a.ibt=1,'Inter Branch Stock Transfer Outwards Issued By',
    IF(a.ibt=2,'Inter Company Delivery Order Issued By',
    'Deliver Order Issued By')) AS title_issued_do,

    'Delivery Order' AS title_DO,



    CONCAT(a.deflocation,' - ',f.description) AS loc_desc,
    CONCAT(loc_group,IF(loc_group=a.deflocation,'',CONCAT(' (',a.deflocation,')'))) AS outlet_loc,
    IF(loc_group=a.deflocation,'Outlet','Outlet (Location)') AS outlet_title,


    CONCAT('Co Reg No : ',reg_no,
    IF(invoicedate BETWEEN (SELECT gst_start_date FROM backend.companyprofile)
    AND (SELECT gst_end_date FROM backend.companyprofile),
    IF(gst_no='','',CONCAT('    GST Reg No : ',gst_no,
    IF((SELECT COUNT(DISTINCT(gst_tax_code)) AS gst_count 
    FROM backend.sichild a
    INNER JOIN backend.simain b
    ON a.refno=b.refno
    WHERE a.refno=%s
    GROUP BY a.refno)=1 AND a.ibt=0,CONCAT('    Tax Code : ',a.tax_code_purchase),''))),'')) reg_sup,

    IF(a.ibt=1,'IBT Branch Copy',
    IF(a.ibt=2,'Inter Company Copy',
    'Customer Copy')) AS title_supcopy,


    IF(a.billstatus=0,'Posted on',CONCAT('Posted on ',DATE_FORMAT(a.postdatetime,'%%d/%%m/%%y %%H:%%I:%%S'))) AS doc_posted,
    CONCAT('Issued on ',DATE_FORMAT(a.issuestamp,'%%d/%%m/%%y %%H:%%I:%%S')) AS doc_created,

    IF(d.docdate IS NULL,'',CONCAT('Picking List Date  ',DATE_FORMAT(d.docdate,'%%d/%%m/%%y'))) AS pick_date,
    a.refno AS si_refno,
    IF((SELECT set_enable FROM backend.`set_module_features` WHERE module_feature = 'Display "No Signature Is Required" @ Docoument')=1,
    '***This document is computer generated. No signature is required.***','') AS no_signature


    FROM backend.simain a

    INNER JOIN backend.supcus c
    ON a.CODE=c.CODE

    INNER JOIN backend.location f
    ON a.deflocation=f.CODE

    LEFT JOIN backend.set_gst_table g
    ON a.tax_code_sales=g.gst_tax_code

    LEFT JOIN backend.pay_term b
    ON a.term=b.CODE

    LEFT JOIN backend.dc_pick d
    ON a.converted_from_guid=d.trans_guid

    LEFT JOIN backend.dc_req e
    ON d.trans_guid=e.converted_guid
    WHERE a.refno=%s AND TYPE='c') a

    INNER JOIN

    (SELECT /*IF(remark IS NULL OR remark='',IF(branch_name ='' OR branch_name IS NULL,companyname,branch_name),remark)*/
    IF(branch_name='' OR branch_name IS NULL,companyname,branch_name) AS companyname,
    (SELECT invremark1 FROM backend.xsetup) AS invremark1,
    (SELECT invremark2 FROM backend.xsetup) AS invremark2,
    (SELECT invremark3 FROM backend.xsetup) AS invremark3,
    IF(branch_add='' OR branch_add IS NULL,address1,'') AS address1,
    IF(branch_add='' OR branch_add IS NULL,address2,'') AS address2,
    IF(branch_add='' OR branch_add IS NULL,address3,'') AS address3,
    IF(branch_add='' OR branch_add IS NULL,CONCAT('Tel: ',c.tel,'    Fax: ',c.fax),CONCAT('Tel: ',branch_tel,'    Fax: ',branch_fax)) AS contactnumber,
    IF(branch_add='' OR branch_add IS NULL,'',branch_add) AS branch_add,

    CONCAT('Co Reg No : ',IF(reg_no='' OR reg_no IS NULL,comp_reg_no,reg_no),
    IF(invoicedate BETWEEN (SELECT gst_start_date FROM backend.companyprofile)
    AND (SELECT gst_end_date FROM backend.companyprofile),
    IF(branch_gst='' OR branch_gst IS NULL,
    IF(gst_no='','',CONCAT('    GST Reg No : ',gst_no)),
    CONCAT('    GST Reg No : ',branch_gst)),
    IF(invoicedate BETWEEN (SELECT sst_start_date FROM backend.companyprofile)
    AND (SELECT sst_end_date FROM backend.companyprofile),
    IF(branch_sst='' OR branch_sst IS NULL,
    IF(sst_no='','',CONCAT('    SST Reg No : ',sst_no)),
    CONCAT('    SST Reg No : ',branch_sst)),''))) reg_no,

    IF(invoicedate BETWEEN (SELECT gst_start_date FROM backend.companyprofile)
    AND (SELECT gst_end_date FROM backend.companyprofile),'Total Amount Exclude Tax',
    IF(invoicedate BETWEEN (SELECT sst_start_date FROM backend.companyprofile)
    AND (SELECT sst_end_date FROM backend.companyprofile),'Total Amount Exclude Tax',
    'Total Amount')) AS title_total,

    a.refno, 
    Branch_name
    FROM backend.simain a

    INNER JOIN backend.companyprofile c

    LEFT JOIN 
    (SELECT a.refno,reg_no,gst_no AS branch_gst,name_reg,branch_add,branch_name,branch_tel,branch_fax,
    SSTRegNo AS branch_sst  
    FROM backend.simain a
    INNER JOIN backend.cp_set_branch b
    ON a.loc_group=b.branch_code
    INNER JOIN backend.supcus c
    ON b.set_supplier_code=c.CODE
    WHERE refno=%s) b

    ON a.refno=b.refno

    WHERE a.refno=%s) b

    ON a.si_refno=b.refno






    """

    result = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno, search_refno])
    result = {"query1": result}

    querystr = """
    #Query 2
    SELECT a.itemcode,barcode,articleno,description,c.item_remark,packsize,bulkqty,unitprice,
    IF(disc1value=0,'',IF(disc1type='%%',CONCAT(disc1value,disc1type),CONCAT(disc1type,disc1value))) AS disc1,
    IF(disc2value=0,'',IF(disc2type='%%',CONCAT(disc2value,disc2type),CONCAT(disc2type,disc2value))) AS disc2,discamt,
    netunitprice,qty,totalprice,itemremark,IF(pricetype='foc','FOC','') AS pricetype,

    line,itemlink,a.refno,disc1type,disc2type,LOWER(um) AS um,
    IF(qty<bulkqty OR bulkqty=1,'',CONCAT('= ',IF(MOD(qty/bulkqty,1)=0,qty/bulkqty,ROUND(qty/bulkqty,1)),' ',umbulk)) AS ctn,
    IF(bqty=0,'',IF(bulkqty=packsize OR bulkqty<=1,'',CONCAT('[',Bqty,' ',LOWER(umbulk),IF(pqty=0,'',CONCAT(' ',Pqty)),']'))) AS b_qty,
    IF(disc1value=0,'',IF(disc1type='%%',CONCAT(ROUND(disc1value,2),disc1type),CONCAT(disc1type,ROUND(disc1value,2)))) AS disc1value,
    IF(disc2value=0,'',IF(disc2type='%%',CONCAT(ROUND(disc2value,2),disc2type),CONCAT(disc2type,ROUND(disc2value,2)))) AS disc2value,
    CONCAT(IF(disc1value=0,'',IF(disc1type='%%',CONCAT(IF(MOD(disc1value,1)=0,ROUND(disc1value),ROUND(disc1value,2)),disc1type),
    CONCAT(disc1type,ROUND(disc1value,2)))),IF(disc2value=0,'',CONCAT(IF(disc1value=0,'',' + '),IF(disc2type='%%',IF(MOD(disc2value,1)=0,
    ROUND(disc2value),ROUND(disc2value,2)),disc2type),ROUND(disc2value,2)))) AS disc_desc,


    IF(a.gst_tax_code IN ('zrl','sr'),UPPER(LEFT(gst_tax_code,1)),UPPER(gst_tax_code)) AS gst_unit_code,
    ROUND(gst_tax_amount/qty,4) AS gst_unit_tax,
    ROUND(IF(discvalue=0,netunitprice+(gst_tax_amount/qty),((totalprice-discvalue)+gst_tax_amount)/qty),4) AS gst_unit_cost,
    gst_tax_amount AS gst_child_tax,

    ROUND((totalprice-discvalue)+
    IF(invoicedate BETWEEN (SELECT gst_start_date FROM backend.companyprofile)
    AND (SELECT gst_end_date FROM backend.companyprofile),gst_tax_amount,
    IF(invoicedate BETWEEN (SELECT sst_start_date FROM backend.companyprofile)
    AND (SELECT sst_end_date FROM backend.companyprofile),taxamount,0)),2) AS gst_unit_total,

    gst_tax_sum AS gst_main_tax,
    ROUND(total+gst_tax_sum,2) AS gst_main_total,
    CONCAT(packsize,IF(bulkqty=1,'',CONCAT('/',bulkqty))) AS ps,

    IF(invoicedate BETWEEN (SELECT gst_start_date FROM backend.companyprofile)
    AND (SELECT gst_end_date FROM backend.companyprofile),gst_tax_code,
    IF(invoicedate BETWEEN (SELECT sst_start_date FROM backend.companyprofile)
    AND (SELECT sst_end_date FROM backend.companyprofile),taxcodemap,'')) AS gst_tax_code,

    a.gst_tax_rate,

    IF(invoicedate BETWEEN (SELECT gst_start_date FROM backend.companyprofile)
    AND (SELECT gst_end_date FROM backend.companyprofile),
    IF(LENGTH(MID(gst_tax_amount,POSITION('.' IN gst_tax_amount)+1,10))<=2,FORMAT(gst_tax_amount,2),
    FORMAT(gst_tax_amount,4)),
    IF(invoicedate BETWEEN (SELECT sst_start_date FROM backend.companyprofile)
    AND (SELECT sst_end_date FROM backend.companyprofile),
    FORMAT(taxamount,2),'0.00')) AS gst_tax_amount,

    ROUND(discvalue/qty,4) AS unit_disc_prorate,
    IF(discvalue=0,netunitprice,ROUND((totalprice-discvalue)/qty,4)) AS unit_price_bfr_tax,
    ROUND((totalprice-discvalue),4) AS total_price_bfr_tax

    FROM backend.sichild a

    INNER JOIN backend.simain b
    ON a.refno=b.refno

    LEFT JOIN (SELECT itemcode, remark AS item_remark FROM backend.itemmaster )c 
    ON a.`Itemcode` = c.`Itemcode`

    WHERE a.refno=%s AND qty<>0
    ORDER BY line;
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["query2"] = result2

    querystr = """
    #Query3
    SELECT a.*,
    IF((SELECT gst_end_date FROM backend.companyprofile)>=invoicedate
    AND (SELECT country FROM backend.companyprofile)='malaysia','Tax @ 6%%','Tax @ >0%%') AS tax_sum_title FROM

    (SELECT a.refno,SUM(gst_zero) AS gst_zero,SUM(gst_std) AS gst_std FROM 

    (SELECT a.refno,ROUND(SUM(totalprice-discvalue),2) AS gst_zero,0 AS gst_std FROM backend.sichild a
    INNER JOIN backend.simain b
    ON a.refno=b.refno
    WHERE gst_tax_amount=0 AND a.refno=%s
    GROUP BY refno

    UNION ALL

    SELECT a.refno,0 AS gst_zero,ROUND(SUM(totalprice-discvalue),2) AS gst_std FROM backend.sichild a
    INNER JOIN backend.simain b
    ON a.refno=b.refno
    WHERE gst_tax_amount<>0 AND a.refno=%s
    GROUP BY refno

    UNION ALL

    SELECT a.refno,0 AS gst_zero,
    ROUND(SUM(ABS(value_calculated)),2) AS value_calculated
    FROM backend.trans_surcharge_discount a
    WHERE a.refno=%s AND dn=0 AND Value_Factor=1 AND gst_amt<>0
    GROUP BY refno) a

    GROUP BY refno) a

    INNER JOIN backend.simain b
    ON a.refno=b.refno
    """
    result3 = panda.raw_query(
        querystr, [search_refno, search_refno, search_refno])
    result["query3"] = result3

    querystr = """

    SELECT a.refno,'0' AS sort,'0' AS sequence,
    CONCAT('Total Amount') AS code_grn,
    0 AS value_grn,
    subtotal1 AS value_calculated FROM backend.simain a
    WHERE a.refno=%s

    UNION ALL

    SELECT a.refno,'1' AS sort,'1' AS sequence,CONCAT(IF(discount1type='%%',IF(discount1>0,'Discount %%   ','Surchage %%   '),
    IF(discount1>0,'Discount $   ','Surcharge $   '))) AS code_grn,
    discount1*-1 AS value_grn,
    ROUND(subtotal1*disc1percent/100,2) AS value_calculated FROM backend.simain a
    LEFT JOIN backend.trans_surcharge_discount b
    ON a.refno=b.refno
    WHERE a.refno=%s AND ROUND(subtotal1*disc1percent/100,2)<>0 AND b.refno IS NULL AND discount1<>0

    UNION ALL

    SELECT a.refno,'2' AS sort,'2' AS sequence,CONCAT(IF(discount2type='%%',IF(discount2>0,'Discount %%   ','Surchage %%   '),
    IF(discount2>0,'Discount $   ','Surcharge $   '))) AS code_grn,
    discount2*-1 AS value_grn,
    ROUND(subtotal2*disc2percent/100,2) AS value_calculated FROM backend.simain a
    LEFT JOIN backend.trans_surcharge_discount b
    ON a.refno=b.refno
    WHERE a.refno=%s AND ROUND(subtotal2*disc2percent/100,2)<>0 AND b.refno IS NULL AND discount2<>0

    UNION ALL

    SELECT refno,'A1' AS sort,sequence,CONCAT(CODE,' (',surcharge_disc_type,')') AS code_grn,
    surcharge_disc_value*Value_Factor AS value_grn,
    ROUND(value_calculated,2) AS value_calculated
    FROM backend.trans_surcharge_discount
    WHERE refno=%s AND dn=0

    UNION ALL

    SELECT refno,'A2' AS sort,'A2' AS sequence,'Total Include Surcharge/Disc' AS code_grn,0 AS value_grn,
    total AS value_calculated FROM backend.simain
    WHERE refno=%s AND discount1+discount2<>0 AND doc_type<>'EStore'

    UNION ALL

    SELECT refno,'B1' AS sort,'B1' AS sequence,'Total Tax Amount' AS code_grn,0 AS value_grn,
    ROUND(gst_tax_sum+surchg_tax_sum+totaltax,2) AS value_calculated FROM backend.simain
    WHERE refno=%s AND
    (invoicedate BETWEEN (SELECT gst_start_date FROM backend.companyprofile)
    AND (SELECT gst_end_date FROM backend.companyprofile) OR
    invoicedate BETWEEN (SELECT sst_start_date FROM backend.companyprofile)
    AND (SELECT sst_end_date FROM backend.companyprofile))

    /*UNION ALL

    SELECT refno,'B2' AS sort,'B2' AS sequence,'Surcharge GST Amount' AS code_grn,0 AS value_grn,
    ROUND(surchg_tax_sum,2) AS value_calculated FROM backend.simain
    WHERE refno=%s and surchg_tax_sum<>0*/

    UNION ALL

    SELECT refno,'C1' AS sort,'C1' AS sequence,'GST Adjustment' AS code_grn,0 AS value_grn,
    ROUND(gst_adj,2) AS value_calculated FROM backend.simain
    WHERE refno=%s AND gst_adj<>0

    UNION ALL

    SELECT refno,'D1' AS sort,'D1' AS sequence,'Total Amount Include Tax' AS code_grn,0 AS value_grn,
    ROUND(total+gst_tax_sum+surchg_tax_sum+totaltax+gst_adj,2) AS value_calculated FROM backend.simain
    WHERE refno=%s AND
    (invoicedate BETWEEN (SELECT gst_start_date FROM backend.companyprofile)
    AND (SELECT gst_end_date FROM backend.companyprofile) OR
    invoicedate BETWEEN (SELECT sst_start_date FROM backend.companyprofile)
    AND (SELECT sst_end_date FROM backend.companyprofile))

    UNION ALL

    SELECT refno,'E1' AS sort,'E1' AS sequence,'Rounding Adjustment' AS code_grn,0 AS value_grn,
    ROUND(rounding_adj,2) AS value_calculated FROM backend.simain
    WHERE refno=%s AND rounding_adj<>0

    UNION ALL

    SELECT refno,'F1' AS sort,'F1' AS sequence,'Total Nett Amount' AS code_grn,0 AS value_grn,
    ROUND(total+gst_tax_sum+surchg_tax_sum+rounding_adj+totaltax+gst_adj,2) AS value_calculated FROM backend.simain
    WHERE refno=%s
    AND (ROUND(gst_tax_sum+surchg_tax_sum+rounding_adj+totaltax+gst_adj,2)<>0
    OR discount1<>0 OR discount2<>0) AND doc_type<>'EStore'

    UNION ALL

    SELECT refno,'A' AS sort,'G1' AS sequence,paytype AS code_grn,
    0 AS value_grn,
    ROUND(payamt*Value_Factor,2) AS value_calculated
    FROM backend.si_payment
    WHERE refno=%s AND Value_Factor=-1

    UNION ALL

    SELECT a.refno,'F1' AS sort,'F1' AS sequence,'Total Nett Amount' AS code_grn,0 AS value_grn,
    ROUND(subtotal1+gst_tax_sum+surchg_tax_sum+totaltax+rounding_adj+b.amount,2) AS value_calculated
    FROM backend.simain a
    INNER JOIN
    (
    SELECT refno,SUM(amount) AS amount FROM
    (
    SELECT refno,SUM(payamt*Value_Factor) AS amount FROM backend.si_payment
    WHERE Value_Factor = -1
    AND refno = %s

    UNION ALL

    SELECT refno,SUM(value_calculated) AS amount FROM backend.`trans_surcharge_discount`
    WHERE refno = %s
    )a
    GROUP BY refno
    )b
    ON a.refno = b.refno
    AND doc_type='EStore'

    ORDER BY sort,sequence
    """

    result4 = panda.raw_query(querystr, [search_refno, search_refno, search_refno, search_refno, search_refno, search_refno,
                              search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno, search_refno])
    result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)


# report STRB

@api_view(['GET'])
def report_StockReturnBatch(request,search_guid):
    print(search_guid)

    querystr = """
    SELECT 
    a.dbnote_guid,a.location,batch_no,CONCAT(a.sup_code,' - ',a.sup_name) AS supplier,
    a.created_at,a.created_by,a.updated_at,a.updated_by,
    posted_by,IF(a.status=0,'',a.posted_at) AS postdatetime,b.scan_barcode,b.itemcode,b.description,b.lastcost,
    b.averagecost,b.sellingprice,qty,b.packsize,b.um,b.reason,
    IF(a.status=0,'Doc Status: Unpost','Doc Status: Posted') AS doc_status,a.status,group_code

    FROM backend.dbnote_batch a
    INNER JOIN backend.dbnote_batch_c b 
        ON a.dbnote_guid=b.dbnote_guid
    INNER JOIN backend.supcus d
        ON a.sup_code=d.CODE
    LEFT JOIN backend.set_group_dept f
        ON b.dept=f.dept_code
    WHERE a.dbnote_guid=%s

    GROUP BY itemcode

    """
   
    result = panda.raw_query(querystr,[search_guid])
    result={"query1":result}

    querystr="""
    SELECT DNRemark1,IF(DNRemark1='' OR dnremark1 IS NULL,'','Remarks') AS remarks FROM backend.xsetup

    """
    result2=panda.raw_query_0(querystr)    
    result["query2"] = result2

    querystr="""
    SELECT contact,CONCAT(IF(add1 IS NULL,'',add1),' ',IF(add2 IS NULL,'',add2),' ',IF(add3 IS NULL,'',add3),' ',IF(city IS NULL,'',city),' ',IF(postcode IS NULL,'',postcode),' ',
    IF(state IS NULL,'',state),' ',IF(country IS NULL,'',country),'  Tel : ',IF(tel IS NULL,'',tel),'  Fax : ',IF(fax IS NULL,'',fax)) AS address 
    FROM backend.supcus a
    INNER JOIN backend.dbnote_batch b
    ON a.code=b.sup_code
    WHERE dbnote_guid=%s

    """
    result3=panda.raw_query(querystr,[search_guid])    
    result["query3"] = result3
    querystr="""
    SELECT a.CODE AS location,b.CODE AS locgroup,CONCAT(locgroup,IF(b.description IS NULL,'',CONCAT(' - ',b.description))) AS outlet,
    IF(a.remark IS NULL OR a.remark='',IF((SELECT ashq FROM backend.companyprofile)=0,companyname,IF(c.branch_name IS NULL,'',c.branch_name)),a.remark) AS companyname,
    IF((SELECT ashq FROM backend.companyprofile)=0,'',IF(c.branch_add IS NULL,'',c.branch_add)) AS address,
    IF((SELECT ashq FROM backend.companyprofile)=0,address1,'') AS address1,
    IF((SELECT ashq FROM backend.companyprofile)=0,address2,'') AS address2,
    IF((SELECT ashq FROM backend.companyprofile)=0,CONCAT('Tel : ',IF(tel IS NULL,'',tel),'  Fax : ',IF(fax IS NULL,'',fax)),
    CONCAT('Tel : ',IF(branch_tel IS NULL,'',branch_tel),'  Fax : ',IF(branch_fax IS NULL,'',branch_fax))) AS contact
    FROM backend.location a
    LEFT JOIN backend.locationgroup b ON a.locgroup=b.CODE
    LEFT JOIN backend.cp_set_branch c ON a.locgroup=c.branch_code
    INNER JOIN backend.companyprofile d
    WHERE a.CODE=(SELECT location FROM backend.dbnote_batch WHERE dbnote_guid=%s)

    """
    result4=panda.raw_query(querystr,[search_guid])    
    result["query4"] = result4



    return Response(result, status=status.HTTP_200_OK)   



# full json info
@api_view(['GET'])
def info_PoMain(request, search_refno):
    print(search_refno)

    querystr = """
    select b.`BRANCH_NAME`,a.*
    from backend.pomain a
    INNER JOIN backend.`cp_set_branch` AS b
    ON a.`loc_group` = b.`BRANCH_CODE`
    where refno=%s

    """

    result = panda.raw_query(querystr, [search_refno])
    result = {"pomain": result}

    querystr = """
    select *
    from backend.pochild
    where refno=%s
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["pochild"] = result2

    querystr = """
    select *
    from backend.trans_surcharge_discount
    where refno=%s
    """
    result3 = panda.raw_query(querystr, [search_refno])
    result["trans_surcharge_discount"] = result3

    querystr = """
    select *
    from backend.poamendmain
    where refno=%s
    """
    result4 = panda.raw_query(querystr, [search_refno])
    result["poamendmain"] = result4

    querystr = """
    select *
    from backend.poamendchild
    where refno=%s
    """
    result5 = panda.raw_query(querystr, [search_refno])
    result["poamendchild"] = result5

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def info_SiMain(request, search_refno):
    print(search_refno)

    querystr = """
    select *
    from backend.simain
    where refno=%s

    """

    result = panda.raw_query(querystr, [search_refno])
    result = {"simain": result}

    querystr = """
    select *
    from backend.sichild
    where refno=%s
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["sichild"] = result2

    querystr = """
    select *
    from backend.si_payment
    where refno=%s
    """
    result3 = panda.raw_query(querystr, [search_refno])
    result["si_payment"] = result3

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def info_GrMain_dncn(request, search_refno):
    print(search_refno)

    querystr = """
    select *
    from backend.grmain_dncn
    where refno=%s

    """

    result = panda.raw_query(querystr, [search_refno])
    result = {"Grmain_dncn": result}

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def info_GrMain(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT *
    FROM backend.grmain
    WHERE refno=%s
    """

    result = panda.raw_query(querystr, [search_refno])
    result = {"grmain": result}

    querystr = """
    SELECT *
    FROM backend.grchild
    WHERE refno=%s
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["grchild"] = result2

    querystr = """
    SELECT *
    FROM backend.trans_surcharge_discount
    WHERE refno=%s
    """
    result3 = panda.raw_query(querystr, [search_refno])
    result["trans_surcharge_discount"] = result3

    querystr = """
    SELECT *
    FROM backend.grmain_dncn
    WHERE refno=%s
    """

    result4 = panda.raw_query(querystr, [search_refno])
    result["grmain_dncn"] = result4
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def info__DisplayIncentive(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT *
    FROM backend.dischememain
    WHERE refno=%s
    """

    result = panda.raw_query(querystr, [search_refno])
    result = {"dischememain": result}

    querystr = """
    SELECT *
    FROM backend.dischemechild
    WHERE refno=%s
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["dischemechild"] = result2

    querystr = """
    SELECT *
    FROM backend.dischememain_location
    WHERE refno=%s
    """
    result3 = panda.raw_query(querystr, [search_refno])
    result["dischememain_location"] = result3

    querystr = """
    SELECT *
    FROM backend.discheme_taxinv
    WHERE refno=%s
    """

    result4 = panda.raw_query(querystr, [search_refno])
    result["discheme_taxinv"] = result4
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def info__PromotionClaim(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT *
    FROM backend.promo_supplier
    WHERE pvc_guid=%s
    """

    result = panda.raw_query(querystr, [search_refno])
    result = {"promo_supplier": result}

    querystr = """
    SELECT *
    FROM backend.promo_supplier_c
    WHERE pvc_guid=%s
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["promo_supplier_c"] = result2

    querystr = """
    SELECT *
    FROM backend.promo_supplier_loc
    WHERE pvc_guid=%s
    """
    result3 = panda.raw_query(querystr, [search_refno])
    result["promo_supplier_loc"] = result3

    querystr = """
    SELECT *
    FROM backend.promo_supplier_result
    WHERE pvc_guid=%s
    """

    result4 = panda.raw_query(querystr, [search_refno])
    result["promo_supplier_result"] = result4

    querystr = """
    SELECT a.*
    FROM backend.promo_taxinv a
    inner join backend.promo_supplier b
        on a.promo_refno=b.refno
    WHERE b.pvc_guid=%s
    """

    result5 = panda.raw_query(querystr, [search_refno])
    result["promo_taxinv"] = result5

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def info_PurchaseReturnDN(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT *
    FROM backend.dbnotemain
    WHERE refno=%s
    """

    result = panda.raw_query(querystr, [search_refno])
    result = {"dbnotemain": result}

    querystr = """
    SELECT *
    FROM backend.dbnotechild
    WHERE refno=%s
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["dbnotechild"] = result2

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def info_PurchaseReturnCN(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT *
    FROM backend.cnnotemain
    WHERE refno=%s
    """

    result = panda.raw_query(querystr, [search_refno])
    result = {"cnnotemain": result}

    querystr = """
    SELECT *
    FROM backend.cnnotechild
    WHERE refno=%s
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["cnnotechild"] = result2

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def info_PurchaseDNCN(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT *
    FROM backend.cndn_amt
    WHERE cndn_guid=%s
    """

    result = panda.raw_query(querystr, [search_refno])
    result = {"cndnamt": result}

    querystr = """
    SELECT *
    FROM backend.cndn_amt_c
    WHERE cndn_guid=%s
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["cndnamtchild"] = result2

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def info_Dbnotebatch(request, search_refno):
    print(search_refno)

    querystr = """
    SELECT *
    FROM backend.dbnote_batch
    WHERE batch_no=%s
    """

    result = panda.raw_query(querystr, [search_refno])
    result = {"dbnote_batch": result}

    querystr = """
    SELECT a.*
    FROM backend.dbnote_batch_c AS a
    INNER JOIN backend.dbnote_batch AS b
    ON a.dbnote_guid = b.dbnote_guid
    WHERE batch_no=%s
    """
    result2 = panda.raw_query(querystr, [search_refno])
    result["dbnote_batch_c"] = result2

    return Response(result, status=status.HTTP_200_OK)