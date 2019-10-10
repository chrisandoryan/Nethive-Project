# --- Plug by SIEM, Do Not MODIFY
alias whoamid="echo $(whoami)@$([ "$SSH_CONNECTION" == "" ] && echo local || echo $SSH_CONNECTION | awk '{print $1}')"
track_commands() {
  # make sure IP is set in .bash_profile instead of capturing it each time here
  printf '%s : %s : %s : %s \n' `date '+%Y-%m-%dT%T.%3N'` "$(whoamid)" "$(pwd)" "$BASH_COMMAND" >> /var/log/bash/history.log
}
# PROMPT_COMMAND="history -a; history -n; logger -p local3.debug '$whoamid [$]: $(history 1 | sed "s/^[ ]*[0-9]\+[ ]*//")'"
trap track_commands DEBUG
# PROMPT_COMMAND="history -a; history -n;"
PROMPT_COMMAND=""
export HISTSIZE=1000
export HISTTIMEFORMAT="%y-%h-%d %H:%M:%S "
export HISTCONTROL="ignorespace:erasedups"
export HISTIGNORE="ls:ps:history"
# --- End of Plug