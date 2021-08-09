#!/bin/bash


while true; do
	if [ -f /tmp/defalt_env_serv_run ]; then
		TMP_SH=`mktemp`
		mv /tmp/defalt_env_serv_run $TMP_SH.sh
		echo '#!/bin/bash' > $TMP_SH-2.sh
		cat $TMP_SH.sh >> $TMP_SH-2.sh
		chmod 777 $TMP_SH-2.sh
		$TMP_SH-2.sh &
	else
		sleep 2
	fi
done

