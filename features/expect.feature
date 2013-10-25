Feature: expect steps

    Scenario: I run a command
        When I run "/bin/ls"
        Then I see "README"

    Scenario: I run a command with arguments
        Given the command line arguments "foobar"
        When I run "/bin/echo"
        Then I see "foobar"

    Scenario: I run a command with input
        When I run "/bin/ed"
        And I type the lines
            |line   |
            |a      |
            |foobar |
            |.      |
            |1p     |
            |Q      |
        Then I see "foobar"
