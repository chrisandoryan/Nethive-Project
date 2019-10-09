# --- Plug by SIEM, Do Not MODIFY
# export whoamid="$(whoami)@$([ '$SSH_CONNECTION' == '' ] && echo local || echo $SSH_CONNECTION | awk '{print $1}')"
# PROMPT_COMMAND="history -a; history -n; logger -p local3.debug '$whoamid [$$]: $(history 1 | sed "s/^[ ]*[0-9]\+[ ]*//")'"
PROMPT_COMMAND="history -a; history -n"
export HISTSIZE=$HISTSIZE
export HISTTIMEFORMAT=$HISTTIMEFORMAT 
export HISTCONTROL=$HISTCONTROL
export HISTIGNORE=$HISTIGNORE
# --- End of Plug