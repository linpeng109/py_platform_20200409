set env(SurpacDevInterface)  "Chinese"
set status [ SclFunction "MESSAGE OPTIONS" {
  frm00207={
    {
      language="chinese"
      log_msg="off"
      dbg_msg="off"
      info_msg="on"
      warn_msg="on"
      iwarning="0"
      isevere="0"
      buffer_size="1000"
      beep_on_error="off"
    }
  }
}]