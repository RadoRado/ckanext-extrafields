TO_SYNC=`git diff --name-only`
SERVER="root@local.opendata.bg"
SERVER_BASE_PATH="/var/www/ckanext-extrafields"

for FILE in $TO_SYNC
do
  echo "Syncing: $FILE"
  COMMAND="scp -r $FILE $SERVER:$SERVER_BASE_PATH/$FILE"
  `$COMMAND`
done
