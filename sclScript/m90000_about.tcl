set Slot_a ""
set Slot_b ""
set Slot_c ""
set Helloworld "Helloworld!";set MasterVersionDigital "11";#ÿ���汾���������ļ��еĸ���������ְ汾�ż���
######################################################################
  # Description   : 
	#
	#				��1.��Ȩ�顰�����п����ſƼ����޹�˾�� ���С�
	#				��2.δ���������п����ſƼ����޹�˾��������ʹ�ñ������������Ϊ��Ȩ��
	#				��3.���ڲ����ش�������������Υ��ʹ�ñ�����ߣ��������п����ſƼ����޹�˾����������׷��Ȩ��
	#				
######################################################################
#��SmInstallDir����¼����İ�װĿ¼��
#�����Ե�״̬�£��������Ե�SclĿ¼��
set Slot_d ""
set Slot_e ""
set Slot_f "" ;set Old_SSI_PLOTTING [SclLogical translate SSI_PLOTTING: / ]

set softwareVersion "Release"
# #####set softwareVersion "Debug"

if {$softwareVersion == "Debug"} {
	set _DEBUG_ 1	
} else {
	set _DEBUG_ 0	
}

set SmInstallDir ""
if {$_DEBUG_} {
	set SmInstallDir "D:/smgmsclpy"
} else {

	foreach item [array name env] {
		#puts "item=$item"
		if {$item == "SMCollaborationDir$MasterVersionDigital"} {		
			set SmInstallDir $env($item)
		}
	}

}
#puts "SmInstallDir=$SmInstallDir"
#regsub -all {\\} $SmInstallDir {\\\\} SmInstallDir

set Slot_g ""
set Slot_h ""
set Slot_i ""


SclLogical add "SMGEO:" 				"$SmInstallDir"
SclLogical add "SMGEOBIN:" 			"$SmInstallDir\\bin\\"
SclLogical add "SMGEOTBC:" 			"$SmInstallDir\\tbc\\"
SclLogical add "SMGEOTEMPLATE:" "$SmInstallDir\\template\\"
SclLogical add "SMGEOWORKING:" 	"$SmInstallDir\\tempworking\\"
SclLogical add "SSI_PLOTTING:" 	"$SmInstallDir\\plotting_sinomine\\"
# if {[SclLogical exists "SMGEOTEMPLATE:"]} {
  # puts "SMGEOTEMPLATE: --> [SclLogical translate SMGEOTEMPLATE:]"
# }

set Slot_j "" ;set tranDir [SclLogical translate SMGEO: / ];set tranDir "${tranDir}/"
set Slot_k ""
set Slot_l ""

set SMGEO_DIR 		 				"$SmInstallDir"	
set SMGEOBIN_DIR 					"${SMGEO_DIR}/bin/"
set SMGEOTBC_DIR 					"${SMGEO_DIR}/tbc/"
set SMGEOTemplate_DIR 		"${SMGEO_DIR}/Template/"
set SMGEOWORKING_DIR  "${SMGEO_DIR}/tempworking/"
set SMGEOPLOTTING_DIR 		"${SMGEO_DIR}/plotting_sinomine/"


set Slot_m ""
set Slot_n ""
set Slot_o ""
set Slot_p ""

set SurpacLanguage "Chinese"
#
foreach item [array name env] {
	if {$item == "SurpacDevInterface$MasterVersionDigital"} {	
		set SurpacLanguage $env($item)
	}
}

set SurpacLanguage [string tolower $SurpacLanguage]

set FLAG "CN"
set Slot_q ""
set Slot_r ""
set Slot_s ""
set Slot_t ""
set Slot_u ""

if {$SurpacLanguage == "chinese"} {
	set FLAG "CN"
} elseif { $SurpacLanguage == "english"} {
	set FLAG "EN"
}
#set FLAG "EN"

set __yy__ [clock format [clock seconds] -format %Y]
set __mm__ [clock format [clock seconds] -format %m]
set __dd__ [clock format [clock seconds] -format %d]
set __s__ [clock seconds]
set __cur_date__ [clock format [clock seconds] -gmt false -format "%Y-%m-%d"]
#		puts "__cur_date__ == $__cur_date__"

set Slot_v ""
set Slot_w ""
set Slot_x ""
set Slot_y ""
set Slot_z ""
# # m90000_about.tcl
set Helloworld "Helloworld!";set MasterVersionDigital "11";#ÿ���汾���������ļ��еĸ���������ְ汾�ż���
######################################################################
#
# Macro Name    : 
#
# Version       : Surpac 6.6.2
#
# Creation Date : Sun Dec 13 08:45:04 2015
#
# Description   : 
#
######################################################################
# GuidoLabel Example 2
# define the form
set formDef {
  GuidoForm form {
    -label "�п����� ���ʽ�ģ��ʦ 1.1"
    -default_buttons
		-help_url http://www.sinomine.com.cn
    -layout BoxLayout X_AXIS
			GuidoPanel leftSide {
			  -layout BoxLayout X_AXIS
			GuidoLabel logo {
			  -icon "images/SinoMineSmartech_logo.jpg"
			}
			
		#	-default_buttons
		#   -layout BoxLayout Y_AXIS
		   GuidoHTMLPane infoMessage {
			  -label "<html><h1><font color=red></font></h1><p>
			<b><font size=5 color=green>�����п����ſƼ����޹�˾</b><br><p><p>
			<br><p><p>
			<a href=http://www.sinomine.com.cn/>http://www.sinomine.com.cn</a><br><p><p>

                                        <p><p></html>"
		   }
	# GuidoButton processBut {
      # -caption "http://www.sinomine.com.cn/"
    # }


   }
    

  }
}
# Create and run the form
SclCreateGuidoForm formHandle $formDef {}
$formHandle SclRun {}
      

return
return
