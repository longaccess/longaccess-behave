Feature: expect steps

    Scenario: I run a command
        Given the command line arguments "foobar"
        When I run "/bin/echo"
        Then I see "foobar"

