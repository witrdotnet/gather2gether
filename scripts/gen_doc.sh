mkdir -p ./doc

function put_cmd_doc() {
	ARGS_CNT=$#
	if [ $ARGS_CNT == 1 ]; then
		echo -e "==========================\n\t g2g $1\n=========================="
		echo "## g2g $1" >> $TRAGET_DOC_FILE
		echo "\`\`\`" >> $TRAGET_DOC_FILE
		g2g $1 --help >> $TRAGET_DOC_FILE
		echo "\`\`\`" >> $TRAGET_DOC_FILE
	elif [ $ARGS_CNT == 2 ]; then
		echo "============= g2g $1 $2"
		echo "* g2g $1 $2" >> $TRAGET_DOC_FILE
		echo "\`\`\`" >> $TRAGET_DOC_FILE
		g2g $1 $2 --help >> $TRAGET_DOC_FILE
		echo "\`\`\`" >> $TRAGET_DOC_FILE
	fi
}

TRAGET_DOC_FILE=./doc/g2g_cli_doc.md

echo "# Gather2gether cli documentation" > $TRAGET_DOC_FILE

echo "## All main commands" >> $TRAGET_DOC_FILE
echo "\`\`\`" >> $TRAGET_DOC_FILE
g2g >> $TRAGET_DOC_FILE
echo "\`\`\`" >> $TRAGET_DOC_FILE

put_cmd_doc db
put_cmd_doc db init

put_cmd_doc projects
put_cmd_doc projects create
put_cmd_doc projects update
put_cmd_doc projects find
put_cmd_doc projects search
put_cmd_doc projects delete

put_cmd_doc tasks
put_cmd_doc tasks create
put_cmd_doc tasks update
put_cmd_doc tasks find
put_cmd_doc tasks search
put_cmd_doc tasks delete

put_cmd_doc users
put_cmd_doc users create
put_cmd_doc users update
put_cmd_doc users find
put_cmd_doc users search
put_cmd_doc users delete
