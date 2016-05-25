    //SetBarsRequired( sbrAll ) ;


ODBCStr = "ODBC;DSN=ODBCAB05;UID=future;APP=AmiBroker for Win32;WSID=TJ64;DATABASE=future;pwd=K@ra0Key;DRIVER={SQL Server};SERVER=192.168.0.5";
    //dtemp=LastValue(DateNum())-1000000;
	Comm=60;    //Param("Comm",60,0,100,0.1);
	symbol= "IF";    //ParamStr( "Symbol", "IF" );
	ac="YEQGEX";    //ac or group


	SID=Param("SID",0,0,1000000,1);    //0:group,>0:single
	V_mode= ParamToggle( "V-mode", "Daily|Month",0 );
	V_mode=0;    //0:day,1:month
	DN= ParamList( "Day/Night", "All|Day|Night");

	Show_Total= ParamToggle( "Show_total", "No|Yes",0 );
	sdate=Param("SDate",120701,20101,1000000,1);
	Showsig= ParamToggle( "Show_signal", "No|Yes",0 );
    //	edate=Param("Edate",dtemp,20101,1000000,1);
    //		Plot(0,DN,colorBlack,styleNoLine);
	d=DateNum()-1000000;
		Plot(0,ac,colorBlack,styleNoLine);

	odbcOpenDatabase(ODBCStr);

	if (dn=="All")
		sttype="(1,2)";
	if (dn=="Day")
		sttype="(1)";
	if (dn=="Night")
		sttype="(2)";


	if(sid==0)
	{
	if(DN=="All")
	{
		Operate=odbcGetArraySQL("Future_query '"+symbol+"','"+ac+"',0");		
		Operate1=odbcGetArraySQL("Future_query '"+symbol+"','"+ac+"',1");
		Otype=0;
	}
	if (dn=="Day")
	{
		Operate=odbcGetArraySQL("Future_query_dn 1,'"+symbol+"','"+ac+"',0");		
		Operate1=odbcGetArraySQL("Future_query_dn 1, '"+symbol+"','"+ac+"',1");
		Otype=0;
	}
	if (dn=="Night")
	{
		Operate=odbcGetArraySQL("Future_query_dn 2, '"+symbol+"','"+ac+"',0");		
		Operate1=odbcGetArraySQL("Future_query_dn 2, '"+symbol+"','"+ac+"',1");
		Otype=0;
	}	
	}
	else
	{
		if (sid<1000)
			st_id=odbcGetValueSQL("SELECT TOP (1) st FROM (SELECT     TOP ("+sid+") st from (select distinct st FROM P_Log WHERE (AC = '"+ac+"') AND (symbol = '"+symbol+"')  AND p_size<>0 and ratio<>0 and st<>123456 and type in "+sttype+" ) as b order by st) AS a  ORDER BY st DESC");
		else
			st_id=sid;
		st_name=odbcGetValueSQL("SELECT top 1 stname FROM p_log where st='"+st_id+"'");
		st_type=odbcGetValueSQL("SELECT top 1 type  FROM p_log where st='"+st_id+"'");
		Plot(0,st_name,colorBlack,styleNoLine|2048|4096);
		Plot(st_id,"stid",colorBlack,styleNoLine|2048|4096);
		Operate=odbcGetArraySQL("Future_query_st '"+symbol+"','"+ac+"','"+st_id+"'");
		Operate1=0;
		Otype=odbcGetArraySQL("Future_query_st_type '"+symbol+"','"+ac+"','"+st_id+"'");
    //		Plot(Operate,"operate",colorBlack,styleNoLine);
	}
	Plot(Operate,"EO",colorBlack,styleNoLine|2048|4096);
	Plot(Operate1,"SO",colorBlack,styleNoLine|2048|4096);
	    //d_max是白天此虚拟组的最大仓位
	d_max=odbcGetValueSQL("SELECT round(sum(p_size*ratio/100),0) FROM p_log where type=1 and st<>123456 and ac='"+ac+"' and symbol='"+symbol+"' and d="+d);
	n_max=odbcGetValueSQL("SELECT round(sum(p_size*ratio/100),0) FROM p_log where type=2 and st<>123456 and ac='"+ac+"' and symbol='"+symbol+"' and d="+d);
	
	if (V_mode==0)
		ksum=BarsSince(Day()!=Ref(Day(),-1));
		//ksum每天开盘第一天是计数0
	ksum_temp=IIf( Cum(1)==LastValue(Cum(1)),0,Ref(ksum,1));
	//cum:累加，第一根bar是1，
	//LastValue:变量数组的最后一个值，在这里指最后这个K线的序号
	if (show_total)
		Tsum=IIf(sdate<=Lowest(DateNum())-1000000,BarIndex()-1,BarsSince((DateNum()-1000000==sdate)&&Day()!=Ref(Day(),-1)));
    //	Tsum2=IIf(edate==LastValue(DateNum()),0,BarsSince((DateNum()-1000000==edate)&&Day()!=Ref(Day(),1)));

    //Plot(ksum,"ksum",colorBlack);
	Position_temp=Sum(Operate+Operate1,BarIndex()-1);
	//累计仓位从第三根bar开始算
	//sum(c,0)=0;sum(c,1)=c;
	//BarIndex 和cum(1)-1效果一样
    //	Position_temp=Sum(Operate+Operate1,BarIndex());
	Position_temp1=Ref(Position_temp,-1)+Operate1;
	//正式觉得这个是夜盘仓位
    //	Plot(position_temp,"pt",colorBlack,styleNoLine);	
    //	Plot(position_temp1,"pt1",colorBlack,styleNoLine);	
	Price=IIf(Otype==1,O,C);
	//这里取C
	real_oper1=round(position_temp1)-round(Ref(position_temp,-1));
	//==Operate1当天仓位变化量
	real_oper=round(position_temp)-round(position_temp1);
	//==当天白天仓位变化量
	Position1=round(Ref(position_temp,-1));
	//==前一根BAR的仓位全天
	Position=round(position_temp1);
	//==当天夜盘的仓位
    //	Position=IIf(Day()!=Ref(Day(),-1),0,Position);

	{
		psum_no_comm=Sum(position1*(O-Ref(C,-1))*PointValue,ksum+1)+Sum(position*(C-O)*PointValue,ksum+1);
		psum=Sum(position1*(O-Ref(C,-1))*PointValue,ksum+1)+Sum(position*(C-O)*PointValue,ksum+1)-Sum((abs(real_oper)+abs(real_oper1))*Comm,ksum+1);
		if (show_total)
		{tsum_gross=Sum(position1*(O-Ref(C,-1))*PointValue,tsum+1)+Sum(position*(C-O)*PointValue,tsum+1);
		tsum_net=Sum(position1*(O-Ref(C,-1))*PointValue,tsum+1)+Sum(position*(C-O)*PointValue,tsum+1)-Sum((abs(real_oper)+abs(real_oper1))*Comm,tsum+1);
		}


	}
    //	pdr=psum-Highest(psum);
    //	pcarmdd=psum/Highest(abs(pdr));
if (show_total)
{
	tdr=Highest(abs(tSum_net-Highest(tSum_net)));
	tcarmdd=tSum_net/tdr;}
	ttimes=Sum(abs(real_oper)+abs(real_oper1),ksum+1);
    Sum_perh=psum/d_max;	
	Plot(position1,"Sp",colorBlack,styleNoLine|2048|4096);	
	Plot(position,"Ep",colorBlack,styleNoLine|2048|4096);	
    //	Plot(real_oper,"oper",colorBlack,styleNoLine );
	Plot(ttimes,"Times",colorBlack,styleNoLine |2048|4096);
	Plot(d_max,"Max_p",colorBlack,styleNoLine |2048|4096);
	Plot(n_max,"Max_np",colorBlack,styleNoLine |2048|4096);
	Plot(Sum_perh,"sum_perhand",colorBlack,styleNoLine |2048|4096);

	Plot(pSum,"Net",IIf(Position>=1,colorLightOrange ,IIf(position<=-1,colorLightBlue,0)),styleArea);
	Plot(pSum_no_comm,"Gross",colorDarkYellow );

    //	Plot(pdr,"dr",colorBlack,styleNoLine |2048|4096);
    //	Plot(pcarmdd,"car/mdd",colorBlack,styleNoLine |2048|4096);

	if (show_total)
{
	Plot(tsum_net,"Net_total",colorGreen,styleArea);
	Plot(tsum_gross,"Gross_total",colorYellow,styleArea);
	Plot(tdr,"total_dr",colorBlack,styleNoLine |2048|4096);
	Plot(tcarmdd,"toltal car/mdd",colorBlack,styleNoLine |2048|4096);


}

	if (V_mode==0)
		Plot( IIf((Day()!=Ref(Day(),1) OR Cum(1)==LastValue(Cum(1))),pSum_no_comm,0),"", IIf(pSum>0,colorRed,colorGreen), ParamStyle("Style", styleHistogram | styleThick|styleArea, maskHistogram ) );
	else
		Plot( IIf((Month()!=Ref(Month(),1) OR Cum(1)==LastValue(Cum(1))),pSum_no_comm,0),"", IIf(pSum>0,colorRed,colorGreen), ParamStyle("Style", styleHistogram | styleThick|styleArea, maskHistogram ) );

		for( k = 0; k < BarCount ; k++ ) 
		{
			if((real_oper[k]!=0) &&showsig)
			PlotText(NumToStr(real_oper[k],1.0), k, 0,IIf(real_oper[k]>0,colorRed,colorGreen)) ;
			if(ksum_temp[k]==0)
			PlotText(NumToStr(pSum[k],1.0), k, pSum[k]*.6,IIf(pSum[k]>0,colorBlue,colorBlack)) ;
		}