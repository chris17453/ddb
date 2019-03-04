
create_deployments_table_sql="$(cat create_deployments.sql)"
select_from_deployments_sql=$(cat select_from_deployments.sql)

bash_array=$(python ddb.py "$create_deployments_table_sql; $select_from_deployments_sql"  -o bash)


for i in $bash_array; 
do
    eval "$i"
done


#loop through all results
for row in {0..$ddb_length};
do
    for column in {0..$ddb_columns};
    do
        echo ${ddb_data[$row][$column]} 
        #echo "./decom-tool.sh ${ddb_data[$key]} -v>results/${ddb_data[$key]}"
    done
done




