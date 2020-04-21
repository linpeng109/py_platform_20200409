set Helloworld "Helloworld!"
######################################################################
#
# Description   : 
	#
	#				【1.版权归“北京中矿智信科技有限公司” 所有】
	#				【2.未经“北京中矿智信科技有限公司”允许不得使用本软件，否则将视为侵权】
	#				【3.对于不遵守此声明或者其他违法使用本软件者，“北京中矿智信科技有限公司”依法保留追究权】
	#				
######################################################################


#【SmInstallDir：记录软件的安装目录】
#【调试的状态下，开发测试的Scl目录】

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
    -label "Surpac软件地质建模流程1.0"
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
			本程序由<b><font size=5 color=green>北京中矿智信科技有限公司</b>根据Surpac软件地质建模流程，结合中国地质储量报告要求   .<br><p><p>
			在Surpac软件平台上以TCL/SCL为工具进行的定制式二次开发.<br><p><p>
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
      

