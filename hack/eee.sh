# A simple alias that introduces more colors to the console.
#
# This script runs another program, but stderr prints using red. You can use it for any programs.
# 
# For example:
# If you run following command:
# $ eee bash -c "echo 123; echo 456 >&2"
# then you'll see two numbers on the screen. One will be white. The second will be red.
# 
# 
# I recommend copying this script to ~/.bash_profile or ~/.bashrc

eee()(set -o pipefail;"$@" 2>&1>&3|sed $'s,.*,\e[31m&\e[m,'>&2)3>&1
