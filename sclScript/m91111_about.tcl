set Helloworld "Helloworld!"
######################################################################
#
# Description   : 
	#
	#				��1.��Ȩ�顰�����п����ſƼ����޹�˾�� ���С�
	#				��2.δ���������п����ſƼ����޹�˾��������ʹ�ñ������������Ϊ��Ȩ��
	#				��3.���ڲ����ش�������������Υ��ʹ�ñ�����ߣ��������п����ſƼ����޹�˾����������׷��Ȩ��
	#				
######################################################################


#��SmInstallDir����¼����İ�װĿ¼��
#�����Ե�״̬�£��������Ե�SclĿ¼��

set softwareVersion "Release"
set softwareVersion "Debug"

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
		if {$item == "SMCollaborationDir"} {		
			set SmInstallDir $env($item)
		}
	}

}
#puts "SmInstallDir=$SmInstallDir"

#regsub -all {\\} $SmInstallDir {\\\\} SmInstallDir

SclLogical add "SMGEO:" "$SmInstallDir"
SclLogical add "SMGEOBIN:" "$SmInstallDir\\bin\\"
SclLogical add "SMGEOTBC:" "$SmInstallDir\\tbc\\"
SclLogical add "SMGEOTEMPLATE:" "$SmInstallDir\\template\\"
SclLogical add "SMGEOWORKING:" "$SmInstallDir\\tempworking\\"

set SMGEO_DIR 		 $SmInstallDir	
set SMGEOBIN_DIR 	"${SMGEO_DIR}/bin/"
set SMGEOTBC_DIR 	"${SMGEO_DIR}/tbc/"
set Template_DIR 	"${SMGEO_DIR}/Template/"


set formDef {
  GuidoForm form {
    -label "Surpac������ʽ�ģ����1.0"
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
			��������<b><font size=5 color=green>�����п����ſƼ����޹�˾</b>����Surpac������ʽ�ģ���̣�����й����ʴ�������Ҫ��   .<br><p><p>
			��Surpac���ƽ̨����TCL/SCLΪ���߽��еĶ���ʽ���ο���.<br><p><p>
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
      

