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

    Scenario: I run module function
        When I run module "features.data.main" target "main"
        Then I see "FOOBAR"

    Scenario: I run module function with input
        When I run module "features.data.main" target "main_input"
        And I type "foobar"
        Then I see "FOOBAR"

    Scenario: I run module function that reads forever
        When I run module "features.data.main" target "main_forever_read"
        And I type "foobar"
        Then I see "FOOBAR"

    Scenario: I run module function and wait for some text
        When I run module "features.data.main" target "main_delay_print"
        And I type "foobar"
        Then I wait 3 seconds to see "FOOBAR"
