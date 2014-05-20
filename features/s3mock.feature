Feature: mock S3
    @s3mock
    Scenario: I list the keys in an empty bucket
        Given an S3 bucket named "foobucket"
        And there are 0 keys

    @s3mock
    Scenario: I list the keys in a bucket with some keys
        Given an S3 bucket named "foobucket"
        When I set the contents of the following keys
            | key   | content |
            | a.txt | foobar  |
            | b.txt | foobar  |
        Then there are 2 keys
        And the following keys exist
            | key   | content |
            | a.txt | foobar  |
            | b.txt | foobar  |
