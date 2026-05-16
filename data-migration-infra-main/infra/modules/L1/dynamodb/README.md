## Dynamo_db
A module to create Dynamo DB
### Resources
- aws_dynamodb_table
With this resource we can create a dynamodb following the best practises.

### Variables
- dynamodb_name: String
Name of the dynamodb
- billing_mode: String
Controls how you are charged for read and write, the valid values are PROVISIONED and PAY_PER_REQUEST. The default is PROVISIONED.
- read_capacity: Number
Number of read units for this table
- write_capacity: Number
 umber of write units for this table
- hash_key: String
Attribute to use as the hash (partition) key
- range_key: String
Attribute to use as the range (sort) key.